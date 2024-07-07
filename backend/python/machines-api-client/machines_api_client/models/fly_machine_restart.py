from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.fly_machine_restart_policy import FlyMachineRestartPolicy
from ..types import UNSET, Unset

T = TypeVar("T", bound="FlyMachineRestart")


@_attrs_define
class FlyMachineRestart:
    """The Machine restart policy defines whether and how flyd restarts a Machine after its main process exits. See
    https://fly.io/docs/machines/guides-examples/machine-restart-policy/.

        Attributes:
            max_retries (Union[Unset, int]): When policy is on-failure, the maximum number of times to attempt to restart
                the Machine before letting it stop.
            policy (Union[Unset, FlyMachineRestartPolicy]): * no - Never try to restart a Machine automatically when its
                main process exits, whether that’s on purpose or on a crash.
                * always - Always restart a Machine automatically and never let it enter a stopped state, even when the main
                process exits cleanly.
                * on-failure - Try up to MaxRetries times to automatically restart the Machine if it exits with a non-zero exit
                code. Default when no explicit policy is set, and for Machines with schedules.
    """

    max_retries: Union[Unset, int] = UNSET
    policy: Union[Unset, FlyMachineRestartPolicy] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        max_retries = self.max_retries

        policy: Union[Unset, str] = UNSET
        if not isinstance(self.policy, Unset):
            policy = self.policy.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if max_retries is not UNSET:
            field_dict["max_retries"] = max_retries
        if policy is not UNSET:
            field_dict["policy"] = policy

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        max_retries = d.pop("max_retries", UNSET)

        _policy = d.pop("policy", UNSET)
        policy: Union[Unset, FlyMachineRestartPolicy]
        if isinstance(_policy, Unset):
            policy = UNSET
        else:
            policy = FlyMachineRestartPolicy(_policy)

        fly_machine_restart = cls(
            max_retries=max_retries,
            policy=policy,
        )

        fly_machine_restart.additional_properties = d
        return fly_machine_restart

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
