from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FlyMachineServiceConcurrency")


@_attrs_define
class FlyMachineServiceConcurrency:
    """
    Attributes:
        hard_limit (Union[Unset, int]):
        soft_limit (Union[Unset, int]):
        type (Union[Unset, str]):
    """

    hard_limit: Union[Unset, int] = UNSET
    soft_limit: Union[Unset, int] = UNSET
    type: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        hard_limit = self.hard_limit

        soft_limit = self.soft_limit

        type = self.type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if hard_limit is not UNSET:
            field_dict["hard_limit"] = hard_limit
        if soft_limit is not UNSET:
            field_dict["soft_limit"] = soft_limit
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        hard_limit = d.pop("hard_limit", UNSET)

        soft_limit = d.pop("soft_limit", UNSET)

        type = d.pop("type", UNSET)

        fly_machine_service_concurrency = cls(
            hard_limit=hard_limit,
            soft_limit=soft_limit,
            type=type,
        )

        fly_machine_service_concurrency.additional_properties = d
        return fly_machine_service_concurrency

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
