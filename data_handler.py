import json
import glob
import os

def process_addition(data):
    for entry in data:
        if 'Addition' in entry:
            addition = entry['Addition']
            
            for key in ["サービス", "食事", "雰囲気"]:
                start_index = addition.find(f"<b>{key}:</b>")
                if start_index != -1:
                    start_index += len(f"<b>{key}:</b>")
                    end_index = addition.find("</span>", start_index)
                    if end_index != -1:
                        value = addition[start_index:end_index].strip()
                        entry[key] = value

            del entry['Addition']

            for key in ["サービス", "食事", "雰囲気"]:
                if key in entry:
                    addition = addition.replace(f"<b>{key}:</b> {entry[key]}", "")

    return data

def process_files(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_path in glob.glob(os.path.join(input_folder, '*.json')):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        processed_data = process_addition(data)
        
        file_name = os.path.basename(file_path)  
        processed_file_name = file_name.replace('.json', '_processed.json')  
        processed_file_path = os.path.join(output_folder, processed_file_name) 
        
        with open(processed_file_path, 'w', encoding='utf-8') as processed_file:
            json.dump(processed_data, processed_file, ensure_ascii=False, indent=4)
        
        print(f"Processed and saved: {processed_file_path}")

input_folder = 'datas'  
output_folder = 'processed_datas'  
process_files(input_folder, output_folder)