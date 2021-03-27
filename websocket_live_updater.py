class LiveUpdater:
    def __init__(self, pipe) -> None:
        self.pipe = pipe

    async def update(websocket, msg):
        await websocket.send(msg)