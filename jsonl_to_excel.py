import pandas as pd
import json
import re

# Initialize an empty list to store the extracted information
extracted_data = []
# Initialize a list to store request_ids with undetectable scores for the subsequent manual check
undetected_scores_request_ids = []

# Set the file path to the JSON file
file_path = "/Users/gaetanomanzone/Desktop/GEMBA/Scalar/JSONL SQM output files/batch_I9E53cCk8gUjlc3buWuqIGog_output_few_shot.jsonl"

with open(file_path, 'r') as file:
    for line in file:
        # Parse the JSON object from each line
        json_line = json.loads(line)

        # Extract the request_id and assistant content
        request_id = json_line["custom_id"]
        content = json_line["response"]["body"]["choices"][0]["message"]["content"]
        full_response = json_line["response"]["body"]["choices"][0]["message"]["content"]

        # Use regular expressions to find scores (GEMBA) or categories (KPE-CoT) in the text - the regex can be adapted depending on the metric
        score_pattern = r"(?i)(?:score:? (\b\d{1,2}\b|\b100\b)/?100?|score of (\b\d{1,2}\b|\b100\b)(/100)?|\*\*(\b\d{1,2}\b|\b100\b)\*\*|\b(\b\d{1,2}\b|\b100\b)\b|(\b\d{1,2}\b|\b100\b)/100|Score: (\b\d{1,2}\b|\b100\b)|\((\b\d{1,2}\b|\b100\b)\))"
        match = re.search(score_pattern, content, re.IGNORECASE)

        if match:
            # Extract the first group that matches (there could be more due to the pattern structure)
            score = [m for m in match.groups() if m][0]
            extracted_data.append((request_id, score, full_response))
        else:
            # If no score is found, add the request_id to the list for manual review
            extracted_data.append((request_id, full_response))
            undetected_scores_request_ids.append(request_id)

# Create a DataFrame with the extracted data
df = pd.DataFrame(extracted_data, columns=['Request_ID', 'GEMBA_score', "full_response"])

# Export the DataFrame to an Excel file
excel_path = ("/Users/gaetanomanzone/Desktop/GEMBA/Scalar/Scores SQM/GEMBA_few_shot.xlsx")
df.to_excel(excel_path, index=False, engine='openpyxl')

print(f'Data has been exported to {excel_path}.')

# Print the request_ids for which the scores could not be detected
if undetected_scores_request_ids:
    print("Could not find scores for the following request IDs:")
    for request_id in undetected_scores_request_ids:
        print(request_id)