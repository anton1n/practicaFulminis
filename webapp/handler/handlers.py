import sys
sys.path.insert(0, '../../')

from controller.atv_controller import ATVWebController
import datetime
import json

atv = None
log_messages = []
connection_status = "Disconnected"

def get_controller():
    global atv
    return atv

def set_controller_ip(ip_addr):
    global atv
    atv = ATVWebController(ip_addr)
    return atv

def add_log(message):
    global log_messages
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    log_messages.append(f"[{timestamp}] {message}")
    if len(log_messages) > 50:
        log_messages.pop(0)

def get_logs():
    return "\n".join(log_messages)

def handle_post(path, post_data):
    global connection_status
    if path == "/start":
        if 'ip_addr' in post_data:
            ip_addr = post_data['ip_addr'][0]
            controller = set_controller_ip(ip_addr)
            add_log(f"IP set to {ip_addr}")
    elif path == "/connect":
        controller = get_controller()
        if controller:
            result = controller.connect(controller.model.ip, 502)
            add_log(f"Connection: {result['connection_status']}")
            connection_status = result['connection_status']
        else:
            add_log("Connection failed")

    elif path == "/disconnect":
        controller = get_controller()
        if controller:
            result = controller.disconnect()
            add_log(f"Disconnected: {result['connection_status']}")
            connection_status = result['connection_status']
        else:
            add_log("Disconnect failed")
    elif path == "/motor/start":
        controller = get_controller()
        if controller:
            direction = post_data.get('direction', ['forward'])[0]
            # freq = float(post_data.get('freq')[0])
            # print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@',freq)
            freq = 25
            result = controller.start(direction, freq)
            add_log(f"Motor start: {'Success' if result['ok'] else 'Failed'}")
        else:
            add_log("Motor start failed")
    elif path == "/motor/stop":
        controller = get_controller()
        if controller:
            result = controller.stop()
            add_log(f"Motor stop: {'Success' if result['ok'] else 'Failed'}")
        else:
            add_log("Motor stop failed")
    elif path == "/motor/emergency":
        controller = get_controller()
        if controller:
            result = controller.emergency()
            add_log(f"Emergency stop: {'Success' if result['ok'] else 'Failed'}")
        else:
            add_log("Emergency stop failed")
    elif path == "/set_frequency":
        controller = get_controller()
        if controller and 'frequency' in post_data:
            freq = float(post_data['frequency'][0])
            print('Frequency at /set_frequency', freq)
            try:
                controller.model.set_frequency(freq)
                add_log(f"Frequency set to {freq} Hz: Success")
            except Exception as e:
                add_log(f"Set frequency failed: {str(e)}")
        else:
            add_log("Set frequency failed")


def handle_get_data():
    controller = get_controller()
    data = {
        'logs': get_logs(),
        'motor_data': {},
        'connection_status': connection_status
    }
    
    if controller:
        try:
            motor_data = controller.read()
            data['motor_data'] = motor_data
            data['connection_status'] = connection_status
        except Exception as e:
            add_log(f"Data fetch error: {str(e)}")
            data['connection_status'] = 'Disconnected'
    
    return json.dumps(data)