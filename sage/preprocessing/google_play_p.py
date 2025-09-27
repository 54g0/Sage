import pandas as pd
import os
data_dir = "/home/egg/Documents/Sage/data/raw/googleplaystore.csv"
out_dir = "data/processed"
def preprocess_gpd(csv_path: str):
    df = pd.read_csv(csv_path)
    df = df.drop_duplicates(subset=['App',"Category","Size",'Installs'],keep ="last")
    df = df.dropna(subset=['Rating'])
    df["Type"].fillna("Free")
    df["Content Rating"].fillna(df["Content Rating"].mode()[0])
    df["Current Ver"].fillna("Varies with device")
    df["Android Ver"].fillna(df["Android Ver"].mode()[0])
    df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce")
    df["Installs"] = df["Installs"].str.replace("[+,]", "", regex=True)
    df["Installs"] = pd.to_numeric(df["Installs"], errors="coerce")
    file_path = os.path.join(out_dir, "google_play_cleaned.csv")
    os.makedirs(out_dir, exist_ok=True)
    df.to_csv(file_path, index=False, header=True)
    print(f"Preprocessed data saved to {file_path}")

if __name__ == "__main__":
    print("Starting preprocessing...")
    preprocess_gpd(os.path.join(data_dir))