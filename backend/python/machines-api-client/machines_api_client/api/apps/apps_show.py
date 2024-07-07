from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.app import App
from ...types import Response


def _get_kwargs(
    app_name: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/apps/{app_name}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, App]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = App.from_dict(response.json())

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
) -> Response[Union[Any, App]]:
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
) -> Response[Union[Any, App]]:
    """Get App

     Retrieve details about a specific app by its name.

    Args:
        app_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, App]]
    """

    kwargs = _get_kwargs(
        app_name=app_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    app_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, App]]:
    """Get App

     Retrieve details about a specific app by its name.

    Args:
        app_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, App]
    """

    return sync_detailed(
        app_name=app_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    app_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, App]]:
    """Get App

     Retrieve details about a specific app by its name.

    Args:
        app_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, App]]
    """

    kwargs = _get_kwargs(
        app_name=app_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    app_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, App]]:
    """Get App

     Retrieve details about a specific app by its name.

    Args:
        app_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, App]
    """

    return (
        await asyncio_detailed(
            app_name=app_name,
            client=client,
        )
    ).parsed
