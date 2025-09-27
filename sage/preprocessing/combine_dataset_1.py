#Combines datasets with respect to play store data
import pandas as pd
import os

data_dir = "data/raw"
out_dir = "data/processed"
os.makedirs(out_dir, exist_ok=True)
def combine_datasets():
    search_result = pd.read_csv(os.path.join(data_dir, 'search_results.csv'))
    app_collections = pd.read_csv(os.path.join(data_dir, 'app_collections.csv'))
    app_details = pd.read_csv(os.path.join(data_dir, 'app_details.csv'))
    googleplaystore = pd.read_csv(os.path.join(out_dir, 'google_play_cleaned.csv'))
    app_developers = pd.read_csv(os.path.join(data_dir, 'app_developers.csv'))
    target_columns = [
        'App', 'Category', 'Rating', 'Reviews', 'Size', 'Installs', 'Type',
        'Price', 'Content Rating', 'Genres', 'Last Updated', 'Current Ver',
        'Required Version'
    ]
    mappings = {
        'search_result': {
            'title': 'App',
            'genres': 'Category',
            'score': 'Rating',
            'reviews': 'Reviews',
            'size': 'Size',
            'free': 'Type',
            'contentRating': 'Content Rating',
            'genres': 'Genres',
            'updated': 'Last Updated',
            'version': 'Current Ver',
            'requiredOsVersion': 'Required Version',
            'price': 'Price'
        },
        
        'app_collections': {
            'title': 'App',
            'genre': 'Category',
            'reviews': 'Reviews',
            'released': 'Last Updated',
            'price': 'Price',
            'free': 'Type'
        },
        
        'app_details': {
            'title': 'App',
            'genres': 'Category',
            'score': 'Rating',
            'reviews': 'Reviews',
            'size': 'Size',
            'free': 'Type',
            'contentRating': 'Content Rating',
            'genres': 'Genres',
            'updated': 'Last Updated',
            'version': 'Current Ver',
            'requiredOsVersion': 'Required Version',
            'price': 'Price'
        },
        
        'app_developers': {
            'title': 'App',
            'genres': 'Category',
            'score': 'Rating',
            'reviews': 'Reviews',
            'size': 'Size',
            'free': 'Type',
            'contentRating': 'Content Rating',
            'genres': 'Genres',
            'updated': 'Last Updated',
            'version': 'Current Ver',
            'requiredOsVersion': 'Required Version',
            'price': 'Price'
        }
    }

    def normalize_dataset(df, column_mapping, target_schema):
        """Convert a dataset to match the target schema"""
        normalized_df = pd.DataFrame()
        for source_col, target_col in column_mapping.items():
            if source_col in df.columns:
                normalized_df[target_col] = df[source_col]
        if 'free' in df.columns:
            if 'Type' in normalized_df.columns:
                normalized_df.drop('Type', axis=1, inplace=True)
            normalized_df['Type'] = df['free'].apply(
                lambda x: 'Free' if (x == True or str(x).lower() == 'free') else 'Paid'
            )
        if 'Required Version' in normalized_df.columns:
            if 'Installs' in df.columns:
                normalized_df['Required Version'] = normalized_df['Required Version'].apply(
                    lambda x: f"Android {x}" if pd.notna(x) else x
                )
            else:  
                normalized_df['Required Version'] = normalized_df['Required Version'].apply(
                    lambda x: f"iOS {x}" if pd.notna(x) else x
                )
        
        for col in target_schema:
            if col not in normalized_df.columns:
                normalized_df[col] = None
        
        return normalized_df[target_schema]

    dfs = []

    googleplaystore_renamed = googleplaystore.rename(columns={
        'App': 'App',
        'Rating': 'Rating',
        'Reviews': 'Reviews',
        'Size': 'Size',
        'Installs': 'Installs',
        'Type': 'Type',
        'Price': 'Price',
        'Content Rating': 'Content Rating',
        'Genres': 'Genres',
        'Last Updated': 'Last Updated',
        'Current Ver': 'Current Ver',
        'Android Ver': 'Required Version'  
    })

    googleplaystore_renamed['Type'] = googleplaystore_renamed['Type'].apply(
        lambda x: 'Free' if str(x).lower() == 'free' else 'Paid'
    )

    googleplaystore_renamed['Required Version'] = googleplaystore_renamed['Required Version'].apply(
        lambda x: f"Android {x}" if pd.notna(x) else x
    )

    dfs.append(googleplaystore_renamed[target_columns])

    datasets_and_mappings = [
        (search_result, mappings['search_result']),
        (app_collections, mappings['app_collections']),
        (app_details, mappings['app_details']),
        (app_developers, mappings['app_developers'])
    ]

    for df, mapping in datasets_and_mappings:
        normalized_df = normalize_dataset(df, mapping, target_columns)
        dfs.append(normalized_df)

    non_empty_dfs = [df for df in dfs if not df.empty and len(df) > 0]

    combined_df = pd.concat(non_empty_dfs, ignore_index=True)


    output_path = os.path.join(out_dir, 'combined_dataset_1.csv')
    combined_df.to_csv(output_path, index=False)

    print(f"Combined dataset saved with {len(combined_df)} rows and {len(combined_df.columns)} columns")
    print("Columns:", combined_df.columns.tolist())
if __name__ == "__main__":
    combine_datasets()