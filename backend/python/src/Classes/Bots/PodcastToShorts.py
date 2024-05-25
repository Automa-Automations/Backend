from youtube_transcript_api import YouTubeTranscriptApi
from typing import  List 
from ollama import Client
from dotenv import load_dotenv
from pytube import YouTube
import os
import json
import math
load_dotenv()

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
            with open("shorts_transcripts.json", "r") as f:
                shorts_transcripts = json.load(f)
        else:
            transcriptions_feedback = self.__get_transcripts_feedback(transcript)
            print(f"Transcriptions With Feedback: (length: {len(transcriptions_feedback)}): {transcriptions_feedback}")

            shorts_transcripts = self.__filter_transcripts(transcriptions_feedback)
            print(f"Shorts Transcripts: (length: {len(shorts_transcripts)}): {shorts_transcripts}")

            if len(shorts_transcripts) < round(podcast_length / 10):
                # get all the shorts that is "should_make_short" false. We need to get the best of them, so that there is enough shorts.
                other_shorts = self.__filter_transcripts(transcriptions_feedback, should_make_short=False)
                extra_shorts = self.__get_best_shorts(shorts_transcripts=other_shorts, total_shorts=round(podcast_length / 10) - len(shorts_transcripts))
                shorts_transcripts.extend(extra_shorts)

            elif len(shorts_transcripts) > round(podcast_length / 10):
                # Make a new list by putting only the highest scores in there, so that it is the length of round(podcast_length / 10)
                highest_score_list = sorted(shorts_transcripts, key=lambda x: x["stats"]["score"], reverse=True)[:round(podcast_length / 10)]
                shorts_transcripts = highest_score_list

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
                chunked_shorts_transcripts.append(current_chunk)
                current_chunk = [short_dict]

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
            prompt = f"""
            Below th example, I will give you the transcript. Remove a few start and end objects of the transcript, so that the result is a better transcript that makes sense, not starting or ending in a middle of a sentence. Additionally, yuu can remove a few start and end objects that are not needed, for an engaging short. Remove all unnecessary "cues", like [STUTTERING SOUNDS], [BACKGROUND MUSIC] (this are just a few examples. Remove all cues in the sentences that are in full capitals.) Here is an example input and example output so you have a better understanding on what to do. 
            ### Example Input:
            {json.dumps({
                "transcript": [
                    {
                        "text": "And speech therapy\ndidn't help that.",
                        "start": 5072.04,
                        "duration": 2.85
                    },
                    {
                        "text": "Nothing helped that.",
                        "start": 5074.89,
                        "duration": 1.53
                    },
                    {
                        "text": "I have to forgo a lot of\nshit to be as fucked up",
                        "start": 5076.42,
                        "duration": 3.78
                    },
                    {
                        "text": "as I am to build\nconfidence, for me",
                        "start": 5080.2,
                        "duration": 3.27
                    },
                    {
                        "text": "to stand in a fucking room of\n10,000-- of one person, and not",
                        "start": 5083.47,
                        "duration": 3.373
                    },
                    {
                        "text": "[STUTTERING SOUNDS] and be\nlike, oh, and put my head down.",
                        "start": 5086.843,
                        "duration": 2.417
                    },
                    {
                        "text": "Let me look around.",
                        "start": 5089.26,
                        "duration": 2.16
                    },
                    {
                        "text": "Let me read these\nparagraphs first.",
                        "start": 5091.42,
                        "duration": 3.037
                    },
                    {
                        "text": "And then before I\nread the paragraphs,",
                        "start": 5094.457,
                        "duration": 1.583
                    },
                    {
                        "text": "because they're\ncalling me next, let",
                        "start": 5096.04,
                        "duration": 1.5
                    },
                    {
                        "text": "me just leave the room\nbecause I'm going to stutter.",
                        "start": 5097.54,
                        "duration": 2.54
                    },
                    {
                        "text": "That's a miserable life.",
                        "start": 5100.08,
                        "duration": 2.2
                    },
                    {
                        "text": "And that's one of many\nthings I did besides lying,",
                        "start": 5102.28,
                        "duration": 3.12
                    },
                    {
                        "text": "besides being insecure,\nbesides being immature,",
                        "start": 5105.4,
                        "duration": 2.52
                    },
                    {
                        "text": "besides being fat, besides\nbeing one of the only Black kids",
                        "start": 5107.92,
                        "duration": 3.208
                    },
                    {
                        "text": "in my school.",
                        "start": 5111.128,
                        "duration": 0.542
                    },
                    {
                        "text": "There's a lot of things I had\nto overcome to gain confidence.",
                        "start": 5111.67,
                        "duration": 5.01
                    },
                    {
                        "text": "And in doing so, a\nlot of that had to go.",
                        "start": 5116.68,
                        "duration": 3.84
                    },
                    {
                        "text": "A lot of it.",
                        "start": 5120.52,
                        "duration": 0.82
                    },
                    {
                        "text": "So I became the guy that became,\nonce again, misunderstood.",
                        "start": 5121.34,
                        "duration": 2.87
                    },
                    {
                        "text": "You only sleep four hours\na day, two hours a day?",
                        "start": 5124.21,
                        "duration": 2.28
                    },
                    {
                        "text": "Sometimes you\ndon't sleep at all?",
                        "start": 5126.49,
                        "duration": 2.28
                    },
                    {
                        "text": "Like, what's this, and\nwhat's this, and what's this?",
                        "start": 5128.77,
                        "duration": 2.55
                    },
                    {
                        "text": "I know it's all important.",
                        "start": 5131.32,
                        "duration": 3.69
                    },
                    {
                        "text": "I can't.",
                        "start": 5135.01,
                        "duration": 0.5
                    },
                    {
                        "text": "Something's got to go.",
                        "start": 5135.51,
                        "duration": 1.2
                    },
                    {
                        "text": "For me to get confidence,\nbecause confidence",
                        "start": 5136.71,
                        "duration": 2.73
                    },
                    {
                        "text": "is the building block of\nwhere I'm trying to go,",
                        "start": 5139.44,
                        "duration": 2.28
                    },
                    {
                        "text": "for me to gain\nconfidence in myself,",
                        "start": 5141.72,
                        "duration": 2.28
                    },
                    {
                        "text": "this fucked up kid has got\nto do a lot of fucked up shit",
                        "start": 5144.0,
                        "duration": 2.73
                    },
                    {
                        "text": "to gain confidence.",
                        "start": 5146.73,
                        "duration": 1.62
                    },
                    {
                        "text": "And along the way,\nthe stutter went away.",
                        "start": 5148.35,
                        "duration": 2.67
                    },
                    {
                        "text": "And I gained confidence.",
                        "start": 5151.02,
                        "duration": 1.62
                    },
                    {
                        "text": "And now, my life is\na little bit more--",
                        "start": 5152.64,
                        "duration": 4.08
                    },
                    {
                        "text": "there is no balance.",
                        "start": 5156.72,
                        "duration": 2.69
                    },
                    {
                        "text": "There is no balance.",
                        "start": 5159.41,
                        "duration": 1.64
                    },
                    {
                        "text": "It's a little bit more what it\nshould be for a lot of people.",
                        "start": 5161.05,
                        "duration": 4.088
                    },
                    {
                        "text": "But there'll never be balance\nbecause confidence is something",
                        "start": 5165.138,
                        "duration": 2.542
                    },
                    {
                        "text": "that you're constantly--",
                        "start": 5167.68,
                        "duration": 1.35
                    },
                    {
                        "text": "confidence and belief\nyou're building every day.",
                        "start": 5169.03,
                        "duration": 4.39
                    },
                    {
                        "text": "And so something's got to give.",
                        "start": 5173.42,
                        "duration": 2.272
                    },
                    {
                        "text": "And I'm willing to\nforego a lot of things",
                        "start": 5175.692,
                        "duration": 1.708
                    },
                    {
                        "text": "to have that because\nI know if you",
                        "start": 5177.4,
                        "duration": 3.54
                    }
                ],
                "stats": {
                    "score": 80,
                    "should_make_short": True,
                    "feedback": "The transcript has a strong narrative that flows well. The speaker shares their personal experience in an engaging way. However, some parts of the transcript could be tightened up for better pacing and impact. For example, the phrase 'something's got to give' is repeated multiple times - it might be more effective to rephrase or use different language to convey this idea. Additionally, the transcript could benefit from a clearer structure and more defined sections to keep the listener engaged."
                }})}
                ### Example Output:
                {json.dumps({
                    "transcript": [
                        {
                            "text": "And that's one of many\nthings I did besides lying,",
                            "start": 5102.28,
                            "duration": 3.12
                        },
                        {
                            "text": "besides being insecure,\nbesides being immature,",
                            "start": 5105.4,
                            "duration": 2.52
                        },
                        {
                            "text": "besides being fat, besides\nbeing one of the only Black kids",
                            "start": 5107.92,
                            "duration": 3.208
                        },
                        {
                            "text": "in my school.",
                            "start": 5111.128,
                            "duration": 0.542
                        },
                        {
                            "text": "There's a lot of things I had\nto overcome to gain confidence.",
                            "start": 5111.67,
                            "duration": 5.01
                        },
                        {
                            "text": "And in doing so, a\nlot of that had to go.",
                            "start": 5116.68,
                            "duration": 3.84
                        },
                        {
                            "text": "A lot of it.",
                            "start": 5120.52,
                            "duration": 0.82
                        },
                        {
                            "text": "So I became the guy that became,\nonce again, misunderstood.",
                            "start": 5121.34,
                            "duration": 2.87
                        },
                        {
                            "text": "You only sleep four hours\na day, two hours a day?",
                            "start": 5124.21,
                            "duration": 2.28
                        },
                        {
                            "text": "Sometimes you\ndon't sleep at all?",
                            "start": 5126.49,
                            "duration": 2.28
                        },
                        {
                            "text": "Like, what's this, and\nwhat's this, and what's this?",
                            "start": 5128.77,
                            "duration": 2.55
                        },
                        {
                            "text": "I know it's all important.",
                            "start": 5131.32,
                            "duration": 3.69
                        },
                        {
                            "text": "I can't.",
                            "start": 5135.01,
                            "duration": 0.5
                        },
                        {
                            "text": "Something's got to go.",
                            "start": 5135.51,
                            "duration": 1.2
                        },
                        {
                            "text": "For me to get confidence,\nbecause confidence",
                            "start": 5136.71,
                            "duration": 2.73
                        },
                        {
                            "text": "is the building block of\nwhere I'm trying to go,",
                            "start": 5139.44,
                            "duration": 2.28
                        },
                        {
                            "text": "for me to gain\nconfidence in myself,",
                            "start": 5141.72,
                            "duration": 2.28
                        },
                        {
                            "text": "this fucked up kid has got\nto do a lot of fucked up shit",
                            "start": 5144.0,
                            "duration": 2.73
                        },
                        {
                            "text": "to gain confidence.",
                            "start": 5146.73,
                            "duration": 1.62
                        },
                        {
                            "text": "And along the way,\nthe stutter went away.",
                            "start": 5148.35,
                            "duration": 2.67
                        },
                        {
                            "text": "And I gained confidence.",
                            "start": 5151.02,
                            "duration": 1.62
                        },
                    ]})}
            ###
            Input: {json.dumps(short)} 
            Output: Give me the output
            """
            llama_response = llama_client.generate(
                model=self.llama_model,
                prompt=prompt,
                format="json",
                keep_alive="1m"
            )["response"]

            append_dict = {
                "transcript": json.loads(llama_response)["transcript"],
                "stats": short["stats"]
            }
            final_transcripts.append(append_dict)

        return final_transcripts

    def _generate_shorts(self, shorts_transcripts: List[dict], shorts_final_transcripts: List):
        # for now, just download the podcast and get shorts, unedited.
        download_response = self.__download_podcast();
        if download_response["status"] == "success":
            clip_shorts_data = []
            for short in shorts_final_transcripts:
                clipped_short_data = self._clip_short(short, download_response["output_path"], download_response["filename"], short)
                clip_shorts_data.append(clipped_short_data)

            return clip_shorts_data
        else:
            raise ValueError(f"Error while downloading the podcast: {download_response['error']}")

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

            print(f"{idx+1}. Formatted Chunk: {chunk}")
            print(f"{idx+1}. Feedback Chunk Stats Length: {len(feedback_chunk["stats"])}")

            transcripts_feedback.append(feedback_chunk)
            with open("transcripts_feedback.json", "w") as f:
                f.write(json.dumps(transcripts_feedback, indent=4))
                print("saved transcripts feedback for this chunk to transcripts_feedback.json")

            with open("transcripts_score.json", "w") as f:
                f.write(json.dumps([transcript["stats"] for transcript in transcripts_feedback], indent=4))
                print("saved scores to transcripts_score.json")

        return transcripts_feedback

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
