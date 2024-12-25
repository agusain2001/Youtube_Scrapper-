import csv

def save_to_csv(filepath, data, headers):
    """Saves the data to a CSV file."""
    try:
        with open(filepath, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
        print(f"Data successfully saved to {filepath}")
    except Exception as e:
         print(f"Error saving to CSV: {e}")