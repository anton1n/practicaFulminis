import sys
sys.path.insert(0, '../')

from model.atv_model import ATVModel

class ATVWebController:
    def __init__(self, ip_addr):
        self.model = ATVModel(ip_addr)

    def index(self, **kwargs):
        return {
            'status': 'Disconnected',
            'freq': 0.0,
            'current': 0.0,
            'log': ''
        }

    def connect(self, ip, port):
        ok = self.model.connect()
        return {'status': 'Connected' if ok else 'Failed to connect'}

    def disconnect(self):
        self.model.disconnect()
        return {'status': 'Disconnected'}

    def read(self):
        status = self.model.read_status() or 0
        freq = self.model.read_frequency() or 0.0
        curr = self.model.read_current() or 0.0
        return {
            'status_word': hex(status),
            'freq': freq,
            'current': curr
        }

    def start(self, direction, freq):
        ok = self.model.start_motor(frequency_hz=float(freq), direction=direction)
        return {'action': 'start', 'ok': ok}

    def stop(self):
        ok = self.model.stop_motor()
        return {'action': 'stop', 'ok': ok}

    def emergency(self):
        ok = self.model.emergency_stop()
        return {'action': 'emergency', 'ok': ok}

    def reset(self):
        ok = self.model.reset_fault()
        return {'action': 'reset', 'ok': ok}

if __name__ == "__main__":
    ATVWebController("192.168.100.1")
