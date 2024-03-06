import pandas as pd

def excel_to_dict(file_path, output_file):
    # 讀取 Excel 文件
    df = pd.read_excel(file_path, header=None)
    
    # 將DataFrame轉換為字典
    data_dict = dict(zip(df[0], df[1]))
    
    # 將結果寫入Python檔案
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('data_dict = ' + str(data_dict))

# 假設你有一個名為data.xlsx的Excel文件
file_path = 'N2.xlsx'
output_file = 'output.py'

# 呼叫函式將Excel資料轉換為字典並寫入Python檔案
excel_to_dict(file_path, output_file)
