import sys
sys.path.insert(0, '../')

from model.atv_model import ATVModel

class ATVWebController:
    def __init__(self, ip_addr):
        self.model = ATVModel(ip_addr)
        self.ip_addr = ip_addr

    def index(self, **kwargs):
        return {
            'status': 'Disconnected',
            'freq': 0.0,
            'current': 0.0,
            'log': ''
        }

    def connect(self, ip, port):
        ok = self.model.connect()
        return {'connection_status': 'Connected' if ok else 'Failed to connect'}

    def disconnect(self):
        self.model.disconnect()
        return {'connection_status': 'Disconnected'}

    def read(self):
        status = self.model.read_status() or 0
        freq = self.model.read_frequency() or 0
        target_freq = self.model.read_target_frequency() or 0
        # print('#################################')
        # print('Freq in controller.read:', freq)
        curr = self.model.read_current() or 0.0
        
        motor_state = "STARTED" if freq > 0.1 else "STOPPED"
            
        return {
            'status_word': hex(status),
            'freq': freq,
            'target_freq' : target_freq,
            'current': curr,
            'motor_state': motor_state
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


if __name__ == "__main__":
    ATVWebController("192.168.100.1")
