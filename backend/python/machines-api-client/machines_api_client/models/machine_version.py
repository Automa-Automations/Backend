from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.fly_machine_config import FlyMachineConfig


T = TypeVar("T", bound="MachineVersion")


@_attrs_define
class MachineVersion:
    """
    Attributes:
        user_config (Union[Unset, FlyMachineConfig]):
        version (Union[Unset, str]):
    """

    user_config: Union[Unset, "FlyMachineConfig"] = UNSET
    version: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        user_config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.user_config, Unset):
            user_config = self.user_config.to_dict()

        version = self.version

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if user_config is not UNSET:
            field_dict["user_config"] = user_config
        if version is not UNSET:
            field_dict["version"] = version

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.fly_machine_config import FlyMachineConfig

        d = src_dict.copy()
        _user_config = d.pop("user_config", UNSET)
        user_config: Union[Unset, FlyMachineConfig]
        if isinstance(_user_config, Unset):
            user_config = UNSET
        else:
            user_config = FlyMachineConfig.from_dict(_user_config)

        version = d.pop("version", UNSET)

        machine_version = cls(
            user_config=user_config,
            version=version,
        )

        machine_version.additional_properties = d
        return machine_version

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
