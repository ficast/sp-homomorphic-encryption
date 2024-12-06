import numpy as np
import pandas as pd

candidates = ["Emanuel", "Nuno", "Filipa", "Maria", "Marta", "Branco", "Nulo"]

prob_candidates = [0.4, 0.2, 0.1, 0.1, 0.1, 0.05, 0.05]

# randomize candidates order with a defined seed
np.random.shuffle(candidates)

# randomize districts order with a defined seed
np.random.shuffle(prob_candidates)

total_candidates = np.random.choice(candidates, 1000, p=prob_candidates)

df = pd.DataFrame({
    "Candidates": total_candidates
})

# save the pivot table to a csv file
df.to_csv("votes.csv")