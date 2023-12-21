import json

def read_scriptai_json(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

    path = data['path']
    if all('t' in point for point in path):
        print("Time based file loaded")
        return 'time-based', data
    elif all('v' in point for point in path):
        print("Velocity based file loaded")
        return 'velocity-based', data
    else:
        raise ValueError("Invalid format: JSON file is neither time-based nor velocity-based.")