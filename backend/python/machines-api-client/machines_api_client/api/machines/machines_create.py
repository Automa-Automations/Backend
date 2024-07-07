from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_machine_request import CreateMachineRequest
from ...models.machine import Machine
from ...types import Response


def _get_kwargs(
    app_name: str,
    *,
    body: CreateMachineRequest,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/apps/{app_name}/machines",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Machine]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Machine.from_dict(response.json())

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
) -> Response[Union[Any, Machine]]:
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
    body: CreateMachineRequest,
) -> Response[Union[Any, Machine]]:
    """Create Machine

     Create a Machine within a specific app using the details provided in the request body.

    **Important**: This request can fail, and you’re responsible for handling that failure. If you ask
    for a large Machine, or a Machine in a region we happen to be at capacity for, you might need to
    retry the request, or to fall back to another region. If you’re working directly with the Machines
    API, you’re taking some responsibility for your own orchestration!

    Args:
        app_name (str):
        body (CreateMachineRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Machine]]
    """

    kwargs = _get_kwargs(
        app_name=app_name,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    app_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateMachineRequest,
) -> Optional[Union[Any, Machine]]:
    """Create Machine

     Create a Machine within a specific app using the details provided in the request body.

    **Important**: This request can fail, and you’re responsible for handling that failure. If you ask
    for a large Machine, or a Machine in a region we happen to be at capacity for, you might need to
    retry the request, or to fall back to another region. If you’re working directly with the Machines
    API, you’re taking some responsibility for your own orchestration!

    Args:
        app_name (str):
        body (CreateMachineRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Machine]
    """

    return sync_detailed(
        app_name=app_name,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    app_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateMachineRequest,
) -> Response[Union[Any, Machine]]:
    """Create Machine

     Create a Machine within a specific app using the details provided in the request body.

    **Important**: This request can fail, and you’re responsible for handling that failure. If you ask
    for a large Machine, or a Machine in a region we happen to be at capacity for, you might need to
    retry the request, or to fall back to another region. If you’re working directly with the Machines
    API, you’re taking some responsibility for your own orchestration!

    Args:
        app_name (str):
        body (CreateMachineRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Machine]]
    """

    kwargs = _get_kwargs(
        app_name=app_name,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    app_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateMachineRequest,
) -> Optional[Union[Any, Machine]]:
    """Create Machine

     Create a Machine within a specific app using the details provided in the request body.

    **Important**: This request can fail, and you’re responsible for handling that failure. If you ask
    for a large Machine, or a Machine in a region we happen to be at capacity for, you might need to
    retry the request, or to fall back to another region. If you’re working directly with the Machines
    API, you’re taking some responsibility for your own orchestration!

    Args:
        app_name (str):
        body (CreateMachineRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Machine]
    """

    return (
        await asyncio_detailed(
            app_name=app_name,
            client=client,
            body=body,
        )
    ).parsed
