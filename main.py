from src.data_holder import DataHolder
from src.data_analyzer import DataAnalyzer

if __name__ == "__main__":
    dh = DataHolder()
    dh.encrypt_data()
    
    da = DataAnalyzer("keys/public.txt")
    da.export_sum()
    
    dh.get_result()
    
