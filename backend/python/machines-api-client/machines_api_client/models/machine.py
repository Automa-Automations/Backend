from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.machine_host_status import MachineHostStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.check_status import CheckStatus
    from ..models.fly_machine_config import FlyMachineConfig
    from ..models.image_ref import ImageRef
    from ..models.machine_event import MachineEvent


T = TypeVar("T", bound="Machine")


@_attrs_define
class Machine:
    """
    Attributes:
        checks (Union[Unset, List['CheckStatus']]):
        config (Union[Unset, FlyMachineConfig]):
        created_at (Union[Unset, str]):
        events (Union[Unset, List['MachineEvent']]):
        host_status (Union[Unset, MachineHostStatus]):
        id (Union[Unset, str]):
        image_ref (Union[Unset, ImageRef]):
        instance_id (Union[Unset, str]): InstanceID is unique for each version of the machine
        name (Union[Unset, str]):
        nonce (Union[Unset, str]): Nonce is only every returned on machine creation if a lease_duration was provided.
        private_ip (Union[Unset, str]): PrivateIP is the internal 6PN address of the machine.
        region (Union[Unset, str]):
        state (Union[Unset, str]):
        updated_at (Union[Unset, str]):
    """

    checks: Union[Unset, List["CheckStatus"]] = UNSET
    config: Union[Unset, "FlyMachineConfig"] = UNSET
    created_at: Union[Unset, str] = UNSET
    events: Union[Unset, List["MachineEvent"]] = UNSET
    host_status: Union[Unset, MachineHostStatus] = UNSET
    id: Union[Unset, str] = UNSET
    image_ref: Union[Unset, "ImageRef"] = UNSET
    instance_id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    nonce: Union[Unset, str] = UNSET
    private_ip: Union[Unset, str] = UNSET
    region: Union[Unset, str] = UNSET
    state: Union[Unset, str] = UNSET
    updated_at: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        checks: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.checks, Unset):
            checks = []
            for checks_item_data in self.checks:
                checks_item = checks_item_data.to_dict()
                checks.append(checks_item)

        config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        created_at = self.created_at

        events: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.events, Unset):
            events = []
            for events_item_data in self.events:
                events_item = events_item_data.to_dict()
                events.append(events_item)

        host_status: Union[Unset, str] = UNSET
        if not isinstance(self.host_status, Unset):
            host_status = self.host_status.value

        id = self.id

        image_ref: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.image_ref, Unset):
            image_ref = self.image_ref.to_dict()

        instance_id = self.instance_id

        name = self.name

        nonce = self.nonce

        private_ip = self.private_ip

        region = self.region

        state = self.state

        updated_at = self.updated_at

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if checks is not UNSET:
            field_dict["checks"] = checks
        if config is not UNSET:
            field_dict["config"] = config
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if events is not UNSET:
            field_dict["events"] = events
        if host_status is not UNSET:
            field_dict["host_status"] = host_status
        if id is not UNSET:
            field_dict["id"] = id
        if image_ref is not UNSET:
            field_dict["image_ref"] = image_ref
        if instance_id is not UNSET:
            field_dict["instance_id"] = instance_id
        if name is not UNSET:
            field_dict["name"] = name
        if nonce is not UNSET:
            field_dict["nonce"] = nonce
        if private_ip is not UNSET:
            field_dict["private_ip"] = private_ip
        if region is not UNSET:
            field_dict["region"] = region
        if state is not UNSET:
            field_dict["state"] = state
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.check_status import CheckStatus
        from ..models.fly_machine_config import FlyMachineConfig
        from ..models.image_ref import ImageRef
        from ..models.machine_event import MachineEvent

        d = src_dict.copy()
        checks = []
        _checks = d.pop("checks", UNSET)
        for checks_item_data in _checks or []:
            checks_item = CheckStatus.from_dict(checks_item_data)

            checks.append(checks_item)

        _config = d.pop("config", UNSET)
        config: Union[Unset, FlyMachineConfig]
        if isinstance(_config, Unset):
            config = UNSET
        else:
            config = FlyMachineConfig.from_dict(_config)

        created_at = d.pop("created_at", UNSET)

        events = []
        _events = d.pop("events", UNSET)
        for events_item_data in _events or []:
            events_item = MachineEvent.from_dict(events_item_data)

            events.append(events_item)

        _host_status = d.pop("host_status", UNSET)
        host_status: Union[Unset, MachineHostStatus]
        if isinstance(_host_status, Unset):
            host_status = UNSET
        else:
            host_status = MachineHostStatus(_host_status)

        id = d.pop("id", UNSET)

        _image_ref = d.pop("image_ref", UNSET)
        image_ref: Union[Unset, ImageRef]
        if isinstance(_image_ref, Unset):
            image_ref = UNSET
        else:
            image_ref = ImageRef.from_dict(_image_ref)

        instance_id = d.pop("instance_id", UNSET)

        name = d.pop("name", UNSET)

        nonce = d.pop("nonce", UNSET)

        private_ip = d.pop("private_ip", UNSET)

        region = d.pop("region", UNSET)

        state = d.pop("state", UNSET)

        updated_at = d.pop("updated_at", UNSET)

        machine = cls(
            checks=checks,
            config=config,
            created_at=created_at,
            events=events,
            host_status=host_status,
            id=id,
            image_ref=image_ref,
            instance_id=instance_id,
            name=name,
            nonce=nonce,
            private_ip=private_ip,
            region=region,
            state=state,
            updated_at=updated_at,
        )

        machine.additional_properties = d
        return machine

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
