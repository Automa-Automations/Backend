from typing import List, Optional
from openai import OpenAI
from pydantic import ValidationError
from aliases import (
    PodcastTranscript,
    MoviePyClip,
    TranscriptFeedback,
    TranscriptFeedbackList,
)
from errors import EditVideoError, GenerationError
from models import (
    ClipShortData,
    ParsedTranscript,
    TranscriptStats,
)
from src.Classes.Utils.FaceTrackingVideo import FaceTrackingVideo
from pytube import YouTube
import os
import json
import base64
from moviepy.editor import VideoFileClip, concatenate_videoclips
import logging
import re
from src.Classes.Utils.PodcastTranscriber import PodcastTranscriber
from src.utils import (
    format_yt_video_url,
    download_podcast,
)

logger = logging.getLogger(__name__)


class PodcastToShorts:
    def __init__(
        self,
        podcast_url: str,
        assembly_api_key: str,
        openai_model: Optional[str] = "gpt-4o",
        openai_api_key: Optional[str] = os.environ.get("OPENAI_API_KEY") or "",
    ) -> None:
        self.openai = OpenAI(api_key=openai_api_key)
        self.podcast_url = podcast_url
        self.assembly_api_key = assembly_api_key
        self.openai_model = openai_model or "gpt-4o"
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
        transcriptor = PodcastTranscriber()
        transcript, audio_duration = transcriptor.get_transcript(
            podcast_url=self.podcast_url,
            api_key=self.assembly_api_key,
            debugging=self.debugging,
        )

        if not transcriptor:
            raise Exception("Transcriptor is none")

        podcast_length = round(audio_duration / 60)
        logger.info(f"Transcript objects length: {len(transcript)}")
        logger.info(f"Podcast Length: {podcast_length} minutes")

        if (self.debugging or debugging) and os.path.exists(
            self.debug_transcripts_feedback_path
        ):
            with open(self.debug_transcripts_feedback_path, "r") as f:
                logger.info("Loading from transcripts_feedback.json...")
                transcriptions_feedback: TranscriptFeedbackList = [
                    TranscriptFeedback.model_validate(feedback_dict)
                    for feedback_dict in json.load(f)
                ]
        else:
            transcriptions_feedback = self.__get_transcripts_feedback(transcript)
        logger.info(
            f"Transcriptions With Feedback length: {len(transcriptions_feedback)}"
        )

        shorts = self.__filter_transcripts(transcriptions_feedback)
        logger.info(f"Shorts Transcripts length: {len(shorts)}")

        if len(shorts) < round(podcast_length / 10):
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
                total_shorts=round(podcast_length / 10) - len(shorts),
            )
            # Doing this since it gives weird type mismatches when I try to add them together, even though they have the same type, since it is a union type of lists
            shorts: TranscriptFeedbackList = json.loads(
                json.dumps(shorts + extra_shorts)
            )
            logger.info(f"New shorts transcripts length: {len(shorts)}")

        elif len(shorts) > round(podcast_length / 10):
            # Make a new list by putting only the highest scores in there, so that it is the length of round(podcast_length / 10)
            logger.info("Shorts transcripts length is too long...")
            shorts = json.loads(
                json.dumps(
                    sorted(
                        shorts,
                        key=lambda x: x.stats.score,
                        reverse=True,
                    )[: round(podcast_length / 10)]
                )
            )

            logger.info(f"New shorts transcripts length: {len(shorts)}.")

        if (self.debugging or debugging) and os.path.exists(
            self.debug_shorts_final_transcripts_path
        ):
            logger.info("Loading from shorts_final_transcripts.json...")
            with open(self.debug_shorts_final_transcripts_path, "r") as f:
                final_shorts: TranscriptFeedbackList = json.load(f)
        else:
            logger.info("Getting shorts final transcripts...")

            final_shorts: TranscriptFeedbackList = [
                self.__get_final_transcript(short) for short in shorts
            ]
        logger.info(
            f"Shorts Final Transcripts: (length: {len(final_shorts)}): {final_shorts}"
        )

        logger.info("Generating shorts...")
        clip_shorts_data = self._generate_shorts(final_shorts)
        logger.info(
            f"Clip Shorts Data: (length: {len(clip_shorts_data)}): {clip_shorts_data}"
        )

        return clip_shorts_data

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

        descending_sorted_shorts = sorted(
            shorts_transcripts,
            key=lambda x: int(x.stats.score),
            reverse=True,
        )
        best_shorts = descending_sorted_shorts[:total_shorts]
        logger.info(f"Got an extra {len(best_shorts)} shorts.")
        return best_shorts

    def _generate_shorts(self, shorts_final_transcripts: List):
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
        short: TranscriptFeedback,
    ) -> dict:
        logger.info("Clipping short...")

        if not os.path.exists(shorts_output_path):
            os.makedirs(shorts_output_path)

        podcast_path = os.path.join(podcast_output_path, filename)
        short_transcript = short.transcript
        short_start_time = short_transcript[0].start_time
        short_end_time = short_transcript[-1].end_time

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
                sentence_dict.start_time / 1000,
                sentence_dict.end_time / 1000,
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
                "base64_clipped_video": base64_clipped_video,
                "short_filename": short_filename,
            }
            return return_dict

        except Exception as e:
            raise EditVideoError(
                message=f"Error while clipping short to right aspect ratio and adding in face detection: {e}",
                video_type="short",
                action_type="process short",
            )

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
        system_prompt = f"""
            The user will provide you with a transcript that is a part of a long form podcast. Your job is to evaluate the transcript for its potential as a viral social media short (whether a part of the transcript has the potential to be turned into a viral short).
            A score of 70+/100 means that a part of the transcript is really good, that it qualifies to be a high quality short. Be relatively strict with the score, as we only want high quality shorts. The transcript or a part of the transcript must have at minimum one or two of the following criterias checked to be considered a score of 70+ :
               - Very engaging or interesting
               - Really funny
               - Highly motivating or inspiring
               - Highly educational or informative
               - Relevant to current trends
               - Strong, relatable story that evokes emotion
               - Unique content
               - "Badass" moments that inspire viewers
               - Stories of overcoming difficulties

            Output in JSON only, strictly in this exact output format:
            {{
                score: [the transcript score out of 100]
            }}
        """
        for idx, chunk in enumerate(chunked_transcript):
            user_message = f"Here is the transcript: {chunk}"
            max_retries = 5
            score = 0
            while max_retries:
                max_retries -= 1
                response = self.openai.chat.completions.create(
                    model=self.openai_model,
                    messages=[
                        {
                            "role": "system",
                            "content": system_prompt,
                        },
                        {
                            "role": "user",
                            "content": user_message,
                        }
                    ]
                )

                response_str = response.choices[0].message.content
                if not response_str:
                    logger.info(f"Error: OpenAI response is None.") if max_retries:
                    continue
                try:
                    response_json = json.loads(response_str)
                except json.JSONDecodeError:
                    logger.info("Error: Failed to decode json from OpenAI response.")
                    continue


                if not "score" in response_json:
                    logger.error(
                        f"'score' not in json responnse from LLM. Retrying..."
                    )
                    continue
                else:
                    score = int(response_json["score"])
                    break
            logger.info("Successfully got response")

            correct_dt_transcript = [
                model for model in chunk if isinstance(model, ParsedTranscript)
            ]
            transcript_and_feedback_chunk = TranscriptFeedback(
                transcript=correct_dt_transcript,
                score=score
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
        short: TranscriptFeedback,
    ) -> TranscriptFeedback:
        """
        Internal method to get final transcript for a short
        """
        system_prompt = f"""
        The user will always provide to you a part of a transcript from a long form podcast, that is a few minutes long. The user want to get only the most engaging part of the transcript that will be for a social media short. The end result transcript must be around 15 - 55 seconds long. Your job is to take the transcript provided to you by the user, keeping in only the most important and engaging sentences in, to reduce the duration. The quality of the final result you output in must be really good for a short. Your output in JSON, in the following output: {{ short_transcript: [...the short transcript dictionaries here, in the same format as the input transcript given to you by the user] }}
        """
        user_message = f"Here the transcript: {short.transcript}"

        max_retries = 5
        short_transcript: PodcastTranscript = []
        while max_retries:
            max_retries -= 1
            response = self.openai.chat.completions.create(
                model=self.openai_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
            )
            text = response.choices[0].message.content
            if not text:
                raise GenerationError(
                    message=f"Failed to generate final transcript, response is empty from OpenAI. OpenAI Chat Complmetion Response: {response}"
                )
            try:
                response_json = json.loads(text)
                if not "short_transcript" in response_json:
                    logger.error(
                        f"'short_transcript' not in json responnse from LLM. Retrying..."
                    )
                    continue
                short_transcript = [
                    ParsedTranscript.model_validate_json(transcript_dict)
                    for transcript_dict in response_json.short_transcript
                ]
                break
            except ValidationError:
                logger.info(
                    f"Failed to validate response from OpenAI to correct output. Response: {response}. Retrying..."
                )
                continue

        if not len(short_transcript):
            raise GenerationError(message=f"Max retries reached, transcript is empty.")

        short.transcript = short_transcript
        return short

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
