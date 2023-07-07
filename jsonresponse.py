import json
#  load and parse a JSON response 
# json_text = json.loads(response.text)
# print(json_text)

# Read the contents of the file
with open('response.text', 'r') as file:
    json_data = file.read()

# Parse the JSON data
json_text = json.loads(json_data)

# Specify the output file path
output_file_path = 'apioutput.json'

# Write the JSON data to the output file
with open(output_file_path, 'w') as file:
    json.dump(json_text, file, indent=4)