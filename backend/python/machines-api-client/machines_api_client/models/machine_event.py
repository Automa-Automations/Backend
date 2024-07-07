from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.machine_event_request import MachineEventRequest


T = TypeVar("T", bound="MachineEvent")


@_attrs_define
class MachineEvent:
    """
    Attributes:
        id (Union[Unset, str]):
        request (Union[Unset, MachineEventRequest]):
        source (Union[Unset, str]):
        status (Union[Unset, str]):
        timestamp (Union[Unset, int]):
        type (Union[Unset, str]):
    """

    id: Union[Unset, str] = UNSET
    request: Union[Unset, "MachineEventRequest"] = UNSET
    source: Union[Unset, str] = UNSET
    status: Union[Unset, str] = UNSET
    timestamp: Union[Unset, int] = UNSET
    type: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        request: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.request, Unset):
            request = self.request.to_dict()

        source = self.source

        status = self.status

        timestamp = self.timestamp

        type = self.type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if request is not UNSET:
            field_dict["request"] = request
        if source is not UNSET:
            field_dict["source"] = source
        if status is not UNSET:
            field_dict["status"] = status
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.machine_event_request import MachineEventRequest

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        _request = d.pop("request", UNSET)
        request: Union[Unset, MachineEventRequest]
        if isinstance(_request, Unset):
            request = UNSET
        else:
            request = MachineEventRequest.from_dict(_request)

        source = d.pop("source", UNSET)

        status = d.pop("status", UNSET)

        timestamp = d.pop("timestamp", UNSET)

        type = d.pop("type", UNSET)

        machine_event = cls(
            id=id,
            request=request,
            source=source,
            status=status,
            timestamp=timestamp,
            type=type,
        )

        machine_event.additional_properties = d
        return machine_event

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
