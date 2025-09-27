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
data_dir = "data/processed/google_play_cleaned.csv"
out_dir = "sage/outputs"
os.makedirs(out_dir, exist_ok=True)
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
    llm_response_2 = llm_response
    try:
        parsed_response = json.loads(llm_response_1.content)
        json_filename = os.path.join(out_dir, f"insights_{selected_category.lower().replace(' ', '_')}.json")
        with open(json_filename, "w") as f:
            json.dump(parsed_response, f, indent=2)
        print(f"✅ Saved JSON to: {json_filename}")
    except Exception as e:
        text_filename = os.path.join(out_dir, f"insights_{selected_category.lower().replace(' ', '_')}.txt")
        with open(text_filename, "w") as f:
            f.write(llm_response.content)
        print(f"📝 Saved raw response to: {text_filename} (not valid JSON)")

    prompt_2 = f"generate a comprehensive market intelligence report based on these insights: {insights}. the response must be in markdown format."
    llm_response_3 = llm.invoke(prompt_2)
    with open(f"{out_dir}/market_intelligence_report_{selected_category.lower().replace(' ', '_')}.md", "w") as f:
        f.write(llm_response_3.content)
    return insights,llm_response_2.content

if __name__ == "__main__":
    insights, llm_response = get_insights("COMICS", "top-free", "books")
    print(llm_response) 