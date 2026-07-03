from fastapi import WebSocket

from futurion_barcode.models.responses.websocket import (WebSocketAck,
                                                         WebSocketError,
                                                         WebSocketResult)


async def send_result(
    ws: WebSocket,
    result: WebSocketResult,
):
    return await ws.send_json(
        result.model_dump(mode='json')
    )


async def send_acknowledgement(
    ws: WebSocket,
    message: WebSocketAck,
):
    return await ws.send_json(
        message.model_dump(mode='json')
    )


async def send_error(
    ws: WebSocket,
    error: WebSocketError,
):
    return await ws.send_json(
        error.model_dump(mode='json')
    )
