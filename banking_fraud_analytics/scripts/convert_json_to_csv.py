import json
import csv
import ast

# Convert mcc_codes.json
with open('json_data/mcc_codes.json', 'r') as f:
    data = json.load(f)

with open('seeds/mcc_codes.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['mcc_code', 'description'])
    for code, description in data.items():
        writer.writerow([code, description])

print("mcc_codes.csv created!")

# Convert train_fraud_labels.json
with open('json_data/train_fraud_labels.json', 'r') as f:
    raw = json.load(f)

# Handle nested structure
with open('seeds/train_fraud_labels.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['transaction_id', 'is_fraud'])
    
    for key, value in raw.items():
        # If value is a dict string like "{'10649266': 'No', ...}"
        if isinstance(value, str) and value.startswith('{'):
            nested = ast.literal_eval(value)
            for txn_id, label in nested.items():
                writer.writerow([txn_id, label])
        # If value is already a dict
        elif isinstance(value, dict):
            for txn_id, label in value.items():
                writer.writerow([txn_id, label])
        # If value is just Yes/No directly
        else:
            writer.writerow([key, value])

print("train_fraud_labels.csv created!")