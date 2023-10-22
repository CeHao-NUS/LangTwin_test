import openai
from utils.file_utils import *
from llm.completor_openai import OpenAICompletor
import time



def main(task, file_name): 
    api_key = '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'
    openai.api_key = api_key

    robot_prompt = read_txt_file('prompts/robots/franka.txt')

    initial_reasoning = read_txt_file('prompts/tasks/initial_reasoning.txt')
    traj_gen = read_txt_file('prompts/tasks/traj_generation.txt')

    API_prompt = read_txt_file('prompts/APIs/articulatoin_model.txt')

    completor = OpenAICompletor()

    prompt = f" \
    Please answer how to finish the robot manipulation task. \n \
    We will show you the descript of robot arm, instruction to follow, task to finish. \n \
    For each block, we use the [xxx Start] and [xxx End] to denote the start and end. \n\
    {robot_prompt} \n \
    {initial_reasoning} \n \
    Task: {task} \n \
    Please answer in [Step Start] and [Step End] \n \
    "


    prompt2 = f" \
        Give the steps in the initial reasoning, you need to consier more details and convert them as \
            JSON files according to the following instructions. \n \
        {traj_gen} \n \
        {API_prompt} \n \
        This time do NOT use [Step Start] and [Step End] \n \
        "
    t0 = time.time()
    ans = completor.answer(prompt)
    print(ans)

    t1 = time.time()
    print(f"Time1: {t1-t0}")

    ans2 = completor.answer(prompt2)
    print(ans2)
    t2 = time.time()
    print(f"Time2: {t2-t1}")

    js = convert_str_to_json(ans2)
    print('js \n', js)

    write_txt_file(file_name, ans + '\n' + ans2)
    # write_json_file('test.json', js)

def temp(task):
    path = os.path.join("./results", task)
    mkdir(path)
    
    for i in range(5):
        file_name = os.path.join(path, "result" + str(i) + ".txt")
        main(task, file_name)

if __name__ == "__main__":

    task1 = 'Open the drawer on the table by 0.2 meters.'
    task2 = "Open the fridge door by 30 degrees."
    task3 = "Put the pen from the table to the closed drawer."
    task4 = "Put the apple from the table to the fridge."

    tasks = [task1, task2, task3, task4]

    import os
    from multiprocessing import Process
    import multiprocessing

    with multiprocessing.Pool(processes=5) as pool:
        # Use the map function to apply the worker function to the list of numbers
        pool.map(temp, tasks)
