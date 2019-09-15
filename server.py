import cherrypy
import textwrap

class Toboggan:
    @cherrypy.expose
    def index(self):
        return textwrap.dedent("""\
            <!DOCTYPE html>
            <h1>Hello World!</h1>

            <p>This is Toboggan, a text-based game generator.</p>
            <p>Access the gui by clicking <a href="gui">here</a>.</p>
        """)

cherrypy.tree.mount(Toboggan(), "/", "server.ini")
cherrypy.engine.start()
cherrypy.engine.block()
