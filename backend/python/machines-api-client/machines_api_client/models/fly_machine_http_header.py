from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FlyMachineHTTPHeader")


@_attrs_define
class FlyMachineHTTPHeader:
    """For http checks, an array of objects with string field Name and array of strings field Values. The key/value pairs
    specify header and header values that will get passed with the check call.

        Attributes:
            name (Union[Unset, str]): The header name
            values (Union[Unset, List[str]]): The header value
    """

    name: Union[Unset, str] = UNSET
    values: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        values: Union[Unset, List[str]] = UNSET
        if not isinstance(self.values, Unset):
            values = self.values

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if values is not UNSET:
            field_dict["values"] = values

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        values = cast(List[str], d.pop("values", UNSET))

        fly_machine_http_header = cls(
            name=name,
            values=values,
        )

        fly_machine_http_header.additional_properties = d
        return fly_machine_http_header

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
