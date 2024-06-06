from youtube_transcript_api import YouTubeTranscriptApi
from typing import List, TypedDict, Union
import face_recognition
from ollama import Client
from dotenv import load_dotenv
from pytube import YouTube
import os
import json
import base64
from moviepy.editor import VideoFileClip
from fuzzywuzzy import fuzz
import random

load_dotenv()
import re

OLLAMA_HOST_URL = os.getenv("OLLAMA_HOST_URL")

# import dataclass
from dataclasses import dataclass

llama_client = Client(OLLAMA_HOST_URL)

class TranscriptDict(TypedDict):
    text: str
    start: float
    duration: float

@dataclass
class PodcastToShorts:
    podcast_url: str
    llama_model: str = "llama3"

    def __post_init__(self):
        self.__validate_env_variables()
        self.yt = YouTube(self.podcast_url)
        self.debugging = True

    def get_shorts(self, debugging=False):
        """
        Method to generate the shorts from the podcast
        """
        transcript = self._get_video_transcript(self.podcast_url)
        print(f"Transcript: (length: {len(transcript)})")
        #
        podcast_length = round(
            (transcript[-1]["start"] + transcript[-1]["duration"]) / 60
        )
        print(f"Podcast Length: {podcast_length} minutes")

        if self.debugging or debugging:
            with open("./src/Classes/Bots/transcripts_feedback.json", "r") as f:
                transcriptions_feedback = json.load(f)
        else:
            transcriptions_feedback = self.__get_transcripts_feedback(transcript)
        print(
            f"Transcriptions With Feedback: (length: {len(transcriptions_feedback)}): {transcriptions_feedback}"
        )

        shorts_transcripts = self.__filter_transcripts(transcriptions_feedback)
        print(
            f"Shorts Transcripts: (length: {len(shorts_transcripts)}): {shorts_transcripts}"
        )

        if len(shorts_transcripts) < round(podcast_length / 10):
            # get all the shorts that is "should_make_short" false. We need to get the best of them, so that there is enough shorts.
            print("length of shorts transcripts not enough. Getting extra shorts...")
            other_shorts = self.__filter_transcripts(
                transcriptions_feedback, should_make_short=False
            )
            extra_shorts = self.__get_best_shorts(
                shorts_transcripts=other_shorts,
                total_shorts=round(podcast_length / 10) - len(shorts_transcripts),
            )
            shorts_transcripts.extend(extra_shorts)
            print(f"New shorts transcripts length: {len(shorts_transcripts)}")

        elif len(shorts_transcripts) > round(podcast_length / 10):
            # Make a new list by putting only the highest scores in there, so that it is the length of round(podcast_length / 10)
            print("Shorts transcripts length is too long...")
            highest_score_list = sorted(
                shorts_transcripts, key=lambda x: x["stats"]["score"], reverse=True
            )[: round(podcast_length / 10)]

            print(f"New shorts transcripts length: {len(highest_score_list)}. Before, it was a length of {len(shorts_transcripts)}")
            shorts_transcripts = highest_score_list

        if self.debugging or debugging:
            print("Loading from shorts_final_transcripts.json...")
            with open("./src/Classes/Bots/shorts_final_transcripts.json", "r") as f:
                shorts_final_transcripts = json.load(f)
        else:
            # take each short, use OpenAI to remove all unnecessary content in the start and end, only getting the juicy part, so that it is just the short.
            print("Getting shorts final transcripts...")
            shorts_final_transcripts = self.__get_shorts_final_transcripts(
                shorts_transcripts
            )
        print(
            f"Shorts Final Transcripts: (length: {len(shorts_final_transcripts)}): {shorts_final_transcripts}"
        )

        print("Generating shorts...")
        clip_shorts_data = self._generate_shorts(
            shorts_final_transcripts
        )
        print(
            f"Clip Shorts Data: (length: {len(clip_shorts_data)}): {clip_shorts_data}"
        )

        return clip_shorts_data

    def __get_best_shorts(self, shorts_transcripts: List[dict], total_shorts: int):
        """
        Method to get the best shorts from the passed in shorts
        Parameters:
        - shorts_transcripts: list: The list of the shorts transcripts
        - total_shorts: int: The total number of shorts needed
        Returns:
        - list: The list of the best shorts
        """

        # sort the shorts_transcripts by the score, in descending order
        descending_sorted_shorts = sorted(shorts_transcripts, key=lambda x: x["stats"]["score"], reverse=True)
        best_shorts = descending_sorted_shorts[:total_shorts]
        print(f"Got an extra {len(best_shorts)} shorts.")
        return best_shorts

    def __get_shorts_final_transcripts(self, shorts_transcripts: List[dict]):
        """
        Method to get the final transcripts of the shorts, by removing the start and end sentences, to get the optimized short.
        Parameters:
        - shorts_transcripts: list: The list of the shorts transcripts
        Returns:
        - list: The list of the final transcripts of the shorts
        """
        final_transcripts = []
        for short in shorts_transcripts:
            prompt = f"""I want to make a great short of 15 - 55 seconds long from the following transcript: {json.dumps(short["transcript"])}. Give me the perfect start text and end text from the transcript that will be the perfect start and end for making an engaging short (DON'T USE THE FIRST TEXT AND THE LAST TEXT FROM THE TRANSCRIPT I GAVE YOU, IT MUST START A LITTLE BIT LATER ON.) Note, the start and end text must be from the transcript. The start text must be before the end text. The start text must be the best starting sentence from the transcript for a short, and the end text must be a the best ending sentence from the transcript for a short. The start text must be the beginning of a sentence, and the end text must end a sentence (meaning first character for start text must be a capital letter, indicating it is the start of a sentence, and the end sentence should be ending with an ending character - "?.!". Keep the start and end text the exact same as what it was from the transcript.

            The start text may not be "{short["transcript"][0]["text"]}", and the end text may not be "{short["transcript"][-1]["text"]}".
            Your output in the following format (ignore the values):
            {json.dumps({
                "start_text": "the exact start text",
                "end_text": "the exact end text"
            }, indent=4)}"""

            llama_response = json.loads(
                llama_client.generate(
                    model=self.llama_model,
                    prompt=prompt,
                    format="json",
                    keep_alive="1m",
                )["response"]
            )

            llama_response["start_text"] = llama_response["start_text"].replace("\n", " ")
            llama_response["end_text"] = llama_response["end_text"].replace("\n", " ")

            shortened_transcript = []
            print("\n")
            for idx, dict in enumerate(short["transcript"]):
                dict["text"] = dict["text"].replace("\n", " ")

                current_text = dict["text"]
                is_similar = validate_similarity(current_text, llama_response["start_text"], 80)
                print(f'{idx+1}. "{current_text}" == "{llama_response["start_text"]}": {is_similar}')
                if is_similar:
                    count = 0
                    while not validate_similarity(current_text, llama_response["end_text"]) and len(
                        shortened_transcript
                    ) < len(short["transcript"]) - (idx + 1):
                        try:
                            regex = r"\[.*?\]"
                            pattern = r'\b[A-Z]{4,}\b(:\s*)?'

                            current_text = short["transcript"][idx + count]["text"]
                            current_text = re.sub(pattern, "", current_text)
                            current_text = re.sub(r'\s+', ' ', current_text).strip()

                            print(f"Current Text: {current_text}")

                            current_text = re.sub(regex, "", current_text).replace("\n", " ")
                            append_dict = short["transcript"][idx + count]
                            append_dict["text"] = current_text

                            shortened_transcript.append(append_dict)
                            count = count + 1
                        except Exception as e:
                            print("Exception occured: ", e)
                            break
                    break


            try:
                random_duration = random.randint(50, 60)
                while True:
                    total_transcript_duration = self.__get_total_transcript_duration(shortened_transcript)

                    if total_transcript_duration and total_transcript_duration > random_duration:
                        shortened_transcript = (
                            shortened_transcript[:-1]
                        )
                    else:
                        break

                # Keeps on removing the last dictionary if it doesn't end with as full stop
                regex = r"[.!?]"
                max_remove_count = 3
                while True:
                    if re.match(regex, shortened_transcript[-1]["text"][-1]) or not max_remove_count:
                        break

                    shortened_transcript = shortened_transcript[:-1]
                    max_remove_count -= 1

                # Keep on removing the first dictionary if it doesn't end with a capital letter (not start of a sentence)
                max_remove_count = 1
                while True:
                    if shortened_transcript[0]["text"][0].isupper() or not max_remove_count:
                        break

                    shortened_transcript = shortened_transcript[1:]
                    max_remove_count -= 1

                transcript_duration = self.__get_total_transcript_duration(shortened_transcript)
                if transcript_duration and transcript_duration < 15:
                    continue
                if not transcript_duration: 
                    continue

                append_dict = {"transcript": shortened_transcript, "stats": short["stats"]}
                append_dict["stats"]["transcript_duration"] = transcript_duration

                final_transcripts.append(append_dict)
            except Exception as e:
                print("Error occured: ", e)
                continue

            if self.debugging:
                with open("./src/Classes/Bots/shorts_final_transcripts.json", "w") as f:
                    f.write(json.dumps(final_transcripts, indent=4))
                    print(
                        "saved shorts final transcripts to shorts_final_transcripts.json"
                    )

        return final_transcripts

    def _generate_shorts(
        self, shorts_final_transcripts: List
    ):
        # for now, just download the podcast and get shorts, unedited.
        download_response = self._download_podcast()
        if download_response["status"] == "success":
            print("Podcast downloaded successfully")
            clip_shorts_data = []
            for short_transcript in shorts_final_transcripts:
                clipped_short_data = self._clip_short(
                    download_response["output_path"],
                    download_response["filename"],
                    short_transcript,
                )
                if not "short_transcript" in clipped_short_data:
                    continue
                else:
                    clip_shorts_data.append(clipped_short_data)

            return clip_shorts_data
        else:
            raise ValueError(
                f"Error while downloading the podcast: {download_response['error']}"
            )

    def _clip_short(
        self, output_path: str, filename: str, short_transcript
    ) -> dict:
        print("Clipping short...")
        podcast_path = os.path.join(output_path, filename)
        short_start_time = short_transcript["transcript"][0]["start"]
        short_end_time = short_transcript["transcript"][-1]["start"] + short_transcript["transcript"][-1]["duration"]

        short_filename = f"{filename}_short_{short_start_time}_{short_end_time}.mp4"
        clipped_video_path = os.path.join(output_path, f"mobile_ratio_{short_filename}")

        # use moviepy to clip the video 
        clipped_video = VideoFileClip(podcast_path).subclip(short_start_time, short_end_time)
        try:
            # clip video to mobile aspect ratio (9:16), along with following faces smoothly
            print("Clipping short to mobile aspect ratio, along with following faces smoothly...")
            mobile_ratio_follow_faces_short = self._clip_and_follow_faces_mobile_ratio(clipped_video)

            mobile_ratio_follow_faces_short.write_videofile(clipped_video_path)

            with open(clipped_video_path, "rb") as video_file:
                base64_clipped_video = base64.b64encode(video_file.read()).decode('utf-8')

            return_dict = {
                "short_transcript": short_transcript,
                "clipped_video_path": clipped_video_path,
                "base64_clipped_video": base64_clipped_video,
                "short_filename": short_filename,
            }
            return return_dict

        except Exception as e:
            print(f"Error while clipping short to right aspect ratio and adding in face detection: {e}")
            return {}

    def _clip_and_follow_faces_mobile_ratio(self, video_clip: VideoFileClip) -> VideoFileClip:
        try:
            # Define the target aspect ratio for mobile (9:16)
            target_aspect_ratio = 9 / 16
            original_width, original_height = video_clip.size
            
            # Calculate the target height based on the original width
            target_height = original_height
            target_width = int(target_height * target_aspect_ratio)

            def process_frame(frame):
                face_locations = face_recognition.face_locations(frame)

                if face_locations:
                    # Choose the first face detected
                    top, right, bottom, left = face_locations[0]

                    face_center_x = (left + right) // 2
                    face_center_y = (top + bottom) // 2

                    # Calculate the top-left corner of the crop box
                    crop_x = max(0, face_center_x - target_width // 2)
                    crop_y = max(0, face_center_y - target_height // 2)

                    # Ensure the crop box is within the frame bounds
                    if crop_x + target_width > frame.shape[1]:
                        crop_x = frame.shape[1] - target_width
                    if crop_y + target_height > frame.shape[0]:
                        crop_y = frame.shape[0] - target_height

                    # Ensure the crop coordinates are non-negative
                    crop_x = max(0, crop_x)
                    crop_y = max(0, crop_y)

                    # Crop the frame to the target aspect ratio
                    cropped_frame = frame[crop_y:crop_y + target_height, crop_x:crop_x + target_width]
                else:
                    # If no face is detected, center the frame
                    crop_x = (frame.shape[1] - target_width) // 2
                    crop_y = (frame.shape[0] - target_height) // 2
                    cropped_frame = frame[crop_y:crop_y + target_height, crop_x:crop_x + target_width]

                return cropped_frame

            # Apply the process_frame function to each frame of the video clip
            processed_clip = video_clip.fl_image(process_frame)
            # Remove the original video clip from memory
            video_clip.close()

            return processed_clip
        except Exception as e:
            print(f"Error in _clip_and_follow_faces_mobile_ratio: {e}")
            raise e

    def _download_podcast(self, output_path: str = "downloads/", filename: str = ""):
        try:
            if filename == "":
                filename = self.yt.title

            self.yt.streams.get_highest_resolution().download(
                output_path=output_path, filename=filename
            )
            return {
                "output_path": output_path,
                "filename": filename,
                "status": "success",
            }
        except Exception as e:
            return {
                "error": e,
                "status": "error",
            }

    def __filter_transcripts(
        self, transcriptions_feedback: List[dict], should_make_short: bool = True
    ):
        """
        Method to filter the transcriptions based on the should_make_short value
        Parameters:
        - transcriptions_feedback: list: The list of the feedback of the transcriptions
        - should_make_short: bool: The value to filter the transcriptions
        Returns:
        - list: The list of the transcriptions that have the should_make_short value
        """
        return [
            transcription
            for transcription in transcriptions_feedback
            if transcription["stats"]["should_make_short"] == should_make_short
        ]

    def __get_transcripts_feedback(self, full_sentences_transcript):
        """
        Method to get the feedback of the transcriptions
        Parameters:
        - full_sentences_transcript: list: The list of the full sentences of the transcriptions
        Returns:
        - list: The list of the feedback of the transcriptions
        """
        chunked_transcript = self.__chunk_transcript(full_sentences_transcript)
        transcripts_feedback = []
        for idx, chunk in enumerate(chunked_transcript):
            prompt = f"""
            Here is transcript data from a long-form podcast style video: {chunk}. Decide whether or not a specific part of the transcript or the whole transcript is valid for a short. Evaluate the short based off of this:
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
            10. Soneone talking about how they went through difficult times, something that could resonate with the audience.
            should_make_short: True or False. True, if the score is above or equal to 70, false if it is below 70
            feedback: Any feedback on the short, what is good and bad about the transcript, how to make it better. Note: only evaluate it based off of the transcript. Don't give feedback saying that there could be visuals or animations. 
###
            Please output in the following format (ignore the values, just use the structure):
            {{
                "score": a score out of 100, on how good this would make for a short. Be quite strict here, as the goal is to make the short as engaging as possible. Use an integer here. Don't surround this value with "",
                "should_make_short": True or False. True, if the score is above or equal to 70, false if it is below 70. Don't surround this value with "",
                "feedback": "Any feedback on the short, what is good and bad about the transcript, how to make it better."
            }}
            """

            response = json.loads(
                llama_client.generate(
                    model=self.llama_model,
                    prompt=prompt,
                    format="json",
                    keep_alive="1m",
                )["response"]
            )

            feedback_chunk = {
                "transcript": chunk,
                "stats": response,
            }

            print(f"{idx+1}. Formatted Chunk: {chunk}")
            print(
                f"{idx+1}. Feedback Chunk Stats Length: {len(feedback_chunk["stats"])}"
            )

            transcripts_feedback.append(feedback_chunk)
            with open("./src/Classes/Bots/transcripts_feedback.json", "w") as f:
                f.write(json.dumps(transcripts_feedback, indent=4))
                print(
                    "saved transcripts feedback for this chunk to transcripts_feedback.json"
                )

            with open("./src/Classes/Bots/transcripts_score.json", "w") as f:
                f.write(
                    json.dumps(
                        [transcript["stats"] for transcript in transcripts_feedback],
                        indent=4,
                    )
                )
                print("saved scores to transcripts_score.json")

        return transcripts_feedback

    def _get_video_transcript(self, video_url: str):
        """
        Method to get the video transcript from the video url
        Parameters:
        - video_url: str: The url of the video
        Returns:
        - video_transcript: list: The list of the transcript of the video
        """
        if "youtu.be" in video_url:
            # Share url type
            video_id = video_url.split("?")[0].split("be/")[1]
            print(f"Video ID: {video_id}")
        elif "youtube" in video_url:
            # watch url type
            video_id = video_url.split("v=")[1]
            print(f"Video ID: {video_id}")
        else:
            raise ValueError(f"Incorrect url format: {video_url}")

        video_transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return video_transcript

    def __chunk_transcript(self, video_transcript: str, chunk_length: int = 4000):
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

        return chunk_transcript_list

    def __validate_env_variables(self):
        """
        Method to evaluate the environment variables, and raise error if needed
        """
        if not OLLAMA_HOST_URL:
            raise ValueError("OLLAMA_HOST_URL is not set in the environment variables")

    def __get_total_transcript_duration(self, transcript: List[TranscriptDict]) -> Union[float, None]:
        if len(transcript) == 0:
            return

        return transcript[-1]["start"] + transcript[-1]["duration"] - transcript[0]["start"]

# TODO: PUT THIS IN UTILS LATER 
def validate_similarity(string1, string2, percentage = 80):
    """
    Method to validate the similarity between two strings
    Parameters:
    - string1: str: The first string
    - string2: str: The second string
    - percentage: int: The percentage of similarity
    Returns:
    - bool: The value of the similarity
    """

    def get_similarity_score(string1, string2):
        return fuzz.token_sort_ratio(string1, string2)

    # check if strings are above 80% similar
    similarity_score = get_similarity_score(string1, string2)

    if len(string1) > 10 and string1 in string2 or len(string2) > 10 and string2 in string1:
        similarity_score = 100

    is_similar_1 = get_similarity_score(string1[:10], string2) >= percentage
    is_similar_2 = get_similarity_score(string2[:10], string1) >= percentage

    if len(string1) > 10 and is_similar_1:
        return True

    if len(string2) > 10 and is_similar_2:
        return True

    if len(string1) > 20:
        if string1[:20] in string2:
            similarity_score = 100

    if len(string2) > 20:
        if string2[:20] in string1:
            similarity_score = 100

    return similarity_score >= percentage
