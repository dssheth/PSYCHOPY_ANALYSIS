import pandas as pd
import os

def clean_csv(input_filepath, output_dir):
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

    result_message = clean_csv(input_file_path, output_dir_path)
    print(result_message)

if __name__ == '__main__':
    main()
"""