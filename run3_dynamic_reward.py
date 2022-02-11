import os
import inspect
import sys 
import os
import datetime
import numpy as np
import math 

from stable_baselines.common.policies import MlpPolicy
from stable_baselines import PPO1
from motion_imitation.robots import robot_config

import importlib
import dynamic_reward


# global_policy_kwargs = {
#     "net_arch": [{"pi": [512, 256],"vf": [512, 256]}],
#     "act_fun": tf.nn.relu
# }

def make_datetime_string():
  return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def test(input_file="output/latest.zip", deterministic=True):
  enable_rendering = True
  reload_model = True
  env = dynamic_reward.build_laikago_env( motor_control_mode = robot_config.MotorControlMode.POSITION, enable_rendering=enable_rendering)
  model = PPO1(MlpPolicy, env, verbose=1, timesteps_per_actorbatch=2048, clip_param=0.2, entcoeff=0.0, optim_epochs=5,
                  optim_stepsize=3e-4, optim_batchsize=256, gamma=0.99, lam=0.95, schedule='linear') # 'linear') # tensorboard_log="tensorboard_log"

  if input_file:
      model.load_parameters(input_file)
  observation = env.reset()
  i = 0
  while True:
    i += 1
    if reload_model and input_file and i % 100 == 0:
      print("\n\n\nRELOADING MODEL\n\n\n")
      importlib.reload(dynamic_reward)
      model.load_parameters(input_file)
    action, _ = model.predict(observation, deterministic=deterministic)
    observation, r, done, info = env.step(action)
    # print(observation)
    if done:
        observation = env.reset()


def train(input_file=None, output_dir="output/"):
  # reloads python file periodically so you can update parameters during training dynamically.
  # the policy schedule is kind of meaningless since a linear schedule reduces the learning rate down to zero 
  # during number of total timesteps which is quite low in this script.  It might make sense to change the 
  # schedule to a 'constant' learning rate.  Alternatively a newer version of this script might allow for dynamic 
  # changing of all of these parameters during training as well.  It would be cool to increase and decrease the 
  # learning rate dynamically.

  env = dynamic_reward.build_laikago_env( motor_control_mode = robot_config.MotorControlMode.POSITION, enable_rendering=False)
  # parameters taken from stable baselinese PPO1 run_robotics.py
  model = PPO1(MlpPolicy, env, verbose=1, timesteps_per_actorbatch=2048, clip_param=0.2, entcoeff=0.0, optim_epochs=5,
                  optim_stepsize=3e-4, optim_batchsize=256, gamma=0.99, lam=0.95, schedule='linear', 
                  tensorboard_log=output_dir + "tensorboard_log")
  if input_file:
      model.load_parameters(input_file)

  for i in range(10000):
      print("\n\n\nRELOADING REWARD\n\n\n")
      importlib.reload(dynamic_reward)
      # dynamic_reward.randomize_gravity(env)
      model.learn(total_timesteps=2048) # , callback=None, log_interval=100, tb_log_name="PPO1", reset_num_timesteps=True)
      print(output_dir + str(i))
      model.save( output_dir + str(i) )
      model.save( output_dir + "latest" )
      model.save("output/latest")


def run():
  if len(sys.argv) != 2:
    quit()
  
  # Train
  if sys.argv[1] == "--train":

      input_file = None # "output/20211013_123037_added_roll_reward/_92160_steps.zip"
      output_dir = "output/20211013_2256_from_scratch_again/" 
      os.mkdir( output_dir )
      train(input_file=input_file, output_dir=output_dir)


  # Demo
  else:
      input_file = sys.argv[1]
      # input_file = "output/latest.zip"
      deterministic=True
      test(input_file=input_file, deterministic=deterministic)


if __name__ == '__main__':
  run()











