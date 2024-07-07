from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.extend_volume_request import ExtendVolumeRequest
from ...models.extend_volume_response import ExtendVolumeResponse
from ...types import Response


def _get_kwargs(
    app_name: str,
    volume_id: str,
    *,
    body: ExtendVolumeRequest,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "put",
        "url": f"/apps/{app_name}/volumes/{volume_id}/extend",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ExtendVolumeResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ExtendVolumeResponse.from_dict(response.json())

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
) -> Response[Union[Any, ExtendVolumeResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    app_name: str,
    volume_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ExtendVolumeRequest,
) -> Response[Union[Any, ExtendVolumeResponse]]:
    """Extend Volume

     Extend a volume's size within an app using the details provided in the request body.

    Args:
        app_name (str):
        volume_id (str):
        body (ExtendVolumeRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ExtendVolumeResponse]]
    """

    kwargs = _get_kwargs(
        app_name=app_name,
        volume_id=volume_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    app_name: str,
    volume_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ExtendVolumeRequest,
) -> Optional[Union[Any, ExtendVolumeResponse]]:
    """Extend Volume

     Extend a volume's size within an app using the details provided in the request body.

    Args:
        app_name (str):
        volume_id (str):
        body (ExtendVolumeRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ExtendVolumeResponse]
    """

    return sync_detailed(
        app_name=app_name,
        volume_id=volume_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    app_name: str,
    volume_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ExtendVolumeRequest,
) -> Response[Union[Any, ExtendVolumeResponse]]:
    """Extend Volume

     Extend a volume's size within an app using the details provided in the request body.

    Args:
        app_name (str):
        volume_id (str):
        body (ExtendVolumeRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ExtendVolumeResponse]]
    """

    kwargs = _get_kwargs(
        app_name=app_name,
        volume_id=volume_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    app_name: str,
    volume_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ExtendVolumeRequest,
) -> Optional[Union[Any, ExtendVolumeResponse]]:
    """Extend Volume

     Extend a volume's size within an app using the details provided in the request body.

    Args:
        app_name (str):
        volume_id (str):
        body (ExtendVolumeRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ExtendVolumeResponse]
    """

    return (
        await asyncio_detailed(
            app_name=app_name,
            volume_id=volume_id,
            client=client,
            body=body,
        )
    ).parsed
