from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.fly_machine_guest import FlyMachineGuest


T = TypeVar("T", bound="CreateVolumeRequest")


@_attrs_define
class CreateVolumeRequest:
    """
    Attributes:
        compute (Union[Unset, FlyMachineGuest]):
        compute_image (Union[Unset, str]):
        encrypted (Union[Unset, bool]):
        fstype (Union[Unset, str]):
        machines_only (Union[Unset, bool]):
        name (Union[Unset, str]):
        region (Union[Unset, str]):
        require_unique_zone (Union[Unset, bool]):
        size_gb (Union[Unset, int]):
        snapshot_id (Union[Unset, str]): restore from snapshot
        snapshot_retention (Union[Unset, int]):
        source_volume_id (Union[Unset, str]): fork from remote volume
    """

    compute: Union[Unset, "FlyMachineGuest"] = UNSET
    compute_image: Union[Unset, str] = UNSET
    encrypted: Union[Unset, bool] = UNSET
    fstype: Union[Unset, str] = UNSET
    machines_only: Union[Unset, bool] = UNSET
    name: Union[Unset, str] = UNSET
    region: Union[Unset, str] = UNSET
    require_unique_zone: Union[Unset, bool] = UNSET
    size_gb: Union[Unset, int] = UNSET
    snapshot_id: Union[Unset, str] = UNSET
    snapshot_retention: Union[Unset, int] = UNSET
    source_volume_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        compute: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.compute, Unset):
            compute = self.compute.to_dict()

        compute_image = self.compute_image

        encrypted = self.encrypted

        fstype = self.fstype

        machines_only = self.machines_only

        name = self.name

        region = self.region

        require_unique_zone = self.require_unique_zone

        size_gb = self.size_gb

        snapshot_id = self.snapshot_id

        snapshot_retention = self.snapshot_retention

        source_volume_id = self.source_volume_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if compute is not UNSET:
            field_dict["compute"] = compute
        if compute_image is not UNSET:
            field_dict["compute_image"] = compute_image
        if encrypted is not UNSET:
            field_dict["encrypted"] = encrypted
        if fstype is not UNSET:
            field_dict["fstype"] = fstype
        if machines_only is not UNSET:
            field_dict["machines_only"] = machines_only
        if name is not UNSET:
            field_dict["name"] = name
        if region is not UNSET:
            field_dict["region"] = region
        if require_unique_zone is not UNSET:
            field_dict["require_unique_zone"] = require_unique_zone
        if size_gb is not UNSET:
            field_dict["size_gb"] = size_gb
        if snapshot_id is not UNSET:
            field_dict["snapshot_id"] = snapshot_id
        if snapshot_retention is not UNSET:
            field_dict["snapshot_retention"] = snapshot_retention
        if source_volume_id is not UNSET:
            field_dict["source_volume_id"] = source_volume_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.fly_machine_guest import FlyMachineGuest

        d = src_dict.copy()
        _compute = d.pop("compute", UNSET)
        compute: Union[Unset, FlyMachineGuest]
        if isinstance(_compute, Unset):
            compute = UNSET
        else:
            compute = FlyMachineGuest.from_dict(_compute)

        compute_image = d.pop("compute_image", UNSET)

        encrypted = d.pop("encrypted", UNSET)

        fstype = d.pop("fstype", UNSET)

        machines_only = d.pop("machines_only", UNSET)

        name = d.pop("name", UNSET)

        region = d.pop("region", UNSET)

        require_unique_zone = d.pop("require_unique_zone", UNSET)

        size_gb = d.pop("size_gb", UNSET)

        snapshot_id = d.pop("snapshot_id", UNSET)

        snapshot_retention = d.pop("snapshot_retention", UNSET)

        source_volume_id = d.pop("source_volume_id", UNSET)

        create_volume_request = cls(
            compute=compute,
            compute_image=compute_image,
            encrypted=encrypted,
            fstype=fstype,
            machines_only=machines_only,
            name=name,
            region=region,
            require_unique_zone=require_unique_zone,
            size_gb=size_gb,
            snapshot_id=snapshot_id,
            snapshot_retention=snapshot_retention,
            source_volume_id=source_volume_id,
        )

        create_volume_request.additional_properties = d
        return create_volume_request

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
