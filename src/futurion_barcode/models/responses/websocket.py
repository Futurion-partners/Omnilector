from typing import Literal

from pydantic import BaseModel

from futurion_barcode.models.responses.barcode import BarcodeResponse


class WebSocketBase(BaseModel):
    type: Literal['ack', 'result']


class WebSocketResultBase(WebSocketBase):
    type: Literal['result'] = 'result'
    ok: bool


class WebSocketResult(WebSocketResultBase, BarcodeResponse):
    ...


class WebSocketError(WebSocketResultBase):
    ok: Literal[False] = False
    error: str


class WebSocketAck(WebSocketBase):
    type: Literal['ack'] = 'ack'
    message: str


__all__ = ['WebSocketResult', 'WebSocketError', 'WebSocketAck']
