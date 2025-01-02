import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
import websockets

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)
@app.websocket("/send_message")
async def send_message(websocket:WebSocket):
    await websocket.accept()

    async with websockets.connect("ws://localhost:8765/ws") as fake_ws:
        async def receive_from_postman():
            async for message in websocket.iter_text():
                print(f"Received from postman: {message}")
                await fake_ws.send(message)
        async def send_to_postman():
            async for fake_message in fake_ws:
                print(f"Received from fake: {fake_message}")
                await websocket.send_text(fake_message)

        await asyncio.gather(receive_from_postman(), send_to_postman())

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8767)
