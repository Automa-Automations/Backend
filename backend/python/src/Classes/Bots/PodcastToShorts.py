from youtube_transcript_api import YouTubeTranscriptApi
from typing import  List 
from ollama import Client
from dotenv import load_dotenv
from pytube import YouTube
import os
import json
import math
load_dotenv()
import re

OLLAMA_HOST_URL=os.getenv("OLLAMA_HOST_URL")

# import dataclass
from dataclasses import dataclass

llama_client = Client(OLLAMA_HOST_URL)

@dataclass
class PodcastToShorts:
    podcast_url: str
    llama_model: str = "llama3"

    def __post_init__(self):
        self.__validate_env_variables()
        self.yt = YouTube(self.podcast_url)
        self.debugging = True

    def get_shorts(self):
        """
        Method to generate the shorts from the podcast
        """
        transcript = self.__get_video_transcript(self.podcast_url)
        print(f"Transcript: (length: {len(transcript)}): {transcript}")
        #
        podcast_length = round((transcript[-1]["start"] + transcript[-1]["duration"]) / 60)
        print(f"Podcast Length: {podcast_length} minutes")

        if self.debugging:
            with open("./src/Classes/Bots/shorts_transcripts.json", "r") as f:
                shorts_transcripts = json.load(f)
        else:
            transcriptions_feedback = self.__get_transcripts_feedback(transcript)
            print(f"Transcriptions With Feedback: (length: {len(transcriptions_feedback)}): {transcriptions_feedback}")

            shorts_transcripts = self.__filter_transcripts(transcriptions_feedback)
            print(f"Shorts Transcripts: (length: {len(shorts_transcripts)}): {shorts_transcripts}")

        # take each short, use OpenAI to remove all unnecessary content in the start, so that it is just the short. 
        shorts_final_transcripts = self.__get_shorts_final_transcripts(shorts_transcripts)
        print(f"Shorts Final Transcripts: (length: {len(shorts_final_transcripts)}): {shorts_final_transcripts}")

        clip_shorts_data = self._generate_shorts(shorts_transcripts, shorts_final_transcripts)
        print(f"Clip Shorts Data: (length: {len(clip_shorts_data)}): {clip_shorts_data}")

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

        # chunk shorts_transcripts into lists, each list being the length of shorts_transcripts / total_shorts. It should select the best one from each list.
        chunked_shorts_transcripts = []
        current_chunk = []

        for short_dict in shorts_transcripts:
            if len(current_chunk) < math.floor(len(shorts_transcripts) / total_shorts):
                current_chunk.append(short_dict)
            else:
                current_chunk.remove(short_dict, param2, param3)
                print(f"Current Chunk: {current_chunk}")
                print(f"Current Chunk Length: {len(current_chunk)}")

        best_shorts = []

        for chunk_list in chunked_shorts_transcripts:
            best_short = self.__get_best_short(chunk_list)
            best_shorts.append(best_short)

        return best_shorts

    def __get_best_short(self, chunk_list: List[dict]):
        prompt = f"""
        Here are the shorts transcripts: {json.dumps(chunk_list, indent=4)}. Decide which one is the best for a short (you must only chooose 1). Return that short dictionary in the exact same format as it was given to you. 
        """
        best_short = json.loads(llama_client.generate(
            model=self.llama_model,
            prompt=prompt,
            format="json",
            keep_alive="1m"
        )["response"])

        return best_short 

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
            prompt = f"""I want to make a great short of 15 - 55 seconds long
            from the following transcript: {json.dumps(short["transcript"])}.
            Give me the perfect start text and end text for the short that will
            make it the most engaging from the transcript. Note, the start and
            end text must be from the transcript. The start text must be before
            the end text. The start text must be engaging, and the end text
            must be a good ending to the short. The start text must be the
            beginning of a sentence, and the end text must end a sentence.
            Your output in the following format (ignore the values):
            {json.dumps({
                "start_text": "the exact start text",
                "end_text": "the exact end text"
            }, indent=4)}"""
            llama_test = json.loads(llama_client.generate(
                model=self.llama_model,
                prompt=prompt,
                format="json",
                keep_alive="1m"
            )["response"])

            shortened_transcript = []
            for idx, dict in enumerate(short["transcript"]):
                if dict["text"] == llama_test["start_text"]:
                    count = 0
                    while dict["text"] != llama_test["end_text"] and len(shortened_transcript) < len(short["transcript"]) - (idx + 1):
                        try:
                            # regex to match [any character in here, with as much of them as possible]
                            regex = r"[a-zA-Z0-9\s]"
                            cleaned_text = short["transcript"][idx+count]["text"].replace("\n", " ")
                            # replace cleaned_text matched of regex with ""
                            cleaned_text = re.sub(regex, "", cleaned_text)
                            append_dict = short["transcript"][idx+count]
                            append_dict["text"] = cleaned_text

                            shortened_transcript.append(append_dict)
                            count += 1
                        except Exception as e:
                            break
                    break


            # keeps on removing a dictionary in the start then in the end (alternating) if the length is longer than 55
            remove_dict_type = "end"
            while True:
                first_start_time = shortened_transcript[0]["start"]
                last_start_time = shortened_transcript[-1]["start"]
                end_time = last_start_time + shortened_transcript[-1]["duration"]
                if end_time - first_start_time > 55:
                    shortened_transcript = shortened_transcript[1:] if remove_dict_type == "start" else shortened_transcript[:-1]
                else:
                    break

            # Keeps on removing the last dictionary if it doesn't end with as full stop
            regex = r"[.!?]"
            max_remove_count = 3
            while not re.match(regex, shortened_transcript[-1]["text"]) and max_remove_count != 3:
                llama_test = llama_test[:-1]
                max_remove_count -= 1

            # Keep on removing the first dictionary if it doesn't end with a capital letter (not start of a sentence)
            while not shortened_transcript[0].isupper() and max_remove_count != 3:
                llama_test = llama_test[1:]
                max_remove_count -= 1

            append_dict = {
                "transcript": shortened_transcript,
                "stats": short["stats"]
            }

            final_transcripts.append(append_dict)

            if self.debugging:
                with open("./src/Classes/Bots/shorts_final_transcripts.json", "w") as f:
                    f.write(json.dumps(final_transcripts, indent=4))
                    print("saved shorts final transcripts to shorts_final_transcripts.json")

        return final_transcripts

    def _generate_shorts(self, shorts_transcripts: List[dict], shorts_final_transcripts: List):
        # for now, just download the podcast and get shorts, unedited.
        download_test = self.__download_podcast();
        if download_test["status"] == "success":
            clip_shorts_data = []
            for short in shorts_final_transcripts:
                clipped_short_data = self._clip_short(short, download_test["output_path"], download_test["filename"], short)
                clip_shorts_data.append(clipped_short_data)

            return clip_shorts_data
        else:
            raise ValueError(f"Error while downloading the podcast: {download_test['error']}")

    def _clip_short(self, short: dict, output_path: str, filename: str, short_transcript):
        print("Clipping short")
        print(short)
        return

    def __download_podcast(self, output_path: str = "downloads/", filename: str = ""):
        try:
            if filename == "":
                filename = self.yt.title

            self.yt.streams.get_highest_resolution().download(output_path=output_path, filename=filename)
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

    def __filter_transcripts(self, transcriptions_feedback: List[dict], should_make_short : bool = True):
        """
        Method to filter the transcriptions based on the should_make_short value
        Parameters:
        - transcriptions_feedback: list: The list of the feedback of the transcriptions
        - should_make_short: bool: The value to filter the transcriptions
        Returns:
        - list: The list of the transcriptions that have the should_make_short value
        """
        return [transcription for transcription in transcriptions_feedback if transcription["stats"]["should_make_short"] == should_make_short]

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

            response = json.loads(llama_client.generate(
                model=self.llama_model,
                prompt=prompt,
                format="json",
                keep_alive="1m"
            )["response"])

            feedback_chunk = {
                "transcript": chunk,
                "stats": response,
            }

            transcripts_feedback.append(feedback_chunk)
            if self.debugging:
                with open("./src/Classes/Bots/transcripts_feedback.json", "w") as f:
                    f.write(json.dumps(transcripts_feedback, indent=4))
                    print("saved transcripts feedback for this chunk to transcripts_feedback.json")
            else:
                processed_feedback_chunk = self.__process_feedback_chunk(feedback_chunk, parent_length=len(transcripts_feedback)) 
                print(f"Processed Feedback Chunk: {processed_feedback_chunk}")
                print(f"Processed Feedback Chunk Length: {len(processed_feedback_chunk)}")

            with open("./src/Classes/Bots/transcripts_score.json", "w") as f:
                f.write(json.dumps([transcript["stats"] for transcript in transcripts_feedback], indent=4))
                print("saved scores to transcripts_score.json")

        return transcripts_feedback
    
    def __process_feedback_chunk(chunk, parent_length: str): 
        for transcript_dict in chunk["transcripts"]:
            transcript = transcript_dict["text"]

            for characer in transcript:
                if characer == "\n":
                    transcript = transcript.replace(characer, " ")
                # check if character contains any chracters that isn't a string, a number, or a ".?"
                elif not re.match(r"[a-zA-Z0-9\s.!?]", characer):
                    transcript = transcript.replace(characer, "")
                else: 
                    continue

        return chunk

    def __get_video_transcript(self, video_url: str):
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
            if len(json.dumps(current_chunk)) + len(json.dumps(transcript_dict)) < chunk_length - 100:
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
