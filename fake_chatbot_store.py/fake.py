import asyncio
from datetime import datetime

import websockets
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
async def handle_media_stream(websocket: WebSocket):
    await websocket.accept()

    async with websockets.connect("ws://localhost:8766/ws") as openai_ws:

        async def receive_from_twilio():
            async for message in websocket.iter_text():
                print(f"Received from Twilio: {message}")
                await openai_ws.send(message)

        async def send_to_twilio():
            async for openai_message in openai_ws:
                print(f"Received from OpenAI: {openai_message}")
                if openai_message == "tool":
                    await openai_ws.send("trigger please wait")
                elif openai_message == "wait":
                    await websocket.send_text("wait")
                    await websocket.send_text("typing")
                    results = await execute_tools()
                    await openai_ws.send(results)
                    await websocket.send_text("stop typing")
                else:
                    await websocket.send_text(openai_message)

        async def execute_tools():
            print(f"Executing tools at {datetime.now()}")
            await asyncio.sleep(5)
            tool_results = "sunny"
            print("Tools executed")
            return tool_results

        await asyncio.gather(receive_from_twilio(), send_to_twilio())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port="8765",
    )
