import tenseal as ts
import sys
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

        for candidato in self.load_encrypted_data("outputs/candidatos_enc.txt"):
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
        # Calculate results from encrypted candidates
        results = self.calculate_result()

        # Perform element-wise addition on encrypted vectors
        for i, candidato in enumerate(results):
            # Calculate progress
            progress = (i + 1) / 1000
            length = int(10 * progress)
            bar = "#" * length + "-" * (10 - length)

            # Print the loading bar
            sys.stdout.write(f"\r[{bar}] {int(progress * 100)}%")
            sys.stdout.flush()

            if i == 0:
                #initialize sum with the first candidate
                sum = candidato
            else:
                # Perform element-wise addition on encrypted vectors
                sum += candidato

        print()

        # Write the serialized sum to the output file
        write_data("outputs/sum_enc.txt", sum.serialize())
