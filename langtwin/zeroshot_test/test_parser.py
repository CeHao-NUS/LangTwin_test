import re
import ast
import json
    
if __name__ == '__main__':
    
    # string = """
    #     ```
    #     {
    #         'success': False,
    #         'change of goal': [-0.0059, -0.01955, -0.0141, 0, 0, 0, 0],
    #     }
    #     ```
    #     """

    file_path = "/home/msc/cehao/github_space/LangTwin_test/src/results/basic_open_cabinet/result0.txt"
    # read txt from file
    with open(file_path, 'r') as f:
        string = f.read()

    string2 = """
    
    ==== Work 3 ====
    ```
    {
        "Task": "Open the cabinet door by 30 degrees.",
        "Sub tasks":[
            { 
                "Sub task": "Open the cabinet door by 30 degrees.",
                "Steps": [
                    { 
                        "Perception": ["Detect"],
                        "Actionable": ["cabinet door handle"],
                        "Constraint": [],
                        "Target": ["cabinet door handle"],
                        "Controller": ["Move"]
                    },
                    { 
                        "Perception": ["Detect"],
                        "Actionable": ["cabinet door handle"],
                        "Constraint": [],
                        "Target": ["cabinet door handle"],
                        "Controller": ["Grasp"]
                    },
                    { 
                        "Perception": ["Articulation Model"],
                        "Actionable": [],
                        "Constraint": ["cabinet door hinge"],
                        "Target": ["cabinet door open position"],
                        "Controller": ["Move"]
                    },
                    { 
                        "Perception": [],
                        "Actionable": [],
                        "Constraint": [],
                        "Target": [],
                        "Controller": ["Release"]
                    }
                ]
            }
        ]
    }
    ```

    """

    # string = "123"

    pattern = r"```(.*?)```"
    # pattern = r"***(.*?)***"
    # pattern = r"***==== Work 3 ====(.*?)***"
    match = re.search(pattern, string, re.DOTALL)  # re.DOTALL makes '.' match newlines as well

    match_str = match.group(1).strip()
   
    match_dict = ast.literal_eval(match_str)
    # print(match_dict)

    json_string = json.dumps(match_dict, indent=4)
    print(json_string, type(json_string))

    # save match_dict to json file
    # with open('test.json', 'w') as f:
    #     json.dump(match_dict, f)

    # save json_string to json file
    with open('test.json', 'w') as f:
        json.dump(json_string, f)
    

    # load json_string 
    with open('test.json', 'r') as f:
        json_string2 = json.load(f)
    print(json_string2)    
    

    # if match:
    #     content = match.group(1).strip()  # This extracts the content within the backticks and strips any leading/trailing whitespace
    #     print(content)
    # else:
    #     print("No match found")