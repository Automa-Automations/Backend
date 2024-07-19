from typing import Literal, TypeAlias, Union, List

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

ReturnStatus: TypeAlias = Literal["error", "success", "warning"]

VideoEditingActionType: TypeAlias = Literal["process frame", "clip video"]

VideoType: TypeAlias = Literal["short", "long video"]
