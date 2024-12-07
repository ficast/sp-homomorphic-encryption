
import tenseal as ts
from .utils import read_data_split, write_data
from .data_holder import AbstractDataHandler


class DataAnalyzer(AbstractDataHandler):
    def __init__(self, public_context_file):
        self.context = self.load_context(public_context_file)
        
    def load_encrypted_data(self, filename):
        '''
        Load the encrypted data from file.
        '''
        return read_data_split(filename)

    def calculate_result(self):
        candidates_list = []

        for candidato in self.load_encrypted_data("outputs/candidatos_enc.txt")[:-1]:
            candidatos_enc = ts.lazy_ckks_vector_from(candidato)
            candidatos_enc.link_context(self.context)
            candidates_list.append(candidatos_enc)

        return candidates_list
    
    def export_sum(self):
        sum = ts.plain_tensor([0, 0, 0, 0, 0, 0, 0])
        results = self.calculate_result()
        for candidato in results[:-1]:
            sum += candidato

        write_data("outputs/soma.txt", sum.serialize())