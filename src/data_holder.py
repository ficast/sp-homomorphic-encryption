import tenseal as ts
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from .utils import read_data, write_data, write_data_append

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
        self.data = self.load_data()

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

        context.make_context_public()
        self.__public_context__ = context.serialize()
        self.export_context(self.__public_context__, "keys/public.txt")

        print("Context generated successfully!")
        return context

    def load_data(self):
        """
        Load the dataset from a CSV file.

        Returns:
        - pd.DataFrame: The loaded dataset.
        """
        return pd.read_csv("data/votes.csv")

    def export_context(self, context, filename):
        """
        Export the encryption context to a file.

        Parameters:
        - context (bytes): Serialized encryption context.
        - filename (str): Path to save the context.
        """
        write_data(filename, context)
        print(f"Context exported successfully to {filename}!")

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
            if i == 0:
                write_data("outputs/candidatos_enc.txt", candidatos_enc.serialize())
            else:
                write_data_append("outputs/candidatos_enc.txt", candidatos_enc.serialize())

    def decrypt_vector(self):
        """
        Decrypt the encrypted vector from a file.

        Returns:
        - list[float]: The decrypted vector.
        """
        m_proto = read_data("outputs/soma.txt")
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

        # Print the result for each candidate
        for number, votes in enumerate(number_of_votes):
            print(f"{candidates_mapping[number]}: {votes:.0f}")