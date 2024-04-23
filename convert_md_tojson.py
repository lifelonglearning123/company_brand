import json

def md_to_json(md_filepath, json_filepath):
    with open(md_filepath, 'r', encoding='utf-8') as md_file:
        lines = md_file.readlines()

    json_data = {}
    current_key = None
    for line in lines:
        # Detect headings to use as JSON keys
        if line.startswith("##"):
            # If there was a previous key, join its list of lines into one string
            if current_key is not None:
                json_data[current_key] = "\n".join(json_data[current_key]).strip()
            current_key = line.strip("# \n")
            json_data[current_key] = []
        elif current_key is not None:
            json_data[current_key].append(line)

    # Ensure the last key-value pair is also properly joined
    if current_key is not None:
        json_data[current_key] = "\n".join(json_data[current_key]).strip()

    # Save the constructed dictionary as JSON
    with open(json_filepath, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, indent=4)

    print("JSON file has been created successfully.")

# Example usage
md_to_json("company_profile.md", "reconstructed_company_profile.json")
