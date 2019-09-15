import cherrypy

class Toboggan:
    @cherrypy.expose
    def index(self):
        return "Hello World! This is Toboggan"

cherrypy.quickstart(Toboggan())
