from src.data_holder import DataHolder
from src.data_analyzer import DataAnalyzer
from src.utils import print_section

if __name__ == "__main__":
    """
    Main entry point for the Homomorphic Encryption application.

    Workflow:
    1. Initialize the DataHolder to encrypt and manage the dataset.
    2. Encrypt the dataset and save the encrypted data to a file.
    3. Initialize the DataAnalyzer to process the encrypted data using a public context.
    4. Compute the sum of encrypted data and save the result.
    5. Decrypt the computed results and print them.
    """
    # Step 1: Initialize the DataHolder
    print_section("CONTEXT STATUS")
    dh = DataHolder()
    
    # Step 2: Encrypt the dataset
    print_section("ENCRYPTION STATUS")
    print("Encrypting dataset...")
    dh.encrypt_data()
    print("Dataset encrypted and saved to: outputs/candidatos_enc.txt")

    # Step 3: Initialize the DataAnalyzer with the public key
    da = DataAnalyzer("keys/public.txt")
    
    # Step 4: Compute the sum and save the result
    print_section("ANALYSIS STATUS")
    print("Calculating sum of encrypted data...")
    da.export_sum()
    print("Encrypted sum calculated and saved to: outputs/sum_enc.txt")

    # Step 5: Decrypt and display the results
    print_section("DECRYPTION RESULTS")
    print("Decrypting results...")
    dh.get_result()
    print("Decryption completed.")
