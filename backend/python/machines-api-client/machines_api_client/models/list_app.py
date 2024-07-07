from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_app_network import ListAppNetwork


T = TypeVar("T", bound="ListApp")


@_attrs_define
class ListApp:
    """
    Attributes:
        id (Union[Unset, str]):
        machine_count (Union[Unset, int]):
        name (Union[Unset, str]):
        network (Union[Unset, ListAppNetwork]):
    """

    id: Union[Unset, str] = UNSET
    machine_count: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    network: Union[Unset, "ListAppNetwork"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        machine_count = self.machine_count

        name = self.name

        network: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.network, Unset):
            network = self.network.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if machine_count is not UNSET:
            field_dict["machine_count"] = machine_count
        if name is not UNSET:
            field_dict["name"] = name
        if network is not UNSET:
            field_dict["network"] = network

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_app_network import ListAppNetwork

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        machine_count = d.pop("machine_count", UNSET)

        name = d.pop("name", UNSET)

        _network = d.pop("network", UNSET)
        network: Union[Unset, ListAppNetwork]
        if isinstance(_network, Unset):
            network = UNSET
        else:
            network = ListAppNetwork.from_dict(_network)

        list_app = cls(
            id=id,
            machine_count=machine_count,
            name=name,
            network=network,
        )

        list_app.additional_properties = d
        return list_app

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
