import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# states 121
environment_rows = 11
environment_columns = 11

cumulative_rewards = []
episodes = 1000

q_values = np.zeros((environment_rows, environment_columns, 4))

# ACTIONS : 0 = up, 1 = right, 2 = down, 3 = left
actions = ['up', 'right', 'down', 'left']

# REWARDS
# reward for GOAL = 100
# penalty for hitting wall = -100
# reward for every other state = -1
rewards = np.full((environment_rows, environment_columns), -100.)
rewards[0, 5] = 100. #reward for the GOAL is 100

#define aisle locations (i.e., white squares) for rows 1 through 9
aisles = {} #store legal locations in a dictionary
aisles[1] = [i for i in range(1, 10)]
# aisles[1] = [i for i in range(1,7)]
# aisles[1].append(9)
aisles[2] = [1, 7, 9]
aisles[3] = [i for i in range(1, 8)]
aisles[3].append(9)
aisles[4] = [3, 7]
aisles[5] = [i for i in range(11)]
aisles[6] = [5]
aisles[7] = [i for i in range(1, 10)]
aisles[8] = [3, 7]
aisles[9] = [i for i in range(11)]

#set the rewards for all aisle locations (i.e., white squares)
for row_index in range(1, 10):
  for column_index in aisles[row_index]:
    rewards[row_index, column_index] = -1.

def is_terminal_state(current_row_index:int, current_column_index:int) -> bool:
  """
  Checks if the state is terminal or not i.e either GOAL or wall
  """
  if rewards[current_row_index, current_column_index] == -1.:
    return False
  else:
    return True


def get_starting_location() -> (int,int):
  """
  Generate a random legal/non-terminal starting location
  """
  # get a random row and column index from the state pool
  current_row_index = np.random.randint(environment_rows)
  current_column_index = np.random.randint(environment_columns)
  #continue choosing random row and column indexes until a non-terminal state is identified
  #(i.e., until the chosen state is a 'white square')
  while is_terminal_state(current_row_index, current_column_index):
    current_row_index = np.random.randint(environment_rows)
    current_column_index = np.random.randint(environment_columns)
  return current_row_index, current_column_index


def get_next_action(current_row_index:int, current_column_index:int, epsilon:float) -> float | int:
  """
  Gets the next actions to take from the current row and col 
  if a randomly chosen value between 0 and 1 is less than epsilon,
  then choose the most promising value from the Q-table for this state.
  """
  # EXPLOITATION
  if np.random.random() < epsilon:
    return np.argmax(q_values[current_row_index, current_column_index])
  # EXPLORATION
  else: #choose a random action
    return np.random.randint(4)

def get_next_location(current_row_index:int, current_column_index:int, action_index:int) -> (int,int):
  new_row_index = current_row_index
  new_column_index = current_column_index
  if actions[action_index] == 'up' and current_row_index > 0:
    new_row_index -= 1
  elif actions[action_index] == 'right' and current_column_index < environment_columns - 1:
    new_column_index += 1
  elif actions[action_index] == 'down' and current_row_index < environment_rows - 1:
    new_row_index += 1
  elif actions[action_index] == 'left' and current_column_index > 0:
    new_column_index -= 1
  return new_row_index, new_column_index


def get_shortest_path(start_row_index:int, start_column_index:int):
  #return immediately if this is an invalid starting location
  if is_terminal_state(start_row_index, start_column_index):
    return []
  else: #if this is a 'legal' starting location
    current_row_index, current_column_index = start_row_index, start_column_index
    shortest_path = []
    shortest_path.append([current_row_index, current_column_index])
    #continue moving along the path until we reach the goal (i.e., the item packaging location)
    while not is_terminal_state(current_row_index, current_column_index):
      #get the best action to take
      action_index = get_next_action(current_row_index, current_column_index, 1.)
      #move to the next location on the path, and add the new location to the list
      current_row_index, current_column_index = get_next_location(current_row_index, current_column_index, action_index)
      if [current_row_index, current_column_index] in shortest_path:
        return "BOUNDED"
      
      shortest_path.append([current_row_index, current_column_index])
    
    return shortest_path
  

