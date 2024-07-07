from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_apps_response import ListAppsResponse
from ...types import UNSET, Response


def _get_kwargs(
    *,
    org_slug: str,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["org_slug"] = org_slug

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/apps",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ListAppsResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListAppsResponse.from_dict(response.json())

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
) -> Response[Union[Any, ListAppsResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    org_slug: str,
) -> Response[Union[Any, ListAppsResponse]]:
    """List Apps

     List all apps with the ability to filter by organization slug.

    Args:
        org_slug (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ListAppsResponse]]
    """

    kwargs = _get_kwargs(
        org_slug=org_slug,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    org_slug: str,
) -> Optional[Union[Any, ListAppsResponse]]:
    """List Apps

     List all apps with the ability to filter by organization slug.

    Args:
        org_slug (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ListAppsResponse]
    """

    return sync_detailed(
        client=client,
        org_slug=org_slug,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    org_slug: str,
) -> Response[Union[Any, ListAppsResponse]]:
    """List Apps

     List all apps with the ability to filter by organization slug.

    Args:
        org_slug (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ListAppsResponse]]
    """

    kwargs = _get_kwargs(
        org_slug=org_slug,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    org_slug: str,
) -> Optional[Union[Any, ListAppsResponse]]:
    """List Apps

     List all apps with the ability to filter by organization slug.

    Args:
        org_slug (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ListAppsResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            org_slug=org_slug,
        )
    ).parsed
