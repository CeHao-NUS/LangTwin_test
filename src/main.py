import openai
from utils.file_utils import *
from llm.completor_openai import OpenAICompletor
import time



def main(task, file_name): 
    api_key = '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'
    openai.api_key = api_key

    robot_prompt = read_txt_file('prompts/robots/franka.txt')
    scene_prompt = read_txt_file('prompts/scenes/test_scene.txt')

    all_reasoning = read_txt_file('prompts/tasks/all_reasoning.txt')
    raw_reasoning = read_txt_file('prompts/tasks/raw_reasoning.txt')
    initial_reasoning = read_txt_file('prompts/tasks/initial_reasoning.txt')
    traj_gen = read_txt_file('prompts/tasks/traj_generation.txt')

    API_prompt = read_txt_file('prompts/APIs/articulatoin_model.txt')

    completor = OpenAICompletor()

    prompt = f" \
    Please answer how to finish the robot manipulation task. \n \
    We will show you the descript of robot arm, scene, instruction to follow, task to finish. \n \
    For each block, we use the [xxx Start] and [xxx End] to denote the start and end. \n\
    {robot_prompt} \n \
    {scene_prompt} \n \
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
    
    prompt_all = f" \
        We will should you the Instructoin, Robot, Scene, and Task in the following. They are quote in [xxx Start] and [xxx End] \n \
        Please answer sequentially according to the instructions. \n \
        {all_reasoning} \n \
        {robot_prompt} \n \
        {scene_prompt} \n \
        [Task Start] {task} [Task End] \n \
    "

    t0 = time.time()
    ans = completor.answer(prompt_all)
    # print(ans)

    t1 = time.time()
    print(f"Time1: {t1-t0}")

    write_txt_file(file_name, ans )

    # ans2 = completor.answer(prompt2)
    # # print(ans2)
    # t2 = time.time()
    # print(f"Time2: {t2-t1}")

    # js = convert_str_to_json(ans2)
    # print('js \n', js)

    # write_txt_file(file_name, ans + '\n' + ans2)
    print(file_name)


# import openai  # for OpenAI API calls
# from tenacity import (
#     retry,
#     stop_after_attempt,
#     wait_random_exponential,
# )  # for exponential backoff


# @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
# def completion_with_backoff(**kwargs):
#     return main(**kwargs)


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

    with multiprocessing.Pool(processes=3) as pool:
        # Use the map function to apply the worker function to the list of numbers
        pool.map(try_many_times, tasks)


    # print('Done!')