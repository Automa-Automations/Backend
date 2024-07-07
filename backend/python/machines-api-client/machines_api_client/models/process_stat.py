from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.listen_socket import ListenSocket


T = TypeVar("T", bound="ProcessStat")


@_attrs_define
class ProcessStat:
    """
    Attributes:
        command (Union[Unset, str]):
        cpu (Union[Unset, int]):
        directory (Union[Unset, str]):
        listen_sockets (Union[Unset, List['ListenSocket']]):
        pid (Union[Unset, int]):
        rss (Union[Unset, int]):
        rtime (Union[Unset, int]):
        stime (Union[Unset, int]):
    """

    command: Union[Unset, str] = UNSET
    cpu: Union[Unset, int] = UNSET
    directory: Union[Unset, str] = UNSET
    listen_sockets: Union[Unset, List["ListenSocket"]] = UNSET
    pid: Union[Unset, int] = UNSET
    rss: Union[Unset, int] = UNSET
    rtime: Union[Unset, int] = UNSET
    stime: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        command = self.command

        cpu = self.cpu

        directory = self.directory

        listen_sockets: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.listen_sockets, Unset):
            listen_sockets = []
            for listen_sockets_item_data in self.listen_sockets:
                listen_sockets_item = listen_sockets_item_data.to_dict()
                listen_sockets.append(listen_sockets_item)

        pid = self.pid

        rss = self.rss

        rtime = self.rtime

        stime = self.stime

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if command is not UNSET:
            field_dict["command"] = command
        if cpu is not UNSET:
            field_dict["cpu"] = cpu
        if directory is not UNSET:
            field_dict["directory"] = directory
        if listen_sockets is not UNSET:
            field_dict["listen_sockets"] = listen_sockets
        if pid is not UNSET:
            field_dict["pid"] = pid
        if rss is not UNSET:
            field_dict["rss"] = rss
        if rtime is not UNSET:
            field_dict["rtime"] = rtime
        if stime is not UNSET:
            field_dict["stime"] = stime

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.listen_socket import ListenSocket

        d = src_dict.copy()
        command = d.pop("command", UNSET)

        cpu = d.pop("cpu", UNSET)

        directory = d.pop("directory", UNSET)

        listen_sockets = []
        _listen_sockets = d.pop("listen_sockets", UNSET)
        for listen_sockets_item_data in _listen_sockets or []:
            listen_sockets_item = ListenSocket.from_dict(listen_sockets_item_data)

            listen_sockets.append(listen_sockets_item)

        pid = d.pop("pid", UNSET)

        rss = d.pop("rss", UNSET)

        rtime = d.pop("rtime", UNSET)

        stime = d.pop("stime", UNSET)

        process_stat = cls(
            command=command,
            cpu=cpu,
            directory=directory,
            listen_sockets=listen_sockets,
            pid=pid,
            rss=rss,
            rtime=rtime,
            stime=stime,
        )

        process_stat.additional_properties = d
        return process_stat

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
