import json
import csv
import ast
import os

def convert_mcc_codes():
    output_path = 'seeds/mcc_codes.csv'
    
    if os.path.exists(output_path):
        print(f"✅ {output_path} already exists - skipping")
        return
    
    print("🔄 Converting mcc_codes.json to CSV...")
    with open('json_data/mcc_codes.json', 'r') as f:
        data = json.load(f)

    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['mcc_code', 'description'])
        for code, description in data.items():
            writer.writerow([code, description])

    print(f"{output_path} created with {len(data)} rows!")

def convert_fraud_labels():
    output_path = 'seeds/train_fraud_labels.csv'
    
    if os.path.exists(output_path):
        print(f"{output_path} already exists - skipping")
        return

    print("🔄 Converting train_fraud_labels.json to CSV...")
    with open('json_data/train_fraud_labels.json', 'r') as f:
        raw = json.load(f)

    rows = []
    for key, value in raw.items():
        if isinstance(value, str) and value.startswith('{'):
            nested = ast.literal_eval(value)
            for txn_id, label in nested.items():
                rows.append([txn_id, label])
        elif isinstance(value, dict):
            for txn_id, label in value.items():
                rows.append([txn_id, label])
        else:
            rows.append([key, value])

    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['transaction_id', 'is_fraud'])
        writer.writerows(rows)

    print(f"{output_path} created with {len(rows)} rows!")

if __name__ == "__main__":
    # Make sure seeds directory exists
    os.makedirs('seeds', exist_ok=True)
    
    convert_mcc_codes()
    convert_fraud_labels()
    
    print("\nAll seed files ready!")