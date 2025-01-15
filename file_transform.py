import json
import csv
import pandas as pd
import glob
import os

def json_to_csv_and_excel(json_file_path, csv_file_path, excel_file_path):
    # 读取 JSON 文件
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 确保列的顺序
    keys = ["名前", "内容", "評価", "サービス", "雰囲気", "食事"]
    for entry in data:
        for key in entry.keys():
            if key not in keys:
                keys.append(key)

    # 将 JSON 数据写入 CSV
    with open(csv_file_path, 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

    # 将 JSON 数据写入 Excel
    df = pd.DataFrame(data)
    df = df[keys]  # 按指定顺序重新排列列
    df.to_excel(excel_file_path, index=False)

def process_all_files(input_folder, csv_folder, excel_folder):
    # 创建输出文件夹（如果不存在）
    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)
    if not os.path.exists(excel_folder):
        os.makedirs(excel_folder)

    # 遍历输入文件夹中的所有 JSON 文件
    for json_file_path in glob.glob(os.path.join(input_folder, '*.json')):
        # 生成 CSV 和 Excel 文件的路径
        file_name = os.path.basename(json_file_path).replace('_processed.json', '')  # 去掉 _processed
        csv_file_path = os.path.join(csv_folder, f"{file_name}.csv")
        excel_file_path = os.path.join(excel_folder, f"{file_name}.xlsx")

        # 调用转换函数
        json_to_csv_and_excel(json_file_path, csv_file_path, excel_file_path)
        print(f"Processed: {json_file_path} -> {csv_file_path}, {excel_file_path}")

# 使用示例
input_folder = 'processed_datas'  # 输入文件夹路径
csv_folder = 'csv'  # CSV 输出文件夹路径
excel_folder = 'excel'  # Excel 输出文件夹路径
process_all_files(input_folder, csv_folder, excel_folder)