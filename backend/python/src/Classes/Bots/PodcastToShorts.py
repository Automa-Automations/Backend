from typing import List, Union, overload, Optional, TypeVar, Sequence
from aliases import (
    PodcastTranscript,
    LLMType,
    MoviePyClip,
    TranscriptFeedback,
    TranscriptFeedbackList,
)
from models import (
    ClipShortData,
    ParsedTranscript,
    TranscriptStats,
)
from src.Classes.Utils.ChatCompletion import ChatCompletion
from src.Classes.Utils.FaceTrackingVideo import FaceTrackingVideo
from pytube import YouTube
import os
import json
import base64
from moviepy.editor import VideoFileClip, concatenate_videoclips
import random
import logging
import re
from src.Classes.Utils.PodcastTranscriber import PodcastTranscriber
from src.utils import (
    format_yt_video_url,
    validate_string_similarity,
    download_podcast,
)
import traceback

logger = logging.getLogger(__name__)


class PodcastToShorts:
    def __init__(
        self,
        podcast_url: str,
        assembly_api_key: str,
        llm_model: Optional[str] = "gpt-4o",
        openai_api_key: Optional[str] = os.environ.get("OPENAI_API_KEY") or "",
    ) -> None:
        self.podcast_url = podcast_url
        self.assembly_api_key = assembly_api_key
        self.llm_model = llm_model
        self.debugging = True
        self.podcast_url = format_yt_video_url(self.podcast_url)
        self.yt = YouTube(self.podcast_url)
        self.debug_transcripts_feedback_path = (
            f"./src/Classes/Bots/json_files/transcripts_feedback.json"
        )
        self.debug_shorts_final_transcripts_path = (
            f"./src/Classes/Bots/json_files/shorts_final_transcripts.json"
        )

    def get_shorts(self, debugging=False) -> List[ClipShortData]:
        self.__validate_params()
        """
        Method to generate the shorts from the podcast
        Parameters:
        - debugging: whether or not it should take shortcuts to increase speed, save results to json files for debugging purposes, ect...
        Returns clip_shorts_data
        """
        transcriptor = PodcastTranscriber.from_assembly(
            self.podcast_url, self.assembly_api_key, self.debugging
        )

        if not transcriptor:
            raise Exception("Transcriptor is none")

        transcript = transcriptor.transcript
        podcast_length = round(transcriptor.audio_duration / 60)

        logger.info(f"Transcript objects length: {len(transcript)}")
        logger.info(f"Podcast Length: {podcast_length} minutes")

        if (self.debugging or debugging) and os.path.exists(
            self.debug_transcripts_feedback_path
        ):
            with open(self.debug_transcripts_feedback_path, "r") as f:
                logger.info("Loading from transcripts_feedback.json...")
                transcriptions_feedback: TranscriptFeedbackList = [
                    TranscriptFeedback.model_validate(dict) for model in json.load(f)
                ]
        else:
            transcriptions_feedback = self.__get_transcripts_feedback(transcript)
        logger.info(
            f"Transcriptions With Feedback length: {len(transcriptions_feedback)}"
        )

        shorts_transcripts = self.__filter_transcripts(transcriptions_feedback)
        logger.info(f"Shorts Transcripts length: {len(shorts_transcripts)}")

        if len(shorts_transcripts) < round(podcast_length / 10):
            # get all the shorts that is "should_make_short" false. We need to get the best of them, so that there is enough shorts.
            logger.info(
                "length of shorts transcripts not enough. Getting extra shorts..."
            )
            other_shorts = self.__filter_transcripts(
                transcriptions_feedback, should_make_short=False
            )
            logger.info(f"Other shorts length: {len(other_shorts)}")

            extra_shorts = self.__get_best_shorts(
                shorts_transcripts=other_shorts,
                total_shorts=round(podcast_length / 10) - len(shorts_transcripts),
            )
            # Doing this since it gives weird type mismatches when I try to add them together, even though they have the same type, since it is a union type of lists
            shorts_transcripts: TranscriptFeedbackList = json.loads(
                json.dumps(shorts_transcripts + extra_shorts)
            )
            logger.info(f"New shorts transcripts length: {len(shorts_transcripts)}")

        elif len(shorts_transcripts) > round(podcast_length / 10):
            # Make a new list by putting only the highest scores in there, so that it is the length of round(podcast_length / 10)
            logger.info("Shorts transcripts length is too long...")
            shorts_transcripts = json.loads(
                json.dumps(
                    sorted(
                        shorts_transcripts,
                        key=lambda x: x.stats.score,
                        reverse=True,
                    )[: round(podcast_length / 10)]
                )
            )

            logger.info(f"New shorts transcripts length: {len(shorts_transcripts)}.")

        # if self.debugging or debugging:
        if (self.debugging or debugging) and os.path.exists(
            self.debug_shorts_final_transcripts_path
        ):
            logger.info("Loading from shorts_final_transcripts.json...")
            with open(self.debug_shorts_final_transcripts_path, "r") as f:
                shorts_final_transcripts: TranscriptFeedbackList = json.load(f)
        else:
            logger.info("Getting shorts final transcripts...")
            shorts_final_transcripts = self.__get_shorts_final_transcripts(
                shorts_transcripts
            )
        logger.info(
            f"Shorts Final Transcripts: (length: {len(shorts_final_transcripts)}): {shorts_final_transcripts}"
        )

        logger.info("Generating shorts...")
        shorts_final_transcripts = self.__add_timestamps_final_transcripts(
            shorts_final_transcripts, transcript
        )
        clip_shorts_data = self._generate_shorts(shorts_final_transcripts)
        logger.info(
            f"Clip Shorts Data: (length: {len(clip_shorts_data)}): {clip_shorts_data}"
        )

        return clip_shorts_data

    def __add_timestamps_final_transcripts(
        self, final_transcripts, assembly_ai_transcript
    ):
        transcript_with_timestamps = []
        for index, final_transcript in enumerate(final_transcripts):
            current_transcript_with_timestamps = []
            for sentence in final_transcript["sentences"]:
                for assembly_sentence_dict in assembly_ai_transcript:
                    if assembly_sentence_dict["sentence"].lower() == sentence.lower():
                        current_transcript_with_timestamps.append(
                            assembly_sentence_dict
                        )
                        break

            if len(current_transcript_with_timestamps) > 5:
                transcript_with_timestamps.append(current_transcript_with_timestamps)
            else:
                logger.warning(f"Transcript {index+1} has less than 5 sentences")

        return transcript_with_timestamps

    def __get_best_shorts(
        self, shorts_transcripts: TranscriptFeedbackList, total_shorts: int
    ) -> TranscriptFeedbackList:
        """
        Method to get the best shorts from the passed in shorts
        Parameters:
        - shorts_transcripts: list: The list of the shorts transcripts
        - total_shorts: int: The total number of shorts needed
        Returns:
        - list: The list of the best shorts
        """

        # sort the shorts_transcripts by the score, in descending order
        # since we know that the list of children will be the same type always, (all will be youtube or assembly transcript type, it will never be a mixture of both), I am going to use json.loads(json.dumps) to make it be of type TranscriptFeedbackList.
        descending_sorted_shorts: TranscriptFeedbackList = json.loads(
            json.dumps(
                sorted(
                    shorts_transcripts,
                    key=lambda x: int(x.stats.score),
                    reverse=True,
                )
            )
        )
        best_shorts = descending_sorted_shorts[:total_shorts]
        logger.info(f"Got an extra {len(best_shorts)} shorts.")
        return best_shorts

    def __get_shorts_final_transcripts(
        self, shorts: TranscriptFeedbackList
    ) -> TranscriptFeedbackList:
        """
        Method to get the final transcripts of the shorts, by removing the start, middle and end sentences, to get the optimized short.
        Parameters:
        - shorts_transcripts: list: The list of the shorts transcripts
        Returns:
        - list: The list of the final transcripts of the shorts
        """

        def get_prompt_first_sentence(short: TranscriptFeedback):
            return f"I want to make a great 15 - 55 seconds long short from the transcript part given to you."

        with open("./src/Classes/Bots/json_files/examples/1_input.json", "r") as f:
            example_input = json.load(f)

        with open("./src/Classes/Bots/json_files/examples/1_output.json", "r") as f:
            example_output = json.load(f)
        # it works, but there are some minor flaws. The LLM sometimes puts sentences together that should be separated.
        # prompt = f"""{prompt_first_sentence}. Give me only 15 - 20 sentences from the transcript I just gave you that will be the most engaging and get the most amount of views, you must stricly output in the following JSON format: {json.dumps({"sentences": ["sentence here", "another sentence here"]}, indent=4)}. Keep the sentences the exact same as what it was from the transcript."""

        # TODO: Change this prompt so that the LLM does not put more than one sentence in a string. Each string should be one sentence.
        prompt = f"""{get_prompt_first_sentence(shorts[0])}. Give me only 15 - 20 sentences from the transcript I just gave you that will be the most engaging and get the most amount of views. You must stricly output in the following JSON format: {json.dumps({"sentences": ["sentence here", "another sentence here"]}, indent=4)}. Keep the sentences the exact same as what it was from the transcript."""
        final_transcripts_sentences = [
            self.__get_final_transcript(prompt, short) for short in shorts
        ]
        final_transcripts = self.__format_assembly_transcripts_sentences(
            final_transcripts_sentences, shorts
        )

        logger.info("Returning final transcripts...")
        return final_transcripts

    def _generate_shorts(self, shorts_final_transcripts: List):
        # for now, just download the podcast and get shorts, unedited.
        download_response = download_podcast(self.podcast_url)
        logger.info("Podcast downloaded successfully")
        clip_shorts_data = []
        for short_transcript in shorts_final_transcripts:
            clipped_short_data = self._clip_short(
                "./shorts",
                download_response.output_path,
                download_response.filename,
                short_transcript,
            )
            clip_shorts_data.append(clipped_short_data)

        if not self.debugging:
            os.remove(f"{download_response.output_path}/{download_response.filename}")

        return clip_shorts_data

    def _clip_short(
        self,
        shorts_output_path: str,
        podcast_output_path: str,
        filename: str,
        short_transcript,
    ) -> dict:
        logger.info("Clipping short...")

        if not os.path.exists(shorts_output_path):
            os.makedirs(shorts_output_path)

        podcast_path = os.path.join(podcast_output_path, filename)
        short_start_time = short_transcript[0]["start_time"]
        short_end_time = short_transcript[-1]["end_time"]

        short_filename = f"{filename}_short_{short_start_time}_{short_end_time}.mp4"
        clipped_video_path = os.path.join(
            shorts_output_path, f"mobile_ratio_{short_filename}"
        )
        original_clip_video_path = os.path.join(
            shorts_output_path, f"original_{short_filename}"
        )

        # Make clips of all the sentences in the short, and then add them together as one clip
        all_sentences_clips = []
        for sentence_dict in short_transcript:
            sentence_clip = VideoFileClip(podcast_path).subclip(
                sentence_dict["start_time"] / 1000,
                sentence_dict["end_time"] / 1000,
            )
            all_sentences_clips.append(sentence_clip)

        logger.info(f"Total sentences clips: {len(all_sentences_clips)}")
        logger.info("Concatenating all the clips together...")
        clipped_video = concatenate_videoclips(all_sentences_clips)

        clipped_video.write_videofile(original_clip_video_path)
        try:
            # clip video to mobile aspect ratio (9:16), along with following faces smoothly
            logger.info(
                "Clipping short to mobile aspect ratio, along with following faces smoothly..."
            )

            mobile_ratio_follow_faces_short = self._clip_and_follow_faces_mobile_ratio(
                clipped_video,
            )
            mobile_ratio_follow_faces_short.write_videofile(clipped_video_path)

            with open(clipped_video_path, "rb") as video_file:
                base64_clipped_video = base64.b64encode(video_file.read()).decode(
                    "utf-8"
                )

            if not self.debugging:
                os.remove(clipped_video_path)

            return_dict = {
                "short_transcript": short_transcript,
                "base64_clipped_video": base64_clipped_video,
                "short_filename": short_filename,
            }
            return return_dict

        except Exception as e:
            logger.error(
                f"Error while clipping short to right aspect ratio and adding in face detection: {e}"
            )
            traceback.print_exc()
            return {}

    def _clip_and_follow_faces_mobile_ratio(self, clipped_video: MoviePyClip):
        return FaceTrackingVideo().process_short(clipped_video)

    def __filter_transcripts(
        self,
        transcriptions_feedback: TranscriptFeedbackList,
        should_make_short: bool = True,
    ) -> TranscriptFeedbackList:
        """
        Method to filter the transcriptions based on the should_make_short value
        Parameters:
        - transcriptions_feedback: list: The list of the feedback of the transcriptions
        - should_make_short: bool: The value to filter the transcriptions
        Returns list[TranscriptFeedback]: The list of the transcriptions that have the should_make_short value
        """

        cleaned_transcripts_feedback: List[TranscriptFeedback] = []
        for transcription in transcriptions_feedback:
            new_transcription = transcription
            cleaned_transcripts_feedback.append(new_transcription)

        result: TranscriptFeedbackList = [
            transcription
            for transcription in cleaned_transcripts_feedback
            if transcription.stats.should_make_short == should_make_short
        ]
        return result

    def __get_transcripts_feedback(
        self, full_sentences_transcript: PodcastTranscript
    ) -> TranscriptFeedbackList:
        """
        Method to get the feedback of the transcriptions
        Parameters:
        - full_sentences_transcript: list: The list of the full sentences of the transcriptions
        Returns:
        - list: The list of the feedback of the transcriptions
        """
        logger.info("Getting transcripts feedback...")
        chunked_transcript = self.__chunk_transcript(full_sentences_transcript)
        transcripts_with_feedback: List[TranscriptFeedback] = []
        for idx, chunk in enumerate(chunked_transcript):
            prompt = f"""
            Your job is to evaluate the following transcript chunk from a long-form podcast style video: {chunk}. Decide whether or not a specific part of the transcript or the whole transcript is valid for a short. Evaluate the short based off of this:
            score: a score out from 0 to 100, on how good this would make for a viral short. Be quite strict here, as the goal is to make the short as engaging as possible. If it is some sort of ad for a product, or introduction for the podcast, then give it a score of 40. NOTE: swearing and cussing shouldn't make the score less or more. The transcript must be one of the following to get a score above 70, anything that is not this should get a score below 70. The transcript should have at least one or a few of the following, to get a score of 70 and above:
            1. Really engaging, or interesting
            2. Really funny, which will make viewers with fried dopamine receptors laugh, meaning it is really funny.
            3. Really highly motivating, or inspiring
            4. Really highly educational, or informative
            5. Something that is following the trends, that people would want to hear from,
            6. A really strong story that will make people feel understood, that people can resonate from. It should envoke a lot of emotion for the viewer.
            7. Anything that will envoke strong emotions for the viewer. Whether that is sadness, happiness, really feeling understood, really feeling hyped up and motivated, a "wow" feeling of understanding or learning something new, that will make the viewer want to watch the full video.
            8. Anything that is really unique, and hasn't been done before. That will make the viewer want to watch the full video.
            9. A "badass" moment, or how someone is talking about how badass they are, something that could inspire and motivate people to do hard things, to push themselves. This is a moment that will make people feel like they can do anything, and they are unstoppable.
            10. Someone talking about how they went through difficult times, something that could resonate with the audience.
            should_make_short: True or False. True, if the score is above or equal to 70, false if it is below 70
            feedback: Any feedback on the short, what is good and bad about the transcript, how to make it better. Note: only evaluate it based off of the transcript. Don't give feedback saying that there could be visuals or animations.
###
            Please output in the following format (ignore the values, just use the structure):
            {json.dumps(
            {
                "score": "a score out of 100, on how good this would make for a short. Be quite strict here, as the goal is to make the short as engaging as possible. Use an integer here. The score must be a number, not surrounded with quotation marks at all",
                "should_make_short": "True or False. True, if the score is above or equal to 70, false if it is below 70. Don't surround this value with quotation marks at all",
                "feedback": "Any feedback on the short, what is good and bad about the transcript, how to make it better."
            }, indent=4)}
            """
            chat_completion = ChatCompletion()
            response = chat_completion.generate(
                system_prompt=prompt,
                user_message=f"Here is the transcript chunk: {chunk}",
                return_type=TranscriptStats,
            )

            logger.info("Successfully got response")

            correct_dt_transcript = [
                model for model in chunk if isinstance(model, ParsedTranscript)
            ]
            transcript_and_feedback_chunk = TranscriptFeedback(
                transcript=correct_dt_transcript,
                stats=response,
            )

            logger.info(f"{idx+1}. Feedback generated successfully.")

            transcripts_with_feedback.append(transcript_and_feedback_chunk)
            with open(self.debug_transcripts_feedback_path, "w") as f:
                f.write(json.dumps(transcripts_with_feedback, indent=4))
                logger.info(
                    f"saved transcripts feedback for this chunk to {self.debug_transcripts_feedback_path}"
                )

            with open(
                f"./src/Classes/Bots/json_files/{self.llm_type}_transcripts_score.json",
                "w",
            ) as f:
                f.write(
                    json.dumps(
                        [transcript.stats for transcript in transcripts_with_feedback],
                        indent=4,
                    )
                )
                logger.info(f"saved scores to {self.llm_type}_transcripts_score.json")

        return transcripts_with_feedback

    def __chunk_transcript(
        self,
        video_transcript: PodcastTranscript,
        chunk_length: int = 4000,
    ) -> List[PodcastTranscript]:
        """
        Method to chunk the transcript
        Parameters:
        - video_transcript: str: The video transcript
        - chunk_length: int: The length of the chunk
        Returns:
        - list: The list of the chunked transcript
        """
        # chunk the list of dictionaries into a final list of lists, each list having less than chunk_length amount of characters
        chunk_transcript_list = []
        current_chunk = []

        for transcript_dict in video_transcript:
            # the chunk can take in another transcription dictionary
            if (
                len(json.dumps(current_chunk)) + len(json.dumps(transcript_dict))
                < chunk_length - 100
            ):
                current_chunk.append(transcript_dict)
            # the chunk cannot take in another transcription dictionary
            else:
                # the length cannot be 0.
                chunk_transcript_list.append(current_chunk)
                current_chunk = [transcript_dict]

        logger.info(f"Total number of chunks: {len(chunk_transcript_list)}")
        return chunk_transcript_list

    def __validate_params(self):
        invalid_params = False
        if self.assembly_api_key:
            logger.error(
                "Assembly AI API Key must be passed in class initialization when using assembly_ai"
            )
            invalid_params = True
            invalid_params = True
            invalid_params = True
        if invalid_params:
            raise ValueError("Invalid parameters passed")

    def __get_final_transcript(
        self,
        prompt: str,
        short: TranscriptFeedback,
    ) -> ShortFinalTranscript:
        """
        Internal method to get final transcript for a short
        """
        chat_completion = ChatCompletion()

        llm_response = chat_completion.generate()
        return llm_response

    def __format_assembly_transcripts_sentences(
        self,
        sentences_lists: List[ShortFinalTranscript],
        shorts: List[TranscriptFeedback],
    ) -> List[FinalTranscriptDict]:
        """
        Method to format the assembly transcripts sentences into the final transcript chunk
        Parameters:
        - sentences_list: list: The list of the assembly transcripts sentences
        - shorts: list: The list of the assembly transcripts
        Returns:
        - list: The list of the final transcript chunk
        """
        # first, make sure there is only one sentence per string in the list. If there is more, add that as its own string.
        end_sentence_regex = re.compile(r"[.!?]")
        final_shorts_sentences: List[List[str]] = []
        for sentence_list in sentences_lists:
            current_sentences_list: List[str] = []
            for sentence in sentence_list.sentences:
                current_sentences_list.extend(re.split(end_sentence_regex, sentence))
            final_shorts_sentences.append(current_sentences_list)

        # final_transcripts: List[FinalTranscriptChunk] = []
        # for idx, sentences in enumerate(sentences_list):
        #     final_transcripts.append(
        #         FinalTranscriptChunk(
        #             transcript=sentences.sentences,
        #             transcript_duration
