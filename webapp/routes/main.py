sys.path.insert(0, '../')

from controller.ATVWebController import ATVWebController

routes = {
    "/" : {
        "template" : "templates/index.html"
    },
    "/style.css" : {
        "template" : "templates/style.css"
    },

}
