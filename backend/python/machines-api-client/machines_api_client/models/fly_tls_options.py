from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FlyTLSOptions")


@_attrs_define
class FlyTLSOptions:
    """
    Attributes:
        alpn (Union[Unset, List[str]]):
        default_self_signed (Union[Unset, bool]):
        versions (Union[Unset, List[str]]):
    """

    alpn: Union[Unset, List[str]] = UNSET
    default_self_signed: Union[Unset, bool] = UNSET
    versions: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        alpn: Union[Unset, List[str]] = UNSET
        if not isinstance(self.alpn, Unset):
            alpn = self.alpn

        default_self_signed = self.default_self_signed

        versions: Union[Unset, List[str]] = UNSET
        if not isinstance(self.versions, Unset):
            versions = self.versions

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if alpn is not UNSET:
            field_dict["alpn"] = alpn
        if default_self_signed is not UNSET:
            field_dict["default_self_signed"] = default_self_signed
        if versions is not UNSET:
            field_dict["versions"] = versions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        alpn = cast(List[str], d.pop("alpn", UNSET))

        default_self_signed = d.pop("default_self_signed", UNSET)

        versions = cast(List[str], d.pop("versions", UNSET))

        fly_tls_options = cls(
            alpn=alpn,
            default_self_signed=default_self_signed,
            versions=versions,
        )

        fly_tls_options.additional_properties = d
        return fly_tls_options

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
