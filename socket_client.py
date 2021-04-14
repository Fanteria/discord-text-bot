import socketio, time

class socket_client:
    @staticmethod
    def __connect_eventhandler(sio, state, sent):
            sio.emit('bot-light', state)
            sent = True
            time.sleep(0.2)
            sio.disconnect()
    @staticmethod
    def __connect_error_eventhandler(sio, err):
        sio.disconnect()
    @staticmethod
    async def switch_light(server_address, state: int = 0):
        sent = False
        state = min(max(int(state), 0), 1)
        sio = socketio.Client()
        sio.on("connect", lambda : socket_client.__connect_eventhandler(sio, state, sent))
        sio.on("connect_error", lambda err: socket_client.__connect_error_eventhandler(sio, err))
        try:
            sio.connect(server_address)
            sio.wait()
        finally:
            return sent
        

if __name__ == "__main__":
    import sys
    server_address = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8080"
    light_state = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    socket_client.switch_light(server_address, light_state)