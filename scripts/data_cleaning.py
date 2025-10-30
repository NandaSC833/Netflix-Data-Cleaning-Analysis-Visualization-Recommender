import pandas as pd

def load_data(path):
    """Load the Netflix dataset"""
    data = pd.read_csv(r"C:\Users\Nanda Chowgle\OneDrive\Desktop\netflix_data\data\netflix1.csv")
    
    print("✅ Data loaded successfully!")
    print(f"Shape of data: {data.shape}")
    print(data.head(3))
    return data


def clean_data(data):
    """Clean the dataset"""
    print("\n🧹 Cleaning Data...")

    data.drop_duplicates(inplace=True)

    data.dropna(subset=['director', 'cast', 'country'], inplace=True)

    # Convert date_added to datetime
    data['date_added'] = pd.to_datetime(data['date_added'], errors='coerce')

    data['rating'].fillna('Unknown', inplace=True)
    data['duration'].fillna('Unknown', inplace=True)
    data['listed_in'].fillna('Unknown', inplace=True)

    print("\n✅ Data cleaned successfully!")
    print(data.info())
    return data
