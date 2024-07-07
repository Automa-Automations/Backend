from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.fly_http_options import FlyHTTPOptions
    from ..models.fly_proxy_proto_options import FlyProxyProtoOptions
    from ..models.fly_tls_options import FlyTLSOptions


T = TypeVar("T", bound="FlyMachinePort")


@_attrs_define
class FlyMachinePort:
    """
    Attributes:
        end_port (Union[Unset, int]):
        force_https (Union[Unset, bool]):
        handlers (Union[Unset, List[str]]):
        http_options (Union[Unset, FlyHTTPOptions]):
        port (Union[Unset, int]):
        proxy_proto_options (Union[Unset, FlyProxyProtoOptions]):
        start_port (Union[Unset, int]):
        tls_options (Union[Unset, FlyTLSOptions]):
    """

    end_port: Union[Unset, int] = UNSET
    force_https: Union[Unset, bool] = UNSET
    handlers: Union[Unset, List[str]] = UNSET
    http_options: Union[Unset, "FlyHTTPOptions"] = UNSET
    port: Union[Unset, int] = UNSET
    proxy_proto_options: Union[Unset, "FlyProxyProtoOptions"] = UNSET
    start_port: Union[Unset, int] = UNSET
    tls_options: Union[Unset, "FlyTLSOptions"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        end_port = self.end_port

        force_https = self.force_https

        handlers: Union[Unset, List[str]] = UNSET
        if not isinstance(self.handlers, Unset):
            handlers = self.handlers

        http_options: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.http_options, Unset):
            http_options = self.http_options.to_dict()

        port = self.port

        proxy_proto_options: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.proxy_proto_options, Unset):
            proxy_proto_options = self.proxy_proto_options.to_dict()

        start_port = self.start_port

        tls_options: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.tls_options, Unset):
            tls_options = self.tls_options.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if end_port is not UNSET:
            field_dict["end_port"] = end_port
        if force_https is not UNSET:
            field_dict["force_https"] = force_https
        if handlers is not UNSET:
            field_dict["handlers"] = handlers
        if http_options is not UNSET:
            field_dict["http_options"] = http_options
        if port is not UNSET:
            field_dict["port"] = port
        if proxy_proto_options is not UNSET:
            field_dict["proxy_proto_options"] = proxy_proto_options
        if start_port is not UNSET:
            field_dict["start_port"] = start_port
        if tls_options is not UNSET:
            field_dict["tls_options"] = tls_options

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.fly_http_options import FlyHTTPOptions
        from ..models.fly_proxy_proto_options import FlyProxyProtoOptions
        from ..models.fly_tls_options import FlyTLSOptions

        d = src_dict.copy()
        end_port = d.pop("end_port", UNSET)

        force_https = d.pop("force_https", UNSET)

        handlers = cast(List[str], d.pop("handlers", UNSET))

        _http_options = d.pop("http_options", UNSET)
        http_options: Union[Unset, FlyHTTPOptions]
        if isinstance(_http_options, Unset):
            http_options = UNSET
        else:
            http_options = FlyHTTPOptions.from_dict(_http_options)

        port = d.pop("port", UNSET)

        _proxy_proto_options = d.pop("proxy_proto_options", UNSET)
        proxy_proto_options: Union[Unset, FlyProxyProtoOptions]
        if isinstance(_proxy_proto_options, Unset):
            proxy_proto_options = UNSET
        else:
            proxy_proto_options = FlyProxyProtoOptions.from_dict(_proxy_proto_options)

        start_port = d.pop("start_port", UNSET)

        _tls_options = d.pop("tls_options", UNSET)
        tls_options: Union[Unset, FlyTLSOptions]
        if isinstance(_tls_options, Unset):
            tls_options = UNSET
        else:
            tls_options = FlyTLSOptions.from_dict(_tls_options)

        fly_machine_port = cls(
            end_port=end_port,
            force_https=force_https,
            handlers=handlers,
            http_options=http_options,
            port=port,
            proxy_proto_options=proxy_proto_options,
            start_port=start_port,
            tls_options=tls_options,
        )

        fly_machine_port.additional_properties = d
        return fly_machine_port

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
