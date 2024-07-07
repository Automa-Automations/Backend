from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import Response


def _get_kwargs(
    app_name: str,
    machine_id: str,
    *,
    fly_machine_lease_nonce: str,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    headers["fly-machine-lease-nonce"] = fly_machine_lease_nonce

    _kwargs: Dict[str, Any] = {
        "method": "delete",
        "url": f"/apps/{app_name}/machines/{machine_id}/lease",
    }

    _kwargs["headers"] = headers
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
    fly_machine_lease_nonce: str,
) -> Response[Any]:
    """Release Lease

     Release the lease of a specific Machine within an app. Machine leases can be used to obtain an
    exclusive lock on modifying a Machine.

    Args:
        app_name (str):
        machine_id (str):
        fly_machine_lease_nonce (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        app_name=app_name,
        machine_id=machine_id,
        fly_machine_lease_nonce=fly_machine_lease_nonce,
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
    fly_machine_lease_nonce: str,
) -> Response[Any]:
    """Release Lease

     Release the lease of a specific Machine within an app. Machine leases can be used to obtain an
    exclusive lock on modifying a Machine.

    Args:
        app_name (str):
        machine_id (str):
        fly_machine_lease_nonce (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        app_name=app_name,
        machine_id=machine_id,
        fly_machine_lease_nonce=fly_machine_lease_nonce,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
