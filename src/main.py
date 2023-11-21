import openai
from utils.file_utils import *
from llm.completor_openai import OpenAICompletor
import time

def main(task, file_name): 
    api_key = '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'
    openai.api_key = api_key

    robot_prompt = read_txt_file('prompts/robots/franka.txt')
    scene_prompt = read_txt_file('prompts/scenes/test_scene.txt')

    perception_API = read_txt_file('prompts/APIs/perception.txt')
    controller_API = read_txt_file('prompts/APIs/controller.txt')

    completor = OpenAICompletor()


    # call one by one
    t1 = time.time()
    raw_intruction = read_txt_file('prompts/tasks/raw_instruction.txt')
    work1 = read_txt_file('prompts/tasks/work1.txt')
    work2 = read_txt_file('prompts/tasks/work2.txt')
    work3 = read_txt_file('prompts/tasks/work3.txt')

    initial_system = f" \
        - We will should you the Instructoin, Robot, Scene, and Task in the following. They are quote in [xxx Start] and [xxx End] \n \
        - Please answer sequentially according to the instructions. \
        {raw_intruction} \n \
        {robot_prompt} \n \
        {scene_prompt} \n \
        [Task Start] {task} [Task End] \n \
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



def try_many_times(task):
    path = os.path.join("./results", task)
    mkdir(path)
    
    for i in range(5):
        file_name = os.path.join(path, "result" + str(i) + ".txt")
        main(task, file_name)

if __name__ == "__main__":

    tasks = []
    task1 = 'Open the drawer on the desk by 0.2 meters.'
    tasks.append(task1)
    task2 = "Open the cabinet door by 30 degrees."
    tasks.append(task2)


    task3 = "Put the pen from the desk to the closed drawer."
    tasks.append(task3)
    task4 = "Put the apple from the desk to the cabinet."
    tasks.append(task4)
    
    task5 = "Put the pear from the drawer to the cabinet."
    tasks.append(task5)
    task6 = "Put the apple from the drawer to the table."
    tasks.append(task6)

    import os
    from multiprocessing import Process
    import multiprocessing

    with multiprocessing.Pool(processes=2) as pool:
        # Use the map function to apply the worker function to the list of numbers
        pool.map(try_many_times, tasks)


    # print('Done!')