import streamlit as st
import openai
import os
from dotenv import load_dotenv
import json

load_dotenv()  # Load environment variables from .env file

openai.api_key = os.getenv("OPENAI_API_KEY")

def load_data_from_json(filename="company_brand.json"):
    """Load data from a JSON file."""
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        return None  # File not found, return None

def save_data_to_json(data, filename="company_brand.json"):
    """Save the given data to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(data, f)


def save_markdown(data, filename="company_brand.md"):
    """Generate and save the company brand data to a Markdown file."""
    md_content = f"""# Company Brand Summary

    ## Niche
    {data['niche']}

    ## Solution Provided
    {data['Solutions']}

    ## Value Statement
    {data['value']}

    ## What Makes Our Company Different
    {data['different']}

    ## Client_avatar
    {data['client_avatar']}

    ## Avatar Narrative
    {data['avatar_narrative']}

    ## Updated Value Proposition 
    {data['updated_value_proposition']}

    ## Brand Voice 
    {data['brand_voice']}
       """
    with open(filename, 'w') as f:
        f.write(md_content)
    full_path = os.path.join(os.getcwd(), filename)
    print(f"Markdown file '{full_path}' has been created successfully.")


def summarize_text(question):
    """Summarize the given text to a specified maximum word length using OpenAI."""
    response = openai.chat.completions.create(
    model="gpt-4-1106-preview",  # or another suitable model
        messages=[
        {   "role": "system",
        "content" : "Act like an experienced marketer and brand messaging expert with a deep knowledge of human desires and what causes them to make purchasing decisions. ",
            "role":"user",
        "content": f"{question}. Ensure to add both business and personal related attributes",
        
        }
    ]
    )
    return response.choices[0].message.content


    
def collect_info():


    existing_data = load_data_from_json()
    if existing_data:
        st.session_state.company_brand = existing_data
        st.session_state.niche = st.session_state.company_brand['niche']
        st.session_state.solutions = st.session_state.company_brand['Solutions']
        st.session_state.value = st.session_state.company_brand['value']
        st.session_state.different = st.session_state.company_brand['different']
        st.session_state.client_avatar_key = st.session_state.company_brand['client_avatar'] 
        st.session_state.avatar_narrative_key = st.session_state.company_brand['avatar_narrative']
        st.session_state.updated_value_proposition_key = st.session_state.company_brand['updated_value_proposition']
 

    # Check if both keys exist in the dictionary before attempting to concatenate their values

    if st.button('Brand Voice Generation'):
        content = st.session_state.company_brand['niche'] + st.session_state.company_brand['Solutions'] + st.session_state.company_brand['value'] + st.session_state.company_brand['different'] + st.session_state.company_brand['updated_value_proposition']
        print("the content is:", content)
        brand_voice = summarize_text(f" Based on the information provided write the brand voice, {content}")
        st.text_area("Brand Voice", key="brand_voice", value=brand_voice, height= 300,)
        st.session_state.company_brand['brand_voice'] = brand_voice
        save_data_to_json(st.session_state.company_brand)  # Save the updated data to JSON
        save_markdown(st.session_state.company_brand) # Save the updated data to markdown




    existing_data = load_data_from_json()
    if existing_data:
        if 'brand_voice' in st.session_state.company_brand:
            st.session_state.company_brand = existing_data
            st.text_area("Brand Voice", key="brand_voice_reload", value=st.session_state.company_brand['brand_voice'], height=1000)

if __name__ == "__main__":
    collect_info()
    st.write("Current Session State keys are:")
    for key in st.session_state.keys():
        st.write(key)

