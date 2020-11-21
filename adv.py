from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

class Stack():
    def __init__(self):
        self.stack = []

    def __str__(self):
        return str(self.stack)

    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

class Graph:
    def __init__(self):
        self.visited = {}
        self.reverse_path = Stack()
        self.reverse_directions = {
            'n': 's',
            'w': 'e',
            'e': 'w',
            's': 'n'
        }

    def add_room(self, room_id):
        self.visited[room_id] = {}

    def add_direction(self, room_id, direction, destination_room=None):
        if destination_room is None:
            destination_room = '?'
        self.visited[room_id][direction] =  destination_room

    def get_unvisited_exits(self, room_id):
        unvisited = []
        exits = self.visited[room_id]

        for direction, exit in exits.items():
            if exit == '?':
                unvisited.append(direction)
        return unvisited


    def dft(self, direction=None, previous_room=None):
        if len(self.visited) == len(room_graph):
            return

        if direction is not None:
            player.travel(direction)
            traversal_path.append(direction)
            self.reverse_path.push(self.reverse_directions[direction])
        current_room = player.current_room

        if current_room.id not in self.visited:
            self.add_room(current_room.id)
            exits = current_room.get_exits()
            for exit in exits:
                self.add_direction(current_room.id, exit)

        if previous_room is not None:
            self.add_direction(previous_room.id,
                               direction,
                               current_room.id)
            self.add_direction(current_room.id,
                               self.reverse_directions[direction],
                               previous_room.id)
        unvisited_exits = self.get_unvisited_exits(current_room.id)

        if len(unvisited_exits) > 0:
            for exit in unvisited_exits:
                self.dft(exit, current_room)
        reverse_step = self.reverse_path.pop()
        player.travel(reverse_step)
        traversal_path.append(reverse_step)

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

world_graph = Graph()
world_graph.dft()

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
