import pandas as pd

def standardize_date_format(df: pd.DataFrame, date_column: str) -> pd.DataFrame:
    """
    Standardizes the date format to 'YYYY-MM-DD' for a given column.

    Args:
        df (pd.DataFrame): The dataframe containing the date column.
        date_column (str): The name of the date column.

    Returns:
        pd.DataFrame: The dataframe with standardized date format.
    """
    try:
        df[date_column] = pd.to_datetime(df[date_column], errors='coerce').dt.strftime('%Y-%m-%d')
        df[date_column] = df[date_column].replace("NaT", "")
        return df
    except KeyError:
        raise ValueError(f"Column '{date_column}' not found in the dataframe.")
    except Exception as e:
        raise Exception(f"Error standardizing date format: {e}")

def convert_id_to_string(df: pd.DataFrame, id_column: str) -> pd.DataFrame:
    """
    Converts a given column to string format.

    Args:
        df (pd.DataFrame): The dataframe containing the ID column.
        id_column (str): The name of the ID column.

    Returns:
        pd.DataFrame: The dataframe with the ID column converted to string.
    """
    try:
        df[id_column] = df[id_column].astype(str)
        return df
    except KeyError:
        raise ValueError(f"Column '{id_column}' not found in the dataframe.")
    except Exception as e:
        raise Exception(f"Error converting ID column to string: {e}")

def sanitize_title_text(df: pd.DataFrame, title_column: str) -> pd.DataFrame:
    """
    Sanitizes and normalizes the text in the title column by:
    1. Removing non-ASCII characters
    2. Removing special characters
    3. Capitalizing words properly
    4. Stripping extra spaces

    Args:
        df (pd.DataFrame): The dataframe containing the title column.
        title_column (str): The name of the title column.

    Returns:
        pd.DataFrame: The dataframe with sanitized title text.
    """
    try:
        df[title_column] = df[title_column].str.encode('ascii', 'ignore').str.decode('utf-8')
        df[title_column] = df[title_column].str.replace(r'[^\w\s-]', '', regex=True)
        df[title_column] = df[title_column].str.title().str.strip().str.replace(r'\s+', ' ', regex=True)
        return df
    except KeyError:
        raise ValueError(f"Column '{title_column}' not found in the dataframe.")
    except Exception as e:
        raise Exception(f"Error sanitizing title text: {e}")

def remove_rows_with_empty_titles_or_journals(df: pd.DataFrame, title_column: str, journal_column: str) -> pd.DataFrame:
    """
    Removes rows where either the title or the journal column is empty or NaN.

    Args:
        df (pd.DataFrame): The dataframe containing the title and journal columns.
        title_column (str): The name of the title column.
        journal_column (str): The name of the journal column.

    Returns:
        pd.DataFrame: The dataframe with rows with empty titles or journals removed.
    """
    try:
        return df.dropna(subset=[title_column, journal_column])
    except KeyError:
        raise ValueError(f"Columns '{title_column}' or '{journal_column}' not found in the dataframe.")
    except Exception as e:
        raise Exception(f"Error removing rows with empty titles or journals: {e}")

def remove_duplicate_ids_and_reindex(df: pd.DataFrame, id_column: str) -> pd.DataFrame:
    """
    Removes duplicate rows based on the ID column and resets the index.

    Args:
        df (pd.DataFrame): The dataframe containing the ID column.
        id_column (str): The name of the ID column.

    Returns:
        pd.DataFrame: The dataframe with duplicates removed and index reset.
    """
    try:
        return df.drop_duplicates(subset=[id_column]).reset_index(drop=True)
    except KeyError:
        raise ValueError(f"Column '{id_column}' not found in the dataframe.")
    except Exception as e:
        raise Exception(f"Error removing duplicates and reindexing: {e}")