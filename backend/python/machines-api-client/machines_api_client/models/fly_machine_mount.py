from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FlyMachineMount")


@_attrs_define
class FlyMachineMount:
    """
    Attributes:
        add_size_gb (Union[Unset, int]):
        encrypted (Union[Unset, bool]):
        extend_threshold_percent (Union[Unset, int]):
        name (Union[Unset, str]):
        path (Union[Unset, str]):
        size_gb (Union[Unset, int]):
        size_gb_limit (Union[Unset, int]):
        volume (Union[Unset, str]):
    """

    add_size_gb: Union[Unset, int] = UNSET
    encrypted: Union[Unset, bool] = UNSET
    extend_threshold_percent: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    path: Union[Unset, str] = UNSET
    size_gb: Union[Unset, int] = UNSET
    size_gb_limit: Union[Unset, int] = UNSET
    volume: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        add_size_gb = self.add_size_gb

        encrypted = self.encrypted

        extend_threshold_percent = self.extend_threshold_percent

        name = self.name

        path = self.path

        size_gb = self.size_gb

        size_gb_limit = self.size_gb_limit

        volume = self.volume

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if add_size_gb is not UNSET:
            field_dict["add_size_gb"] = add_size_gb
        if encrypted is not UNSET:
            field_dict["encrypted"] = encrypted
        if extend_threshold_percent is not UNSET:
            field_dict["extend_threshold_percent"] = extend_threshold_percent
        if name is not UNSET:
            field_dict["name"] = name
        if path is not UNSET:
            field_dict["path"] = path
        if size_gb is not UNSET:
            field_dict["size_gb"] = size_gb
        if size_gb_limit is not UNSET:
            field_dict["size_gb_limit"] = size_gb_limit
        if volume is not UNSET:
            field_dict["volume"] = volume

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        add_size_gb = d.pop("add_size_gb", UNSET)

        encrypted = d.pop("encrypted", UNSET)

        extend_threshold_percent = d.pop("extend_threshold_percent", UNSET)

        name = d.pop("name", UNSET)

        path = d.pop("path", UNSET)

        size_gb = d.pop("size_gb", UNSET)

        size_gb_limit = d.pop("size_gb_limit", UNSET)

        volume = d.pop("volume", UNSET)

        fly_machine_mount = cls(
            add_size_gb=add_size_gb,
            encrypted=encrypted,
            extend_threshold_percent=extend_threshold_percent,
            name=name,
            path=path,
            size_gb=size_gb,
            size_gb_limit=size_gb_limit,
            volume=volume,
        )

        fly_machine_mount.additional_properties = d
        return fly_machine_mount

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
