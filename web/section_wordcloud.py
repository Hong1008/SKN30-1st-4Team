import streamlit as st
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

def section_wordcloud(selected_year):
  image_path = BASE_DIR / "domain" / "crawling" / f"{selected_year}.jpg"
  if not image_path.exists():
    return
  st.image(str(image_path), caption=f"{selected_year} 워드클라우드")
