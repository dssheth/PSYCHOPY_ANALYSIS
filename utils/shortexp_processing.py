import pandas as pd
import os

def shortexp_clean_csv(input_filepath, output_dir):
    """
    Cleans and filters a CSV file based on specific columns and saves the cleaned data to a new file.

    Parameters:
    - input_filepath (str): The path to the input CSV file that needs to be cleaned.
    - output_dir (str): The directory where the cleaned CSV file will be saved.

    Returns:
    - str: A message indicating the location of the saved cleaned CSV file.

    Raises:
    - ValueError: If any of the required columns are missing from the input file.

    Detailed Steps:
    1. Reads the CSV file into a pandas DataFrame.
    2. Checks for the presence of required columns.
    3. Keeps only the specified columns in the DataFrame.
    4. Drops rows where the 'face_images' column has null values.
    5. Constructs the output file path by appending '_cleaned' to the base name of the input file.
    6. Ensures the output directory exists; creates it if necessary.
    7. Saves the cleaned DataFrame to the new CSV file.
    8. Returns a message with the path to the cleaned CSV file.
    """

    # Read the CSV file
    df = pd.read_csv(input_filepath)
    
    # List of columns to keep
    cols_to_take = [
        'face_images',
        'valence_slider.response', 'valence_slider.rt',
        'arousal_slider.response', 'arousal_slider.rt',
        'emotional_intensity_slider.response', 'emotional_intensity_slider.rt',
        'familiarity_slider.response', 'familiarity_slider.rt',
        'emotion_express_slider.response', 'emotion_express_slider.rt'
    ]
    
    # Check if all columns exist in the dataframe
    missing_cols = [col for col in cols_to_take if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing columns in the input file: {', '.join(missing_cols)}")
    
    # Keep only the specified columns
    df = df[cols_to_take]
    
    # Drop rows where 'face_images' column has null values
    df = df.dropna(subset=['face_images'])
    
    # Generate the output file path with '_cleaned' suffix in the specified output directory
    base_name = os.path.basename(input_filepath)
    base, ext = os.path.splitext(base_name)
    output_filepath = os.path.join(output_dir, f"{base}_cleaned{ext}")
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Save the cleaned DataFrame to the new CSV file
    df.to_csv(output_filepath, index=False)
    
    return f"Cleaned data saved to {output_filepath}"

"""
def main():
    print('TESTING...')
    input_file_path = '01_M_shortexp.csv'
    output_dir_path = 'temp/'

    result_message = clean_csv_shortexp(input_file_path, output_dir_path)
    print(result_message)

if __name__ == '__main__':
    main()
"""