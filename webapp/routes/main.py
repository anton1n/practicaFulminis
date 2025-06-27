routes = {
    "/" : {
        "template" : "templates/index.html"
    },
    "/style.css" : {
        "template" : "templates/style.css"
    },
    "/start" : {
        "method": "POST",
        "handler": "set_ip"
    },
    "/connect" : {
        "method": "POST",
        "handler": "connect"
    },
    "/disconnect" : {
        "method": "POST",
        "handler": "disconnect"
    },
    "/motor/start" : {
        "method": "POST",
        "handler": "motor_start"
    },
    "/motor/stop" : {
        "method": "POST",
        "handler": "motor_stop"
    },
    "/motor/emergency" : {
        "method": "POST",
        "handler": "motor_emergency"
    },
    "/set_frequency" : {
        "method": "POST",
        "handler": "set_frequency"
    },
    "/data" : {
        "method": "GET",
        "handler": "get_data"
    }
}
