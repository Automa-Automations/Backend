from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MachineExecRequest")


@_attrs_define
class MachineExecRequest:
    """
    Attributes:
        cmd (Union[Unset, str]): Deprecated: use Command instead
        command (Union[Unset, List[str]]):
        timeout (Union[Unset, int]):
    """

    cmd: Union[Unset, str] = UNSET
    command: Union[Unset, List[str]] = UNSET
    timeout: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        cmd = self.cmd

        command: Union[Unset, List[str]] = UNSET
        if not isinstance(self.command, Unset):
            command = self.command

        timeout = self.timeout

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cmd is not UNSET:
            field_dict["cmd"] = cmd
        if command is not UNSET:
            field_dict["command"] = command
        if timeout is not UNSET:
            field_dict["timeout"] = timeout

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        cmd = d.pop("cmd", UNSET)

        command = cast(List[str], d.pop("command", UNSET))

        timeout = d.pop("timeout", UNSET)

        machine_exec_request = cls(
            cmd=cmd,
            command=command,
            timeout=timeout,
        )

        machine_exec_request.additional_properties = d
        return machine_exec_request

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
