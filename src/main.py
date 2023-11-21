import os
from utils.file_utils import *
from llm.completor_openai import OpenAICompletor
import time

TASK_DIR = "./prompts/tasks"
SCENE_DIR = "./prompts/scenes"
ROBOT_DIR = "./prompts/robots"
api_key = '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'

def main(task, file_name): 

    task_dir = os.path.join(TASK_DIR, task + ".yaml")
    config = read_yaml_file(task_dir)
    task_prompt = f"[Task Start] \n {config['Task']} \n [Task End]"

    scene_dir = os.path.join(SCENE_DIR, config['Scene'])
    scene_prompt = read_txt_file(scene_dir)

    robot_dir = os.path.join(ROBOT_DIR, config['Robot'])
    robot_prompt = read_txt_file(robot_dir)
    
    perception_API = read_txt_file('prompts/APIs/perception.txt')
    controller_API = read_txt_file('prompts/APIs/controller.txt')

    completor = OpenAICompletor(api_key)

    # call one by one
    t1 = time.time()
    raw_intruction = read_txt_file('prompts/works/raw_instruction.txt')
    work1 = read_txt_file('prompts/works/work1.txt')
    work2 = read_txt_file('prompts/works/work2.txt')
    work3 = read_txt_file('prompts/works/work3.txt')

    initial_system = f" \
        - We will should you the Instructoin, Robot, Scene, and Task in the following. They are quote in [xxx Start] and [xxx End] \n \
        - Please answer sequentially according to the instructions. \
        {raw_intruction} \n \
        {robot_prompt} \n \
        {scene_prompt} \n \
        {task_prompt} \n \
    "

    completor.add_system(initial_system)

    prompt_work1 = f" \
    - Please finish the following Work 1: \n \
    {work1} \
    "
    ans = completor.answer(prompt_work1)

    prompt_work2 = f" \
    - Please finish the following Work 2: \n \
    {work2} \
    "
    ans = completor.answer(prompt_work2)

    prompt_work3 = f" \
    - The Perception Functions and Controller Functions are as follows: \n \
    {perception_API} \n \
    {controller_API} \n \
    - Please finish the following Work 3: \n \
    {work3} \
    "
    ans = completor.answer(prompt_work3)
    t2 = time.time()
    print(f"Time2: {t2-t1}")

    ans = completor.get_all_answers()
    write_txt_file(file_name, ans)
    print(file_name)



def try_many_times(task, times=1):
    path = os.path.join("./results", task)
    mkdir(path)
    
    for i in range(times):
        file_name = os.path.join(path, "result" + str(i) + ".txt")
        main(task, file_name)

if __name__ == "__main__":

    tasks = os.listdir(TASK_DIR)
    tasks = [task[:-5] for task in tasks]
    try_many_times(tasks[1], times=1)

    # import os
    # from multiprocessing import Process
    # import multiprocessing

    # with multiprocessing.Pool(processes=2) as pool:
        # Use the map function to apply the worker function to the list of numbers
        # pool.map(try_many_times, tasks)

    # try_many_times(task1)

    # print('Done!')