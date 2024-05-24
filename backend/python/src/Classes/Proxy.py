import datetime
from dataclasses import dataclass
from src.utils import get_value, update_value
from typing import Any

@dataclass
class Proxy:
    id: int
    created_at: datetime.datetime
    host: str
    port: int
    type_: str
    security: str
    username: str
    password: str
    country: str
    
    @property
    def url(self) -> str:
        return f"{self.type_}://{self.username}:{self.password}@{self.host}:{self.port}"
    
    @property
    def requests_proxy(self) -> dict:
        return {
            "http": self.url,
            "https": self.url
        }

    @classmethod
    def from_dict(cls, dict_: dict):
        return Proxy(**dict_)

    @classmethod
    def from_id(cls, id: int):
        table = "proxies"
        value = get_value(table=table, line=id)
        return cls.from_dict(value)


class DatabaseSyncedProxy:
    def __init__(self, proxy: Proxy):
        self.proxy = proxy
        self.last_used = datetime.datetime.now()
    
    @property
    def id(self):
        self._sync()
        return self.proxy.id
    
    @property
    def created_at(self):
        self._sync()
        return self.proxy.created_at

    @created_at.setter
    def created_at(self, value):
        self._update('created_at', value)
        self.proxy.created_at = value
    
    @property
    def host(self):
        self._sync()
        return self.proxy.host
    
    @host.setter
    def host(self, value):
        self._update('host', value)
        self.proxy.host = value

    @property
    def port(self):
        self._sync()
        return self.proxy.port

    @port.setter
    def port(self, value):
        self._update('port', value)
        self.proxy.port = value

    @property
    def type_(self):
        self._sync()
        return self.proxy.type_

    @type_.setter
    def type_(self, value):
        self._update('type_', value)
        self.proxy.type_ = value


    @property
    def security(self):
        self._sync()
        return self.proxy.security

    @security.setter
    def security(self, value):
        self._update('security', value)
        self.proxy.security = value

    @property
    def username(self):
        self._sync()
        return self.proxy.username
    
    @username.setter
    def username(self, value):
        self._update('username', value)
        self.proxy.username = value

    @property
    def password(self):
        self._sync()
        return self.proxy.password

    @password.setter
    def password(self, value):
        self._update('password', value)
        self.proxy.password = value 

    @property
    def country(self):
        self._sync()
        return self.proxy.country

    @country.setter
    def country(self, value):
        self._update('country', value)
        self.proxy.country = value 

    @property
    def url(self):
        return self.proxy.url

    @property
    def requests_proxy(self):
        return self.proxy.requests_proxy

    def __eq__(self, other):
        return self.proxy == other.proxy

    def __hash__(self):
        return hash(self.proxy)

    def __str__(self):
        return f"{self.proxy.host}:{self.proxy.port}"

    def __repr__(self):
        return f"{self.proxy.host}:{self.proxy.port}"

    def _sync(self):
        new_data = get_value(table='proxies', line=self.proxy.id)
        for key, value in new_data.items():
            if key.startswith('_'):
                key = key[1:]

            setattr(self.proxy, key, value)

    def _update(self, val: str, new_value: Any):
        table = "proxies"
        line = self.proxy.id
        val = val
        line_name = 'id'

        update_value(table=table, line=line, val=val, new_value=new_value, line_name=line_name)


    @classmethod
    def from_dict(cls, dict_: dict):
        return DatabaseSyncedProxy(proxy=Proxy(**dict_))

    @classmethod
    def from_id(cls, id: int):
        table = "proxies"
        value = get_value(table=table, line=id)
        return cls.from_dict(value)
