import os
import pandas as pd
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
data_dir = "data/raw"
out_dir = "data/processed"
# def preprocess_search_result(df:pd.DataFrame):
#     search_result = df.drop(columns=["icon","genreIds","primaryGenre","primaryGenreId","languages",'developerUrl', 'developerWebsite','screenshots','ipadScreenshots', 'appletvScreenshots'], axis=1)
#     file_path = os.path.join(RAW_DATA_DIR, "search_results_cleaned.csv")
#     os.makedirs(out_dir, exist_ok=True)
#     if not os.path.exists(file_path):
#         search_result.to_csv(file_path,index=False,header=True)
#     else:
#         search_result.to_csv(file_path,mode="a",header=False,index=False)
# def preprocess_app_collections(df:pd.DataFrame):
#     app_collections = df.drop(columns=["developerUrl","genreId"], axis=1)
#     file_path = os.path.join(out_dir, "app_collections_cleaned.csv")
#     os.makedirs(out_dir, exist_ok=True)
#     if not os.path.exists(file_path):
#         app_collections.to_csv(file_path,index=False,header=True)
#     else:
#         app_collections.to_csv(file_path,mode="a",header=False,index=False)
# def preprocess_app_details(df:pd.DataFrame):
#     app_details = df.drop(columns=["icon","genreIds","primaryGenre","primaryGenreId","languages",'developerUrl', 'developerWebsite','screenshots','ipadScreenshots', 'appletvScreenshots'], axis=1)
#     file_path = os.path.join(out_dir, "app_details_cleaned.csv")
#     os.makedirs(out_dir, exist_ok=True)
#     if not os.path.exists(file_path):
#         app_details.to_csv(file_path,index=False,header=True)
#     else:
#         app_details.to_csv(file_path,mode="a",header=False,index=False)
# def preprocess_app_developers(df:pd.DataFrame):
#     app_developers = df.drop(columns=["icon","genreIds","primaryGenre","primaryGenreId","languages",'developerUrl', 'developerWebsite','screenshots','ipadScreenshots', 'appletvScreenshots'], axis=1)
#     file_path = os.path.join(out_dir, "app_developers_cleaned.csv")
#     os.makedirs(out_dir, exist_ok=True)
#     if not os.path.exists(file_path):
#         app_developers.to_csv(file_path,index=False,header=True)
#     else:
#         app_developers.to_csv(file_path,mode="a",header=False,index=False)

def preprocess_asd():
    search_result = pd.read_csv(os.path.join(data_dir, 'search_results.csv'))
    app_collections = pd.read_csv(os.path.join(data_dir, 'app_collections.csv'))
    app_details = pd.read_csv(os.path.join(data_dir, 'app_details.csv'))
    app_developers = pd.read_csv(os.path.join(data_dir, 'app_developers.csv'))
    search_result = search_result.drop(columns=["icon","genreIds","primaryGenre","primaryGenreId","languages",'developerUrl', 'developerWebsite','screenshots','ipadScreenshots', 'appletvScreenshots'], axis=1)
    app_developers = app_developers.drop(columns=["icon","genreIds","primaryGenre","primaryGenreId","languages",'developerUrl', 'developerWebsite','screenshots','ipadScreenshots', 'appletvScreenshots'], axis=1)
    app_details = app_details.drop(columns=["icon","genreIds","primaryGenre","primaryGenreId","languages",'developerUrl', 'developerWebsite','screenshots','ipadScreenshots', 'appletvScreenshots'], axis=1)
    app_collections = app_collections.drop(columns=["developerUrl","genreId"], axis=1)
    search_result.to_csv(os.path.join(out_dir, 'search_results_cleaned.csv'), index=False)
    app_collections.to_csv(os.path.join(out_dir, 'app_collections_cleaned.csv'), index=False)
    app_details.to_csv(os.path.join(out_dir, 'app_details_cleaned.csv'), index=False)
    app_developers.to_csv(os.path.join(out_dir, 'app_developers_cleaned.csv'), index=False)
    print(f"Preprocessed data saved to {out_dir}")
if __name__ == "__main__":
    os.makedirs(out_dir, exist_ok=True)
    preprocess_asd()