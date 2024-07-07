from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.machine import Machine
from ...types import UNSET, Response, Unset


def _get_kwargs(
    app_name: str,
    *,
    include_deleted: Union[Unset, bool] = UNSET,
    region: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["include_deleted"] = include_deleted

    params["region"] = region

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/apps/{app_name}/machines",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, List["Machine"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Machine.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[Union[Any, List["Machine"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    app_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_deleted: Union[Unset, bool] = UNSET,
    region: Union[Unset, str] = UNSET,
) -> Response[Union[Any, List["Machine"]]]:
    """List Machines

     List all Machines associated with a specific app, with optional filters for including deleted
    Machines and filtering by region.

    Args:
        app_name (str):
        include_deleted (Union[Unset, bool]):
        region (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['Machine']]]
    """

    kwargs = _get_kwargs(
        app_name=app_name,
        include_deleted=include_deleted,
        region=region,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    app_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_deleted: Union[Unset, bool] = UNSET,
    region: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, List["Machine"]]]:
    """List Machines

     List all Machines associated with a specific app, with optional filters for including deleted
    Machines and filtering by region.

    Args:
        app_name (str):
        include_deleted (Union[Unset, bool]):
        region (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['Machine']]
    """

    return sync_detailed(
        app_name=app_name,
        client=client,
        include_deleted=include_deleted,
        region=region,
    ).parsed


async def asyncio_detailed(
    app_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_deleted: Union[Unset, bool] = UNSET,
    region: Union[Unset, str] = UNSET,
) -> Response[Union[Any, List["Machine"]]]:
    """List Machines

     List all Machines associated with a specific app, with optional filters for including deleted
    Machines and filtering by region.

    Args:
        app_name (str):
        include_deleted (Union[Unset, bool]):
        region (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['Machine']]]
    """

    kwargs = _get_kwargs(
        app_name=app_name,
        include_deleted=include_deleted,
        region=region,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    app_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_deleted: Union[Unset, bool] = UNSET,
    region: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, List["Machine"]]]:
    """List Machines

     List all Machines associated with a specific app, with optional filters for including deleted
    Machines and filtering by region.

    Args:
        app_name (str):
        include_deleted (Union[Unset, bool]):
        region (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['Machine']]
    """

    return (
        await asyncio_detailed(
            app_name=app_name,
            client=client,
            include_deleted=include_deleted,
            region=region,
        )
    ).parsed
