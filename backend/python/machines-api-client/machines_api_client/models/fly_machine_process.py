from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.fly_env_from import FlyEnvFrom
    from ..models.fly_machine_process_env import FlyMachineProcessEnv
    from ..models.fly_machine_secret import FlyMachineSecret


T = TypeVar("T", bound="FlyMachineProcess")


@_attrs_define
class FlyMachineProcess:
    """
    Attributes:
        cmd (Union[Unset, List[str]]):
        entrypoint (Union[Unset, List[str]]):
        env (Union[Unset, FlyMachineProcessEnv]):
        env_from (Union[Unset, List['FlyEnvFrom']]): EnvFrom can be provided to set environment variables from machine
            fields.
        exec_ (Union[Unset, List[str]]):
        ignore_app_secrets (Union[Unset, bool]): IgnoreAppSecrets can be set to true to ignore the secrets for the App
            the Machine belongs to
            and only use the secrets provided at the process level. The default/legacy behavior is to use
            the secrets provided at the App level.
        secrets (Union[Unset, List['FlyMachineSecret']]): Secrets can be provided at the process level to explicitly
            indicate which secrets should be
            used for the process. If not provided, the secrets provided at the machine level will be used.
        user (Union[Unset, str]):
    """

    cmd: Union[Unset, List[str]] = UNSET
    entrypoint: Union[Unset, List[str]] = UNSET
    env: Union[Unset, "FlyMachineProcessEnv"] = UNSET
    env_from: Union[Unset, List["FlyEnvFrom"]] = UNSET
    exec_: Union[Unset, List[str]] = UNSET
    ignore_app_secrets: Union[Unset, bool] = UNSET
    secrets: Union[Unset, List["FlyMachineSecret"]] = UNSET
    user: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        cmd: Union[Unset, List[str]] = UNSET
        if not isinstance(self.cmd, Unset):
            cmd = self.cmd

        entrypoint: Union[Unset, List[str]] = UNSET
        if not isinstance(self.entrypoint, Unset):
            entrypoint = self.entrypoint

        env: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.env, Unset):
            env = self.env.to_dict()

        env_from: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.env_from, Unset):
            env_from = []
            for env_from_item_data in self.env_from:
                env_from_item = env_from_item_data.to_dict()
                env_from.append(env_from_item)

        exec_: Union[Unset, List[str]] = UNSET
        if not isinstance(self.exec_, Unset):
            exec_ = self.exec_

        ignore_app_secrets = self.ignore_app_secrets

        secrets: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.secrets, Unset):
            secrets = []
            for secrets_item_data in self.secrets:
                secrets_item = secrets_item_data.to_dict()
                secrets.append(secrets_item)

        user = self.user

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cmd is not UNSET:
            field_dict["cmd"] = cmd
        if entrypoint is not UNSET:
            field_dict["entrypoint"] = entrypoint
        if env is not UNSET:
            field_dict["env"] = env
        if env_from is not UNSET:
            field_dict["env_from"] = env_from
        if exec_ is not UNSET:
            field_dict["exec"] = exec_
        if ignore_app_secrets is not UNSET:
            field_dict["ignore_app_secrets"] = ignore_app_secrets
        if secrets is not UNSET:
            field_dict["secrets"] = secrets
        if user is not UNSET:
            field_dict["user"] = user

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.fly_env_from import FlyEnvFrom
        from ..models.fly_machine_process_env import FlyMachineProcessEnv
        from ..models.fly_machine_secret import FlyMachineSecret

        d = src_dict.copy()
        cmd = cast(List[str], d.pop("cmd", UNSET))

        entrypoint = cast(List[str], d.pop("entrypoint", UNSET))

        _env = d.pop("env", UNSET)
        env: Union[Unset, FlyMachineProcessEnv]
        if isinstance(_env, Unset):
            env = UNSET
        else:
            env = FlyMachineProcessEnv.from_dict(_env)

        env_from = []
        _env_from = d.pop("env_from", UNSET)
        for env_from_item_data in _env_from or []:
            env_from_item = FlyEnvFrom.from_dict(env_from_item_data)

            env_from.append(env_from_item)

        exec_ = cast(List[str], d.pop("exec", UNSET))

        ignore_app_secrets = d.pop("ignore_app_secrets", UNSET)

        secrets = []
        _secrets = d.pop("secrets", UNSET)
        for secrets_item_data in _secrets or []:
            secrets_item = FlyMachineSecret.from_dict(secrets_item_data)

            secrets.append(secrets_item)

        user = d.pop("user", UNSET)

        fly_machine_process = cls(
            cmd=cmd,
            entrypoint=entrypoint,
            env=env,
            env_from=env_from,
            exec_=exec_,
            ignore_app_secrets=ignore_app_secrets,
            secrets=secrets,
            user=user,
        )

        fly_machine_process.additional_properties = d
        return fly_machine_process

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
