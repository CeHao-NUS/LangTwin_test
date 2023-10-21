import openai
from utils.file_utils import read_txt_file
from llm.completor_openai import OpenAICompletor
import time

if __name__ == "__main__":
    api_key = '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'
    openai.api_key = api_key

    robot_prompt = read_txt_file('prompts/robots/franka.txt')

    initial_reasoning = read_txt_file('prompts/tasks/initial_reasoning.txt')
    traj_gen = read_txt_file('prompts/tasks/traj_generation.txt')

    API_prompt = read_txt_file('prompts/APIs/articulatoin_model.txt')

    task = 'Open the drawer on the table by 0.2 meters.'
    # task = "Open the fridge door by 30 degrees."
    # task = "Put the pen from the table to the closed drawer."
    # task = "Put the apple from the table to the fridge."

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
        Please answer in [Step Start] and [Step End] \n \
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