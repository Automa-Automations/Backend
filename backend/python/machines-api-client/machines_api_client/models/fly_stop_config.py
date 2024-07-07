from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.fly_duration import FlyDuration


T = TypeVar("T", bound="FlyStopConfig")


@_attrs_define
class FlyStopConfig:
    """
    Attributes:
        signal (Union[Unset, str]):
        timeout (Union[Unset, FlyDuration]):
    """

    signal: Union[Unset, str] = UNSET
    timeout: Union[Unset, "FlyDuration"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        signal = self.signal

        timeout: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.timeout, Unset):
            timeout = self.timeout.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if signal is not UNSET:
            field_dict["signal"] = signal
        if timeout is not UNSET:
            field_dict["timeout"] = timeout

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.fly_duration import FlyDuration

        d = src_dict.copy()
        signal = d.pop("signal", UNSET)

        _timeout = d.pop("timeout", UNSET)
        timeout: Union[Unset, FlyDuration]
        if isinstance(_timeout, Unset):
            timeout = UNSET
        else:
            timeout = FlyDuration.from_dict(_timeout)

        fly_stop_config = cls(
            signal=signal,
            timeout=timeout,
        )

        fly_stop_config.additional_properties = d
        return fly_stop_config

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
