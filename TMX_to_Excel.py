# Source of the code: https://medium.com/@said.surucu/step-by-step-guide-to-converting-tmx-files-to-excel-using-python-c4dc72ef0875

import sys
import os
from lxml import etree
import pandas as pd

# Get the input file name from the command line arguments
input_file = os.path.basename(sys.argv[1:][0])

# Create an empty DataFrame with specified columns and data type as string
df = pd.DataFrame(columns=["Source", "Target"], dtype="string")

# Parse the XML file into a tree structure
xml_tree = etree.parse(input_file)

# Find all translation units (tu elements) in the XML tree
trans_units = xml_tree.findall(".//tu")

# Initialize empty lists to store source and target texts
source_texts = []
target_texts = []

# Iterate over each translation unit
for trans_unit in trans_units:
    # Find the first two 'tuv' elements within the translation unit
    tuv1 = trans_unit.findall(".//tuv")[0]
    tuv2 = trans_unit.findall(".//tuv")[1]
    # Find the 'seg' elements within each 'tuv' element
    source = tuv1.findall(".//seg")[0]
    target = tuv2.findall(".//seg")[0]

    # Extract text content from each 'seg' element
    source_text = ''.join(source.itertext())
    target_text = ''.join(target.itertext())

    # Append the extracted texts to the respective lists
    source_texts.append(source_text)
    target_texts.append(target_text)

# Populate the DataFrame with the collected source and target texts
df["Source"] = source_texts
df["Target"] = target_texts

# Save the DataFrame to an Excel file with a name based on the input file
df.to_excel("TMX_" + os.path.splitext(input_file)[0] + ".xlsx",index=False)