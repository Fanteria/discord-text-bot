import socketio, time

class socket_client:
    @staticmethod
    def __connect(sio, state):
            print(state)
            sio.emit('light', int(state))
            time.sleep(0.2)
            sio.disconnect()
    @staticmethod
    def switch_light(server_address, state: int = 0):
        state = min(max(int(state), 0), 1)
        sio = socketio.Client()
        sio.connect(server_address)
        sio.wait()

if __name__ == "__main__":
    import sys
    server_address = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8080"
    light_state = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    socket_client.switch_light(server_address, light_state)