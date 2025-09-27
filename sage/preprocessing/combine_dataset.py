#Combines Datasets with respect to app store data
import pandas as pd
import os
data_dir = "data/raw"
out_dir = "data/processed"
def combine_datasets():
    google_play_path = os.path.join(out_dir,"google_play_cleaned.csv")
    search_results_path = os.path.join(data_dir,"search_results.csv")
    app_details_path = os.path.join(data_dir,"app_details.csv")
    app_collections_path = os.path.join(data_dir,"app_collections.csv")
    app_developers_path = os.path.join(data_dir,"app_developers.csv")
    search_results_df = pd.read_csv(search_results_path)
    app_details_df = pd.read_csv(app_details_path)
    app_collections_df = pd.read_csv(app_collections_path)
    app_developers_df = pd.read_csv(app_developers_path)
    google_play_df = pd.read_csv(google_play_path)
    unified_columns = [
    'id', 'appId', 'title', 'url', 'description', 'icon',
    'genres', 'genreIds', 'primaryGenre', 'primaryGenreId',
    'contentRating', 'languages', 'size', 'requiredOsVersion',
    'released', 'updated', 'releaseNotes', 'version',
    'price', 'currency', 'free',
    'developerId', 'developer', 'developerUrl', 'developerWebsite',
    'score', 'reviews', 'currentVersionScore', 'currentVersionReviews',
    'screenshots', 'ipadScreenshots', 'appletvScreenshots', 'supportedDevices'
    ]
    def normalize_df(df, schema):
        for col in schema:
            if col not in df.columns:
                df[col] = None
        return df[schema]
    dfs = [
        normalize_df(search_results_df, unified_columns),
        normalize_df(app_details_df, unified_columns),
        normalize_df(app_collections_df.rename(columns={'genre': 'genres', 'genreId': 'genreIds'}), unified_columns),
        normalize_df(app_developers_df, unified_columns),
    ]
    google_play_df = google_play_df.rename(columns={
            'App': 'title',
            'Rating': 'score',
            'Reviews': 'reviews',
            'Size': 'size',
            'Installs': 'installs',
            'Type': 'free',
            'Price': 'price',
            'Content Rating': 'contentRating',
            'Genres': 'genres',
            'Last Updated': 'updated',
            'Current Ver': 'version',
            'Android Ver': 'requiredOsVersion'
        })
    google_play_df['free'] = google_play_df['free']=='Free'
    dfs.append(normalize_df(google_play_df, unified_columns))
    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df.to_csv(os.path.join(out_dir, "combined_dataset.csv"), index=False)
    print(f"Combined dataset saved to {os.path.join(out_dir, 'combined_dataset.csv')}")
if __name__ == "__main__":
    os.makedirs(out_dir, exist_ok=True)
    combine_datasets()