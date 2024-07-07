from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.image_ref_labels import ImageRefLabels


T = TypeVar("T", bound="ImageRef")


@_attrs_define
class ImageRef:
    """
    Attributes:
        digest (Union[Unset, str]):
        labels (Union[Unset, ImageRefLabels]):
        registry (Union[Unset, str]):
        repository (Union[Unset, str]):
        tag (Union[Unset, str]):
    """

    digest: Union[Unset, str] = UNSET
    labels: Union[Unset, "ImageRefLabels"] = UNSET
    registry: Union[Unset, str] = UNSET
    repository: Union[Unset, str] = UNSET
    tag: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        digest = self.digest

        labels: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = self.labels.to_dict()

        registry = self.registry

        repository = self.repository

        tag = self.tag

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if digest is not UNSET:
            field_dict["digest"] = digest
        if labels is not UNSET:
            field_dict["labels"] = labels
        if registry is not UNSET:
            field_dict["registry"] = registry
        if repository is not UNSET:
            field_dict["repository"] = repository
        if tag is not UNSET:
            field_dict["tag"] = tag

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.image_ref_labels import ImageRefLabels

        d = src_dict.copy()
        digest = d.pop("digest", UNSET)

        _labels = d.pop("labels", UNSET)
        labels: Union[Unset, ImageRefLabels]
        if isinstance(_labels, Unset):
            labels = UNSET
        else:
            labels = ImageRefLabels.from_dict(_labels)

        registry = d.pop("registry", UNSET)

        repository = d.pop("repository", UNSET)

        tag = d.pop("tag", UNSET)

        image_ref = cls(
            digest=digest,
            labels=labels,
            registry=registry,
            repository=repository,
            tag=tag,
        )

        image_ref.additional_properties = d
        return image_ref

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
