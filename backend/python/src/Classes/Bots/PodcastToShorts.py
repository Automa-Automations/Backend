from typing import List, Union, overload, Optional, TypeVar
from aliases import (
    PodcastTranscript,
    TranscriptorType,
    LLMType,
    MoviePyClip,
    ShortsFinalTranscripts,
    TranscriptFeedback,
    TranscriptFeedbackList,
    FinalTranscript,
)
from models import (
    FinalTranscriptChunk,
    YouTubeAPIStartEndTimes,
    ClipShortData,
    AssemblyShortFinalTranscript,
    YoutubeAPITranscript,
    AssemblyAIParsedTranscript,
    TranscriptStats,
    YoutubeTranscriptFeedback,
    AssemblyTranscriptFeedback,
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

TranscriptFeedbackType = TypeVar(
    "TranscriptFeedbackType", YoutubeTranscriptFeedback, AssemblyTranscriptFeedback
)


class PodcastToShorts:
    def __init__(
        self,
        podcast_url: str,
        llm_type: LLMType = "openai",
        transcriptor_type: TranscriptorType = "assembly_ai",
        assembly_api_key: str = "",
        llm_model: str = "gpt-4o",
        ollama_base_url: str = "",
        llm_api_key: str = "",
    ) -> None:
        self.podcast_url = podcast_url
        self.transcriptor_type = transcriptor_type
        self.assembly_api_key = assembly_api_key
        self.llm_type = llm_type
        self.llm_model = llm_model
        self.debugging = True
        self.podcast_url = format_yt_video_url(self.podcast_url)
        self.yt = YouTube(self.podcast_url)
        self.ollama_base_url = ollama_base_url
        self.llm_api_key = llm_api_key
        self.debug_transcripts_feedback_path = f"./src/Classes/Bots/json_files/transcripts_feedback_{transcriptor_type}.json"
        self.debug_shorts_final_transcripts_path = f"./src/Classes/Bots/json_files/shorts_final_transcripts_{transcriptor_type}.json"

    def get_shorts(self, debugging=False) -> List[ClipShortData]:
        self.__validate_params()
        """
        Method to generate the shorts from the podcast
        Parameters:
        - debugging: whether or not it should take shortcuts to increase speed, save results to json files for debugging purposes, ect...
        Returns clip_shorts_data
        """
        if self.transcriptor_type == "assembly_ai":
            transcriptor = PodcastTranscriber.from_assembly(
                self.podcast_url, self.assembly_api_key, self.debugging
            )
        elif self.transcriptor_type == "yt_transcript_api":
            transcriptor = PodcastTranscriber.from_transcription_api(
                self.podcast_url, self.debugging
            )
        else:
            logger.error("Transcriptor type is not valid")
            raise ValueError("Transcriptor type is not valid")

        if not transcriptor:
            raise Exception("Transcriptor is none")

        transcript = transcriptor.transcript
        if self.transcriptor_type == "assembly_ai":
            podcast_length = round(transcriptor.audio_duration / 60)
        else:
            transcript = [
                YoutubeAPITranscript.model_validate(dict) for dict in transcript
            ]
            podcast_length = round(
                (transcript[-1].start + transcript[-1].duration) / 60
            )
            raise ValueError("Transcriptor type is not valid")

        logger.info(f"Transcript objects length: {len(transcript)}")
        logger.info(f"Podcast Length: {podcast_length} minutes")

        if (self.debugging or debugging) and os.path.exists(
            self.debug_transcripts_feedback_path
        ):
            with open(self.debug_transcripts_feedback_path, "r") as f:
                logger.info("Loading from transcripts_feedback.json...")
                data = json.load(f)
                transcriptions_feedback: TranscriptFeedbackList = []
                if self.transcriptor_type == "assembly_ai":
                    transcriptions_feedback = [
                        (YoutubeTranscriptFeedback.model_validate(dict))
                        for dict in data
                    ]
                else:
                    transcriptions_feedback = [
                        (AssemblyTranscriptFeedback.model_validate(dict))
                        for dict in data
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
            shorts_transcripts = shorts_transcripts + extra_shorts
            logger.info(f"New shorts transcripts length: {len(shorts_transcripts)}")

        elif len(shorts_transcripts) > round(podcast_length / 10):
            # Make a new list by putting only the highest scores in there, so that it is the length of round(podcast_length / 10)
            logger.info("Shorts transcripts length is too long...")
            highest_score_list = sorted(
                shorts_transcripts,
                key=lambda x: x.stats.score,
                reverse=True,
            )[: round(podcast_length / 10)]

            logger.info(
                f"New shorts transcripts length: {len(highest_score_list)}. Before, it was a length of {len(shorts_transcripts)}"
            )
            shorts_transcripts = highest_score_list

        # if self.debugging or debugging:
        if (self.debugging or debugging) and os.path.exists(
            self.debug_shorts_final_transcripts_path
        ):
            logger.info("Loading from shorts_final_transcripts.json...")
            with open(self.debug_shorts_final_transcripts_path, "r") as f:
                shorts_final_transcripts: ShortsFinalTranscripts = json.load(f)
        else:
            logger.info("Getting shorts final transcripts...")
            shorts_final_transcripts = self.__get_shorts_final_transcripts(
                shorts_transcripts
            )
        logger.info(
            f"Shorts Final Transcripts: (length: {len(shorts_final_transcripts)}): {shorts_final_transcripts}"
        )

        logger.info("Generating shorts...")
        # add in the start and end times to each sentence
        if self.transcriptor_type == "assembly_ai":
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
        self, shorts_transcripts: List[TranscriptFeedbackType], total_shorts: int
    ) -> List[TranscriptFeedbackType]:
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
        self, shorts_transcripts: List[TranscriptFeedbackType]
    ) -> List[FinalTranscript]:
        """
        Method to get the final transcripts of the shorts, by removing the start, middle and end sentences, to get the optimized short.
        Parameters:
        - shorts_transcripts: list: The list of the shorts transcripts
        Returns:
        - list: The list of the final transcripts of the shorts
        """
        final_transcripts = []

        def get_prompt_first_sentence(short: TranscriptFeedback):
            if self.llm_type == "ollama":
                return f"I want to make a great 15 - 55 seconds long short from the following transcript: {json.dumps(short.transcript)}"
            else:
                return f"I want to make a great 15 - 55 seconds long short from the transcript part given to you."

        if self.transcriptor_type == "assembly_ai":
            with open("./src/Classes/Bots/json_files/examples/1_input.json", "r") as f:
                example_input = json.load(f)

            with open("./src/Classes/Bots/json_files/examples/1_output.json", "r") as f:
                example_output = json.load(f)
            # it works, but there are some minor flaws. The LLM sometimes puts sentences together that should be separated.
            # prompt = f"""{prompt_first_sentence}. Give me only 15 - 20 sentences from the transcript I just gave you that will be the most engaging and get the most amount of views, you must stricly output in the following JSON format: {json.dumps({"sentences": ["sentence here", "another sentence here"]}, indent=4)}. Keep the sentences the exact same as what it was from the transcript."""

            # TODO: Change this prompt so that the LLM does not put more than one sentence in a string. Each string should be one sentence.
            prompt = f"""{get_prompt_first_sentence(shorts_transcripts[0])}. Give me only 15 - 20 sentences from the transcript I just gave you that will be the most engaging and get the most amount of views. You must stricly output in the following JSON format: {json.dumps({"sentences": ["sentence here", "another sentence here"]}, indent=4)}. Keep the sentences the exact same as what it was from the transcript."""
            all_shorts_transcripts = [short.transcript for short in shorts_transcripts]
            correct_type_transcripts: List[List[AssemblyAIParsedTranscript]] = []
            for short_transcript in all_shorts_transcripts:
                correct_type_short_transcript: List[AssemblyAIParsedTranscript] = []
                for transcript_model in short_transcript:
                    if isinstance(transcript_model, AssemblyAIParsedTranscript):
                        correct_type_short_transcript.append(transcript_model)
                    else:
                        raise ValueError(
                            "Short is not a AssemblyAIParsedTranscript object"
                        )
                correct_type_transcripts.append(correct_type_short_transcript)

            final_transcripts = [
                self.__get_final_transcript(prompt, correct_type_transcript)
                for correct_type_transcript in correct_type_transcripts
            ]
        else:
            final_transcripts = []
            for short in enumerate(shorts_transcripts):
                if not isinstance(short, YoutubeTranscriptFeedback):
                    raise ValueError("Short is not a YoutubeTranscriptFeedback object")

                prompt = f"""{get_prompt_first_sentence(shorts_transcripts[0])}. Give me the perfect start text and end text from the transcript that will be the perfect start and end for making an engaging short (DON'T USE THE FIRST TEXT AND THE LAST TEXT FROM THE TRANSCRIPT I GAVE YOU, IT MUST START A LITTLE BIT LATER ON.) Note, the start and end text must be from the transcript. The start text must be before the end text. The start text must be the best starting sentence from the transcript for a short, and the end text must be a the best ending sentence from the transcript for a short. The start text must be the beginning of a sentence, and the end text must end a sentence (meaning first character for start text must be a capital letter, indicating it is the start of a sentence, and the end sentence should be ending with an ending character - '?.!'. Keep the start and end text the exact same as what it was from the transcript.

                The start text may not be "{short.transcript[0].text}", and the end text may not be '{short.transcript[0].text}'.
                Your output in the following format (ignore the values):
                {json.dumps({
                    'start_text': 'the exact start text',
                    'end_text': 'the exact end text'
                }, indent=3)}"""

                final_transcripts.append(self.__get_final_transcript(prompt))

        logger.info("Returning final transcripts...")
        return final_transcripts

    def _cleanup_shortened_transcript_response(
        self,
        llm_response: YouTubeAPIStartEndTimes,
        short_transcript: List[YoutubeAPITranscript],
    ) -> Union[FinalTranscriptChunk, None]:
        logger.info("Cleaning up shortened transcript response...")
        llm_response.start_text = llm_response.start_text.replace("\n", " ")
        llm_response.end_text = llm_response.end_text.replace("\n", " ")
        logger.info("Successfully got response")

        shortened_transcript: List[YoutubeAPITranscript] = []
        logger.info("\n")
        for idx, dict in enumerate(short_transcript):
            dict.text = dict.text.replace("\n", " ")

            current_text = dict.text
            is_similar = validate_string_similarity(
                current_text, llm_response.start_text, 80
            )
            logger.info(
                f'{idx+1}. "{current_text}" == "{llm_response.start_text}": {is_similar}'
            )
            if is_similar:
                count = 0
                while not validate_string_similarity(
                    current_text, llm_response.end_text
                ) and len(shortened_transcript) < len(short_transcript) - (idx + 1):
                    try:
                        regex = r"\[.*?\]"
                        pattern = r"\b[A-Z]{4,}\b(:\s*)?"

                        current_text = short_transcript[idx + count].text
                        current_text = re.sub(pattern, "", current_text)
                        current_text = re.sub(r"\s+", " ", current_text).strip()

                        logger.info(f"Current Text: {current_text}")

                        current_text = re.sub(regex, "", current_text).replace(
                            "\n", " "
                        )
                        append_model = short_transcript[idx + count]
                        append_model.text = current_text

                        shortened_transcript.append(append_model)
                        count = count + 1
                    except Exception as e:
                        raise Exception(
                            "Error occured while getting shortened final transcript: ",
                            e,
                        ) from e
                break

        try:
            random_duration = random.randint(50, 60)
            while True:
                total_transcript_duration = self.__get_total_transcript_duration(
                    shortened_transcript
                )

                if (
                    total_transcript_duration
                    and total_transcript_duration > random_duration
                ):
                    shortened_transcript = shortened_transcript[:-1]
                else:
                    break

            # Keeps on removing the last dictionary if it doesn't end with as full stop
            regex = r"[.!?]"
            max_remove_count = 3
            while True:
                if (
                    re.match(regex, shortened_transcript[-1].text[-1])
                    or not max_remove_count
                ):
                    break

                shortened_transcript = shortened_transcript[:-1]
                max_remove_count -= 1

            # Keep on removing the first dictionary if it doesn't end with a capital letter (not start of a sentence)
            max_remove_count = 1
            while True:
                if shortened_transcript[0].text[0].isupper() or not max_remove_count:
                    break

                shortened_transcript = shortened_transcript[1:]
                max_remove_count -= 1

            transcript_duration = self.__get_total_transcript_duration(
                shortened_transcript
            )

            if not transcript_duration or transcript_duration < 15:
                logger.error(
                    f"Transcript duration is less than 15 seconds: {transcript_duration}"
                )
                return

            final_transcript_chunk = FinalTranscriptChunk(
                transcript=shortened_transcript,
                transcript_duration=transcript_duration,
            )

            return final_transcript_chunk
        except Exception as e:
            logger.error("Error occured: ", e)

    def _generate_shorts(self, shorts_final_transcripts: List):
        # for now, just download the podcast and get shorts, unedited.
        download_response = download_podcast(self.podcast_url)
        if download_response["status"] == "success":
            logger.info("Podcast downloaded successfully")
            clip_shorts_data = []
            for short_transcript in shorts_final_transcripts:
                clipped_short_data = self._clip_short(
                    "./shorts",
                    download_response["output_path"],
                    download_response["filename"],
                    short_transcript,
                )
                if not "short_transcript" in clipped_short_data:
                    continue
                else:
                    clip_shorts_data.append(clipped_short_data)

            if not self.debugging:
                os.remove(
                    f"{download_response['output_path']}/{download_response['filename']}"
                )

            return clip_shorts_data
        else:
            raise ValueError(
                f"Error while downloading the podcast: {download_response['error']}"
            )

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
        if self.transcriptor_type == "yt_transcript_api":
            short_start_time = short_transcript["transcript"][0]["start"]
            short_end_time = (
                short_transcript["transcript"][-1]["start"]
                + short_transcript["transcript"][-1]["duration"]
            )
        elif self.transcriptor_type == "assembly_ai":
            short_start_time = short_transcript[0]["start_time"]
            short_end_time = short_transcript[-1]["end_time"]
        else:
            raise ValueError("Transcriptor type is not valid")

        short_filename = f"{filename}_short_{short_start_time}_{short_end_time}.mp4"
        clipped_video_path = os.path.join(
            shorts_output_path, f"mobile_ratio_{short_filename}"
        )
        original_clip_video_path = os.path.join(
            shorts_output_path, f"original_{short_filename}"
        )

        if self.transcriptor_type == "yt_transcript_api":
            # use moviepy to clip the video
            clipped_video = VideoFileClip(podcast_path).subclip(
                short_start_time, short_end_time
            )
        elif self.transcriptor_type == "assembly_ai":
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
        else:
            raise ValueError("Transcriptor type is not valid")

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

        return [
            transcription
            for transcription in cleaned_transcripts_feedback
            if transcription.stats.should_make_short == should_make_short
        ]

    def __get_transcripts_feedback(
        self, full_sentences_transcript: PodcastTranscript
    ) -> List[TranscriptFeedbackType]:
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
            if self.llm_type == "openai":
                chat_completion = ChatCompletion(
                    llm_type=self.llm_type,
                    llm_model=self.llm_model,
                    api_key=self.llm_api_key,
                )
                response = chat_completion.generate(
                    system_prompt=prompt,
                    user_message=f"Here is the transcript chunk: {chunk}",
                    return_type=TranscriptStats,
                )
            elif self.llm_type == "ollama":
                chat_completion = ChatCompletion(
                    llm_type=self.llm_type,
                    llm_model=self.llm_model,
                    ollama_base_url=self.ollama_base_url,
                )
                response = chat_completion.generate(
                    user_message=prompt, return_type=TranscriptStats
                )
            else:
                raise ValueError("LLM type is not valid")

            logger.info("Successfully got response")

            transcript_and_feedback_chunk = TranscriptFeedback(
                transcript=chunk,
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
        chunk_transcript_list: List[PodcastTranscript] = []
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

    def __get_total_transcript_duration(
        self, transcript: PodcastTranscript
    ) -> Union[float, None]:
        if len(transcript) == 0:
            return

        if isinstance(transcript[0], YoutubeAPITranscript):
            return transcript[-1].start + transcript[-1].duration - transcript[0].start

    def __validate_params(self):
        invalid_params = False
        if self.transcriptor_type == "assembly_ai" and not self.assembly_api_key:
            logger.error(
                "Assembly AI API Key must be passed in class initialization when using assembly_ai"
            )
            invalid_params = True
        if self.llm_type == "openai" and self.llm_model and "gpt" not in self.llm_model:
            logger.error("OpenAI model must be a GPT model")
            invalid_params = True
        if self.llm_type == "openai" and not self.llm_api_key:
            logger.error(
                "OpenAI API Key must be passed in class initialization when using openai"
            )
            invalid_params = True
        if self.llm_type == "ollama" and not self.ollama_base_url:
            logger.error(
                "ollama_host_url must be passed in class initialization when using ollama"
            )
            invalid_params = True
        if self.llm_type not in ["openai", "ollama"]:
            logger.error("LLM type is not valid")
            invalid_params = True
        if invalid_params:
            raise ValueError("Invalid parameters passed")

    @overload
    def __get_final_transcript(
        self,
        prompt: str,
        short_transcript: List[AssemblyAIParsedTranscript],
    ) -> AssemblyShortFinalTranscript: ...

    @overload
    def __get_final_transcript(
        self,
        prompt: str,
        short_transcript: List[YoutubeAPITranscript],
    ) -> FinalTranscriptChunk: ...

    def __get_final_transcript(
        self,
        prompt: str,
        short_transcript: Union[
            List[AssemblyAIParsedTranscript], List[YoutubeAPITranscript]
        ],  # If it is provided, we are using assembly ai.
    ) -> Union[AssemblyShortFinalTranscript, FinalTranscriptChunk]:
        """
        Internal method to get final transcript for a short
        """
        if self.llm_type == "openai":
            chat_completion = ChatCompletion(
                llm_type=self.llm_type,
                llm_model=self.llm_model,
                api_key=self.llm_api_key,
            )
        elif self.llm_type == "ollama":
            chat_completion = ChatCompletion(
                llm_type=self.llm_type,
                llm_model=self.llm_model,
                ollama_base_url=self.ollama_base_url,
            )
        else:
            raise ValueError("LLM type is not valid")

        if short_transcript:  # assembly transcript
            llm_response = chat_completion.generate(
                system_prompt=prompt,
                user_message=f"Here is the transcript: {short_transcript}",
                return_type=AssemblyShortFinalTranscript,
            )
            return llm_response
        else:  # youtube transcript
            llm_response = chat_completion.generate(
                user_message=prompt,
                return_type=YouTubeAPIStartEndTimes,
            )
            final_transcript = llm_response

            yt_api_short_transcript: List[YoutubeAPITranscript] = [
                short_transcript_model
                for short_transcript_model in short_transcript
                if isinstance(short_transcript_model, YoutubeAPITranscript)
            ]
            final_transcript_chunk = self._cleanup_shortened_transcript_response(
                final_transcript,
                yt_api_short_transcript,
            )

            if final_transcript_chunk:
                return final_transcript_chunk
            else:
                raise Exception(
                    "Final transcript chunk empty. Nothing appended to 'final_transcripts'."
                )
