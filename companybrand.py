import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai
import os
from dotenv import load_dotenv
import time 
import json
import os   
import glob

load_dotenv()  # Load environment variables from .env file

openai.api_key = os.getenv("OPENAI_API_KEY")

def save_data_to_json(data, filename="company_brand.json"):
    """Save the given data to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(data, f)

def load_data_from_json(filename="company_brand.json"):
    """Load data from a JSON file."""
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        return None  # File not found, return None
    
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
       """
    with open(filename, 'w') as f:
        f.write(md_content)
    full_path = os.path.join(os.getcwd(), filename)
    print(f"Markdown file '{full_path}' has been created successfully.")




if "company_brand" not in st.session_state:
    st.session_state.company_brand = None


def scrape_website(url):
    """Scrape website content from the given URL."""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extracting text from the webpage; this might need adjustments
        # depending on the website's structure
        text = ' '.join(p.get_text() for p in soup.find_all('p'))
        return text
    except Exception as e:
        return f"An error occurred: {e}"
    

def summarize_text(question, text):
    """Summarize the given text to a specified maximum word length using OpenAI."""
    response = openai.chat.completions.create(
    model="gpt-4-1106-preview",  # or another suitable model
        messages=[
        {   "role": "system",
        "content" : "Act like a high level  marketer and sales expert withh a deep knowledge of human desires and what causes them to make purchasing decisions. Please answer the following questions with the avaliable information.",
            "role":"user",
        "content": f"Based on information {text}. {question}. ",
        
        }
    ]
    )
    return response.choices[0].message.content

# Streamlit app
def main():
    #load json data
    existing_data = load_data_from_json()
    if existing_data:
        st.session_state.company_brand = existing_data
        #Create the key variable within session state.company_brand
        st.text_area("Niche", key="niche", value=st.session_state.company_brand['niche'])
        st.text_area("Solutions", key="solutions", value=st.session_state.company_brand['Solutions'])
        st.text_area("Value", key="value", value=st.session_state.company_brand['value'])
        st.text_area("Different", key="different", value=st.session_state.company_brand['different'])

    st.title('Social Media')
    content = ""    
    # User choice for input type
    name = st.text_input("Enter your company name")
    product_service = st.text_input("Enter the product or service your company offers")
    website_url = st.text_input("Enter the website URL to summarize:")
    if website_url:
        with st.spinner('Scraping website content...'):
            content = scrape_website(website_url) + " " + name + " " + product_service
            if not content:
                st.error("Failed to scrape the website or the website is empty.")


    if st.button('Summarize'):
        with st.spinner('Creating you company brand...'):        
            time.sleep(10) #External API calls requires time to retrieve back.
            
        if content and content.strip():
            with st.spinner('Creating you company brand...'):
                niche = summarize_text("the company niche is? Reply in a sales & marketing perspective in the tone of the company. Answer in one sentence", content)
                Solutions = summarize_text("What are the solutions that the company offers? Reply in a sales & marketing perspective in the tone of the company. Answer in one sentence", content)
                value= summarize_text("We help xxx to xxx so that they xxx without . We do this using our (method). Reply in a sales & marketing perspective in the tone of the company. Answer in one sentence", content)
                different = summarize_text("What makes the company different from the competition? Reply in a sales & marketing perspective in the tone of the company. Answer in one sentence", content)
                st.text_area("Niche", value=niche, height=150)
                st.text_area("Solution Provided", value=Solutions, height=150)
                st.text_area("Value Statement", value=value, height=150)
                st.text_area("What makes your company different", value=different, height=150)
                # Save the results to the session state
                st.session_state.company_brand = {"niche": niche, "Solutions": Solutions, "value": value, "different": different}
                save_data_to_json(st.session_state.company_brand)  # Save the updated data to JSON
                save_markdown(st.session_state.company_brand) # Save the updated data to markdown
                # Using the .values() method to get the values
                values_list = list(st.session_state.company_brand.values())
                # Printing the list of values
                print(values_list)
                if "company_brand" in st.session_state and st.session_state.company_brand:
                    if st.button('Update'):
                        st.session_state.company_brand = {"niche": niche, "Solutions": Solutions, "value": value, "different": different}
                        save_data_to_json(st.session_state.company_brand)  # Save the updated data to JSON
                        save_markdown(st.session_state.company_brand) # Save the updated data to markdown
                        values_list = list(st.session_state.company_brand.values())
                        # Printing the list of values
                        print(values_list)
                        st.text(values_list)

         


        else:   
            st.error("Please enter a valid URL or text to summarize.")

  

if __name__ == "__main__":

    main()
