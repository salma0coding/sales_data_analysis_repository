import pandas as pd
from pathlib import Path
def load_data (file_path : str) -> pd.DataFrame:
    try:
        df = pd.read_csv(file_path,encoding="latin1")
        print(f"dataset uploaded successfully: {file_path}")
        return df
    except FileNotFoundError:
        raise FileNotFoundError (f"file not found:{file_path}")
    except Exception as e:
        raise Exception(f"Error loading file: {e}")
def inspect_data(df: pd.DataFrame) -> None:
    #print basic info about the data
    print("\n -- first 5 rows --")
    print(df.head())

    print("\n -- shape --")
    print(df.shape)

    print("\n -- columns --")
    print(df.columns.tolist())

    print("\n -- data types --")
    print(df.dtypes)

    print("\n -- missing values --")
    print(df.isnull().sum())

    print("\n -- duplicate Rows --")
    print(df.duplicated().sum())
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
#Clean the sales dataset.
    clean_df = df.copy()

    # Standardize column names
    clean_df.columns = clean_df.columns.str.strip().str.upper()

    # Remove duplicate rows
    clean_df = clean_df.drop_duplicates()

    # Handle missing values
    clean_df = clean_df.dropna()

    # Convert ORDERDATE to datetime if it exists
    if "ORDERDATE" in clean_df.columns:
        clean_df["ORDERDATE"] = pd.to_datetime(clean_df["ORDERDATE"], errors="coerce")

    # Remove rows with invalid dates after conversion
    if "ORDERDATE" in clean_df.columns:
        clean_df = clean_df.dropna(subset=["ORDERDATE"])

    # Ensure SALES is numeric
    if "SALES" in clean_df.columns:
        clean_df["SALES"] = pd.to_numeric(clean_df["SALES"], errors="coerce")
        clean_df = clean_df.dropna(subset=["SALES"])

    # Optional: strip spaces from text columns
    text_cols = clean_df.select_dtypes(include="object").columns
    for col in text_cols:
        clean_df[col] = clean_df[col].astype(str).str.strip()

    return clean_df


def save_clean_data(df: pd.DataFrame, output_path: str) -> None:
    """
    Save cleaned dataset to CSV.
    """
    df.to_csv(output_path, index=False)
    print(f"\nCleaned dataset saved to: {output_path}")


def main():
    # File paths
    input_file = "sales_data_sample.csv"
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "cleaned_sales_data.csv"

    # Load
    df = load_data(input_file)

    # Inspect before cleaning
    print("\n========== BEFORE CLEANING ==========")
    inspect_data(df)

    # Clean
    clean_df = clean_data(df)

    # Inspect after cleaning
    print("\n========== AFTER CLEANING ==========")
    inspect_data(clean_df)

    # Save
    save_clean_data(clean_df, output_file)


if __name__ == "__main__":
    main()
    
    
    
    
    
