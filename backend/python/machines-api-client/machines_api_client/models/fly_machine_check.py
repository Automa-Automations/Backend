from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.fly_duration import FlyDuration
    from ..models.fly_machine_http_header import FlyMachineHTTPHeader


T = TypeVar("T", bound="FlyMachineCheck")


@_attrs_define
class FlyMachineCheck:
    """An optional object that defines one or more named checks. The key for each check is the check name.

    Attributes:
        grace_period (Union[Unset, FlyDuration]):
        headers (Union[Unset, List['FlyMachineHTTPHeader']]):
        interval (Union[Unset, FlyDuration]):
        method (Union[Unset, str]): For http checks, the HTTP method to use to when making the request
        path (Union[Unset, str]): For http checks, the path to send the request to
        port (Union[Unset, int]): The port to connect to, often the same as internal_port
        protocol (Union[Unset, str]): For http checks, whether to use http or https
        timeout (Union[Unset, FlyDuration]):
        tls_server_name (Union[Unset, str]): If the protocol is https, the hostname to use for TLS certificate
            validation
        tls_skip_verify (Union[Unset, bool]): For http checks with https protocol, whether or not to verify the TLS
            certificate
        type (Union[Unset, str]): tcp or http
    """

    grace_period: Union[Unset, "FlyDuration"] = UNSET
    headers: Union[Unset, List["FlyMachineHTTPHeader"]] = UNSET
    interval: Union[Unset, "FlyDuration"] = UNSET
    method: Union[Unset, str] = UNSET
    path: Union[Unset, str] = UNSET
    port: Union[Unset, int] = UNSET
    protocol: Union[Unset, str] = UNSET
    timeout: Union[Unset, "FlyDuration"] = UNSET
    tls_server_name: Union[Unset, str] = UNSET
    tls_skip_verify: Union[Unset, bool] = UNSET
    type: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        grace_period: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.grace_period, Unset):
            grace_period = self.grace_period.to_dict()

        headers: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.headers, Unset):
            headers = []
            for headers_item_data in self.headers:
                headers_item = headers_item_data.to_dict()
                headers.append(headers_item)

        interval: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.interval, Unset):
            interval = self.interval.to_dict()

        method = self.method

        path = self.path

        port = self.port

        protocol = self.protocol

        timeout: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.timeout, Unset):
            timeout = self.timeout.to_dict()

        tls_server_name = self.tls_server_name

        tls_skip_verify = self.tls_skip_verify

        type = self.type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if grace_period is not UNSET:
            field_dict["grace_period"] = grace_period
        if headers is not UNSET:
            field_dict["headers"] = headers
        if interval is not UNSET:
            field_dict["interval"] = interval
        if method is not UNSET:
            field_dict["method"] = method
        if path is not UNSET:
            field_dict["path"] = path
        if port is not UNSET:
            field_dict["port"] = port
        if protocol is not UNSET:
            field_dict["protocol"] = protocol
        if timeout is not UNSET:
            field_dict["timeout"] = timeout
        if tls_server_name is not UNSET:
            field_dict["tls_server_name"] = tls_server_name
        if tls_skip_verify is not UNSET:
            field_dict["tls_skip_verify"] = tls_skip_verify
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.fly_duration import FlyDuration
        from ..models.fly_machine_http_header import FlyMachineHTTPHeader

        d = src_dict.copy()
        _grace_period = d.pop("grace_period", UNSET)
        grace_period: Union[Unset, FlyDuration]
        if isinstance(_grace_period, Unset):
            grace_period = UNSET
        else:
            grace_period = FlyDuration.from_dict(_grace_period)

        headers = []
        _headers = d.pop("headers", UNSET)
        for headers_item_data in _headers or []:
            headers_item = FlyMachineHTTPHeader.from_dict(headers_item_data)

            headers.append(headers_item)

        _interval = d.pop("interval", UNSET)
        interval: Union[Unset, FlyDuration]
        if isinstance(_interval, Unset):
            interval = UNSET
        else:
            interval = FlyDuration.from_dict(_interval)

        method = d.pop("method", UNSET)

        path = d.pop("path", UNSET)

        port = d.pop("port", UNSET)

        protocol = d.pop("protocol", UNSET)

        _timeout = d.pop("timeout", UNSET)
        timeout: Union[Unset, FlyDuration]
        if isinstance(_timeout, Unset):
            timeout = UNSET
        else:
            timeout = FlyDuration.from_dict(_timeout)

        tls_server_name = d.pop("tls_server_name", UNSET)

        tls_skip_verify = d.pop("tls_skip_verify", UNSET)

        type = d.pop("type", UNSET)

        fly_machine_check = cls(
            grace_period=grace_period,
            headers=headers,
            interval=interval,
            method=method,
            path=path,
            port=port,
            protocol=protocol,
            timeout=timeout,
            tls_server_name=tls_server_name,
            tls_skip_verify=tls_skip_verify,
            type=type,
        )

        fly_machine_check.additional_properties = d
        return fly_machine_check

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
