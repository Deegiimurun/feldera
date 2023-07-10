from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.error_response import ErrorResponse
from ...models.pipeline_stats_response_200 import PipelineStatsResponse200
from ...types import Response


def _get_kwargs(
    pipeline_id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/pipelines/{pipeline_id}/stats".format(client.base_url, pipeline_id=pipeline_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
    }


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[ErrorResponse, PipelineStatsResponse200]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PipelineStatsResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[ErrorResponse, PipelineStatsResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    pipeline_id: str,
    *,
    client: Client,
) -> Response[Union[ErrorResponse, PipelineStatsResponse200]]:
    """Retrieve pipeline metrics and performance counters.

     Retrieve pipeline metrics and performance counters.

    Args:
        pipeline_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, PipelineStatsResponse200]]
    """

    kwargs = _get_kwargs(
        pipeline_id=pipeline_id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    pipeline_id: str,
    *,
    client: Client,
) -> Optional[Union[ErrorResponse, PipelineStatsResponse200]]:
    """Retrieve pipeline metrics and performance counters.

     Retrieve pipeline metrics and performance counters.

    Args:
        pipeline_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, PipelineStatsResponse200]
    """

    return sync_detailed(
        pipeline_id=pipeline_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    pipeline_id: str,
    *,
    client: Client,
) -> Response[Union[ErrorResponse, PipelineStatsResponse200]]:
    """Retrieve pipeline metrics and performance counters.

     Retrieve pipeline metrics and performance counters.

    Args:
        pipeline_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, PipelineStatsResponse200]]
    """

    kwargs = _get_kwargs(
        pipeline_id=pipeline_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    pipeline_id: str,
    *,
    client: Client,
) -> Optional[Union[ErrorResponse, PipelineStatsResponse200]]:
    """Retrieve pipeline metrics and performance counters.

     Retrieve pipeline metrics and performance counters.

    Args:
        pipeline_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, PipelineStatsResponse200]
    """

    return (
        await asyncio_detailed(
            pipeline_id=pipeline_id,
            client=client,
        )
    ).parsed
