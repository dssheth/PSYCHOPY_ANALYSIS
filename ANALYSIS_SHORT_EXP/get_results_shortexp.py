import os
import sys
from pathlib import Path
from utils import shortexp_clean_csv


# Add the parent directory to the system path to locate the `utils` module
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Define the input and output directories
INPUT_DIR = Path('ANALYSIS_SHORT_EXP/DATASET_SHORT_EXP')
OUTPUT_DIR = Path('ANALYSIS_SHORT_EXP/RESULTS')

def main():
    # Ensure the output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Iterate over all files in the input directory
    for file_name in os.listdir(INPUT_DIR):
        file_path = INPUT_DIR / file_name
        
        # Only process CSV files
        if file_path.suffix == '.csv':
            print(f"Processing file: {file_name}")
            
            # Call the cleaning function
            result_message = shortexp_clean_csv(file_path, OUTPUT_DIR)
            print(result_message)

if __name__ == '__main__':
    main()
