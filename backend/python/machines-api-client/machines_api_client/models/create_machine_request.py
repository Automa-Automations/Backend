from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.fly_machine_config import FlyMachineConfig


T = TypeVar("T", bound="CreateMachineRequest")


@_attrs_define
class CreateMachineRequest:
    """
    Attributes:
        config (Union[Unset, FlyMachineConfig]):
        lease_ttl (Union[Unset, int]):
        lsvd (Union[Unset, bool]):
        name (Union[Unset, str]): Unique name for this Machine. If omitted, one is generated for you
        region (Union[Unset, str]): The target region. Omitting this param launches in the same region as your WireGuard
            peer connection (somewhere near you).
        skip_launch (Union[Unset, bool]):
        skip_service_registration (Union[Unset, bool]):
    """

    config: Union[Unset, "FlyMachineConfig"] = UNSET
    lease_ttl: Union[Unset, int] = UNSET
    lsvd: Union[Unset, bool] = UNSET
    name: Union[Unset, str] = UNSET
    region: Union[Unset, str] = UNSET
    skip_launch: Union[Unset, bool] = UNSET
    skip_service_registration: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        lease_ttl = self.lease_ttl

        lsvd = self.lsvd

        name = self.name

        region = self.region

        skip_launch = self.skip_launch

        skip_service_registration = self.skip_service_registration

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if config is not UNSET:
            field_dict["config"] = config
        if lease_ttl is not UNSET:
            field_dict["lease_ttl"] = lease_ttl
        if lsvd is not UNSET:
            field_dict["lsvd"] = lsvd
        if name is not UNSET:
            field_dict["name"] = name
        if region is not UNSET:
            field_dict["region"] = region
        if skip_launch is not UNSET:
            field_dict["skip_launch"] = skip_launch
        if skip_service_registration is not UNSET:
            field_dict["skip_service_registration"] = skip_service_registration

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.fly_machine_config import FlyMachineConfig

        d = src_dict.copy()
        _config = d.pop("config", UNSET)
        config: Union[Unset, FlyMachineConfig]
        if isinstance(_config, Unset):
            config = UNSET
        else:
            config = FlyMachineConfig.from_dict(_config)

        lease_ttl = d.pop("lease_ttl", UNSET)

        lsvd = d.pop("lsvd", UNSET)

        name = d.pop("name", UNSET)

        region = d.pop("region", UNSET)

        skip_launch = d.pop("skip_launch", UNSET)

        skip_service_registration = d.pop("skip_service_registration", UNSET)

        create_machine_request = cls(
            config=config,
            lease_ttl=lease_ttl,
            lsvd=lsvd,
            name=name,
            region=region,
            skip_launch=skip_launch,
            skip_service_registration=skip_service_registration,
        )

        create_machine_request.additional_properties = d
        return create_machine_request

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
