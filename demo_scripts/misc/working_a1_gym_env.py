"""Wrapper to make the a1 environment suitable for OpenAI gym."""

import sys 
import os 
sys.path.append(os.getcwd())
import gym

from motion_imitation.envs import env_builder
from motion_imitation.robots import a1
from motion_imitation.robots import robot_config


class A1GymEnv(gym.Env):
  """A1 environment that supports the gym interface."""
  metadata = {'render.modes': ['rgb_array']}

  def __init__(self,
               action_limit=(0.75, 0.75, 0.75),
               render=False,
               on_rack=False):
    self._env = env_builder.build_regular_env(
        a1.A1,
        motor_control_mode=robot_config.MotorControlMode.POSITION,
        enable_rendering=render,
        action_limit=action_limit,
        on_rack=on_rack)
    self.observation_space = self._env.observation_space
    self.action_space = self._env.action_space

  def step(self, action):
    return self._env.step(action)

  def reset(self):
    return self._env.reset()

  def close(self):
    self._env.close()

  def render(self, mode):
    return self._env.render(mode)

  def __getattr__(self, attr):
    return getattr(self._env, attr)








# def main():
  
#   # Make a Gym Environment, specifically the locomotion_gym_env.LocomotionGymEnv(gym.Env) 
#   # which is in motion_imitation/envs/locomotion_gym_env.py
#   env = A1GymEnv()
#   # env.set_ground(env._pybullet_client.loadURDF("plane_implicit_modified.urdf"))

#   observation = env.reset()
#   while 1:
#     action, _ = model.predict(observation, deterministic=True)
#     observation, reward, done, info = env.step(action)

#     print("observation,reward,done,action\n", observation,"\n", reward,"\n", done,"\n", action,"\n")
#     time.sleep(0.1)
#     if done:
#         observation = env.reset()
#         print("DONE")
#         break
  
#   return

# if __name__ == '__main__':
#   main()



