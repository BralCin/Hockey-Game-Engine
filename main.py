# IMPORTS #
import numpy as np
import statistics as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# INITIALIZE TEAM OBJECTS #
# init team_1 players
t1_f = pd.DataFrame({'lw': [93, 90, 87, 85],
                      'c': [93, 90, 87, 85],
                     'rw': [93, 90, 87, 85]})
t1_d = pd.DataFrame({'ld': [93, 90, 87, 85],
                     'rd': [93, 90, 87, 85]})
t1_g = [93, 83]
t1_f_overall = t1_f.sum().sum() / 12
t1_d_overall = t1_d.sum().sum() / 6
t1_g_overall = t1_g[0]
# init team_2 players
t2_f = pd.DataFrame({'lw': [85, 83, 80, 77],
                      'c': [85, 83, 80, 77],
                     'rw': [85, 83, 80, 77]})
t2_d = pd.DataFrame({'ld': [85, 83, 80, 77],
                     'rd': [85, 83, 80, 77]})
t2_g = [83, 80]
t2_f_overall = t2_f.sum().sum() / 12
t2_d_overall = t2_d.sum().sum() / 6
t2_g_overall = t2_g[0]
# init core weights
forward_weight = .875
defense_weight = .825
goalie_weight = .90
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
print(team_1, team_2)


# DEFINE GAME ENGINE #
def game_engine(t1, t2):

    # init gamescore
    def score_generator(t1, t2):
        gamescores = np.random.normal(loc=.25, scale=.21, size=(1, 2))
        gamescores = gamescores.tolist()
        t1_gamescore = t1 * gamescores[0][0]
        t2_gamescore = t2 * gamescores[0][1]
        # init scoring variables
        scoring_rate = 7.4  # lower for a higher score
        t1_score = round(t1_gamescore / scoring_rate)
        t2_score = round(t2_gamescore / scoring_rate)
        team_scores = [t1_score, t2_score]
        return team_scores

    # init score values
    team_scores = score_generator(t1, t2)
    # fumble calculation
    fumble = []
    for j in range(2):
        if team_scores[j] < 0:
            fumble.append(abs(team_scores[j]))
            team_scores[j] = 0
        else:
            fumble.append(0)
    if fumble[0] + fumble[1] != 0:
        fumble[0] += team_scores[1]
        fumble[1] += team_scores[0]
    final_scores = [team_scores[0], team_scores[1]]
    # overtime
    ot = False
    if final_scores[0] == final_scores[1]:
        tie_breaker = score_generator(t1, t2)
        if tie_breaker[0] > tie_breaker[1]:
            final_scores[0] += 1
        elif tie_breaker[0] < tie_breaker[1]:
            final_scores[1] += 1
        ot = True
    return final_scores, ot


# TEST #
def simulation_test(t_1, t_2, n):
    test_scores = []
    t1_wins = 0
    t2_wins = 0
    ties = 0
    ot_games = 0
    for i in range(n):
        score, ot = game_engine(t_1, t_2)
        goals = score[0] + score[1]
        test_scores.append(goals)
        if score[0] > score[1]:
            t1_wins += 1
        elif score[0] < score[1]:
            t2_wins += 1
        else:
            ties += 1
        if ot == True:
            ot_games += 1
    # score counts
    counter = Counter(test_scores)
    goals = list(counter.keys())
    counts = list(counter.values())
    # create dataframe
    df = pd.DataFrame([goals, counts])
    df = df.T
    print(df.value_counts().sort_index().tail(5))
    # average goals
    total_goals = 0
    for i in range(len(goals)):
        total_goals += (goals[i] * counts[i])
    average_goals = total_goals / 100000
    print(average_goals)
    # print win totals
    print('t1_wins: ' + str(t1_wins))
    print('t2_wins: ' + str(t2_wins))
    print('ot_games: ' + str(ot_games))
    print('ties: ' + str(ties))
    print('t1_win_share: ' + str(round((t1_wins / (n - ties)), 2)))
    # plot results
    plt.bar(goals, counts)
    plt.xticks(range(20))
    plt.axvline(average_goals, linestyle='dotted')
    plt.show()


simulation_test(team_1, team_2, 100000)
