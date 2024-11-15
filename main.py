import streamlit as st
from scrape import scrape_website, extract_body_content, clean_body_content, split_dom_content
from parse import parse_with_ollama
st.title('AI web scrapper')
st.write('This is a simple web scrapper that uses AI to Scrape')
url=st.text_input('Enter the URL')
if st.button('Scrape Site'):
  st.write("Scraping the site...")
  dom_content=scrape_website(url)
  # print(dom_content)
  body_content=extract_body_content(dom_content)
  cleaned_content=clean_body_content(body_content)
  st.session_state.dom_content=cleaned_content

  with st.expander('view dom content'):
    st.text_area('DOM content', cleaned_content, height=300)

if "dom_content" in st.session_state:
  parse_description=st.text_area('what you want to parse', 'description')
  if st.button('Parse'):
    if parse_description:
      st.write('Parsing the content...')
      dom_chunks=split_dom_content(st.session_state.dom_content)
      result = parse_with_ollama(dom_chunks, parse_description)
      st.write(result)