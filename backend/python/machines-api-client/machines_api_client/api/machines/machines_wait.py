from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.machines_wait_state import MachinesWaitState
from ...types import UNSET, Response, Unset


def _get_kwargs(
    app_name: str,
    machine_id: str,
    *,
    instance_id: Union[Unset, str] = UNSET,
    timeout: Union[Unset, int] = UNSET,
    state: Union[Unset, MachinesWaitState] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["instance_id"] = instance_id

    params["timeout"] = timeout

    json_state: Union[Unset, str] = UNSET
    if not isinstance(state, Unset):
        json_state = state.value

    params["state"] = json_state

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/apps/{app_name}/machines/{machine_id}/wait",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if response.status_code == HTTPStatus.OK:
        return None
    if response.status_code == HTTPStatus.BAD_REQUEST:
        return None
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        return None
    if response.status_code == HTTPStatus.NOT_FOUND:
        return None
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    app_name: str,
    machine_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    instance_id: Union[Unset, str] = UNSET,
    timeout: Union[Unset, int] = UNSET,
    state: Union[Unset, MachinesWaitState] = UNSET,
) -> Response[Any]:
    """Wait for State

     Wait for a Machine to reach a specific state. Specify the desired state with the state parameter.
    See the [Machine states table](https://fly.io/docs/machines/working-with-machines/#machine-states)
    for a list of possible states. The default for this parameter is `started`.

    This request will block for up to 60 seconds. Set a shorter timeout with the timeout parameter.

    Args:
        app_name (str):
        machine_id (str):
        instance_id (Union[Unset, str]):
        timeout (Union[Unset, int]):
        state (Union[Unset, MachinesWaitState]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        app_name=app_name,
        machine_id=machine_id,
        instance_id=instance_id,
        timeout=timeout,
        state=state,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    app_name: str,
    machine_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    instance_id: Union[Unset, str] = UNSET,
    timeout: Union[Unset, int] = UNSET,
    state: Union[Unset, MachinesWaitState] = UNSET,
) -> Response[Any]:
    """Wait for State

     Wait for a Machine to reach a specific state. Specify the desired state with the state parameter.
    See the [Machine states table](https://fly.io/docs/machines/working-with-machines/#machine-states)
    for a list of possible states. The default for this parameter is `started`.

    This request will block for up to 60 seconds. Set a shorter timeout with the timeout parameter.

    Args:
        app_name (str):
        machine_id (str):
        instance_id (Union[Unset, str]):
        timeout (Union[Unset, int]):
        state (Union[Unset, MachinesWaitState]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        app_name=app_name,
        machine_id=machine_id,
        instance_id=instance_id,
        timeout=timeout,
        state=state,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
