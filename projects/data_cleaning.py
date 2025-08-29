import pandas as pd
import io

def clean_data(file_path):
    """
    Cleans a CSV or Excel file by performing common data cleaning tasks.

    Args:
        file_path (str): The path to the input CSV or Excel file.

    Returns:
        pd.DataFrame: A cleaned DataFrame.
    """
    try:
        # Check file extension to determine how to read the file
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith(('.xls', '.xlsx')):
            # Note: You may need to install openpyxl or xlrd for Excel files
            # pip install openpyxl
            df = pd.read_excel(file_path)
        else:
            print("Unsupported file format. Please use a .csv, .xls, or .xlsx file.")
            return None

        print("Original data:")
        print(df.head())
        print("-" * 30)

        # 1. Standardize column names
        # Make them lowercase and replace spaces with underscores
        df.columns = df.columns.str.lower().str.replace(' ', '_')
        print("Standardized column names:")
        print(df.columns)
        print("-" * 30)

        # 2. Handle missing values
        # Fill missing numeric values with the mean
        numeric_cols = df.select_dtypes(include=['number']).columns
        for col in numeric_cols:
            df[col] = df[col].fillna(df[col].mean())
        
        # Fill missing non-numeric values with 'Unknown'
        non_numeric_cols = df.select_dtypes(exclude=['number']).columns
        for col in non_numeric_cols:
            df[col] = df[col].fillna('Unknown')
        
        print("Data after handling missing values:")
        print(df.isnull().sum())
        print("-" * 30)

        # 3. Remove duplicate rows
        num_duplicates = df.duplicated().sum()
        df = df.drop_duplicates()
        print(f"Removed {num_duplicates} duplicate rows.")
        print("-" * 30)

        # 4. Optional: Convert a column to a specific data type
        # For example, convert a date column to datetime objects
        # if 'date' in df.columns:
        #     df['date'] = pd.to_datetime(df['date'])
        #     print("Converted 'date' column to datetime objects.")
        #     print("-" * 30)
        
        # 5. Save the cleaned data to a new file
        cleaned_file_path = "cleaned_" + file_path
        df.to_csv(cleaned_file_path, index=False)
        print(f"Cleaned data saved to '{cleaned_file_path}'")
        
        return df

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    # In a real-world scenario, you would replace this with your actual file.
    # For this example, we'll create a dummy CSV file-like object.
    
    sample_csv_data = """id,name,value,date
1,Alice,100,2023-01-01
2,Bob,150,2023-01-02
3,Charlie,120,2023-01-03
1,Alice,100,2023-01-01
4,David,,
5,Eve,180,2023-01-05
"""
    # Create a dummy CSV file to demonstrate the script
    file_name = "sample_data.csv"
    with open(file_name, 'w') as f:
        f.write(sample_csv_data)

    print(f"Created dummy file '{file_name}' for demonstration.")
    print("-" * 30)

    # Call the cleaning function with the dummy file
    cleaned_df = clean_data(file_name)
    
    if cleaned_df is not None:
        print("\nFinal cleaned data (head):")
        print(cleaned_df.head())
        print("-" * 30)
