
import pdb

import gymnasium as gym
import copy

import physilogic.envs

from physilogic.planners.base_planner import BasePlanner
from physilogic.utils.py_utils import *

from langtwin.utils.file_utils import *
from langtwin.parser.task_manager import TaskManager

import os
data_path = "./"


def main():
    
    # use os.path.join to make sure the path is correct
    conf = ParamDict({
            "render": True,
            'asset_root': os.path.join(data_path, "data/"),
            "model_json": os.path.join(data_path, "data/mani_skill2_ycb/info_pick_v0.json"),
            "train_scene_json": os.path.join(data_path, "data/mani_skill2_ycb/ycb_scene_pose_and_scale_fruit.json"),
            "test_scene_json": os.path.join(data_path, "data/mani_skill2_ycb/ycb_scene_pose_and_scale_fruit.json"),
            "seen_objects": True,
            "table_urdf": "table_29921/mobility.urdf"})

    # initialize nev
    env = gym.make("Pick_Container-v0",
        conf=conf,
        obs_mode="rgbd",
        # shader_dir = "rt",
        control_mode="pd_ee_delta_pose",
        render_mode="human",
        camera_cfgs=dict(texture_names=("Color", "Position", "Segmentation")))
    
    # initialize planner
    link_names, joint_names = env.init_plan_setting()
    planner = BasePlanner(link_names, joint_names)
    for _ in range(100):
        run(env, planner)

def move_to(env, planner, pose, use_point_cloud=False):
    robot_joint_pose = env.get_robot_joint_pos()
    plan_res = planner.move_to_pose(target_pose=pose, robot_q_pos=robot_joint_pose, use_point_cloud=use_point_cloud)
    if plan_res["plan"] == 1:
        env.follow_path(plan_res["traj"])
    
def find_same_part(a,b):
    set_a = set(a.replace('_', ' ').split())
    set_b = set(b.replace('_', ' ').split())

    # Find common elements
    common_elements = set_a.intersection(set_b)
    return common_elements



def run(env, planner, target_object_name=None, target_position_name=None):
    # initialize scene
    obs, reset_info = env.reset(seed=0) # reset with a seed for random
    _, object_seg = env.get_mesh_and_object_seg(obs["image"]["head_camera"]["Segmentation"])
    env.get_scene_object(object_seg)
    object_task_infos = env.get_or_save_actor_scene_object_and_task_info(obs=obs)
    if target_object_name is None:
        target_object_name = env.scene_json["target_object"]
    if target_position_name is None:
        target_position_name = env.scene_json["target_container"]

    env.setup_robot()
    planner.setup_planner()

    print(target_object_name)

    # load json
    if 'apple' in target_object_name:
        json_dir = "./langtwin/results/apple_bowl/result0.json"
    elif 'pear' in target_object_name:
        json_dir = "./langtwin/results/pear_bowl/result0.json"

    else:
        print("wrong target_object_name")
        return

    task_manager = TaskManager(json_dir)
   

    while not task_manager.finished:
        step = task_manager.next_step()
        do_next_step(env, planner, step)
    
def do_next_step(env, planner, step):
    perception, actionable, constraint, target, controller = step
    print("==="*3)
    print(perception, actionable, constraint, target, controller)

    # 1.  perception
    if 'Detect' in perception:
        target_object_name = env.scene_json["target_object"]
        target_position_name = env.scene_json["target_container"]


    # 2. actionable
    if actionable:
        if find_same_part(actionable[0], target_object_name):
            grasp_pose = env.get_grasp_pose(object_name=target_object_name)

    # 3. constraint
    has_constraint = constraint != []

    # 4. target
    if target:
        if find_same_part(target[0], target_object_name):
            target_pose = env.get_grasp_pose(object_name=target_object_name)
        elif find_same_part(target[0], target_position_name):
            target_pose = env.get_place_pose(container_name=target_position_name)
        else:
            target_pose = None


        outside = ['above', 'outside', 'top']
        inside = ['inside', 'in']
        if any(outword in target[0] for outword in outside):
            target_pose = copy.deepcopy(target_pose)
            target_pose[2] = target_pose[2] + 0.15
            print('move to above')

    
    # 5. controller
    if controller[0] == "Move":
        # move to the target pos
        move_to(env, planner, target_pose, use_point_cloud=has_constraint)

    elif controller[0] == "Grasp":
        pre_grasp_pose = copy.deepcopy(grasp_pose)
        pre_grasp_pose[2] = pre_grasp_pose[2] + 0.15

        move_to(env, planner, pre_grasp_pose, use_point_cloud=has_constraint)
        env.open_gripper()
        move_to(env, planner, grasp_pose, use_point_cloud=has_constraint)
        env.close_gripper()
        move_to(env, planner, pre_grasp_pose, use_point_cloud=has_constraint)
        
    elif controller[0] == "Release":
        env.open_gripper()


if __name__=="__main__":
    main()