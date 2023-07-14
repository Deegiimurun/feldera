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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[Any, ErrorResponse]]:
    if response.status_code == HTTPStatus.ACCEPTED:
        response_202 = cast(Any, None)
        return response_202
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


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Any, ErrorResponse]]:
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
) -> Response[Union[Any, ErrorResponse]]:
    """Change the desired state of the pipeline.

     Change the desired state of the pipeline.

    This endpoint allows the user to control the execution of the pipeline,
    by changing its desired state attribute (see the discussion of the desired
    state model in the [`PipelineStatus`] documentation).

    The endpoint returns immediately after validating the request and forwarding
    it to the pipeline. The requested status change completes asynchronously.  On success,
    the pipeline enters the requested desired state.  On error, the pipeline
    transitions to the `Failed` state. The user
    can monitor the current status of the pipeline by polling the `GET /pipeline`
    endpoint.

    The following values of the `action` argument are accepted by this endpoint:

    - 'deploy': Deploy the pipeline: create a process () or Kubernetes pod
    (cloud deployment) to execute the pipeline and initialize its connectors.
    - 'start': Start processing data.
    - 'pause': Pause the pipeline.
    - 'shutdown': Terminate the execution of the pipeline.

    Args:
        pipeline_id (str):
        action (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ErrorResponse]]
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
) -> Optional[Union[Any, ErrorResponse]]:
    """Change the desired state of the pipeline.

     Change the desired state of the pipeline.

    This endpoint allows the user to control the execution of the pipeline,
    by changing its desired state attribute (see the discussion of the desired
    state model in the [`PipelineStatus`] documentation).

    The endpoint returns immediately after validating the request and forwarding
    it to the pipeline. The requested status change completes asynchronously.  On success,
    the pipeline enters the requested desired state.  On error, the pipeline
    transitions to the `Failed` state. The user
    can monitor the current status of the pipeline by polling the `GET /pipeline`
    endpoint.

    The following values of the `action` argument are accepted by this endpoint:

    - 'deploy': Deploy the pipeline: create a process () or Kubernetes pod
    (cloud deployment) to execute the pipeline and initialize its connectors.
    - 'start': Start processing data.
    - 'pause': Pause the pipeline.
    - 'shutdown': Terminate the execution of the pipeline.

    Args:
        pipeline_id (str):
        action (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ErrorResponse]
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
) -> Response[Union[Any, ErrorResponse]]:
    """Change the desired state of the pipeline.

     Change the desired state of the pipeline.

    This endpoint allows the user to control the execution of the pipeline,
    by changing its desired state attribute (see the discussion of the desired
    state model in the [`PipelineStatus`] documentation).

    The endpoint returns immediately after validating the request and forwarding
    it to the pipeline. The requested status change completes asynchronously.  On success,
    the pipeline enters the requested desired state.  On error, the pipeline
    transitions to the `Failed` state. The user
    can monitor the current status of the pipeline by polling the `GET /pipeline`
    endpoint.

    The following values of the `action` argument are accepted by this endpoint:

    - 'deploy': Deploy the pipeline: create a process () or Kubernetes pod
    (cloud deployment) to execute the pipeline and initialize its connectors.
    - 'start': Start processing data.
    - 'pause': Pause the pipeline.
    - 'shutdown': Terminate the execution of the pipeline.

    Args:
        pipeline_id (str):
        action (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ErrorResponse]]
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
) -> Optional[Union[Any, ErrorResponse]]:
    """Change the desired state of the pipeline.

     Change the desired state of the pipeline.

    This endpoint allows the user to control the execution of the pipeline,
    by changing its desired state attribute (see the discussion of the desired
    state model in the [`PipelineStatus`] documentation).

    The endpoint returns immediately after validating the request and forwarding
    it to the pipeline. The requested status change completes asynchronously.  On success,
    the pipeline enters the requested desired state.  On error, the pipeline
    transitions to the `Failed` state. The user
    can monitor the current status of the pipeline by polling the `GET /pipeline`
    endpoint.

    The following values of the `action` argument are accepted by this endpoint:

    - 'deploy': Deploy the pipeline: create a process () or Kubernetes pod
    (cloud deployment) to execute the pipeline and initialize its connectors.
    - 'start': Start processing data.
    - 'pause': Pause the pipeline.
    - 'shutdown': Terminate the execution of the pipeline.

    Args:
        pipeline_id (str):
        action (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ErrorResponse]
    """

    return (
        await asyncio_detailed(
            pipeline_id=pipeline_id,
            action=action,
            client=client,
        )
    ).parsed
