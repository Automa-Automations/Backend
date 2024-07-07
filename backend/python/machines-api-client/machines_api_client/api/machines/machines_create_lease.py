from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_lease_request import CreateLeaseRequest
from ...models.lease import Lease
from ...types import UNSET, Response, Unset


def _get_kwargs(
    app_name: str,
    machine_id: str,
    *,
    body: CreateLeaseRequest,
    fly_machine_lease_nonce: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    if not isinstance(fly_machine_lease_nonce, Unset):
        headers["fly-machine-lease-nonce"] = fly_machine_lease_nonce

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/apps/{app_name}/machines/{machine_id}/lease",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Lease]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Lease.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, Lease]]:
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
    body: CreateLeaseRequest,
    fly_machine_lease_nonce: Union[Unset, str] = UNSET,
) -> Response[Union[Any, Lease]]:
    """Create Lease

     Create a lease for a specific Machine within an app using the details provided in the request body.
    Machine leases can be used to obtain an exclusive lock on modifying a Machine.

    Args:
        app_name (str):
        machine_id (str):
        fly_machine_lease_nonce (Union[Unset, str]):
        body (CreateLeaseRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Lease]]
    """

    kwargs = _get_kwargs(
        app_name=app_name,
        machine_id=machine_id,
        body=body,
        fly_machine_lease_nonce=fly_machine_lease_nonce,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    app_name: str,
    machine_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateLeaseRequest,
    fly_machine_lease_nonce: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, Lease]]:
    """Create Lease

     Create a lease for a specific Machine within an app using the details provided in the request body.
    Machine leases can be used to obtain an exclusive lock on modifying a Machine.

    Args:
        app_name (str):
        machine_id (str):
        fly_machine_lease_nonce (Union[Unset, str]):
        body (CreateLeaseRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Lease]
    """

    return sync_detailed(
        app_name=app_name,
        machine_id=machine_id,
        client=client,
        body=body,
        fly_machine_lease_nonce=fly_machine_lease_nonce,
    ).parsed


async def asyncio_detailed(
    app_name: str,
    machine_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateLeaseRequest,
    fly_machine_lease_nonce: Union[Unset, str] = UNSET,
) -> Response[Union[Any, Lease]]:
    """Create Lease

     Create a lease for a specific Machine within an app using the details provided in the request body.
    Machine leases can be used to obtain an exclusive lock on modifying a Machine.

    Args:
        app_name (str):
        machine_id (str):
        fly_machine_lease_nonce (Union[Unset, str]):
        body (CreateLeaseRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Lease]]
    """

    kwargs = _get_kwargs(
        app_name=app_name,
        machine_id=machine_id,
        body=body,
        fly_machine_lease_nonce=fly_machine_lease_nonce,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    app_name: str,
    machine_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateLeaseRequest,
    fly_machine_lease_nonce: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, Lease]]:
    """Create Lease

     Create a lease for a specific Machine within an app using the details provided in the request body.
    Machine leases can be used to obtain an exclusive lock on modifying a Machine.

    Args:
        app_name (str):
        machine_id (str):
        fly_machine_lease_nonce (Union[Unset, str]):
        body (CreateLeaseRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Lease]
    """

    return (
        await asyncio_detailed(
            app_name=app_name,
            machine_id=machine_id,
            client=client,
            body=body,
            fly_machine_lease_nonce=fly_machine_lease_nonce,
        )
    ).parsed
