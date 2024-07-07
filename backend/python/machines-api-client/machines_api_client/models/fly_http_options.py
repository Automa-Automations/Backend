from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.fly_http_response_options import FlyHTTPResponseOptions


T = TypeVar("T", bound="FlyHTTPOptions")


@_attrs_define
class FlyHTTPOptions:
    """
    Attributes:
        compress (Union[Unset, bool]):
        h2_backend (Union[Unset, bool]):
        response (Union[Unset, FlyHTTPResponseOptions]):
    """

    compress: Union[Unset, bool] = UNSET
    h2_backend: Union[Unset, bool] = UNSET
    response: Union[Unset, "FlyHTTPResponseOptions"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        compress = self.compress

        h2_backend = self.h2_backend

        response: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.response, Unset):
            response = self.response.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if compress is not UNSET:
            field_dict["compress"] = compress
        if h2_backend is not UNSET:
            field_dict["h2_backend"] = h2_backend
        if response is not UNSET:
            field_dict["response"] = response

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.fly_http_response_options import FlyHTTPResponseOptions

        d = src_dict.copy()
        compress = d.pop("compress", UNSET)

        h2_backend = d.pop("h2_backend", UNSET)

        _response = d.pop("response", UNSET)
        response: Union[Unset, FlyHTTPResponseOptions]
        if isinstance(_response, Unset):
            response = UNSET
        else:
            response = FlyHTTPResponseOptions.from_dict(_response)

        fly_http_options = cls(
            compress=compress,
            h2_backend=h2_backend,
            response=response,
        )

        fly_http_options.additional_properties = d
        return fly_http_options

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
