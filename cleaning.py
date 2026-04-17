import pandas as pd
from pathlib import Path


def load_data(file_path: str) -> pd.DataFrame:
    """
    Load sales dataset from a CSV file.
    """
    try:
        df = pd.read_csv(file_path, encoding="latin1")
        print(f"Dataset loaded successfully: {file_path}")
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error loading file: {e}")


def inspect_data(df: pd.DataFrame, title: str = "DATA OVERVIEW") -> None:
    """
    Print basic information about the dataset.
    """
    print(f"\n========== {title} ==========")

    print("\n-- First 5 rows --")
    print(df.head())

    print("\n-- Shape --")
    print(df.shape)

    print("\n-- Columns --")
    print(df.columns.tolist())

    print("\n-- Data types --")
    print(df.dtypes)

    print("\n-- Missing values --")
    print(df.isnull().sum())

    print("\n-- Duplicate rows --")
    print(df.duplicated().sum())


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and standardize column names.
    """
    df = df.copy()
    df.columns = df.columns.str.strip().str.upper()
    return df


def clean_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove leading/trailing spaces from text columns.
    """
    df = df.copy()
    text_cols = df.select_dtypes(include="object").columns

    for col in text_cols:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace("nan", pd.NA)

    return df


def convert_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert important columns to correct data types.
    """
    df = df.copy()

    if "ORDERDATE" in df.columns:
        df["ORDERDATE"] = pd.to_datetime(df["ORDERDATE"], errors="coerce")

    if "SALES" in df.columns:
        df["SALES"] = pd.to_numeric(df["SALES"], errors="coerce")

    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing values more safely without dropping too much data.
    """
    df = df.copy()

    # Only drop rows if critical columns are missing
    required_cols = [col for col in ["SALES", "ORDERDATE"] if col in df.columns]
    if required_cols:
        df = df.dropna(subset=required_cols)

    # Fill optional categorical columns if they exist
    optional_fill_columns = ["STATE", "TERRITORY", "ADDRESSLINE2", "POSTALCODE"]
    for col in optional_fill_columns:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate rows.
    """
    df = df.copy()
    df = df.drop_duplicates()
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Full cleaning pipeline for the sales dataset.
    """
    clean_df = df.copy()

    # 1) Standardize column names
    clean_df = standardize_column_names(clean_df)

    # 2) Remove duplicates
    clean_df = remove_duplicates(clean_df)

    # 3) Clean text columns
    clean_df = clean_text_columns(clean_df)

    # 4) Convert data types
    clean_df = convert_data_types(clean_df)

    # 5) Handle missing values safely
    clean_df = handle_missing_values(clean_df)

    return clean_df


def save_clean_data(df: pd.DataFrame, output_path: Path) -> None:
    """
    Save cleaned dataset to CSV.
    """
    df.to_csv(output_path, index=False)
    print(f"\nCleaned dataset saved to: {output_path}")


def print_cleaning_summary(before_df: pd.DataFrame, after_df: pd.DataFrame) -> None:
    """
    Print summary of cleaning results.
    """
    print("\n========== CLEANING SUMMARY ==========")
    print(f"Rows before cleaning: {before_df.shape[0]}")
    print(f"Rows after cleaning:  {after_df.shape[0]}")
    print(f"Columns:              {after_df.shape[1]}")
    print(f"Rows removed:         {before_df.shape[0] - after_df.shape[0]}")


def main():
    input_file = r"C:\Users\A&A\Downloads\sales_data_sample.csv"

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "cleaned_sales_data.csv"

    # Load data
    df = load_data(input_file)

    # Inspect before cleaning
    inspect_data(df, title="BEFORE CLEANING")

    # Clean data
    clean_df = clean_data(df)

    # Inspect after cleaning
    inspect_data(clean_df, title="AFTER CLEANING")

    # Print summary
    print_cleaning_summary(df, clean_df)

    # Save cleaned data
    save_clean_data(clean_df, output_file)


if __name__ == "__main__":
    main()