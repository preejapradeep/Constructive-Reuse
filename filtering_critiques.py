import json
from json2graph import tree_dict

# Tasks: https://docs.google.com/document/d/1d0_sDxLGPb63Z_5pQ42OgtNt0jT2oR-CheRfMaZovH8/edit

# Load the explainer list 
with open('explainer_list.json', 'r') as file:
    explainer_list = json.load(file)

# Load the property fields
with open('explainer_fields.json', 'r') as file:
    explainer_fields = json.load(file)

# Get properties of the explainers from the explainer list
def get_explainer_properties(explainer_list):

    # Create a dictionary to store the properties
    exp_properties_dict = {}

    # Extract the properties for each 'name'
    for entry in explainer_list:
        name = entry['name']
        properties = {
            'technique': entry['technique'],
            'dataset_type': entry['dataset_type'],
            'explanation_type': entry['explanation_type'],
            'concurrentness': entry['concurrentness'],
            'scope': entry['scope'],
            'portability': entry['portability'],   
            'target': entry['target'],
            'presentations': entry['presentations'],
            'computational_complexity': entry['computational_complexity'],
            'ai_methods': entry['ai_methods'],
            'ai_tasks': entry['ai_tasks'],
            "implementation": entry['implementation'],
            # "metadata": entry['metadata']
        }
        exp_properties_dict[name] = properties
    
    # Specify the file path and name
    file_path = "explainer_properties.txt"

    # Open the file in write mode
    with open(file_path, "w") as file:
        # Write the dictionary as a JSON string
        json.dump(exp_properties_dict, file, indent=4)
        
    return exp_properties_dict

# Extract the children from the properties
def extract_children_data(list):
    children_data = {}
    for child in list['children']:
        child_key = child['key']
        child_label = child['label']
        children_data[child_key] = child_label
        children_data.update(extract_children_data(child))
    return children_data

# Get the property values from the explainer fields
def get_properties(explainer_fields):
    children_dict, properties_dict = {}, {}
    for field in explainer_fields:
        field_structure = ['ExplainabilityTechnique', 'Explanation', 'InformationContentEntity', 'AIMethod', 'AITask']
        type_list = explainer_fields[field]
        if field in field_structure:
            children_dict = extract_children_data(type_list)
            properties_dict[field] = children_dict
        else:
            type_mapping = {entry["key"]: entry["label"] for entry in type_list}
            properties_dict[field] = type_mapping

    # Specify the file path and name
    file_path = "properties.txt"

    # Open the file in write mode
    with open(file_path, "w") as file:
        # Write the dictionary as a JSON string
        json.dump(properties_dict, file, indent=4)

    return properties_dict

# List the property values that appear in the explainers in our library
def filter_properties(exp_properties_dict, filter_properties_dict):
    for explainer, properties in exp_properties_dict.items():
        for prop, prop_value in properties.items():
            if isinstance(prop_value, list): # isinstance() check is performed to identify if the value is a list. 
                filter_properties_dict.setdefault(prop, set()).update(prop_value) # update() method is used to add all elements of the list to the set       
            else:
                filter_properties_dict.setdefault(prop, set()).add(prop_value)

    # filter_properties_dict = {
    # prop: list(set(values)) for prop, values in filter_properties_dict.items()
    # }

    # # Specify the file path and name
    # file_path = "filter_properties.txt"

    # # Open the file in write mode
    # with open(file_path, "w") as file:
    #     # Write the dictionary as a JSON string
    #     json.dump(filter_properties_dict, file, indent=4)

    return filter_properties_dict

# Get dataset_type
def get_dataset_type(exp_properties_dict):
    explainer_dataset_type = {}
    explainer_dataset_type = {name: properties['dataset_type'] for name, properties in exp_properties_dict.items() if 'dataset_type' in properties}
    return explainer_dataset_type


# Lists out all the explainers that have the marked property values
def find_explainers_by_propertyvalues(property_values, exp_properties_dict):
    matching_explainers = []
    for explainer, properties in exp_properties_dict.items():
        satisfies_all_properties = True
        for property_value in property_values:
            property_satisfied = False

            for key, value in properties.items():
                if property_value == value:
                    property_satisfied = True
                    break

            if not property_satisfied:
                satisfies_all_properties = False
                break

        if satisfies_all_properties:
            matching_explainers.append(explainer)

    print(matching_explainers)

    return matching_explainers

# Select only the BTs with the explainers that have the property values marked on the form
def BTs_with_critiques(exp_properties_dict):
    bt_graph_dict = {}

    # Read the property values from the user
    property_values_input = input("Enter the property values (comma-separated): ")
    property_values = [value.strip() for value in property_values_input.split(",")]
    # example: http://www.w3id.org/iSeeOnto/explainer#modelClassSpecific, http://www.w3id.org/iSeeOnto/explainer#image

    # Find explainers with the given property value
    matching_explainers = find_explainers_by_propertyvalues(property_values, exp_properties_dict)
    # example: ['/Images/IntegratedGradients', '/Images/NearestNeighbours']

    for index, tree in tree_dict.items():
        if 'tree_graph' in tree:
            graph = tree['tree_graph']
            if 'nodes' in graph:
                nodes = graph['nodes']
                common_explainers = set(nodes) & set(matching_explainers)
                for explainer_name in common_explainers:
                    bt_graph_dict[index] = tree
                    break  # Exit the inner loop after finding a match
   
    return bt_graph_dict



exp_properties_dict = get_explainer_properties(explainer_list)
explainer_dataset_type = get_dataset_type(exp_properties_dict)
# print(explainer_dataset_type)
properties_dict = get_properties(explainer_fields)
filter_properties_dict = filter_properties(exp_properties_dict, filter_properties_dict = {})
bt_graph_dict = BTs_with_critiques(exp_properties_dict)

# Specify the file path and name
file_path = "bt_graph_filtering.txt" # save the results to a text file

# Open the file in write mode
with open(file_path, "w") as file:
    # Write the dictionary as a JSON string
    json.dump(bt_graph_dict, file, indent=4)

