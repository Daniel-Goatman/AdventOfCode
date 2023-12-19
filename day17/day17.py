import math
import time
import heapq
from functools import cache
class Node:
    def __init__(self, label):
        self.connections = {}
        self.label = label

    def __repr__(self):
        return f'Node {(self.label)}'
    
heat_loss_map = """
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""


ultra_mode = True

# my path = 21 to 0,5
# their path=24


#3+2+1+5+3+4+3
with open('heat_loss_map.txt', 'r') as f:
    heat_loss_map = f.read()


heat_loss_map = heat_loss_map.splitlines()

start = (0,0)
end = (len(heat_loss_map)-1, len(heat_loss_map[0])-1)
cell_num = len(heat_loss_map)*len(heat_loss_map[0])

print(end)

@cache
def validate_coords(y, x):
    #print(f'recieved {y, x}')
    if not 0<=y<len(heat_loss_map) or not 0 <=x < len(heat_loss_map[0]):
        return False
    return True

@cache
def get_cell_cost(y, x):

    return int(heat_loss_map[y][x])

@cache
def check_cell(coords, dir, steps_left, cost, ultra):
    y, x = coords

    cells = []


    # Possible moves
    moves = {
        'right': (0, 1),
        'left': (0, -1),
        'up': (-1, 0),
        'down': (1, 0)
    }

    opposite_directions = {'right': 'left', 'left': 'right', 'up': 'down', 'down': 'up'}

    if not ultra:
        # Continue in same direction if steps are left
        if steps_left > 0:

            dy, dx = moves[dir]
            new_coords = (y + dy, x + dx)
            if validate_coords(*new_coords):
                cells.append((new_coords, dir, steps_left - 1, cost + get_cell_cost(*new_coords)))


        # Allow turns, avoiding immediate reversal
        for direction, (dy, dx) in moves.items():
            new_coords = (y + dy, x + dx)
            if direction != dir and direction != opposite_directions[dir] and validate_coords(*new_coords):

                cells.append((new_coords, direction, 2, cost + get_cell_cost(*new_coords)))  # Reset steps_left to 3 after turning

    else:
        # Continue in same direction if steps are left
        if steps_left > 0:

            dy, dx = moves[dir]
            new_coords = (y + dy, x + dx)
            if validate_coords(*new_coords):
                cells.append((new_coords, dir, steps_left - 1, cost + get_cell_cost(*new_coords)))


        if steps_left < 7: #can only turn after 4 moves
            # Allow turns, avoiding immediate reversal
            for direction, (dy, dx) in moves.items():
                new_coords = (y + dy, x + dx)

                if direction != dir and direction != opposite_directions[dir] and validate_coords(*new_coords):

                    cells.append((new_coords, direction, 9, cost + get_cell_cost(*new_coords)))  # Reset steps_left to 3 after turning

    return cells



nodes = {}

nodes[start] = Node(start)


costs = {}
predecessors = {node: None for node in nodes}


costs[(nodes[start].label, 'right', 9)] = 0

priority_queue = []
heapq.heappush(priority_queue, (0, nodes[start].label, 'right', 9)) 

visited_nodes = set()

start_time = time.monotonic()
while priority_queue:


    cost, node_label, dir, step = heapq.heappop(priority_queue)  # Modify this line
    current_node = nodes[node_label]  # Get the node from the label    #print(priority_queue)

    #print(cost, current_node)
    if (current_node.label, dir, step) in visited_nodes:
        continue
    visited_nodes.add((current_node.label, dir, step))

    current_node.connections = check_cell(current_node.label, dir, step, cost, ultra_mode)
    
    for next_coords, next_dir, next_step, next_cost in current_node.connections:
        if not validate_coords(*next_coords) or (next_coords, next_dir, next_step) in visited_nodes:
            continue
        
        if next_cost < costs.get((next_coords, next_dir, next_step), math.inf):
            if ultra_mode and next_coords == end:
                if not next_step < 7:
                    #print(f'Failed to pass step check for end')
                    continue

            if not next_coords in nodes:
                nodes[next_coords] = Node(next_coords)

            costs[(next_coords, next_dir, next_step)] = next_cost
            predecessors[(next_coords, next_dir, next_step)] = (current_node.label, dir, step)
            heapq.heappush(priority_queue, (next_cost, next_coords, next_dir, next_step))  # Modify this line


end_time = time.monotonic()


print(f'\n\n\n____________________________________________\nAll paths found in {end_time-start_time} seconds.\n')

#print(costs)

#print(predecessors)

#print(f"{(1,2), 'right', 2, 4} has connections: {check_cell((1,2), 'right', 2, 4)}")
#print(get_cell_cost(*end))
#print(check_cell((1, 4), 'left', 1, 0))

# Backtracking the shortest path

current_node = min([i for i in costs if i[0] == end], key=lambda x: costs[x])
#print(current_node)
shortest_path = [(current_node, get_cell_cost(*current_node[0]))]
total_cost = costs[current_node]
#print(f'Starting cost: {total_cost}')
while current_node[0] != start:
    current_node = predecessors[current_node]
    #print(current_node)
    shortest_path.append((current_node, get_cell_cost(*current_node[0])))

shortest_path.reverse()

print(f'Final path: {shortest_path}')
print(f'Total cost: {total_cost}')