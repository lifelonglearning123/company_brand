import json

def load_data_from_json(filename="company_brand.json"):
    """Load data from a JSON file."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print("File not found.")
        return None

# Load JSON data directly into a Python dictionary
data = load_data_from_json()
if data is not None:
    print("This is the json data:")
    print(data)

    # Start formatting the Markdown content
    md_content = "# Company Profile\n\n"

    # Loop through each key-value pair in the data and format it into Markdown
    for key, value in data.items():
        md_content += f"## {key.replace('_', ' ').title()}\n{value}\n\n"

    # Save the Markdown content to a file
    with open("company_profile.md", "w", encoding="utf-8") as md_file:
        md_file.write(md_content)

    print("Markdown file has been created successfully.")
else:
    print("Failed to load JSON data.")
