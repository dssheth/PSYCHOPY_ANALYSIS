import pandas as pd
import numpy as np
import re

def longexp_process_data(file_path):
    """
    Processes a CSV file containing behavioral data from an experiment, evaluates responses,
    and computes performance metrics.

    Parameters:
    - file_path (str): The path to the CSV file. The filename should follow the format:
      'P_Id_gender_longexp.csv', where 'P_Id' is a numerical participant identifier and
      'gender' is either 'M' or 'F'.

    Returns:
    - dict: A dictionary containing the following keys and their corresponding values:
        - 'P_Id': (str) Participant identifier extracted from the filename.
        - 'gender': (str) Gender extracted from the filename ('M' or 'F').
        - 'trial_accuracy': (float) Accuracy percentage for the trial block.
        - 'avg_rt_trials': (float) Average reaction time (RT) in seconds for the trial block.
        - 'block_1_accuracy': (float) Accuracy percentage for block 1.
        - 'avg_rt_block1': (float) Average RT in seconds for block 1.
        - 'block_2_accuracy': (float) Accuracy percentage for block 2.
        - 'avg_rt_block2': (float) Average RT in seconds for block 2.
        - 'block_3_accuracy': (float) Accuracy percentage for block 3.
        - 'avg_rt_block3': (float) Average RT in seconds for block 3.
        - 'block_4_accuracy': (float) Accuracy percentage for block 4.
        - 'avg_rt_block4': (float) Average RT in seconds for block 4.
        - 'total_accuracy': (float) Average accuracy across all blocks.
        - 'avg_rt_all': (float) Average RT across all blocks.

    Raises:
    - ValueError: If the filename does not match the expected format.

    Detailed Steps:
    1. Extracts the participant ID and gender from the filename.
    2. Loads the CSV data into a pandas DataFrame and filters relevant columns.
    3. Converts reaction time values from list-like strings to float.
    4. Filters rows with valid responses.
    5. Evaluates responses based on conditions and calculates accuracies.
    6. Computes average reaction times for trials and blocks.
    7. Returns a dictionary with the calculated metrics and participant details.
    """
    
    # Extract P_Id and gender from the file name
    file_name = file_path.split('/')[-1]
    # Extract P_Id before the first underscore and gender after it
    match = re.match(r'(\d+)_([MF])_.+\.csv', file_name)
    if match:
        P_Id, gender = match.groups()
    else:
        raise ValueError("Filename does not match expected format.")
    
    # Load data from CSV
    df = pd.read_csv(file_path)

    # Define columns to include
    cols_to_include = [
        'face_images_1', 'face_images_2', 
        'trial_resp.keys', 
        'trial_resp.rt',
        'resp_1.keys',
        'resp_1.rt', 
        'resp_2.keys',
        'resp_2.rt', 
        'resp_3.keys',
        'resp_3.rt',
        'resp_4.keys',
        'resp_4.rt'
    ]
    df = df[cols_to_include]

    # Create DataFrames for each block
    trial_df = df[['face_images_1', 'face_images_2', 'trial_resp.keys', 'trial_resp.rt']]
    block_1_df = df[['face_images_1', 'face_images_2', 'resp_1.keys', 'resp_1.rt']]
    block_2_df = df[['face_images_1', 'face_images_2', 'resp_2.keys', 'resp_2.rt']]
    block_3_df = df[['face_images_1', 'face_images_2', 'resp_3.keys', 'resp_3.rt']]
    block_4_df = df[['face_images_1', 'face_images_2', 'resp_4.keys', 'resp_4.rt']]

    # Function to convert list-like reaction times to floats
    def convert_rt(value):
        try:
            # Convert string representations of lists to float
            if isinstance(value, str):
                value = value.strip('[]')  # Remove square brackets
                return float(value) if value else np.nan
            return float(value)
        except:
            return np.nan

    # Apply the function to convert reaction times to floats
    for df, rt_col in [
        (trial_df, 'trial_resp.rt'),
        (block_1_df, 'resp_1.rt'),
        (block_2_df, 'resp_2.rt'),
        (block_3_df, 'resp_3.rt'),
        (block_4_df, 'resp_4.rt')
    ]:
        df[rt_col] = df[rt_col].apply(convert_rt)

    # Filter rows with valid responses
    trial_df = trial_df[trial_df['trial_resp.keys'].notna()]
    block_1_df = block_1_df[block_1_df['resp_1.keys'].notna()]
    block_2_df = block_2_df[block_2_df['resp_2.keys'].notna()]
    block_3_df = block_3_df[block_3_df['resp_3.keys'].notna()]
    block_4_df = block_4_df[block_4_df['resp_4.keys'].notna()]

    # Evaluate responses
    for df, key_col, rt_col, eval_col in [
        (trial_df, 'trial_resp.keys', 'trial_resp.rt', 'trial_resp.eval'),
        (block_1_df, 'resp_1.keys', 'resp_1.rt', 'resp_1.eval'),
        (block_2_df, 'resp_2.keys', 'resp_2.rt', 'resp_2.eval'),
        (block_3_df, 'resp_3.keys', 'resp_3.rt', 'resp_3.eval'),
        (block_4_df, 'resp_4.keys', 'resp_4.rt', 'resp_4.eval')
    ]:
        df[eval_col] = 0
        condition_case1 = (df['face_images_1'] == df['face_images_2']) & (df[key_col].str.contains('z'))
        condition_case2 = (df['face_images_1'] != df['face_images_2']) & (df[key_col].str.contains('m'))
        df.loc[condition_case1 | condition_case2, eval_col] = 1

    # Calculate accuracies
    trial_accuracy = round((trial_df['trial_resp.eval'].sum() / len(trial_df)) * 100, 2)
    block_1_accuracy = round((block_1_df['resp_1.eval'].sum() / len(block_1_df)) * 100, 2)
    block_2_accuracy = round((block_2_df['resp_2.eval'].sum() / len(block_2_df)) * 100, 2)
    block_3_accuracy = round((block_3_df['resp_3.eval'].sum() / len(block_3_df)) * 100, 2)
    block_4_accuracy = round((block_4_df['resp_4.eval'].sum() / len(block_4_df)) * 100, 2)
    total_accuracy = round((block_1_accuracy + block_2_accuracy + block_3_accuracy + block_4_accuracy) / 4, 2)

    # Calculate average reaction times
    avg_rt_trials = round(trial_df['trial_resp.rt'].mean(), 2)
    avg_rt_block1 = round(block_1_df['resp_1.rt'].mean(), 2)
    avg_rt_block2 = round(block_2_df['resp_2.rt'].mean(), 2)
    avg_rt_block3 = round(block_3_df['resp_3.rt'].mean(), 2)
    avg_rt_block4 = round(block_4_df['resp_4.rt'].mean(), 2)
    avg_rt_all = round((avg_rt_block1 + avg_rt_block2 + avg_rt_block3 + avg_rt_block4) / 4, 2)

    # Prepare the output dictionary
    output = {
        'P_Id': P_Id,
        'gender': gender,
        'trial_accuracy': trial_accuracy,
        'avg_rt_trials': avg_rt_trials,
        'block_1_accuracy': block_1_accuracy,
        'avg_rt_block1': avg_rt_block1,
        'block_2_accuracy': block_2_accuracy,
        'avg_rt_block2': avg_rt_block2,
        'block_3_accuracy': block_3_accuracy,
        'avg_rt_block3': avg_rt_block3,
        'block_4_accuracy': block_4_accuracy,
        'avg_rt_block4': avg_rt_block4,
        'total_accuracy': total_accuracy,
        'avg_rt_all': avg_rt_all
    }

    return output

"""
def main():
    print('TESTING...')
    print(longexp_process_data('/home/iiserb/Desktop/PSYCHOPY_ANALYSIS/ANALYSIS_LONG_EXP/DATASET_LONG_EXP/01_M_longexp.csv'))

if __name__ == '__main__':
    main()
"""