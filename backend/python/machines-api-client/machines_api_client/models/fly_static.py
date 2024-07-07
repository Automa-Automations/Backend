from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FlyStatic")


@_attrs_define
class FlyStatic:
    """
    Attributes:
        guest_path (str):
        url_prefix (str):
        tigris_bucket (Union[Unset, str]):
    """

    guest_path: str
    url_prefix: str
    tigris_bucket: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        guest_path = self.guest_path

        url_prefix = self.url_prefix

        tigris_bucket = self.tigris_bucket

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "guest_path": guest_path,
                "url_prefix": url_prefix,
            }
        )
        if tigris_bucket is not UNSET:
            field_dict["tigris_bucket"] = tigris_bucket

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        guest_path = d.pop("guest_path")

        url_prefix = d.pop("url_prefix")

        tigris_bucket = d.pop("tigris_bucket", UNSET)

        fly_static = cls(
            guest_path=guest_path,
            url_prefix=url_prefix,
            tigris_bucket=tigris_bucket,
        )

        fly_static.additional_properties = d
        return fly_static

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
