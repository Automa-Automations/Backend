from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.volume_host_status import VolumeHostStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="Volume")


@_attrs_define
class Volume:
    """
    Attributes:
        attached_alloc_id (Union[Unset, str]):
        attached_machine_id (Union[Unset, str]):
        auto_backup_enabled (Union[Unset, bool]):
        block_size (Union[Unset, int]):
        blocks (Union[Unset, int]):
        blocks_avail (Union[Unset, int]):
        blocks_free (Union[Unset, int]):
        created_at (Union[Unset, str]):
        encrypted (Union[Unset, bool]):
        fstype (Union[Unset, str]):
        host_status (Union[Unset, VolumeHostStatus]):
        id (Union[Unset, str]):
        name (Union[Unset, str]):
        region (Union[Unset, str]):
        size_gb (Union[Unset, int]):
        snapshot_retention (Union[Unset, int]):
        state (Union[Unset, str]):
        zone (Union[Unset, str]):
    """

    attached_alloc_id: Union[Unset, str] = UNSET
    attached_machine_id: Union[Unset, str] = UNSET
    auto_backup_enabled: Union[Unset, bool] = UNSET
    block_size: Union[Unset, int] = UNSET
    blocks: Union[Unset, int] = UNSET
    blocks_avail: Union[Unset, int] = UNSET
    blocks_free: Union[Unset, int] = UNSET
    created_at: Union[Unset, str] = UNSET
    encrypted: Union[Unset, bool] = UNSET
    fstype: Union[Unset, str] = UNSET
    host_status: Union[Unset, VolumeHostStatus] = UNSET
    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    region: Union[Unset, str] = UNSET
    size_gb: Union[Unset, int] = UNSET
    snapshot_retention: Union[Unset, int] = UNSET
    state: Union[Unset, str] = UNSET
    zone: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        attached_alloc_id = self.attached_alloc_id

        attached_machine_id = self.attached_machine_id

        auto_backup_enabled = self.auto_backup_enabled

        block_size = self.block_size

        blocks = self.blocks

        blocks_avail = self.blocks_avail

        blocks_free = self.blocks_free

        created_at = self.created_at

        encrypted = self.encrypted

        fstype = self.fstype

        host_status: Union[Unset, str] = UNSET
        if not isinstance(self.host_status, Unset):
            host_status = self.host_status.value

        id = self.id

        name = self.name

        region = self.region

        size_gb = self.size_gb

        snapshot_retention = self.snapshot_retention

        state = self.state

        zone = self.zone

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if attached_alloc_id is not UNSET:
            field_dict["attached_alloc_id"] = attached_alloc_id
        if attached_machine_id is not UNSET:
            field_dict["attached_machine_id"] = attached_machine_id
        if auto_backup_enabled is not UNSET:
            field_dict["auto_backup_enabled"] = auto_backup_enabled
        if block_size is not UNSET:
            field_dict["block_size"] = block_size
        if blocks is not UNSET:
            field_dict["blocks"] = blocks
        if blocks_avail is not UNSET:
            field_dict["blocks_avail"] = blocks_avail
        if blocks_free is not UNSET:
            field_dict["blocks_free"] = blocks_free
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if encrypted is not UNSET:
            field_dict["encrypted"] = encrypted
        if fstype is not UNSET:
            field_dict["fstype"] = fstype
        if host_status is not UNSET:
            field_dict["host_status"] = host_status
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if region is not UNSET:
            field_dict["region"] = region
        if size_gb is not UNSET:
            field_dict["size_gb"] = size_gb
        if snapshot_retention is not UNSET:
            field_dict["snapshot_retention"] = snapshot_retention
        if state is not UNSET:
            field_dict["state"] = state
        if zone is not UNSET:
            field_dict["zone"] = zone

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        attached_alloc_id = d.pop("attached_alloc_id", UNSET)

        attached_machine_id = d.pop("attached_machine_id", UNSET)

        auto_backup_enabled = d.pop("auto_backup_enabled", UNSET)

        block_size = d.pop("block_size", UNSET)

        blocks = d.pop("blocks", UNSET)

        blocks_avail = d.pop("blocks_avail", UNSET)

        blocks_free = d.pop("blocks_free", UNSET)

        created_at = d.pop("created_at", UNSET)

        encrypted = d.pop("encrypted", UNSET)

        fstype = d.pop("fstype", UNSET)

        _host_status = d.pop("host_status", UNSET)
        host_status: Union[Unset, VolumeHostStatus]
        if isinstance(_host_status, Unset):
            host_status = UNSET
        else:
            host_status = VolumeHostStatus(_host_status)

        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        region = d.pop("region", UNSET)

        size_gb = d.pop("size_gb", UNSET)

        snapshot_retention = d.pop("snapshot_retention", UNSET)

        state = d.pop("state", UNSET)

        zone = d.pop("zone", UNSET)

        volume = cls(
            attached_alloc_id=attached_alloc_id,
            attached_machine_id=attached_machine_id,
            auto_backup_enabled=auto_backup_enabled,
            block_size=block_size,
            blocks=blocks,
            blocks_avail=blocks_avail,
            blocks_free=blocks_free,
            created_at=created_at,
            encrypted=encrypted,
            fstype=fstype,
            host_status=host_status,
            id=id,
            name=name,
            region=region,
            size_gb=size_gb,
            snapshot_retention=snapshot_retention,
            state=state,
            zone=zone,
        )

        volume.additional_properties = d
        return volume

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
