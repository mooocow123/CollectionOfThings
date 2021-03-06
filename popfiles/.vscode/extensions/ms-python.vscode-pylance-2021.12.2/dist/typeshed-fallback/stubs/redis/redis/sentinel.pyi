from typing import Any, Type, TypeVar, overload
from typing_extensions import Literal

from redis.client import Redis
from redis.commands.sentinel import SentinelCommands
from redis.connection import Connection, ConnectionPool, SSLConnection
from redis.exceptions import ConnectionError

_Redis = TypeVar("_Redis", bound=Redis[Any])

class MasterNotFoundError(ConnectionError): ...
class SlaveNotFoundError(ConnectionError): ...

class SentinelManagedConnection(Connection):
    connection_pool: Any
    def __init__(self, **kwargs) -> None: ...
    def connect_to(self, address) -> None: ...
    def connect(self) -> None: ...
    def read_response(self): ...

class SentinelManagedSSLConnection(SentinelManagedConnection, SSLConnection): ...

class SentinelConnectionPool(ConnectionPool):
    is_master: bool
    check_connection: bool
    connection_kwargs: Any
    service_name: str
    sentinel_manager: Any
    def __init__(self, service_name, sentinel_manager, **kwargs) -> None: ...
    def reset(self) -> None: ...
    def owns_connection(self, connection) -> bool: ...
    def get_master_address(self): ...
    def rotate_slaves(self): ...

class Sentinel(SentinelCommands):
    sentinel_kwargs: Any
    sentinels: Any
    min_other_sentinels: int
    connection_kwargs: Any
    def __init__(
        self, sentinels, min_other_sentinels: int = ..., sentinel_kwargs: Any | None = ..., **connection_kwargs
    ) -> None: ...
    def check_master_state(self, state, service_name) -> bool: ...
    def discover_master(self, service_name): ...
    def filter_slaves(self, slaves): ...
    def discover_slaves(self, service_name): ...
    @overload
    def master_for(self, service_name: str, *, connection_pool_class=..., **kwargs) -> Redis[Any]: ...
    @overload
    def master_for(self, service_name: str, redis_class: Type[_Redis] = ..., connection_pool_class=..., **kwargs) -> _Redis: ...
    @overload
    def slave_for(self, service_name: str, connection_pool_class=..., **kwargs) -> Redis[Any]: ...
    @overload
    def slave_for(self, service_name: str, redis_class: Type[_Redis] = ..., connection_pool_class=..., **kwargs) -> _Redis: ...
    def execute_command(self, *args, **kwargs) -> Literal[True]: ...
