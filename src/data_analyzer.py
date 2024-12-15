import tenseal as ts
from .utils import read_data_split, write_data
from .data_holder import AbstractDataHandler

class DataAnalyzer(AbstractDataHandler):
    def __init__(self, public_context_file):
        """
        Initialize the DataAnalyzer with the public context file.

        Parameters:
        - public_context_file (str): Path to the file containing the public context for encryption.
        """
        self.context = self.load_context(public_context_file)

    def load_encrypted_data(self, filename):
        """
        Load encrypted data from a file.

        Parameters:
        - filename (str): Path to the file containing encrypted data.

        Returns:
        - list[bytes]: List of encrypted data splits.
        """
        return read_data_split(filename)

    def calculate_result(self):
        """
        Process encrypted data to extract and prepare candidate vectors.

        Returns:
        - list[ts.CKKSVector]: List of CKKS vectors linked to the current context.
        """
        candidates_list = []

        for candidato in self.load_encrypted_data("outputs/candidatos_enc.txt")[:-1]:
            # Create a lazy CKKS vector from the encrypted data
            candidatos_enc = ts.lazy_ckks_vector_from(candidato)
            # Link the context to the vector to enable operations
            candidatos_enc.link_context(self.context)
            candidates_list.append(candidatos_enc)

        return candidates_list

    def export_sum(self):
        """
        Compute the sum of encrypted vectors and export the result.

        The sum is written to a file as a serialized tensor.
        """
        # Initialize a plain tensor with zero values for summation
        sum = ts.plain_tensor([0, 0, 0, 0, 0, 0, 0])
        
        # Calculate results from encrypted candidates
        results = self.calculate_result()

        for candidato in results[:-1]:
            # Perform element-wise addition on encrypted vectors
            sum += candidato

        # Write the serialized sum to the output file
        write_data("outputs/soma.txt", sum.serialize())
