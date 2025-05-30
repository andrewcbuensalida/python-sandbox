import asyncio

import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.websocket("/ws")
async def openai_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    async def receive_from_fake():
        async for message in websocket.iter_text():
            print(f"Received from fake: {message}")
            if message == "get weather":
                await websocket.send_text("tool")

            elif message == "trigger please wait":
                await websocket.send_text("please")
                await asyncio.sleep(1)
                await websocket.send_text("wait")

            else:
                await websocket.send_text(f"Message is {message}")

    await asyncio.gather(receive_from_fake())


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8766)
