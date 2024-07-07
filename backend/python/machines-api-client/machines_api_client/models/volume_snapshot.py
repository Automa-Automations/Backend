from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="VolumeSnapshot")


@_attrs_define
class VolumeSnapshot:
    """
    Attributes:
        created_at (Union[Unset, str]):
        digest (Union[Unset, str]):
        id (Union[Unset, str]):
        size (Union[Unset, int]):
        status (Union[Unset, str]):
    """

    created_at: Union[Unset, str] = UNSET
    digest: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    size: Union[Unset, int] = UNSET
    status: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        created_at = self.created_at

        digest = self.digest

        id = self.id

        size = self.size

        status = self.status

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if digest is not UNSET:
            field_dict["digest"] = digest
        if id is not UNSET:
            field_dict["id"] = id
        if size is not UNSET:
            field_dict["size"] = size
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        created_at = d.pop("created_at", UNSET)

        digest = d.pop("digest", UNSET)

        id = d.pop("id", UNSET)

        size = d.pop("size", UNSET)

        status = d.pop("status", UNSET)

        volume_snapshot = cls(
            created_at=created_at,
            digest=digest,
            id=id,
            size=size,
            status=status,
        )

        volume_snapshot.additional_properties = d
        return volume_snapshot

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
