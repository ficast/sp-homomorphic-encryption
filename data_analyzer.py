import os
import tenseal as ts

def read_encrypted_data(file_path):
    with open(file_path, 'r') as file:
        encrypted_data = file.readlines()

    return encrypted_data

# Realizar soma homomórfica dos votos por distrito
def sum_votes_by_district(encrypted_votes):
    district_sums = {}

    for vote in encrypted_votes:
        district = vote["District"]

        if district not in district_sums:
            district_sums[district] = vote["Encrypted_Candidate_Vector"]

        else:
            district_sums[district] += vote["Encrypted_Candidate_Vector"]

    return district_sums
