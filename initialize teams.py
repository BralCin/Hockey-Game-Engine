import statistics as st
import pandas as pd

# INITIALIZE TEAM OBJECTS #
# init team_1 players
t1_f = pd.DataFrame({'lw': [90, 85 , 83, 80],
                     'c': [90, 85 , 83, 80],
                     'rw': [90, 85 , 83, 80]})
t1_d = pd.DataFrame({'ld': [90, 85 , 83, 80],
                     'rd': [90, 85 , 83, 80]})
t1_g = [87, 83]
t1_f_overall = t1_f.sum().sum() / 12
t1_d_overall = t1_d.sum().sum() / 6
t1_g_overall = t1_g[0]
# init team_2 players
t2_f = pd.DataFrame({'lw': [90, 85 , 83, 80],
                     'c': [90, 85 , 83, 80],
                     'rw': [90, 85 , 83, 80]})
t2_d = pd.DataFrame({'ld': [90, 85 , 83, 80],
                     'rd': [90, 85 , 83, 80]})
t2_g = [87, 83]
t2_f_overall = t2_f.sum().sum() / 12
t2_d_overall = t2_d.sum().sum() / 6
t2_g_overall = t2_g[0]
# init core weights
forward_weight = .95
defense_weight = .85
goalie_weight = .9
# init core weighted strengths
t1_f_strength = (t1_f_overall * forward_weight)
t1_d_strength = (t1_d_overall * defense_weight)
t1_g_strength = (t1_g_overall * goalie_weight)
t2_f_strength = (t2_f_overall * forward_weight)
t2_d_strength = (t2_d_overall * defense_weight)
t2_g_strength = (t2_g_overall * goalie_weight)
# init teams
team_1 = st.mean([t1_f_strength, t1_d_strength, t1_g_strength])
team_2 = st.mean([t2_f_strength, t2_d_strength, t2_g_strength])
