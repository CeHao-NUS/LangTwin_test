import pdb

import gymnasium as gym
import copy

import physilogic.envs

from physilogic.planners.base_planner import BasePlanner
from physilogic.utils.py_utils import *

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
    for _ in range(10000):
        run(env, planner)

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
    
    # 0. percept
        
    print('target_object_name: ', target_object_name)
    print('target_position_name: ', target_position_name)

    # find the object
    if target_object_name not in env.scene_actors_names:
        return
    

    # set robot to initial pose
    env.setup_robot()
    planner.setup_planner()


    # 1 set constraint
    # observe initial states
    scene_pcd_base, scene_object_mask, scene_pcd_rgb = env.get_scene_point_cloud(obs, multi_view=True)
    planner.update_point_cloud(scene_pcd_base)

    # 2 set actionable
    # move to grasp pose and lift up
    grasp_pose = env.get_grasp_pose(object_name=target_object_name)
    pre_grasp_pose = copy.deepcopy(grasp_pose)
    pre_grasp_pose[2] = pre_grasp_pose[2] + 0.15
    
    # 3. move to 
    move_to(env, planner, pre_grasp_pose, use_point_cloud=True)
    env.open_gripper()
    move_to(env, planner, grasp_pose)
    env.close_gripper()
    move_to(env, planner, pre_grasp_pose, use_point_cloud=True)
    
    # move to final position
    place_pose = env.get_place_pose(container_name=target_position_name)
    pre_place_pose = copy.deepcopy(place_pose)
    pre_place_pose[2] = pre_place_pose[2] + 0.15
    
    move_to(env, planner, pre_place_pose, use_point_cloud=True)
    move_to(env, planner, place_pose)
    env.open_gripper()

    
def move_to(env, planner, pose, use_point_cloud=False):
    robot_joint_pose = env.get_robot_joint_pos()
    plan_res = planner.move_to_pose(target_pose=pose, robot_q_pos=robot_joint_pose, use_point_cloud=use_point_cloud)
    if plan_res["plan"] == 1:
        env.follow_path(plan_res["traj"])
    
    
if __name__=="__main__":
    main()