from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FlyMachineInit")


@_attrs_define
class FlyMachineInit:
    """
    Attributes:
        cmd (Union[Unset, List[str]]):
        entrypoint (Union[Unset, List[str]]):
        exec_ (Union[Unset, List[str]]):
        kernel_args (Union[Unset, List[str]]):
        swap_size_mb (Union[Unset, int]):
        tty (Union[Unset, bool]):
    """

    cmd: Union[Unset, List[str]] = UNSET
    entrypoint: Union[Unset, List[str]] = UNSET
    exec_: Union[Unset, List[str]] = UNSET
    kernel_args: Union[Unset, List[str]] = UNSET
    swap_size_mb: Union[Unset, int] = UNSET
    tty: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        cmd: Union[Unset, List[str]] = UNSET
        if not isinstance(self.cmd, Unset):
            cmd = self.cmd

        entrypoint: Union[Unset, List[str]] = UNSET
        if not isinstance(self.entrypoint, Unset):
            entrypoint = self.entrypoint

        exec_: Union[Unset, List[str]] = UNSET
        if not isinstance(self.exec_, Unset):
            exec_ = self.exec_

        kernel_args: Union[Unset, List[str]] = UNSET
        if not isinstance(self.kernel_args, Unset):
            kernel_args = self.kernel_args

        swap_size_mb = self.swap_size_mb

        tty = self.tty

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cmd is not UNSET:
            field_dict["cmd"] = cmd
        if entrypoint is not UNSET:
            field_dict["entrypoint"] = entrypoint
        if exec_ is not UNSET:
            field_dict["exec"] = exec_
        if kernel_args is not UNSET:
            field_dict["kernel_args"] = kernel_args
        if swap_size_mb is not UNSET:
            field_dict["swap_size_mb"] = swap_size_mb
        if tty is not UNSET:
            field_dict["tty"] = tty

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        cmd = cast(List[str], d.pop("cmd", UNSET))

        entrypoint = cast(List[str], d.pop("entrypoint", UNSET))

        exec_ = cast(List[str], d.pop("exec", UNSET))

        kernel_args = cast(List[str], d.pop("kernel_args", UNSET))

        swap_size_mb = d.pop("swap_size_mb", UNSET)

        tty = d.pop("tty", UNSET)

        fly_machine_init = cls(
            cmd=cmd,
            entrypoint=entrypoint,
            exec_=exec_,
            kernel_args=kernel_args,
            swap_size_mb=swap_size_mb,
            tty=tty,
        )

        fly_machine_init.additional_properties = d
        return fly_machine_init

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
