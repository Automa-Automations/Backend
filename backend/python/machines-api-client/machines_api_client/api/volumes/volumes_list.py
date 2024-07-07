from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.volume import Volume
from ...types import Response


def _get_kwargs(
    app_name: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/apps/{app_name}/volumes",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, List["Volume"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Volume.from_dict(response_200_item_data)

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
) -> Response[Union[Any, List["Volume"]]]:
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
) -> Response[Union[Any, List["Volume"]]]:
    """List Volumes

     List all volumes associated with a specific app.

    Args:
        app_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['Volume']]]
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
) -> Optional[Union[Any, List["Volume"]]]:
    """List Volumes

     List all volumes associated with a specific app.

    Args:
        app_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['Volume']]
    """

    return sync_detailed(
        app_name=app_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    app_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, List["Volume"]]]:
    """List Volumes

     List all volumes associated with a specific app.

    Args:
        app_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['Volume']]]
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
) -> Optional[Union[Any, List["Volume"]]]:
    """List Volumes

     List all volumes associated with a specific app.

    Args:
        app_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['Volume']]
    """

    return (
        await asyncio_detailed(
            app_name=app_name,
            client=client,
        )
    ).parsed
