class Move:
  def __init__(self, direction, distance):
    self.direction = direction
    self.distance = distance
class Interact:
  def __init__(self, interaction, thing):
    self.interaction = interaction
    self.thing = thing
class Percieve:
  def __init__(self, location, sense):
    self.location = location
    self.sense = sense
class Attack:
  def __init__(self, target, player):
    self.target = target
    self.player = player
class Speak:
  def __init__(self, target, dialogue):
    self.target = target
    self.dialogue = dialogue
class CheckSelf:
  def __init__(self, player):
    self.player = player
