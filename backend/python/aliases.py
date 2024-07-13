from typing import TypeAlias, Union, List

from models import AssemblyAIParsedTranscript, YoutubeAPITranscript

PodcastTranscript: TypeAlias = List[
    Union[AssemblyAIParsedTranscript, YoutubeAPITranscript]
]
