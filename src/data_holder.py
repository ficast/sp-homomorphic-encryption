import tenseal as ts
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from .utils import read_data, write_data, write_data_append


class AbstractDataHandler:
    def __init__(self, context_file):
        self.context = self.load_context(context_file)

    def load_context(self, filename):
        """
        Load the context from file.
        """
        return ts.context_from(read_data(filename))


class DataHolder(AbstractDataHandler):
    def __init__(self):
        """
        Initialize the data holder.
        """
        self.context = self.initialize_context()
        self.data = self.load_data()

    def initialize_context(self):
        """
        Initialize the context for CKKS encryption.
        """
        context = ts.context(
            ts.SCHEME_TYPE.CKKS,
            poly_modulus_degree=8192,
            coeff_mod_bit_sizes=[60, 40, 40, 60],
        )
        context.generate_galois_keys()
        context.global_scale = 2**40

        self.__secret_context__ = context.serialize(save_secret_key=True)
        self.export_context(self.__secret_context__, "keys/secret.txt")

        context.make_context_public()
        self.__public_context__ = context.serialize()
        self.export_context(self.__public_context__, "keys/public.txt")

        print("Context generated successfully!")
        return context

    def load_data(self):
        """
        Load the data from file.
        """
        return pd.read_csv("data/votes.csv")

    def export_context(self, context, filename):
        """
        Export the context to a binary file using pickle.
        """
        write_data(filename, context)
        print("Context exported successfully!")

    def encrypt_data(self):
        """
        Encrypt a vector using CKKS encryption.
        """
        self.context = self.load_context("keys/secret.txt")

        self.encoder = OneHotEncoder(sparse_output=False, dtype=int)

        candidates = self.encoder.fit_transform(self.data[["Candidates"]])

        for i, candidato in enumerate(candidates):
            candidatos_enc = ts.ckks_vector(self.context, candidato)
            if i == 0:
                write_data("outputs/candidatos_enc.txt", candidatos_enc.serialize())
            else:
                write_data_append(
                    "outputs/candidatos_enc.txt", candidatos_enc.serialize()
                )

    def decrypt_vector(self):
        m_proto = read_data("outputs/soma.txt")
        m = ts.lazy_ckks_vector_from(m_proto)
        m.link_context(self.context)
        return m.decrypt()

    def get_result(self):
        candidates_mapping = dict(enumerate(self.encoder.categories_[0]))
        number_of_votes = self.decrypt_vector()

        for number, votes in enumerate(number_of_votes):
            print(f"{candidates_mapping[number]}: {votes:.0f}")
