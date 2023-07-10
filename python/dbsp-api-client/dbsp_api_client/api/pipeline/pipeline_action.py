from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    pipeline_id: str,
    action: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/pipelines/{pipeline_id}/{action}".format(client.base_url, pipeline_id=pipeline_id, action=action)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[ErrorResponse, str]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = cast(str, response.json())
        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500
    if response.status_code == HTTPStatus.SERVICE_UNAVAILABLE:
        response_503 = ErrorResponse.from_dict(response.json())

        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[ErrorResponse, str]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    pipeline_id: str,
    action: str,
    *,
    client: Client,
) -> Response[Union[ErrorResponse, str]]:
    """Perform action on a pipeline.

     Perform action on a pipeline.

    - 'deploy': Deploy a pipeline for the specified program and configuration.
    This is a synchronous endpoint, which sends a response once the pipeline has
    been initialized.
    - 'start': Start a pipeline.
    - 'pause': Pause the pipeline.
    - 'shutdown': Terminate the execution of a pipeline. Sends a termination
    request to the pipeline process. Returns immediately, without waiting for
    the pipeline to terminate (which can take several seconds). The pipeline is
    not deleted from the database, but its `status` is set to `shutdown`.

    Args:
        pipeline_id (str):
        action (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, str]]
    """

    kwargs = _get_kwargs(
        pipeline_id=pipeline_id,
        action=action,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    pipeline_id: str,
    action: str,
    *,
    client: Client,
) -> Optional[Union[ErrorResponse, str]]:
    """Perform action on a pipeline.

     Perform action on a pipeline.

    - 'deploy': Deploy a pipeline for the specified program and configuration.
    This is a synchronous endpoint, which sends a response once the pipeline has
    been initialized.
    - 'start': Start a pipeline.
    - 'pause': Pause the pipeline.
    - 'shutdown': Terminate the execution of a pipeline. Sends a termination
    request to the pipeline process. Returns immediately, without waiting for
    the pipeline to terminate (which can take several seconds). The pipeline is
    not deleted from the database, but its `status` is set to `shutdown`.

    Args:
        pipeline_id (str):
        action (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, str]
    """

    return sync_detailed(
        pipeline_id=pipeline_id,
        action=action,
        client=client,
    ).parsed


async def asyncio_detailed(
    pipeline_id: str,
    action: str,
    *,
    client: Client,
) -> Response[Union[ErrorResponse, str]]:
    """Perform action on a pipeline.

     Perform action on a pipeline.

    - 'deploy': Deploy a pipeline for the specified program and configuration.
    This is a synchronous endpoint, which sends a response once the pipeline has
    been initialized.
    - 'start': Start a pipeline.
    - 'pause': Pause the pipeline.
    - 'shutdown': Terminate the execution of a pipeline. Sends a termination
    request to the pipeline process. Returns immediately, without waiting for
    the pipeline to terminate (which can take several seconds). The pipeline is
    not deleted from the database, but its `status` is set to `shutdown`.

    Args:
        pipeline_id (str):
        action (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, str]]
    """

    kwargs = _get_kwargs(
        pipeline_id=pipeline_id,
        action=action,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    pipeline_id: str,
    action: str,
    *,
    client: Client,
) -> Optional[Union[ErrorResponse, str]]:
    """Perform action on a pipeline.

     Perform action on a pipeline.

    - 'deploy': Deploy a pipeline for the specified program and configuration.
    This is a synchronous endpoint, which sends a response once the pipeline has
    been initialized.
    - 'start': Start a pipeline.
    - 'pause': Pause the pipeline.
    - 'shutdown': Terminate the execution of a pipeline. Sends a termination
    request to the pipeline process. Returns immediately, without waiting for
    the pipeline to terminate (which can take several seconds). The pipeline is
    not deleted from the database, but its `status` is set to `shutdown`.

    Args:
        pipeline_id (str):
        action (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, str]
    """

    return (
        await asyncio_detailed(
            pipeline_id=pipeline_id,
            action=action,
            client=client,
        )
    ).parsed
