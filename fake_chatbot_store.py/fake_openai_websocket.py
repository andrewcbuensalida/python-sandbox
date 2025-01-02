import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    async def receive_from_fake():
        async for message in websocket.iter_text():
            print(f"Received from fake: {message}")
            print('''*Example message:\n''', message)
            await websocket.send_text(f"hello {message}")

    await asyncio.gather(receive_from_fake())


if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8766)