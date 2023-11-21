
import json
import yaml
import os

# ================ JSON ================
# JSON file reader
def read_json_file(file_path):
    with open(file_path, 'r') as json_file:
        return json.load(json_file)

# JSON file writer
def write_json_file(file_path, data):
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file)

# convert string to JSON
def convert_str_to_json(str):
    return json.loads(str)

# ================ txt ================
# txt file reader
def read_txt_file(file_path):
    with open(file_path, 'r') as txt_file:
        return txt_file.read()
    
# txt file writer
def write_txt_file(file_path, data):
    with open(file_path, 'w') as txt_file:
        txt_file.write(data)

# ================ yaml ================
# yaml file reader
def read_yaml_file(file_path):
    with open(file_path, 'r') as yaml_file:
        return yaml.safe_load(yaml_file)
    
# yaml file writer
def write_yaml_file(file_path, data):
    with open(file_path, 'w') as yaml_file:
        yaml.safe_dump(data, yaml_file)

# ================ dir ================
def mkdir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


