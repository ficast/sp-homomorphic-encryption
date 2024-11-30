import numpy as np
import pandas as pd

candidates = ["Emanuel", "Nuno", "Filipa", "Maria", "Marta", "Branco", "Nulo"]

prob_candidates = [0.4, 0.15, 0.1, 0.1, 0.05, 0.1, 0.1]

districts = [
    "Aveiro",
    "Beja",
    "Braga",
    "Bragança",
    "Castelo Branco",
    "Coimbra",
    "Évora",
    "Faro",
    "Guarda",
    "Leiria",
    "Lisboa",
    "Portalegre",
    "Porto",
    "Santarém",
    "Setúbal",
    "Viana do Castelo",
    "Vila Real",
    "Viseu"
]

prob_districts = [
    0.07,
    0.02,
    0.09,
    0.03,
    0.03,
    0.04,
    0.03,
    0.03,
    0.01,
    0.04,
    0.2,
    0.03,
    0.17,
    0.04,
    0.07,
    0.03,
    0.03,
    0.04
]

total_districts = np.random.choice(districts, 1000, p=prob_districts)
total_candidates = np.random.choice(candidates, 1000, p=prob_candidates)

df = pd.DataFrame({
    "Districts": total_districts,
    "Candidates": total_candidates
})

# save the pivot table to a csv file
df.to_csv("votes.csv")