import tenseal as ts
import pickle
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from utils import encode_data, decode_data


class DataHolder:
    def __init__(self):
        '''
        Initialize the data holder.
        '''
        self.context = self.initialize_context()
        self.data = self.load_data()

    def initialize_context(self):
        '''
        Initialize the context for CKKS encryption.
        '''
        context = ts.context(
            ts.SCHEME_TYPE.CKKS,
            poly_modulus_degree=8192,
            coeff_mod_bit_sizes=[60, 40, 40, 60]
        )
        context.global_scale = 2**40
        context.generate_galois_keys()
        self.__secret_context__ = context.serialize(save_secret_key=True)
        self.export_context(self.__secret_context__, "data/secret_context.txt")
        
        context.make_context_public()
        self.__public_context__ = context.serialize()
        self.export_context(self.__public_context__, "data/public_context.txt")
        
        print("Context generated successfully!")
        return context
    
    
    def load_context(self, filename):
        '''
        Load the context from file.
        '''
        return pd.read_csv(filename)
    
    
    def export_context(self, context, filename):
        '''
        Export the context to a binary file using pickle.
        '''
        encode_data(filename, context)
        print("Context exported successfully!")


    def encrypt_data(self):
        '''
        Encrypt a vector using CKKS encryption.
        '''
        encrypted_vector = ts.ckks_vector(self.context, self.data)
        encode_data("data/encrypted_vector.txt", encrypted_vector.serialize())
        return encrypted_vector
    

    def decrypt_vector(self, encrypted_vector):
        '''
        Decrypt a vector using CKKS encryption.
        '''
        return encrypted_vector.decrypt()



class DataAnalyzer:
    def __init__(self, public_context_file):
        self.context = self.load_context(public_context_file)
        
        
    def load_context(self, filename):
        '''
        Load the context from file.
        '''
        context = decode_data(filename)
        return ts.context_from(context)
    
    def load_encrypted_data(self, filename):
        '''
        Load the encrypted data from file.
        '''
        return decode_data(filename)


if __name__ == "__main__":
    data_holder = DataHolder()
    data_holder.encrypt_data()
    
    data_analyzer = DataAnalyzer("data/public_context.txt")
    encrypted_data = data_analyzer.load_encrypted_data("data/encrypted_vector.txt")
