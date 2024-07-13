from typing import TypeAlias, Union, List

from models import (
    AssemblyAIParsedTranscript,
    YoutubeAPITranscript,
    FaceFramePosition,
    ReturnMessage,
)

PodcastTranscript: TypeAlias = List[
    Union[AssemblyAIParsedTranscript, YoutubeAPITranscript]
]
FacePositions: TypeAlias = Union[FaceFramePosition, ReturnMessage, None]
