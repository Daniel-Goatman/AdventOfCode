import math
from functools import cache
class Node:
    def __init__(self, label):
        self.connections = {}
        self.label = label

    def __repr__(self):
        return f'Node {(self.label)}'
    
heat_loss_map = """2413432311323
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

#with open('heat_loss_map.txt', 'r') as f:
#    heat_loss_map = f.read()


heat_loss_map = heat_loss_map.splitlines()

start = (0,0)
end = (len(heat_loss_map)-1, len(heat_loss_map[0])-1)
cell_num = len(heat_loss_map)*len(heat_loss_map[0])



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
def check_cell(coords, dir, steps_left, cost):
    y, x = coords
    if not validate_coords(y, x):
        return []

    cells = []
    next_cost = cost + get_cell_cost(y, x)

    # Possible moves
    moves = {
        'right': (0, 1),
        'left': (0, -1),
        'up': (-1, 0),
        'down': (1, 0)
    }

    opposite_directions = {'right': 'left', 'left': 'right', 'up': 'down', 'down': 'up'}

    
    # Continue in same direction if steps are left
    if steps_left > 0:
        dy, dx = moves[dir]
        new_coords = (y + dy, x + dx)
        if validate_coords(*new_coords):
            cells.append((new_coords, dir, steps_left - 1, next_cost))

    # Allow turns, avoiding immediate reversal
    for direction, (dy, dx) in moves.items():
        if direction != dir and direction != opposite_directions[dir]:
            new_coords = (y + dy, x + dx)
            if validate_coords(*new_coords):
                cells.append((new_coords, direction, 3, next_cost))  # Reset steps_left to 3 after turning

    return cells




nodes = {}

nodes[(0,0)] = Node((0,0))


costs = {}
predecessors = {node: None for node in nodes}


costs[nodes[(0,0)].label] = 0

priority_queue = [(nodes[(0,0)], 'right', 3, 0)]
visited_nodes = set()


print(priority_queue[0][2])
while priority_queue:
    priority_queue = sorted(priority_queue, key=lambda x: costs[x[0].label])
    current_node, dir, step, cost = priority_queue.pop(0)

    if current_node.label in visited_nodes:
        continue
    visited_nodes.add(current_node.label)

    current_node.connections = check_cell(current_node.label, dir, step, cost)

    for next_coords, next_dir, next_step, next_cost in current_node.connections:
        if not validate_coords(*next_coords) or next_coords in visited_nodes:
            continue


        if next_cost < costs.get(next_coords, math.inf):

            costs[next_coords] = next_cost
            predecessors[next_coords] = current_node.label
            priority_queue.append((Node(next_coords), next_dir, next_step, next_cost))



print(f'\n\n\n____________________________________________\nAll paths found\n')


print(costs)
print(check_cell((1, 4), 'left', 1, 2))


# Backtracking the shortest path
current_coords = end
shortest_path = [(current_coords, get_cell_cost(*current_coords))]
total_cost = costs[current_coords]

while current_coords != start:
    current_coords = predecessors[current_coords]
    print(current_coords)
    shortest_path.append((current_coords, get_cell_cost(*current_coords)))

shortest_path.reverse()

print(f'Final path: {shortest_path}')
print(f'Total cost: {total_cost}')