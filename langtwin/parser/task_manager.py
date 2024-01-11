



'''
Sub tasks: []
Steps: []

"Perception": [],
"Actionable": [],
"Constraint": [],
"Target": [],
"Controller": []

'''
from langtwin.utils.file_utils import *

class TaskManager:

    def __init__(self, file_dir):
        self.file_dir = file_dir
        self.json_string = convert_str_to_json(read_json_file(file_dir))
        self.reset()

    def reset(self):
        self.sub_task = 0
        self.step = 0
        
    def update_index(self):
        self.step += 1
        if self.step == len(self.json_string["Sub tasks"][self.sub_task]["Steps"]):
            self.sub_task += 1
            self.step = 0

    @ property
    def finished(self):
        return self.sub_task == len(self.json_string["Sub tasks"])

    def next_step(self):
        if self.step == 0:
            if self.sub_task == 0:
                print("Now task is: ", self.json_string["Task"])
            print("Now sub task is: ", self.json_string["Sub tasks"][self.sub_task]["Sub task"])

        step = self.json_string["Sub tasks"][self.sub_task]["Steps"][self.step]
        perception = step["Perception"]
        actionable = step["Actionable"]
        constraint = step["Constraint"]
        target = step["Target"]
        controller = step["Controller"]

        self.update_index()
        return perception, actionable, constraint, target, controller