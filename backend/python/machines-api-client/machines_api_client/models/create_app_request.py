from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateAppRequest")


@_attrs_define
class CreateAppRequest:
    """
    Attributes:
        app_name (Union[Unset, str]):
        enable_subdomains (Union[Unset, bool]):
        network (Union[Unset, str]):
        org_slug (Union[Unset, str]):
    """

    app_name: Union[Unset, str] = UNSET
    enable_subdomains: Union[Unset, bool] = UNSET
    network: Union[Unset, str] = UNSET
    org_slug: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        app_name = self.app_name

        enable_subdomains = self.enable_subdomains

        network = self.network

        org_slug = self.org_slug

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if app_name is not UNSET:
            field_dict["app_name"] = app_name
        if enable_subdomains is not UNSET:
            field_dict["enable_subdomains"] = enable_subdomains
        if network is not UNSET:
            field_dict["network"] = network
        if org_slug is not UNSET:
            field_dict["org_slug"] = org_slug

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        app_name = d.pop("app_name", UNSET)

        enable_subdomains = d.pop("enable_subdomains", UNSET)

        network = d.pop("network", UNSET)

        org_slug = d.pop("org_slug", UNSET)

        create_app_request = cls(
            app_name=app_name,
            enable_subdomains=enable_subdomains,
            network=network,
            org_slug=org_slug,
        )

        create_app_request.additional_properties = d
        return create_app_request

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
