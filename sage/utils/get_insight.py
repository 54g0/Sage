import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from typing import Dict, List
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from sage.ingestion.app_store_ingestor import AppStoreIngestor
from dotenv import load_dotenv
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
data_dir = "sage/app/data/processed/google_play_cleaned.csv"
ingestor = AppStoreIngestor()
def get_insights(selected_category, custom_query, custom_query_1):
    gpd = pd.read_csv(data_dir)
    filtered_df = gpd[gpd['Category'] == selected_category]
    insights = {
        "selected_category": selected_category,
        "total_apps": len(filtered_df),
        "avg_rating": float(filtered_df['Rating'].mean()),
        "top_rated_apps": filtered_df.sort_values('Rating', ascending=False).head(5).to_dict('records'),
        "top_installed_apps": filtered_df.sort_values('Installs', ascending=False).head(5).to_dict('records'),
    }
    if custom_query and custom_query_1:
        top_ios_apps = ingestor.get_list_by_collections_genre(custom_query, custom_query_1)
        insights["top_ios_apps"] = top_ios_apps
    prompt = f"you are a market research analyst. provide the insights for this data: {insights}"
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=os.getenv("GEMINI_API_KEY"))
    llm_response = llm.invoke(prompt)
    llm_response_1 = llm_response
    prompt_2 = f"generate a comprehensive market intelligence report based on these insights: {insights}. the response must be in markdown format."
    llm_response_3 = llm.invoke(prompt_2)
    return insights,llm_response_1.content,llm_response_3.content

if __name__ == "__main__":
    insights, llm_response_1, llm_response_3 = get_insights("COMICS", "top-free", "books")
    print(llm_response_1)