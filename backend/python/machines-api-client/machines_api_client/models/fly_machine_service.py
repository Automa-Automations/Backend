from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.fly_machine_check import FlyMachineCheck
    from ..models.fly_machine_port import FlyMachinePort
    from ..models.fly_machine_service_concurrency import FlyMachineServiceConcurrency


T = TypeVar("T", bound="FlyMachineService")


@_attrs_define
class FlyMachineService:
    """
    Attributes:
        autostart (Union[Unset, bool]):
        autostop (Union[Unset, bool]):
        checks (Union[Unset, List['FlyMachineCheck']]):
        concurrency (Union[Unset, FlyMachineServiceConcurrency]):
        force_instance_description (Union[Unset, str]):
        force_instance_key (Union[Unset, str]):
        internal_port (Union[Unset, int]):
        min_machines_running (Union[Unset, int]):
        ports (Union[Unset, List['FlyMachinePort']]):
        protocol (Union[Unset, str]):
    """

    autostart: Union[Unset, bool] = UNSET
    autostop: Union[Unset, bool] = UNSET
    checks: Union[Unset, List["FlyMachineCheck"]] = UNSET
    concurrency: Union[Unset, "FlyMachineServiceConcurrency"] = UNSET
    force_instance_description: Union[Unset, str] = UNSET
    force_instance_key: Union[Unset, str] = UNSET
    internal_port: Union[Unset, int] = UNSET
    min_machines_running: Union[Unset, int] = UNSET
    ports: Union[Unset, List["FlyMachinePort"]] = UNSET
    protocol: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        autostart = self.autostart

        autostop = self.autostop

        checks: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.checks, Unset):
            checks = []
            for checks_item_data in self.checks:
                checks_item = checks_item_data.to_dict()
                checks.append(checks_item)

        concurrency: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.concurrency, Unset):
            concurrency = self.concurrency.to_dict()

        force_instance_description = self.force_instance_description

        force_instance_key = self.force_instance_key

        internal_port = self.internal_port

        min_machines_running = self.min_machines_running

        ports: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.ports, Unset):
            ports = []
            for ports_item_data in self.ports:
                ports_item = ports_item_data.to_dict()
                ports.append(ports_item)

        protocol = self.protocol

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if autostart is not UNSET:
            field_dict["autostart"] = autostart
        if autostop is not UNSET:
            field_dict["autostop"] = autostop
        if checks is not UNSET:
            field_dict["checks"] = checks
        if concurrency is not UNSET:
            field_dict["concurrency"] = concurrency
        if force_instance_description is not UNSET:
            field_dict["force_instance_description"] = force_instance_description
        if force_instance_key is not UNSET:
            field_dict["force_instance_key"] = force_instance_key
        if internal_port is not UNSET:
            field_dict["internal_port"] = internal_port
        if min_machines_running is not UNSET:
            field_dict["min_machines_running"] = min_machines_running
        if ports is not UNSET:
            field_dict["ports"] = ports
        if protocol is not UNSET:
            field_dict["protocol"] = protocol

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.fly_machine_check import FlyMachineCheck
        from ..models.fly_machine_port import FlyMachinePort
        from ..models.fly_machine_service_concurrency import FlyMachineServiceConcurrency

        d = src_dict.copy()
        autostart = d.pop("autostart", UNSET)

        autostop = d.pop("autostop", UNSET)

        checks = []
        _checks = d.pop("checks", UNSET)
        for checks_item_data in _checks or []:
            checks_item = FlyMachineCheck.from_dict(checks_item_data)

            checks.append(checks_item)

        _concurrency = d.pop("concurrency", UNSET)
        concurrency: Union[Unset, FlyMachineServiceConcurrency]
        if isinstance(_concurrency, Unset):
            concurrency = UNSET
        else:
            concurrency = FlyMachineServiceConcurrency.from_dict(_concurrency)

        force_instance_description = d.pop("force_instance_description", UNSET)

        force_instance_key = d.pop("force_instance_key", UNSET)

        internal_port = d.pop("internal_port", UNSET)

        min_machines_running = d.pop("min_machines_running", UNSET)

        ports = []
        _ports = d.pop("ports", UNSET)
        for ports_item_data in _ports or []:
            ports_item = FlyMachinePort.from_dict(ports_item_data)

            ports.append(ports_item)

        protocol = d.pop("protocol", UNSET)

        fly_machine_service = cls(
            autostart=autostart,
            autostop=autostop,
            checks=checks,
            concurrency=concurrency,
            force_instance_description=force_instance_description,
            force_instance_key=force_instance_key,
            internal_port=internal_port,
            min_machines_running=min_machines_running,
            ports=ports,
            protocol=protocol,
        )

        fly_machine_service.additional_properties = d
        return fly_machine_service

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
