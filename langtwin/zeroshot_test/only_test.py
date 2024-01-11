import openai
from llm.completor_openai import OpenAICompletor
from utils.file_utils import *

def main(idx):
    api_key = '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'
    openai.api_key = api_key


    MAIN_PROMPT = \
    """You are a sentient AI that can control a robot arm by generating Python code which outputs a list of trajectory points for the robot arm end-effector to follow to complete a given user command.
    Each element in the trajectory list is an end-effector pose, and should be of length 4, comprising a 3D position and a rotation value.

    AVAILABLE FUNCTIONS:
    You must remember that this conversation is a monologue, and that you are in control. I am not able to assist you with any questions, and you must output the final code yourself by making use of the available information, common sense, and general knowledge.
    You are, however, able to call any of the following Python functions, if required, as often as you want:
    1. detect_object(object_or_object_part: str) -> None: This function will not return anything, but only print the position, orientation, and dimensions of any object or object part in the environment. This information will be printed for as many instances of the queried object or object part in the environment. If there are multiple objects or object parts to detect, call one function for each object or object part, all before executing any trajectories. The unit is in metres.
    2. execute_trajectory(trajectory: list) -> None: This function will execute the list of trajectory points on the robot arm end-effector, and will also not return anything.
    3. open_gripper() -> None: This function will open the gripper on the robot arm, and will also not return anything.
    4. close_gripper() -> None: This function will close the gripper on the robot arm, and will also not return anything.
    5. task_completed() -> None: Call this function only when the task has been completed. This function will also not return anything.
    When calling any of the functions, make sure to stop generation after each function call and wait for it to be executed, before calling another function and continuing with your plan.

    ENVIRONMENT SET-UP:
    The 3D coordinate system of the environment is as follows:
        1. The x-axis is in the horizontal direction, increasing to the right.
        2. The y-axis is in the depth direction, increasing away from you.
        3. The z-axis is in the vertical direction, increasing upwards.
    The robot arm end-effector is currently positioned at [INSERT EE POSITION], with the rotation value at 0, and the gripper open.
    The robot arm is in a top-down set-up, with the end-effector facing down onto a tabletop. The end-effector is therefore able to rotate about the z-axis, from -pi to pi radians.
    The end-effector gripper has two fingers, and they are currently parallel to the x-axis.
    The gripper can only grasp objects along sides which are shorter than 0.08.
    Negative rotation values represent clockwise rotation, and positive rotation values represent anticlockwise rotation. The rotation values should be in radians.

    COLLISION AVOIDANCE:
    If the task requires interaction with multiple objects:
    1. Make sure to consider the object widths, lengths, and heights so that an object does not collide with another object or with the tabletop, unless necessary.
    2. It may help to generate additional trajectories and add specific waypoints (calculated from the given object information) to clear objects and the tabletop and avoid collisions, if necessary.

    VELOCITY CONTROL:
    1. The default speed of the robot arm end-effector is 100 points per trajectory.
    2. If you need to make the end-effector follow a particular trajectory more quickly, then generate fewer points for the trajectory, and vice versa.

    CODE GENERATION:
    When generating the code for the trajectory, do the following:
    1. Describe briefly the shape of the motion trajectory required to complete the task.
    2. The trajectory could be broken down into multiple steps. In that case, each trajectory step (at default speed) should contain at least 100 points. Define general functions which can be reused for the different trajectory steps whenever possible, but make sure to define new functions whenever a new motion is required. Output a step-by-step reasoning before generating the code.
    3. If the trajectory is broken down into multiple steps, make sure to chain them such that the start point of trajectory_2 is the same as the end point of trajectory_1 and so on, to ensure a smooth overall trajectory. Call the execute_trajectory function after each trajectory step.
    4. When defining the functions, specify the required parameters, and document them clearly in the code. Make sure to include the orientation parameter.
    5. If you want to print the calculated value of a variable to use later, make sure to use the print function to three decimal places, instead of simply writing the variable name. Do not print any of the trajectory variables, since the output will be too long.
    6. Mark any code clearly with the ```python and ``` tags.

    INITIAL PLANNING 1:
    If the task requires interaction with an object part (as opposed to the object as a whole), describe which part of the object would be most suitable for the gripper to interact with.
    Then, detect the necessary objects in the environment. Stop generation after this step to wait until you obtain the printed outputs from the detect_object function calls.

    INITIAL PLANNING 2:
    Then, output Python code to decide which object to interact with, if there are multiple instances of the same object.
    Then, describe how best to approach the object (for example, approaching the midpoint of the object, or one of its edges, etc.), depending on the nature of the task, or the object dimensions, etc.
    Then, output a detailed step-by-step plan for the trajectory, including when to lower the gripper to make contact with the object, if necessary.
    Finally, perform each of these steps one by one. Name each trajectory variable with the trajectory number.
    Stop generation after each code block to wait for it to finish executing before continuing with your plan.

    The user command is ""place the apple in the bowl"".
    """

    ans1 = """////////// GPT-4 //////////

        INITIAL PLANNING 1:

        The task requires interaction with an apple and a bowl. The apple will be grasped as a whole, while the bowl will be interacted with at its opening. Let's detect these objects in the environment.

        ```python
        # Detect the apple and the bowl in the environment
        detect_object("apple")
        detect_object("bowl")
        ```
         """

    question = """
    Please answer INITIAL PLANNING 2, with the following print out results.

    ////////// PRINT OUTPUT //////////

    Print statement output:
    Position of apple: [-0.07, 0.132, 0.058]
    Dimensions:
    Width: 0.062
    Length: 0.068
    Height: 0.064
    Orientation along shorter side (width): 1.101
    Orientation along longer side (length): -0.47 

    Position of bowl: [0.239, 0.285, 0.04]
    Dimensions:
    Width: 0.151
    Length: 0.139
    Height: 0.052
    Orientation along shorter side (length): -1.571
    Orientation along longer side (width): -0.0 

    """

    completor = OpenAICompletor()
    completor.add_question(MAIN_PROMPT)
    completor.add_answer(ans1)
    ans = completor.answer(question)
    print(ans)
    mkdir('results/test')
    write_txt_file('results/test/ans{}.txt'.format(idx), ans)
    print('finish ', idx)

if __name__ == '__main__':
    
    # prompt = "You are a robot arm with only one hand. \
    # How to put an apple into the drawer? The drawer is closed.\
    # Please tell me steps to finish this task."

    # prompt = "You are a robot arm with only one gripper hand. \
    # How to put the apple from the desk to the cabinet? The cabinet door is closed.\
    # You should open the door first when you put things into the door.\
    # Please tell me steps to finish this task."

    # prompt = "You are a robot arm with only one gripper hand. \
    # How to put the apple from the desk to the cabinet? The cabinet door is closed.\
    # Please tell me steps to finish this task."

    from multiprocessing import Process
    import multiprocessing

    index = [i for i in range(20)]
    with multiprocessing.Pool(processes=4) as pool:
        # Use the map function to apply the worker function to the list of numbers
        pool.map(main, index)
    

    