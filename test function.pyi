# TEST #

def simulation_test(t_1, t_2, n)
    scores = []
    for i in range(n):
        score = game_engine(t_1, t_2)
        goals = score[0] + score[1]
        scores.append(goals)
    counter = Counter(scores)
    goals = list(counter.keys())
    counts = list(counter.values())

    plt.bar(goals, counts)
    plt.show()

    df = pd.DataFrame([goals, counts])
    df = df.T
    print(df.value_counts().sort_index())
