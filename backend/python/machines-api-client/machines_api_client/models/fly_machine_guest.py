from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FlyMachineGuest")


@_attrs_define
class FlyMachineGuest:
    """
    Attributes:
        cpu_kind (Union[Unset, str]):
        cpus (Union[Unset, int]):
        gpu_kind (Union[Unset, str]):
        gpus (Union[Unset, int]):
        host_dedication_id (Union[Unset, str]):
        kernel_args (Union[Unset, List[str]]):
        memory_mb (Union[Unset, int]):
    """

    cpu_kind: Union[Unset, str] = UNSET
    cpus: Union[Unset, int] = UNSET
    gpu_kind: Union[Unset, str] = UNSET
    gpus: Union[Unset, int] = UNSET
    host_dedication_id: Union[Unset, str] = UNSET
    kernel_args: Union[Unset, List[str]] = UNSET
    memory_mb: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        cpu_kind = self.cpu_kind

        cpus = self.cpus

        gpu_kind = self.gpu_kind

        gpus = self.gpus

        host_dedication_id = self.host_dedication_id

        kernel_args: Union[Unset, List[str]] = UNSET
        if not isinstance(self.kernel_args, Unset):
            kernel_args = self.kernel_args

        memory_mb = self.memory_mb

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cpu_kind is not UNSET:
            field_dict["cpu_kind"] = cpu_kind
        if cpus is not UNSET:
            field_dict["cpus"] = cpus
        if gpu_kind is not UNSET:
            field_dict["gpu_kind"] = gpu_kind
        if gpus is not UNSET:
            field_dict["gpus"] = gpus
        if host_dedication_id is not UNSET:
            field_dict["host_dedication_id"] = host_dedication_id
        if kernel_args is not UNSET:
            field_dict["kernel_args"] = kernel_args
        if memory_mb is not UNSET:
            field_dict["memory_mb"] = memory_mb

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        cpu_kind = d.pop("cpu_kind", UNSET)

        cpus = d.pop("cpus", UNSET)

        gpu_kind = d.pop("gpu_kind", UNSET)

        gpus = d.pop("gpus", UNSET)

        host_dedication_id = d.pop("host_dedication_id", UNSET)

        kernel_args = cast(List[str], d.pop("kernel_args", UNSET))

        memory_mb = d.pop("memory_mb", UNSET)

        fly_machine_guest = cls(
            cpu_kind=cpu_kind,
            cpus=cpus,
            gpu_kind=gpu_kind,
            gpus=gpus,
            host_dedication_id=host_dedication_id,
            kernel_args=kernel_args,
            memory_mb=memory_mb,
        )

        fly_machine_guest.additional_properties = d
        return fly_machine_guest

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
