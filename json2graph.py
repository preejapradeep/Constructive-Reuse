import json

def get_index(node_id, nodes_dict, id_list):
    node = nodes_dict[node_id]
    node_instance = node.get('Instance')
    node_index = id_list.index(node_id)
    node_index = node_index + 1

    return node_index, node_instance

def get_parent(parent_child_dict, child_index):
    for parent, children in parent_child_dict.items():
        if child_index in children:
            return parent+1
    return None

def find_parent(node_id, node, parent_child_dict, id_list):
    parent_index, parent_instance = get_index(node_id, nodes_dict, id_list)
    
    if 'firstChild' in node:
        first_child_id = node['firstChild']['Id']
        child_index, child_instance = get_index(first_child_id, nodes_dict, id_list)

        if parent_index not in parent_child_dict:
            parent_child_dict[parent_index] = []
        if child_index not in parent_child_dict[parent_index]:
            parent_child_dict[parent_index].append(child_index)
        
        next_child = node['firstChild'].get('Next')
        while next_child is not None:
            next_child_id = next_child['Id']
            child_index, child_instance = get_index(next_child_id, nodes_dict, id_list)
            if child_index not in parent_child_dict[parent_index]:
                parent_child_dict[parent_index].append(child_index)  # Add child index to the parent's list
            next_child = next_child.get('Next')

        return parent_instance


def create_parent_child_dict(nodes_dict, node_list, id_list): 
    parent_child_dict = {}   
    # root = node_list[0] #r 
    parent_child_dict[0] = [1]  # Add root node with index 0

    for i, (instance, node_id) in enumerate(zip(node_list[1:], id_list), start=1):
        node_index = i
        node_id =id_list[node_index-1]
        node = nodes_dict[node_id]
        find_parent(node_id, node, parent_child_dict, id_list)
    
    return parent_child_dict


def print_node_instances(node_id, nodes_dict): 
    node = nodes_dict[node_id]
    node_instance = node['Instance']
    if node_instance is None:
        return None
    node_list.append(node_instance)
    id_list.append(node_id)

    if 'firstChild' in node:
        first_child_id = node['firstChild']['Id']
        print_node_instances(first_child_id, nodes_dict)
        next_child = node['firstChild'].get('Next')

        while next_child is not None:
            next_child_id = next_child['Id']
            print_node_instances(next_child_id, nodes_dict)
            next_child = next_child.get('Next')

    return node_list, id_list


def build_adjacency_list(node_list, parent_child_dict): 
    adjacency_list = [[] for _ in range(len(node_list))]

    for node_index, node_instance in enumerate(node_list):
        if node_index in parent_child_dict:
            children = parent_child_dict[node_index]
            adjacency_list[node_index] = children

    return adjacency_list


# Load case base from json file
with open("BT_complicated.json", "r") as f:
    data = json.load(f)

tree_dict, parent_child_dict = {}, {}

for idx, obj in enumerate(data, start=1):
    trees = obj['data']['trees']
    # Get the 'nodes'
    for tree in trees:
        nodes_dict = {}
        nodes = tree.get('nodes', {})
        nodes_dict.update(nodes)
        # Get the root node
        root_node_id = tree.get('root')    

    node_list = ['r']
    id_list =[]

    # Call the recursive function to print node instances
    node_list, id_list= print_node_instances(root_node_id, nodes_dict)
    parent_child_dict = create_parent_child_dict(nodes_dict, node_list, id_list)
    # print('\nFinal parent_child_dict:', parent_child_dict)

    # Build the adjacency list from the behavior tree
    adjacency_list = build_adjacency_list(node_list, parent_child_dict)

    tree_key = f'tree_{idx}'
    tree_dict[tree_key] = trees
    tree_dict[tree_key] = {
            'tree_json': trees,
            'tree_graph': {
                'nodes': node_list,
                'adj': adjacency_list
            }
    }
    
# Print the dictionary
print('\n',tree_dict)


# Output:
# {'tree_1': {'tree_json': [{'version': '0.1.0', 'scope': 'tree', 'id': '33def3ec-31a8-47c1-856c-7fd724718df2', 'Instance': 'Explanation Experience', 'description': '', 'root': '546f5cee-68b0-4b90-85be-786b9957d03a', 'properties': {}, 'nodes': {'5112868d-f790-4665-ab3e-18a36a857363': {'id': '5112868d-f790-4665-ab3e-18a36a857363', 'Concept': 'Sequence', 'Instance': 'Sequence', 'description': '', 'properties': {}, 'display': {'x': -60, 'y': 168}, 'firstChild': {'Id': '85b9b22e-1b0a-4a9b-81a9-83952d27271a', 'Next': {'Id': '5829d6db-5011-4ad8-846a-ab8452c6be46', 'Next': None}}}, '546f5cee-68b0-4b90-85be-786b9957d03a': {'id': '546f5cee-68b0-4b90-85be-786b9957d03a', 'Concept': 'Priority', 'Instance': 'Priority', 'description': '', 'properties': {}, 'display': {'x': -60, 'y': 84}, 'firstChild': {'Id': '5112868d-f790-4665-ab3e-18a36a857363', 'Next': None}}, '85b9b22e-1b0a-4a9b-81a9-83952d27271a': {'id': '85b9b22e-1b0a-4a9b-81a9-83952d27271a', 'Concept': 'User Question', 'Instance': 'User Question', 'description': '', 'properties': {}, 'display': {'x': -192, 'y': 324}, 'params': {'Question': {'key': 'Question', 'value': 'Why does the system predict category Y for image X?'}}}, '5829d6db-5011-4ad8-846a-ab8452c6be46': {'id': '5829d6db-5011-4ad8-846a-ab8452c6be46', 'Concept': 'Explanation Method', 'Instance': '/Images/IntegratedGradients', 'description': '', 'properties': {}, 'display': {'x': 60, 'y': 324}, 'params': {'output_classes': {'key': 'output_classes', 'value': '[ ]', 'default': '[ ]', 'range': [None, None], 'required': 'false', 'description': 'Array of integers representing the classes to be explained. Defaults to class 1.', 'type': 'text'}, 'top_classes': {'key': 'top_classes', 'value': 1, 'default': 1, 'range': [None, None], 'required': 'false', 'description': "Integer representing the number of classes with the highest prediction probability to be explained. Overrides 'output_classes' if provided.", 'type': 'number'}, 'num_features': {'key': 'num_features', 'value': 10, 'default': 10, 'range': [None, None], 'required': 'false', 'description': 'Integer representing the maximum number of features to be included in the explanation.', 'type': 'number'}, 'png_width': {'key': 'png_width', 'value': 1000, 'default': 1000, 'range': [None, None], 'required': 'false', 'description': 'Width (in pixels) of the png image containing the explanation.', 'type': 'number'}, 'png_height': {'key': 'png_height', 'value': 400, 'default': 400, 'range': [None, None], 'required': 'false', 'description': 'Height (in pixels) of the png image containing the explanation.', 'type': 'number'}}}}, 'display': {'camera_x': 937, 'camera_y': 472, 'camera_z': 1, 'x': -60, 'y': 0}}], 
# 'tree_graph': {'nodes': ['r', 'Priority', 'Sequence', 'User Question', '/Images/IntegratedGradients'],"adj": [[1], [2], [3,4], [], []]}