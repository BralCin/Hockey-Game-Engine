# IMPORTS #
import numpy as np
import statistics as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# INITIALIZE TEAM OBJECTS #
# init team_1 players
# forwards
t1_f_lw = [90, 87, 85, 83]
t1_f_c = [90, 87, 85, 83]
t1_f_rw = [90, 87, 85, 83]
t1_f = pd.DataFrame({'lw': t1_f_lw, 'c': t1_f_c, 'rw': t1_f_rw})
# defense
t1_d_ld = [90, 85, 83]
t1_d_rd = [90, 85, 83]
t1_d = pd.DataFrame({'ld': t1_d_ld, 'rd': t1_d_rd})
# goalies
t1_g = [90, 83]
# init team_1 overalls
t1_f_overall = (t1_f.loc[0].mean() * .325) + (t1_f.loc[1].mean() * .275) \
               + (t1_f.loc[2].mean() * .2) + (t1_f.loc[3].mean() * .175)
t1_d_overall = (t1_d.loc[0].mean() * .395) + (t1_d.loc[1].mean() * .335) + (t1_d.loc[2].mean() * .27)
t1_g_overall = t1_g[0]

# init team_2 players
# forwards
t2_f_lw = [90, 87, 85, 83]
t2_f_c = [90, 87, 85, 83]
t2_f_rw = [90, 87, 85, 83]
t2_f = pd.DataFrame({'lw': t2_f_lw, 'c': t2_f_c, 'rw': t2_f_rw})
# defense
t2_d_ld = [90, 85, 83]
t2_d_rd = [90, 85, 83]
t2_d = pd.DataFrame({'ld': t2_d_ld, 'rd': t2_d_rd})
# goalies
t2_g = [90, 83]
# init team_2 overalls
t2_f_overall = (t2_f.loc[0].mean() * .325) + (t2_f.loc[1].mean() * .275) \
               + (t2_f.loc[2].mean() * .2) + (t2_f.loc[3].mean() * .175)
t2_d_overall = (t2_d.loc[0].mean() * .395) + (t2_d.loc[1].mean() * .335) + (t2_d.loc[2].mean() * .27)
t2_g_overall = t2_g[0]

# init core weights
forward_weight = .985
defense_weight = .96
goalie_weight = 1
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
def game_engine(t1=team_1, t2=team_2):

    # init gamescore    ===    x=loc, y=scale, scoring_rate(lower for higher scoring)
    def score_generator(t_1, t_2, x=.168, y=.125, avg_team=85, scoring_rate=6):  #
        # generate gamescores
        t_1_dif = float((t_1 - avg_team) / 100)
        t_1_gamescore = np.random.normal(loc=(x+t_1_dif), scale=y) * 100
        t_2_dif = float((t_2 - avg_team) / 100)
        t_2_gamescore = np.random.normal(loc=(x+t_2_dif), scale=y) * 100
        # init scoring variables
        t_1_score = round(t_1_gamescore / scoring_rate)
        t_2_score = round(t_2_gamescore / scoring_rate)
        t_scores = [t_1_score, t_2_score]
        return t_scores

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
        tie_breaker = score_generator(t1, t2, x=0, y=.05)
        if tie_breaker[0] > tie_breaker[1]:
            final_scores[0] += 1
        elif tie_breaker[0] < tie_breaker[1]:
            final_scores[1] += 1
        ot = True
    return final_scores, ot


# TEST #
def simulation_test(t1=team_1, t2=team_2, n=100000):
    # init variables
    test_scores = []
    t1_wins = 0
    t2_wins = 0
    ties = 0
    ot_games = 0
    # calculate win totals
    for i in range(n):
        score, ot = game_engine(t1, t2)
        goals = score[0] + score[1]
        test_scores.append(goals)
        if score[0] > score[1]:
            t1_wins += 1
        elif score[0] < score[1]:
            t2_wins += 1
        else:
            ties += 1
        if ot:
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
    print('goals_per_game: ' + str(average_goals))
    # print win totals
    print('t1_wins: ' + str(t1_wins) + '  | ', ('t2_wins: ' + str(t2_wins)))
    print('ot_games: ' + str(ot_games) + ' | ', ('ties: ' + str(ties)))
    print('t1_win_share: ' + str(round((t1_wins / (n - ties)), 2)))
    # plot results
    plt.bar(goals, counts)
    plt.xticks(range(20))
    plt.axvline(average_goals, linestyle='--', color='black')
    return plt.show()


simulation_test()
