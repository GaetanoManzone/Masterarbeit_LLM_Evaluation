import pandas as pd
import json

# Load the Excel file
file_path = '/Users/gaetanomanzone/Desktop/final_all_texts_aligned.xlsx'
excel_data = pd.read_excel(file_path)

# Specifying the path for the JSONL file to be saved
jsonl_file_path = '/Users/gaetanomanzone/Desktop/request_GEMBA_best_practice_SQM.jsonl'

# Create a .jsonl file to write into
with open(jsonl_file_path, 'w') as jsonl_file:
    for index, row in excel_data.iterrows():
        # Construct the dictionary for each request
        request_data = {
            "custom_id": f"request-{index + 1}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": "gpt-4-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": "Score the following translation from English to German with respect to the human reference on a continuous scale from 0 to 100 that starts with \"No meaning preserved\", goes through \"Some meaning preserved\", then \"Most meaning preserved and few grammar mistakes\", up to \"Perfect meaning and grammar\"."
                    },
                    {
                        "role": "user",
                        "content": f"English source: \"{row['Source']}\"\nGerman human reference: \"{row['Reference']}\"\nGerman translation: \"{row['Best_Practice']}\"\nScore (0−100):"
                    }
                ],
                "max_tokens": 1000
            }
        }
        # Write the dictionary to the .jsonl file as a json string
        jsonl_file.write(json.dumps(request_data) + '\n')
