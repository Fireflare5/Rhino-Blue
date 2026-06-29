import pandas as pd
import numpy as np
from tqdm import trange
import os

os.system("Clear")

Data = []
n_doors = 4
for i in trange(100000, ncols=100):
    possible_values = np.arange(n_doors)
    winning_door = np.random.choice(possible_values)
    initial_choice = np.random.choice(possible_values)
    
    possible_values = np.delete(possible_values, np.where(possible_values == initial_choice))
    
    if initial_choice == winning_door:
        closed_door = np.random.choice(possible_values)
    else:
        closed_door = winning_door
    
    swap_or_stay = np.random.choice(["swap", "stay"])
    
    
    if swap_or_stay == "swap":
        final_choice = closed_door
    else:
        final_choice = initial_choice

    d = {"winning_door":winning_door, "initial_choice":initial_choice, "final_choice":final_choice, "closed_door":closed_door, "Win":(final_choice==winning_door), "swap_or_stay":swap_or_stay}
    Data.append(d)

df = pd.DataFrame(Data)

df_swap = df[ df.swap_or_stay == "swap" ]
df_stay = df[ df.swap_or_stay == "stay" ]

swap_win = len(df_swap[ df_swap.final_choice == df_swap.winning_door ]) / len(df_swap)
stay_win = len(df_stay[ df_stay.final_choice == df_stay.winning_door ]) / len(df_stay)
ran_win = len(df[ df.final_choice == df.winning_door ]) / len(df)
df.to_csv("/Users/829005/Desktop/Monty Hall.csv")
print("The number of doors is {}".format(n_doors))
print("Random win percent: {:.2%}".format(ran_win))
print("Swap win percent: {:.2%}".format(swap_win))
print("Stay win percent: {:.2%}".format(stay_win))
