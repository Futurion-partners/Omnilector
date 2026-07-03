import asyncio
import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from omnilector.models.responses.websocket import (WebSocketAck,
                                                         WebSocketError,
                                                         WebSocketResult)
from omnilector.utils.image import process_image
from omnilector.utils.websocket import (send_acknowledgement, send_error,
                                              send_result)

router = APIRouter(
    prefix='/realtime',
    tags=[
        'realtime',
    ]
)


@router.websocket("/")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    print("[WS] Client connected")

    # Internal state per connection
    last_frame = None
    processing = False

    async def process_loop():
        nonlocal processing, last_frame
        while True:
            try:
                if not last_frame or processing:
                    await asyncio.sleep(0.01)
                    continue

                processing = True
                buf = last_frame
                last_frame = None

                try:
                    result = await process_image(buf)
                    await send_result(
                        ws,
                        WebSocketResult(
                            ok=bool(result.barcodes),
                            barcodes=result.barcodes,
                            locations=result.locations,
                            sources=result.sources,
                        )
                    )
                except Exception as e:
                    logging.exception("Processing error")
                    try:
                        await send_error(ws, WebSocketError(error=str(e)))
                    except Exception as send_error_ex:
                        print(f"[WS] Failed to send error message: {send_error_ex}")
                        # If we can't send error, connection is likely broken
                        break
                finally:
                    processing = False
                    
            except asyncio.CancelledError:
                print("[WS] Process loop cancelled")
                break
            except Exception as e:
                logging.exception("Unexpected error in process loop")
                await asyncio.sleep(0.1)  # Brief pause before continuing

    # Run loop in the background
    bg_task = asyncio.create_task(process_loop())

    try:
        while True:
            data = await ws.receive()
            
            # Handle disconnect message
            if data.get("type") == "websocket.disconnect":
                print("[WS] Received disconnect message")
                break
                
            if "bytes" in data:
                last_frame = data["bytes"]
            elif "text" in data:
                msg = data.get("text")
                print("[WS] Received text:", msg)
                try:
                    await send_acknowledgement(
                        ws,
                        WebSocketAck(message='Text messages not supported'),
                    )
                except Exception as e:
                    print("[WS] Error sending acknowledgement:", e)
                    # If we can't send, the connection is likely broken
                    break
    except WebSocketDisconnect:
        print("[WS] Client disconnected")
    except RuntimeError as e:
        if "disconnect message has been received" in str(e):
            print("[WS] Connection already closed")
        else:
            print("[WS] RuntimeError:", e)
    except Exception as e:
        print("[WS] Unexpected error:", e)
    finally:
        bg_task.cancel()
