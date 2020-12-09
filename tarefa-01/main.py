import random
import copy


class Node():
    def __init__(self, state, prev_node, prev_action, g):
        self.state = state
        self.prev_node = prev_node
        self.prev_action = prev_action
        self.g = g
        self.h = self._heuristic()

    def _heuristic(self):
        distance_sum = 0
        for value in range(1, 9):
            value_index = self.state.index(value)
            distance_i = abs((value_index // 3) - ((value - 1) // 3))
            distance_j = abs((value_index % 3) - ((value - 1) % 3))
            distance_sum += distance_i + distance_j
        return distance_sum

    def get_f(self):
        return self.g + self.h

    def is_final(self):
        return self.state == [1, 2, 3, 4, 5, 6, 7, 8, 0]

    def unroll(self):
        if self.prev_node == None:
            return [(self.state, None)]
        return self.prev_node.unroll() + [(self.state, self.prev_action)]

    def get_neighbors_nodes(self):
        neighbors = []
        blank_index = self.state.index(0)
        # UP
        if blank_index - 3 >= 0:
            new_state = copy.deepcopy(self.state)
            new_state[blank_index] = self.state[blank_index - 3]
            new_state[blank_index - 3] = self.state[blank_index]
            neighbors.append(
                Node(state=new_state, prev_node=self, prev_action="UP", g=self.g + 1))
        # DOWN
        if blank_index + 3 < 9:
            new_state = copy.deepcopy(self.state)
            new_state[blank_index] = self.state[blank_index + 3]
            new_state[blank_index + 3] = self.state[blank_index]
            neighbors.append(
                Node(state=new_state, prev_node=self, prev_action="DOWN", g=self.g + 1))
        # LEFT
        if blank_index % 3 > 0:
            new_state = copy.deepcopy(self.state)
            new_state[blank_index] = self.state[blank_index - 1]
            new_state[blank_index - 1] = self.state[blank_index]
            neighbors.append(
                Node(state=new_state, prev_node=self, prev_action="LEFT", g=self.g + 1))
        # RIGHT
        if blank_index % 3 < 2:
            new_state = copy.deepcopy(self.state)
            new_state[blank_index] = self.state[blank_index + 1]
            new_state[blank_index + 1] = self.state[blank_index]
            neighbors.append(
                Node(state=new_state, prev_node=self, prev_action="RIGHT", g=self.g + 1))

        return neighbors


def is_best_path_to_node(node, open_list, closed_list):
    for node_in_list in open_list:
        if node.state == node_in_list.state:
            if node_in_list.get_f() <= node.get_f():
                return False

    for node_in_list in closed_list:
        if node.state == node_in_list.state:
            if node_in_list.get_f() <= node.get_f():
                return False

    return True


def search_a_star(initial_state):
    open_list = [Node(state=initial_state, prev_node=None,
                      prev_action=None, g=0)]
    closed_list = []
    step = 0

    while len(open_list):
        step += 1
        open_list.sort(key=Node.get_f)
        # Print open list

        str1 =  ""
        str2 =  ""
        str3 =  ""
        str4 =  ""
        str5 =  ""
        str6 =  ""
        str7 =  ""
        print("===============================================================")
        print(f"Step = {step}")
        print("Open List")
        for node in open_list:
            str1 +=  (str(node.state[0:3]) + "               ")[:15]
            str2 +=  (str(node.state[3:6]) + "               ")[:15]
            str3 +=  (str(node.state[6:9]) + "               ")[:15]
            str4 +=  (f"g -> {node.g}" + "               ")[:15]
            str5 +=  (f"h -> {node.h}" + "               ")[:15]
            str6 +=  (f"f -> {node.get_f()}" + "               ")[:15]
            str7 +=  (f"{node.prev_action}" + "               ")[:15]

        print(str1)
        print(str2)
        print(str3)
        print(str4)
        print(str5)
        print(str6)
        print(str7)
        
        current_node = open_list.pop(0)
        closed_list.append(current_node)

        # print("Current Node")
        # print(current_node.state[0:3])
        # print(current_node.state[3:6])
        # print(current_node.state[6:9])
        # print(f"g -> {current_node.g}")
        # print(f"h -> {current_node.h}")
        # print(f"f -> {current_node.get_f()}")
        # print(f"prev_action -> {current_node.prev_action}")
        
        if current_node.is_final():
            return current_node.unroll()
        
        for neighbor in current_node.get_neighbors_nodes():
            if is_best_path_to_node(neighbor, open_list, closed_list):
                open_list.append(neighbor)



    return None


def is_state_solvable(state):
    # final state as invalid initial state
    if state == [1, 2, 3, 4, 5, 6, 7, 8, 0]:
        return False

    n_inversions = 0
    for i in range(len(state)):
        if state[i] == 0:
            continue
        for j in range(i+1, len(state)):
            if state[j] == 0:
                continue
            if state[i] > state[j]:
                n_inversions += 1

    return n_inversions % 2 == 0


def get_initial_state():
    state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    while not is_state_solvable(state):
        random.shuffle(state)
    return state
