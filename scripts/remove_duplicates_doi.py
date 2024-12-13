
import pandas as pd

def remove_duplicates(input_file, output_file):
    # Load CSV file into a DataFrame
    df = pd.read_csv(input_file)

    # Remove duplicates based on the values in the fourth column
    df_no_duplicates = df.drop_duplicates(subset=df.columns[3])

    # Save the result to a new CSV file
    df_no_duplicates.to_csv(output_file, index=False)

if __name__ == "__main__":
    # Replace 'input.csv' and 'output.csv' with your file name
    input_file = '../data/ponctual_search_results/2024_NeuroPIs_LitSearch_Raw.csv'
    output_file = '../data/ponctual_search_results/2024_NeuroPIs_LitSearch_NoDuplicates.csv'

    remove_duplicates(input_file, output_file)
    print(f'Duplicates removed and saved to {output_file}')