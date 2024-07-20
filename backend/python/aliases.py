from typing import Literal, Sequence, TypeAlias, Union, List, Sequence
from moviepy.editor import CompositeVideoClip, VideoClip

from models import (
    AssemblyAIParsedTranscript,
    AssemblyTranscriptFeedback,
    YoutubeAPITranscript,
    FaceFramePosition,
    ReturnMessage,
    DownloadPodcastResponse,
    YoutubeTranscriptFeedback,
)

PodcastTranscript: TypeAlias = Sequence[
    Union[AssemblyAIParsedTranscript, YoutubeAPITranscript]
]
FacePositions: TypeAlias = Union[FaceFramePosition, ReturnMessage, None]

ReturnStatus: TypeAlias = Literal["error", "success", "warning"]

VideoEditingActionType: TypeAlias = Literal[
    "process frame", "clip video", "process short"
]

VideoType: TypeAlias = Literal["short", "long video"]

MoviePyClip: TypeAlias = Union[VideoClip, CompositeVideoClip]

ShortsFinalTranscripts: TypeAlias = List[
    Union[YoutubeAPITranscript, DownloadPodcastResponse]
]
TranscriptFeedback: TypeAlias = Union[
    YoutubeTranscriptFeedback, AssemblyTranscriptFeedback
]
TranscriptFeedbackList: TypeAlias = Sequence[TranscriptFeedback]
TranscriptorType: TypeAlias = Literal["assembly_ai", "yt_transcript_api"]
LLMType: TypeAlias = Literal["openai", "ollama"]
