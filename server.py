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

    @cherrypy.expose
    def api(self):
        input_text = cherrypy.request.body.read().decode()
        response = f'You typed the magical word(s):<br><br> {input_text}'
        return response

cherrypy.tree.mount(Toboggan(), "/", "server.ini")
cherrypy.engine.start()
cherrypy.engine.block()
# Hello tests