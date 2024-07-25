from typing import Literal, TypeAlias, Union, List
from moviepy.editor import CompositeVideoClip, VideoClip

from models import (
    AssemblyAIParsedTranscript,
    AssemblyTranscriptFeedback,
    YoutubeAPITranscript,
    FaceFramePosition,
    ReturnMessage,
    DownloadPodcastResponse,
    YoutubeTranscriptFeedback,
    AssemblyShortFinalTranscript,
)

PodcastTranscript: TypeAlias = Union[
    List[AssemblyAIParsedTranscript], List[YoutubeAPITranscript]
]

FinalTranscript: TypeAlias = Union[
    AssemblyShortFinalTranscript, List[YoutubeAPITranscript]
]
FacePositions: TypeAlias = Union[FaceFramePosition, ReturnMessage, None]

ReturnStatus: TypeAlias = Literal["error", "success", "warning"]

VideoEditingActionType: TypeAlias = Literal[
    "process frame", "clip video", "process short"
]

VideoType: TypeAlias = Literal["short", "long video"]

MoviePyClip: TypeAlias = Union[VideoClip, CompositeVideoClip]

TranscriptFeedback: TypeAlias = Union[
    YoutubeTranscriptFeedback, AssemblyTranscriptFeedback
]

TranscriptFeedbackList: TypeAlias = Union[
    List[YoutubeTranscriptFeedback], List[AssemblyTranscriptFeedback]
]
TranscriptorType: TypeAlias = Literal["assembly_ai", "yt_transcript_api"]
LLMType: TypeAlias = Literal["openai", "ollama"]
