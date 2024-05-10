import pandas as pd
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Load CSV file
df = pd.read_csv('gyg_data.csv')

# Fill NaN values in "description" column with an empty string
df['description'] = df['description'].fillna('')

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained('ml6team/keyphrase-generation-t5-small-inspec')
model = AutoModelForSeq2SeqLM.from_pretrained('ml6team/keyphrase-generation-t5-small-inspec')

# Define function to extract keywords
def extract_keywords(text):
    # Check if the input is a string
    if isinstance(text, str):
        encoded_input = tokenizer(text, padding=True, truncation=True, return_tensors='pt')
        outputs = model.generate(encoded_input['input_ids'], num_beams=4, max_length=50, early_stopping=True)
        keywords = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return keywords
    else:
        return None  # Return None or some default value for non-string inputs

# Apply function to "description" column to create "keywords" column
df['keywords'] = df['description'].apply(extract_keywords)

# Print DataFrame
print(df)

# Save DataFrame back to CSV
df.to_csv('gyg_data.csv', index=False)