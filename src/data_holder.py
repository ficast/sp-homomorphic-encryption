import tenseal as ts
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from .utils import read_data, write_data, write_data_append, print_section
import sys

class AbstractDataHandler:
    def __init__(self, context_file):
        """
        Initialize the AbstractDataHandler with a context file.

        Parameters:
        - context_file (str): Path to the file containing the encryption context.
        """
        self.context = self.load_context(context_file)

    def load_context(self, filename):
        """
        Load the encryption context from a file.

        Parameters:
        - filename (str): Path to the file containing the encryption context.

        Returns:
        - ts.Context: The loaded encryption context.
        """
        return ts.context_from(read_data(filename))

class DataHolder(AbstractDataHandler):
    def __init__(self):
        """
        Initialize the DataHolder by creating a context and loading data.
        """
        self.context = self.initialize_context()
        self.data = self.load_data("data/votes.csv")

    def initialize_context(self):
        """
        Initialize the context for CKKS encryption.

        Returns:
        - ts.Context: The initialized encryption context.
        """
        context = ts.context(
            ts.SCHEME_TYPE.CKKS,
            poly_modulus_degree=8192,
            coeff_mod_bit_sizes=[60, 40, 40, 60],
        )
        context.generate_galois_keys()
        context.global_scale = 2**40

        # Save the secret and public contexts
        self.__secret_context__ = context.serialize(save_secret_key=True)
        self.export_context(self.__secret_context__, "keys/secret.txt")
        print("- Full Context (with Secret Key) saved to: keys/secret.txt")

        context.make_context_public()
        self.__public_context__ = context.serialize()
        self.export_context(self.__public_context__, "keys/public.txt")
        print("- Public Context (without Secret Key) saved to: keys/public.txt")

        print("Context generated successfully!")
        return context

    def load_data(self, path):
        """
        Load the dataset from a CSV file.

        Returns:
        - pd.DataFrame: The loaded dataset.
        """
        return pd.read_csv(path)

    def export_context(self, context, filename):
        """
        Export the encryption context to a file.

        Parameters:
        - context (bytes): Serialized encryption context.
        - filename (str): Path to save the context.
        """
        write_data(filename, context)

    def encrypt_data(self):
        """
        Encrypt the data using CKKS encryption and save it to a file.
        """
        # Load the secret context for encryption
        self.context = self.load_context("keys/secret.txt")

        # One-hot encode the candidate data
        self.encoder = OneHotEncoder(sparse_output=False, dtype=int)
        candidates = self.encoder.fit_transform(self.data[["Candidates"]])

        # Encrypt and save each candidate vector
        for i, candidato in enumerate(candidates):
            candidatos_enc = ts.ckks_vector(self.context, candidato)

            # Calculate progress
            progress = (i + 1) / 1000
            length = int(10 * progress)
            bar = "#" * length + "-" * (10 - length)

            # Print the loading bar
            sys.stdout.write(f"\r[{bar}] {int(progress * 100)}%")
            sys.stdout.flush()

            # Creates file with the encrypted data of first candidate
            if i == 0:
                write_data("outputs/candidatos_enc.txt", candidatos_enc.serialize())

            # Appends the encrypted data of the other candidates    
            else:
                write_data_append("outputs/candidatos_enc.txt", candidatos_enc.serialize())

        print()

    def decrypt_vector(self):
        """
        Decrypt the encrypted vector from a file.

        Returns:
        - list[float]: The decrypted vector.
        """
        m_proto = read_data("outputs/sum_enc.txt")
        m = ts.lazy_ckks_vector_from(m_proto)
        m.link_context(self.context)
        return m.decrypt()

    def get_result(self):
        """
        Print the decrypted results, mapping candidates to their vote counts.
        """
        # Map candidate categories to their indices
        candidates_mapping = dict(enumerate(self.encoder.categories_[0]))
        number_of_votes = self.decrypt_vector()

        # Print header
        print("\n" + "-" * 30)
        print("Candidate Results")
        print("-" * 30)

        # Print each candidate's name and votes
        for number, votes in enumerate(number_of_votes):
            candidate = candidates_mapping[number]
            print(f"{candidate:<15} | {votes:>5.0f}")
        print("-" * 30 + "\n")
