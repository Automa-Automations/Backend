import os
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
from pydub import AudioSegment
import assemblyai as aai
import json

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

            # yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].download()
            # yt.streams.get_highest_resolution().download()
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

    def _convert_to_mp3(self, file_path: str):
        mp4_audio = AudioSegment.from_file(file_path, format="mp4")
        mp3_file_path = file_path.rsplit('.', 1)[0] + '.mp3'
        mp4_audio.export(mp3_file_path, format="mp3")
        return mp3_file_path

    @classmethod
    def from_assembly(cls, podcast_url: str, api_key: str):
        podcast_transcriber = cls(podcast_url)
        download_output = podcast_transcriber.download_podcast()
        print(download_output)

        if download_output['status'] == 'success':
            download_path = os.path.join(download_output['output_path'], download_output['filename'])
            podcast_mp3_path = podcast_transcriber._convert_to_mp3(download_path)
            assembly_ai = AssemblyAI(api_key)
            transcript = assembly_ai.get_yt_podcast_transcription(podcast_mp3_path)
            parsed_transcript = assembly_ai.parse_transcript(transcript)
            podcast_transcriber.transcript = parsed_transcript
            os.remove(podcast_mp3_path)
            
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
        transcript = transcript.wait_for_completion()
        print(f"Transcript (Assembly): {json.dumps(transcript.json_response, indent=4)}")
        return transcript.json_response

    def parse_transcript(self, transcript):
        """Function to parse transcript into full sentences."""
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

        video_transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return video_transcript
