from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Lease")


@_attrs_define
class Lease:
    """
    Attributes:
        description (Union[Unset, str]): Description or reason for the Lease.
        expires_at (Union[Unset, int]): ExpiresAt is the unix timestamp in UTC to denote when the Lease will no longer
            be valid.
        nonce (Union[Unset, str]): Nonce is the unique ID autogenerated and associated with the Lease.
        owner (Union[Unset, str]): Owner is the user identifier which acquired the Lease.
        version (Union[Unset, str]): Machine version
    """

    description: Union[Unset, str] = UNSET
    expires_at: Union[Unset, int] = UNSET
    nonce: Union[Unset, str] = UNSET
    owner: Union[Unset, str] = UNSET
    version: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        description = self.description

        expires_at = self.expires_at

        nonce = self.nonce

        owner = self.owner

        version = self.version

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at
        if nonce is not UNSET:
            field_dict["nonce"] = nonce
        if owner is not UNSET:
            field_dict["owner"] = owner
        if version is not UNSET:
            field_dict["version"] = version

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        description = d.pop("description", UNSET)

        expires_at = d.pop("expires_at", UNSET)

        nonce = d.pop("nonce", UNSET)

        owner = d.pop("owner", UNSET)

        version = d.pop("version", UNSET)

        lease = cls(
            description=description,
            expires_at=expires_at,
            nonce=nonce,
            owner=owner,
            version=version,
        )

        lease.additional_properties = d
        return lease

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
