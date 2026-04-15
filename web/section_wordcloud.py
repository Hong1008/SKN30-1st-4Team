import streamlit as st

def section_wordcloud(year):
  st.subheader("워드 클라우드")
  st.markdown(
      "<div style='height:300px; display:flex; align-items:center; justify-content:center;"
      " border:2px dashed #aaa; border-radius:8px; color:#aaa;'>워드 클라우드 이미지 자리</div>",
      unsafe_allow_html=True
  )
