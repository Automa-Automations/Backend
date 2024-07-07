from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.fly_dns_forward_rule import FlyDnsForwardRule
    from ..models.fly_dns_option import FlyDnsOption


T = TypeVar("T", bound="FlyDNSConfig")


@_attrs_define
class FlyDNSConfig:
    """
    Attributes:
        dns_forward_rules (Union[Unset, List['FlyDnsForwardRule']]):
        nameservers (Union[Unset, List[str]]):
        options (Union[Unset, List['FlyDnsOption']]):
        searches (Union[Unset, List[str]]):
        skip_registration (Union[Unset, bool]):
    """

    dns_forward_rules: Union[Unset, List["FlyDnsForwardRule"]] = UNSET
    nameservers: Union[Unset, List[str]] = UNSET
    options: Union[Unset, List["FlyDnsOption"]] = UNSET
    searches: Union[Unset, List[str]] = UNSET
    skip_registration: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        dns_forward_rules: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.dns_forward_rules, Unset):
            dns_forward_rules = []
            for dns_forward_rules_item_data in self.dns_forward_rules:
                dns_forward_rules_item = dns_forward_rules_item_data.to_dict()
                dns_forward_rules.append(dns_forward_rules_item)

        nameservers: Union[Unset, List[str]] = UNSET
        if not isinstance(self.nameservers, Unset):
            nameservers = self.nameservers

        options: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.options, Unset):
            options = []
            for options_item_data in self.options:
                options_item = options_item_data.to_dict()
                options.append(options_item)

        searches: Union[Unset, List[str]] = UNSET
        if not isinstance(self.searches, Unset):
            searches = self.searches

        skip_registration = self.skip_registration

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if dns_forward_rules is not UNSET:
            field_dict["dns_forward_rules"] = dns_forward_rules
        if nameservers is not UNSET:
            field_dict["nameservers"] = nameservers
        if options is not UNSET:
            field_dict["options"] = options
        if searches is not UNSET:
            field_dict["searches"] = searches
        if skip_registration is not UNSET:
            field_dict["skip_registration"] = skip_registration

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.fly_dns_forward_rule import FlyDnsForwardRule
        from ..models.fly_dns_option import FlyDnsOption

        d = src_dict.copy()
        dns_forward_rules = []
        _dns_forward_rules = d.pop("dns_forward_rules", UNSET)
        for dns_forward_rules_item_data in _dns_forward_rules or []:
            dns_forward_rules_item = FlyDnsForwardRule.from_dict(dns_forward_rules_item_data)

            dns_forward_rules.append(dns_forward_rules_item)

        nameservers = cast(List[str], d.pop("nameservers", UNSET))

        options = []
        _options = d.pop("options", UNSET)
        for options_item_data in _options or []:
            options_item = FlyDnsOption.from_dict(options_item_data)

            options.append(options_item)

        searches = cast(List[str], d.pop("searches", UNSET))

        skip_registration = d.pop("skip_registration", UNSET)

        fly_dns_config = cls(
            dns_forward_rules=dns_forward_rules,
            nameservers=nameservers,
            options=options,
            searches=searches,
            skip_registration=skip_registration,
        )

        fly_dns_config.additional_properties = d
        return fly_dns_config

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
