from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.process_stat import ProcessStat
from ...types import UNSET, Response, Unset


def _get_kwargs(
    app_name: str,
    machine_id: str,
    *,
    sort_by: Union[Unset, str] = UNSET,
    order: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["sort_by"] = sort_by

    params["order"] = order

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/apps/{app_name}/machines/{machine_id}/ps",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, List["ProcessStat"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ProcessStat.from_dict(response_200_item_data)

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
) -> Response[Union[Any, List["ProcessStat"]]]:
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
    sort_by: Union[Unset, str] = UNSET,
    order: Union[Unset, str] = UNSET,
) -> Response[Union[Any, List["ProcessStat"]]]:
    """List Processes

     List all processes running on a specific Machine within an app, with optional sorting parameters.

    Args:
        app_name (str):
        machine_id (str):
        sort_by (Union[Unset, str]):
        order (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['ProcessStat']]]
    """

    kwargs = _get_kwargs(
        app_name=app_name,
        machine_id=machine_id,
        sort_by=sort_by,
        order=order,
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
    sort_by: Union[Unset, str] = UNSET,
    order: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, List["ProcessStat"]]]:
    """List Processes

     List all processes running on a specific Machine within an app, with optional sorting parameters.

    Args:
        app_name (str):
        machine_id (str):
        sort_by (Union[Unset, str]):
        order (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['ProcessStat']]
    """

    return sync_detailed(
        app_name=app_name,
        machine_id=machine_id,
        client=client,
        sort_by=sort_by,
        order=order,
    ).parsed


async def asyncio_detailed(
    app_name: str,
    machine_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    sort_by: Union[Unset, str] = UNSET,
    order: Union[Unset, str] = UNSET,
) -> Response[Union[Any, List["ProcessStat"]]]:
    """List Processes

     List all processes running on a specific Machine within an app, with optional sorting parameters.

    Args:
        app_name (str):
        machine_id (str):
        sort_by (Union[Unset, str]):
        order (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['ProcessStat']]]
    """

    kwargs = _get_kwargs(
        app_name=app_name,
        machine_id=machine_id,
        sort_by=sort_by,
        order=order,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    app_name: str,
    machine_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    sort_by: Union[Unset, str] = UNSET,
    order: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, List["ProcessStat"]]]:
    """List Processes

     List all processes running on a specific Machine within an app, with optional sorting parameters.

    Args:
        app_name (str):
        machine_id (str):
        sort_by (Union[Unset, str]):
        order (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['ProcessStat']]
    """

    return (
        await asyncio_detailed(
            app_name=app_name,
            machine_id=machine_id,
            client=client,
            sort_by=sort_by,
            order=order,
        )
    ).parsed
