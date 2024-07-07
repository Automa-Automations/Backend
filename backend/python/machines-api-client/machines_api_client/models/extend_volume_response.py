from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.volume import Volume


T = TypeVar("T", bound="ExtendVolumeResponse")


@_attrs_define
class ExtendVolumeResponse:
    """
    Attributes:
        needs_restart (Union[Unset, bool]):
        volume (Union[Unset, Volume]):
    """

    needs_restart: Union[Unset, bool] = UNSET
    volume: Union[Unset, "Volume"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        needs_restart = self.needs_restart

        volume: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.volume, Unset):
            volume = self.volume.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if needs_restart is not UNSET:
            field_dict["needs_restart"] = needs_restart
        if volume is not UNSET:
            field_dict["volume"] = volume

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.volume import Volume

        d = src_dict.copy()
        needs_restart = d.pop("needs_restart", UNSET)

        _volume = d.pop("volume", UNSET)
        volume: Union[Unset, Volume]
        if isinstance(_volume, Unset):
            volume = UNSET
        else:
            volume = Volume.from_dict(_volume)

        extend_volume_response = cls(
            needs_restart=needs_restart,
            volume=volume,
        )

        extend_volume_response.additional_properties = d
        return extend_volume_response

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
