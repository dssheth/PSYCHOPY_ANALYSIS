import os
import sys
import pandas as pd
from pathlib import Path
from utils import longexp_process_data


# Add the parent directory to the system path
sys.path.append(str(Path(__file__).resolve().parent.parent))


def process_directory(directory_path, output_file):
    results = []

    # Loop over each file in the directory
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(directory_path, file_name)
            try:
                result = longexp_process_data(file_path)
                results.append(result)
            except Exception as e:
                print(f"Error processing {file_name}: {e}")
    
    # Convert results to a DataFrame
    results_df = pd.DataFrame(results)
    
    # Save the DataFrame to an Excel file
    results_df.to_excel(output_file, index=False)
    print(f"Results saved to {output_file}")

def main():
    # Define the path to the directory containing CSV files and the output Excel file
    directory_path = 'ANALYSIS_LONG_EXP/DATASET_LONG_EXP'
    output_file = 'ANALYSIS_LONG_EXP/longexp_results.xlsx'
    
    # Process the directory and save results
    process_directory(directory_path, output_file)

if __name__ == '__main__':
    main()
