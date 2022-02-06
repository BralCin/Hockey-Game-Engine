# DEFINE GAME ENGINE #
def game_engine(t_1, t_2):
    # init gamescore
    gamescores = np.random.normal(loc=.25, scale=.25, size=(1, 2))
    gamescores = gamescores.tolist()
    t1_gamescore = t_1 * gamescores[0][0]
    t2_gamescore = t_2 * gamescores[0][1]
    # init scoring variables
    scoring_rate = 9  # lower for a lower score
    t1_score = round(t1_gamescore / scoring_rate)
    t2_score = round(t2_gamescore / scoring_rate)
    team_scores = [t1_score, t2_score]
    fumble = []
    # score calculation
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
    return final_scores
