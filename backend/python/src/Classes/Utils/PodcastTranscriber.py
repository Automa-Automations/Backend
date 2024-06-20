from dotenv import load_dotenv
import os
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
import assemblyai as aai

load_dotenv()

class PodcastTranscriber:
    def __init__(self, podcast_url):
        self.podcast_url = podcast_url
        self.transcript = None

    def download_podcast(self, output_path: str = "downloads/", filename: str = ""):
        print("Downloading podcast...")
        try:
            yt = YouTube(self.podcast_url)
            if filename == "":
                filename = yt.title

            yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].download(
                output_path=output_path, filename=filename
            )

            return {
                "output_path": output_path,
                "filename": filename,
                "status": "success",
            } 
        except Exception as e: 
            return {
                "error": str(e),
                "status": "error",
            }

    @classmethod
    def from_assembly(cls, podcast_url: str, api_key: str):
        # Create an instance of PodcastTranscriber
        podcast_transcriber = cls(podcast_url)
        download_output = podcast_transcriber.download_podcast()

        # Check if the podcast was downloaded successfully
        if download_output['status'] == 'success':
            download_path = os.path.join(download_output['output_path'], download_output['filename'])
            
            # Initialize AssemblyAI with the API key
            assembly_ai = AssemblyAI(api_key)
            
            # Get the transcript using AssemblyAI
            transcript = assembly_ai.get_yt_podcast_transcription(download_path)
            
            # Optionally parse the transcript
            parsed_transcript = assembly_ai.parse_transcript(transcript)
            
            # Set the transcript to the instance
            podcast_transcriber.transcript = parsed_transcript
            
        return podcast_transcriber

    @classmethod
    def from_transcription_api(cls, podcast_url: str):
        podcast_transcriber = cls(podcast_url)
        transcription_api = YoutubeTranscriptionAPITranscriber(podcast_url)
        podcast_transcriber.transcript = transcription_api.get_video_transcript()
        return podcast_transcriber

class AssemblyAI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        aai.settings.api_key = api_key

    def get_yt_podcast_transcription(self, podcast_download_path: str):
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(podcast_download_path)
        return transcript

    def parse_transcript(self, transcript: str):
        """Function to parse transcript"""
        # Dummy parsing implementation
        return transcript


class YoutubeTranscriptionAPITranscriber:
    def __init__(self, podcast_url: str):
        self.podcast_url = podcast_url

    def get_video_transcript(self):
        """
        Method to get the video transcript from the video url
        Returns:
        - video_transcript: list: The list of the transcript of the video
        """
        # watch url type
        video_id = self.podcast_url.split("v=")[1]
        print(f"Video ID: {video_id}")

        video_transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return video_transcript
