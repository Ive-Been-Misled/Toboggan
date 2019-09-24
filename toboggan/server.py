import cherrypy
import textwrap
import os.path
import webbrowser
from .game_components import Game


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

def main():
    cherrypy.tree.mount(Toboggan(), "/", config={
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