def train(max_episodes:int = episodes):
  #define training parameters
  epsilon = 0.9
  discount_factor = 0.9
  learning_rate = 0.9

  for episode in range(max_episodes):
    row_index, column_index = get_starting_location()
    
    while not is_terminal_state(row_index, column_index):
      action_index = get_next_action(row_index, column_index, epsilon)

      old_row_index, old_column_index = row_index, column_index 
      row_index, column_index = get_next_location(row_index, column_index, action_index)

      reward = rewards[row_index, column_index]
      old_q_value = q_values[old_row_index, old_column_index, action_index]
      temporal_difference = reward + (discount_factor * np.max(q_values[row_index, column_index])) - old_q_value

      new_q_value = old_q_value + (learning_rate * temporal_difference)
      q_values[old_row_index, old_column_index, action_index] = new_q_value

    episode_reward = np.sum(q_values)
    cumulative_rewards.append(episode_reward)
  print('Training complete!')

# #display a few shortest paths
# print(get_shortest_path(3, 9)) #starting at row 3, column 9
# print(get_shortest_path(5, 0)) #starting at row 5, column 0
# print(get_shortest_path(9, 5)) #starting at row 9, column 5

#display an example of reversed shortest path
# path = get_shortest_path(5, 2) #go to row 5, column 2
# path.reverse()
# print(path)


# FOR GUI ===============================================================
def get_path(a:int,b:int) -> list | str:
    """
    returns either [], "BOUNDED" or [[x1,y1],[x2,y2]...]
    """
    li = get_shortest_path(a,b)
    return li

def get_grid() -> list[list]:
  """
  returns the environment grid
  0 if aisle i.e. white squares
  1 if wall i.e illegal/terminal state
  2 if GOAL
  """
  grid = []
  for rows in rewards:
    x=[]
    for cols in rows:
      if(cols == -100):
        x.append(1)
      elif(cols == -1):
        x.append(0)
      else:
        x.append(2)
    grid.append(x)
  return grid


#  TESTING--------------------------------------------------------------

train()
print(get_shortest_path(3, 9))
plt.figure(figsize=(13, 7))
sns.lineplot(x=range(episodes), y=cumulative_rewards)
plt.title('Learning Curve for Q-learning')
plt.xlabel('Episode')
plt.ylabel('Cumulative Reward')
plt.show()

# episodes = 2000

# cumulative_rewards = []  # List to store cumulative rewards for each episode

# def train_simulated_anealling(epsilon_initial=0.9, epsilon_min=0.1, epsilon_decay=0.001, max_episodes=episodes):
#   discount_factor = 0.9
#   learning_rate = 0.9

#   for episode in range(max_episodes):
#     row_index, column_index = get_starting_location()
#     epsilon = epsilon_initial  # Initialize epsilon for this episode
#     episode_reward = 0  # Initialize cumulative reward for this episode

#     while not is_terminal_state(row_index, column_index):
#         action_index = get_next_action(row_index, column_index, epsilon)

#         old_row_index, old_column_index = row_index, column_index
#         row_index, column_index = get_next_location(row_index, column_index, action_index)

#         reward = rewards[row_index, column_index]
#         # episode_reward += reward  # Accumulate the reward for this episode

#         old_q_value = q_values[old_row_index, old_column_index, action_index]
#         temporal_difference = reward + (discount_factor * np.max(q_values[row_index, column_index])) - old_q_value

#         new_q_value = old_q_value + (learning_rate * temporal_difference)
#         q_values[old_row_index, old_column_index, action_index] = new_q_value

#         # Simulated Annealing: Decrease epsilon over time
#         # epsilon = max(epsilon * epsilon_decay, epsilon_min)

#     episode_reward = np.sum(q_values)
#     cumulative_rewards.append(episode_reward)

# train_simulated_anealling()
# print(get_shortest_path(3, 9)) #starting at row 3, column 9
# # print(q_values)
# plt.figure(figsize=(13, 7))
# sns.lineplot(x=range(episodes), y=cumulative_rewards)
# plt.title('Learning Curve for Q-learning')
# plt.xlabel('Episode')
# plt.ylabel('Cumulative Reward')
# plt.show()