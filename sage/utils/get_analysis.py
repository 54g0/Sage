import pandas as pd
import numpy as np
import os
import sys
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash",api_key=GEMINI_API_KEY)
def get_analysis_from_D2C():
    path = "data/raw/Kasparro_Phase5_D2C_Synthetic_Dataset.xlsx"
    d2c_df = pd.read_excel(path)
    d2c_df['cac'] = d2c_df['spend_usd'] / d2c_df['first_purchase']
    d2c_df['roas'] = d2c_df['revenue_usd'] / d2c_df['spend_usd']
    d2c_df['retention_rate'] = d2c_df['repeat_purchase'] / d2c_df['first_purchase']
    d2c_df.replace([np.inf, -np.inf], np.nan, inplace=True)
    high_volume_low_pos = d2c_df[(d2c_df['monthly_search_volume'] > 1000) & (d2c_df['avg_position'] > 3)]
    best_categories = high_volume_low_pos['seo_category'].value_counts().index.tolist()
    top_seo_keywords_proxy = high_volume_low_pos['seo_category'].value_counts().nlargest(3).index.tolist()

    prompt_for_creatives = f"""
    Generate 3 creative outputs for a D2C brand based on this data:
    - Top performing category: {best_categories[0] if best_categories else 'N/A'}
    - Average Customer Acquisition Cost: ${d2c_df['cac'].mean():.2f}
    - Average Return on Ad Spend: {d2c_df['roas'].mean():.2f}
    - High-potential SEO keywords: {top_seo_keywords_proxy}

    Create:
    Ad headline (under 30 chars)
    SEO meta description (under 160 chars)
    Product Detail Page (PDP) text (short paragraph)
    """
    response = llm.invoke(prompt_for_creatives)
    return response.content
if __name__ == "__main__":
    analysis = get_analysis_from_D2C()
    print(analysis)
    