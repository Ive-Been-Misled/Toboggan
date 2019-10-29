"""Script for running a local instance of the game"""
import textwrap
import os.path
import webbrowser
import cherrypy

from .calvin_and_hobbes import Calvin


class Server:
    """Simple CherryPy server"""
    # pylint: disable=no-self-use

    def __init__(self):
        self._calvin = Calvin()

    @cherrypy.expose
    def index(self):
        """Create a barebones landing page"""
        return textwrap.dedent("""\
            <!DOCTYPE html>
            <h1>Hello World!</h1>

            <p>This is Toboggan, a text-based game generator.</p>
            <p>Access the gui by clicking <a href="gui">here</a>.</p>
        """)

    @cherrypy.expose
    def api(self):
        """Takes in text input and returns info about game state"""
        input_string = cherrypy.request.body.read().decode()
        return self._calvin.generate_response(input_string)

def main():
    """Launches the CherryPy server and opens a web browser to play the game"""
    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.tree.mount(Server(), "/", config={
        '/':
        {
            'tools.staticdir.root': os.path.abspath(os.path.dirname(__file__))
        },
        '/gui':
        {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': "gui",
            'tools.staticdir.index': 'index.html'
        }
    })
    cherrypy.engine.start()
    webbrowser.open('localhost:8080/gui')
    cherrypy.engine.block()

if __name__ == '__main__':
    main()
