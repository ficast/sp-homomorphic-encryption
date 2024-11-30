import src.data_holder as dh
import src.data_analysis as da


if __name__ == "__main__":
    # Inicializar contexto e chaves
    context = dh.initialize_context()
    print("Contexto inicializado com sucesso.")

    # Criptografar os votos
    encrypted_votes = dh.generate_encrypted_votes(context, df)
    print("Votos criptografados gerados com sucesso.")

    # Soma homomórfica dos votos por distrito
    print("Realizando soma homomórfica dos votos por distrito...")
    encrypted_sums = da.sum_votes_by_district(encrypted_votes)
    print("Soma homomórfica concluída.")

    # # Descriptografar resultados por distrito
    # print("Descriptografando os resultados...")
    # district_mapping = {idx: district for idx, district in enumerate(label_encoder.classes_)}
    # for district, encrypted_result in encrypted_sums.items():
    #     decrypted_result = decrypt_vector(context, encrypted_result)
    #     print(f"Distrito: {district_mapping[district]}")
    #     for i, count in enumerate(decrypted_result):
    #         print(f"  Candidato {encoder.categories_[0][i]}: {count} votos")