from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.machines_show_metadata_response_200 import MachinesShowMetadataResponse200
from ...types import Response


def _get_kwargs(
    app_name: str,
    machine_id: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/apps/{app_name}/machines/{machine_id}/metadata",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, MachinesShowMetadataResponse200]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = MachinesShowMetadataResponse200.from_dict(response.json())

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
) -> Response[Union[Any, MachinesShowMetadataResponse200]]:
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
) -> Response[Union[Any, MachinesShowMetadataResponse200]]:
    """Get Metadata

     Retrieve metadata for a specific Machine within an app.

    Args:
        app_name (str):
        machine_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, MachinesShowMetadataResponse200]]
    """

    kwargs = _get_kwargs(
        app_name=app_name,
        machine_id=machine_id,
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
) -> Optional[Union[Any, MachinesShowMetadataResponse200]]:
    """Get Metadata

     Retrieve metadata for a specific Machine within an app.

    Args:
        app_name (str):
        machine_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, MachinesShowMetadataResponse200]
    """

    return sync_detailed(
        app_name=app_name,
        machine_id=machine_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    app_name: str,
    machine_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, MachinesShowMetadataResponse200]]:
    """Get Metadata

     Retrieve metadata for a specific Machine within an app.

    Args:
        app_name (str):
        machine_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, MachinesShowMetadataResponse200]]
    """

    kwargs = _get_kwargs(
        app_name=app_name,
        machine_id=machine_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    app_name: str,
    machine_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, MachinesShowMetadataResponse200]]:
    """Get Metadata

     Retrieve metadata for a specific Machine within an app.

    Args:
        app_name (str):
        machine_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, MachinesShowMetadataResponse200]
    """

    return (
        await asyncio_detailed(
            app_name=app_name,
            machine_id=machine_id,
            client=client,
        )
    ).parsed
