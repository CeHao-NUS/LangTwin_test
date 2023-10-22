import openai
from llm.completor_openai import OpenAICompletor

if __name__ == '__main__':
    api_key = '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'
    openai.api_key = api_key

    # prompt = "You are a robot arm with only one hand. \
    # How to put an apple into the drawer? The drawer is closed.\
    # Please tell me steps to finish this task."

    # prompt = "You are a robot arm with only one gripper hand. \
    # How to put the apple from the desk to the cabinet? The cabinet door is closed.\
    # You should open the door first when you put things into the door.\
    # Please tell me steps to finish this task."

    prompt = "You are a robot arm with only one gripper hand. \
    How to put the apple from the desk to the cabinet? The cabinet door is closed.\
    Please tell me steps to finish this task."

    

    completor = OpenAICompletor()
    ans = completor.answer(prompt)
    print(ans)