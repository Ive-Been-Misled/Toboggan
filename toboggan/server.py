import cherrypy
import textwrap
import game_components as gc

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

# Test Code
g = gc.Game()

print(g.player.current_room.title)
print(g.player.current_room.characters)
moved = g.player.move_to(g.player.current_room.north_room)
print(moved)
print(g.player.current_room.title)

goblin = g.player.current_room.characters['Goblin']
print(goblin.hit_points)
g.player.attack(goblin, 20)
print(goblin.hit_points)
# Test Code

cherrypy.engine.block()
