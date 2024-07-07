from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.fly_dns_config import FlyDNSConfig
    from ..models.fly_file import FlyFile
    from ..models.fly_machine_config_checks import FlyMachineConfigChecks
    from ..models.fly_machine_config_env import FlyMachineConfigEnv
    from ..models.fly_machine_config_metadata import FlyMachineConfigMetadata
    from ..models.fly_machine_guest import FlyMachineGuest
    from ..models.fly_machine_init import FlyMachineInit
    from ..models.fly_machine_metrics import FlyMachineMetrics
    from ..models.fly_machine_mount import FlyMachineMount
    from ..models.fly_machine_process import FlyMachineProcess
    from ..models.fly_machine_restart import FlyMachineRestart
    from ..models.fly_machine_service import FlyMachineService
    from ..models.fly_static import FlyStatic
    from ..models.fly_stop_config import FlyStopConfig


T = TypeVar("T", bound="FlyMachineConfig")


@_attrs_define
class FlyMachineConfig:
    """
    Attributes:
        auto_destroy (Union[Unset, bool]): Optional boolean telling the Machine to destroy itself once it’s complete
            (default false)
        checks (Union[Unset, FlyMachineConfigChecks]):
        disable_machine_autostart (Union[Unset, bool]): Deprecated: use Service.Autostart instead
        dns (Union[Unset, FlyDNSConfig]):
        env (Union[Unset, FlyMachineConfigEnv]): An object filled with key/value pairs to be set as environment
            variables
        files (Union[Unset, List['FlyFile']]):
        guest (Union[Unset, FlyMachineGuest]):
        image (Union[Unset, str]): The docker image to run
        init (Union[Unset, FlyMachineInit]):
        metadata (Union[Unset, FlyMachineConfigMetadata]):
        metrics (Union[Unset, FlyMachineMetrics]):
        mounts (Union[Unset, List['FlyMachineMount']]):
        processes (Union[Unset, List['FlyMachineProcess']]):
        restart (Union[Unset, FlyMachineRestart]): The Machine restart policy defines whether and how flyd restarts a
            Machine after its main process exits. See https://fly.io/docs/machines/guides-examples/machine-restart-policy/.
        schedule (Union[Unset, str]):
        services (Union[Unset, List['FlyMachineService']]):
        size (Union[Unset, str]): Deprecated: use Guest instead
        standbys (Union[Unset, List[str]]): Standbys enable a machine to be a standby for another. In the event of a
            hardware failure,
            the standby machine will be started.
        statics (Union[Unset, List['FlyStatic']]):
        stop_config (Union[Unset, FlyStopConfig]):
    """

    auto_destroy: Union[Unset, bool] = UNSET
    checks: Union[Unset, "FlyMachineConfigChecks"] = UNSET
    disable_machine_autostart: Union[Unset, bool] = UNSET
    dns: Union[Unset, "FlyDNSConfig"] = UNSET
    env: Union[Unset, "FlyMachineConfigEnv"] = UNSET
    files: Union[Unset, List["FlyFile"]] = UNSET
    guest: Union[Unset, "FlyMachineGuest"] = UNSET
    image: Union[Unset, str] = UNSET
    init: Union[Unset, "FlyMachineInit"] = UNSET
    metadata: Union[Unset, "FlyMachineConfigMetadata"] = UNSET
    metrics: Union[Unset, "FlyMachineMetrics"] = UNSET
    mounts: Union[Unset, List["FlyMachineMount"]] = UNSET
    processes: Union[Unset, List["FlyMachineProcess"]] = UNSET
    restart: Union[Unset, "FlyMachineRestart"] = UNSET
    schedule: Union[Unset, str] = UNSET
    services: Union[Unset, List["FlyMachineService"]] = UNSET
    size: Union[Unset, str] = UNSET
    standbys: Union[Unset, List[str]] = UNSET
    statics: Union[Unset, List["FlyStatic"]] = UNSET
    stop_config: Union[Unset, "FlyStopConfig"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        auto_destroy = self.auto_destroy

        checks: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.checks, Unset):
            checks = self.checks.to_dict()

        disable_machine_autostart = self.disable_machine_autostart

        dns: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.dns, Unset):
            dns = self.dns.to_dict()

        env: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.env, Unset):
            env = self.env.to_dict()

        files: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.files, Unset):
            files = []
            for files_item_data in self.files:
                files_item = files_item_data.to_dict()
                files.append(files_item)

        guest: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.guest, Unset):
            guest = self.guest.to_dict()

        image = self.image

        init: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.init, Unset):
            init = self.init.to_dict()

        metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        metrics: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metrics, Unset):
            metrics = self.metrics.to_dict()

        mounts: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.mounts, Unset):
            mounts = []
            for mounts_item_data in self.mounts:
                mounts_item = mounts_item_data.to_dict()
                mounts.append(mounts_item)

        processes: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.processes, Unset):
            processes = []
            for processes_item_data in self.processes:
                processes_item = processes_item_data.to_dict()
                processes.append(processes_item)

        restart: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.restart, Unset):
            restart = self.restart.to_dict()

        schedule = self.schedule

        services: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.services, Unset):
            services = []
            for services_item_data in self.services:
                services_item = services_item_data.to_dict()
                services.append(services_item)

        size = self.size

        standbys: Union[Unset, List[str]] = UNSET
        if not isinstance(self.standbys, Unset):
            standbys = self.standbys

        statics: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.statics, Unset):
            statics = []
            for statics_item_data in self.statics:
                statics_item = statics_item_data.to_dict()
                statics.append(statics_item)

        stop_config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.stop_config, Unset):
            stop_config = self.stop_config.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if auto_destroy is not UNSET:
            field_dict["auto_destroy"] = auto_destroy
        if checks is not UNSET:
            field_dict["checks"] = checks
        if disable_machine_autostart is not UNSET:
            field_dict["disable_machine_autostart"] = disable_machine_autostart
        if dns is not UNSET:
            field_dict["dns"] = dns
        if env is not UNSET:
            field_dict["env"] = env
        if files is not UNSET:
            field_dict["files"] = files
        if guest is not UNSET:
            field_dict["guest"] = guest
        if image is not UNSET:
            field_dict["image"] = image
        if init is not UNSET:
            field_dict["init"] = init
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if metrics is not UNSET:
            field_dict["metrics"] = metrics
        if mounts is not UNSET:
            field_dict["mounts"] = mounts
        if processes is not UNSET:
            field_dict["processes"] = processes
        if restart is not UNSET:
            field_dict["restart"] = restart
        if schedule is not UNSET:
            field_dict["schedule"] = schedule
        if services is not UNSET:
            field_dict["services"] = services
        if size is not UNSET:
            field_dict["size"] = size
        if standbys is not UNSET:
            field_dict["standbys"] = standbys
        if statics is not UNSET:
            field_dict["statics"] = statics
        if stop_config is not UNSET:
            field_dict["stop_config"] = stop_config

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.fly_dns_config import FlyDNSConfig
        from ..models.fly_file import FlyFile
        from ..models.fly_machine_config_checks import FlyMachineConfigChecks
        from ..models.fly_machine_config_env import FlyMachineConfigEnv
        from ..models.fly_machine_config_metadata import FlyMachineConfigMetadata
        from ..models.fly_machine_guest import FlyMachineGuest
        from ..models.fly_machine_init import FlyMachineInit
        from ..models.fly_machine_metrics import FlyMachineMetrics
        from ..models.fly_machine_mount import FlyMachineMount
        from ..models.fly_machine_process import FlyMachineProcess
        from ..models.fly_machine_restart import FlyMachineRestart
        from ..models.fly_machine_service import FlyMachineService
        from ..models.fly_static import FlyStatic
        from ..models.fly_stop_config import FlyStopConfig

        d = src_dict.copy()
        auto_destroy = d.pop("auto_destroy", UNSET)

        _checks = d.pop("checks", UNSET)
        checks: Union[Unset, FlyMachineConfigChecks]
        if isinstance(_checks, Unset):
            checks = UNSET
        else:
            checks = FlyMachineConfigChecks.from_dict(_checks)

        disable_machine_autostart = d.pop("disable_machine_autostart", UNSET)

        _dns = d.pop("dns", UNSET)
        dns: Union[Unset, FlyDNSConfig]
        if isinstance(_dns, Unset):
            dns = UNSET
        else:
            dns = FlyDNSConfig.from_dict(_dns)

        _env = d.pop("env", UNSET)
        env: Union[Unset, FlyMachineConfigEnv]
        if isinstance(_env, Unset):
            env = UNSET
        else:
            env = FlyMachineConfigEnv.from_dict(_env)

        files = []
        _files = d.pop("files", UNSET)
        for files_item_data in _files or []:
            files_item = FlyFile.from_dict(files_item_data)

            files.append(files_item)

        _guest = d.pop("guest", UNSET)
        guest: Union[Unset, FlyMachineGuest]
        if isinstance(_guest, Unset):
            guest = UNSET
        else:
            guest = FlyMachineGuest.from_dict(_guest)

        image = d.pop("image", UNSET)

        _init = d.pop("init", UNSET)
        init: Union[Unset, FlyMachineInit]
        if isinstance(_init, Unset):
            init = UNSET
        else:
            init = FlyMachineInit.from_dict(_init)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, FlyMachineConfigMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = FlyMachineConfigMetadata.from_dict(_metadata)

        _metrics = d.pop("metrics", UNSET)
        metrics: Union[Unset, FlyMachineMetrics]
        if isinstance(_metrics, Unset):
            metrics = UNSET
        else:
            metrics = FlyMachineMetrics.from_dict(_metrics)

        mounts = []
        _mounts = d.pop("mounts", UNSET)
        for mounts_item_data in _mounts or []:
            mounts_item = FlyMachineMount.from_dict(mounts_item_data)

            mounts.append(mounts_item)

        processes = []
        _processes = d.pop("processes", UNSET)
        for processes_item_data in _processes or []:
            processes_item = FlyMachineProcess.from_dict(processes_item_data)

            processes.append(processes_item)

        _restart = d.pop("restart", UNSET)
        restart: Union[Unset, FlyMachineRestart]
        if isinstance(_restart, Unset):
            restart = UNSET
        else:
            restart = FlyMachineRestart.from_dict(_restart)

        schedule = d.pop("schedule", UNSET)

        services = []
        _services = d.pop("services", UNSET)
        for services_item_data in _services or []:
            services_item = FlyMachineService.from_dict(services_item_data)

            services.append(services_item)

        size = d.pop("size", UNSET)

        standbys = cast(List[str], d.pop("standbys", UNSET))

        statics = []
        _statics = d.pop("statics", UNSET)
        for statics_item_data in _statics or []:
            statics_item = FlyStatic.from_dict(statics_item_data)

            statics.append(statics_item)

        _stop_config = d.pop("stop_config", UNSET)
        stop_config: Union[Unset, FlyStopConfig]
        if isinstance(_stop_config, Unset):
            stop_config = UNSET
        else:
            stop_config = FlyStopConfig.from_dict(_stop_config)

        fly_machine_config = cls(
            auto_destroy=auto_destroy,
            checks=checks,
            disable_machine_autostart=disable_machine_autostart,
            dns=dns,
            env=env,
            files=files,
            guest=guest,
            image=image,
            init=init,
            metadata=metadata,
            metrics=metrics,
            mounts=mounts,
            processes=processes,
            restart=restart,
            schedule=schedule,
            services=services,
            size=size,
            standbys=standbys,
            statics=statics,
            stop_config=stop_config,
        )

        fly_machine_config.additional_properties = d
        return fly_machine_config

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
