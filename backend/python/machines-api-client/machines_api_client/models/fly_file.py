from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FlyFile")


@_attrs_define
class FlyFile:
    """A file that will be written to the Machine. One of RawValue or SecretName must be set.

    Attributes:
        guest_path (Union[Unset, str]): GuestPath is the path on the machine where the file will be written and must be
            an absolute path.
            For example: /full/path/to/file.json
        raw_value (Union[Unset, str]): The base64 encoded string of the file contents.
        secret_name (Union[Unset, str]): The name of the secret that contains the base64 encoded file contents.
    """

    guest_path: Union[Unset, str] = UNSET
    raw_value: Union[Unset, str] = UNSET
    secret_name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        guest_path = self.guest_path

        raw_value = self.raw_value

        secret_name = self.secret_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if guest_path is not UNSET:
            field_dict["guest_path"] = guest_path
        if raw_value is not UNSET:
            field_dict["raw_value"] = raw_value
        if secret_name is not UNSET:
            field_dict["secret_name"] = secret_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        guest_path = d.pop("guest_path", UNSET)

        raw_value = d.pop("raw_value", UNSET)

        secret_name = d.pop("secret_name", UNSET)

        fly_file = cls(
            guest_path=guest_path,
            raw_value=raw_value,
            secret_name=secret_name,
        )

        fly_file.additional_properties = d
        return fly_file

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
