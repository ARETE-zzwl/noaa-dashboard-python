import os
import kaggle

# 下载数据集

# 解压缩数据集（确保已安装 unzip）
import zipfile

with zipfile.ZipFile('dataset-name.zip', 'r') as zip_ref:
    zip_ref.extractall('./data')

# 列出解压缩后的文件
data_path = './data/gsod_all_years'  # 根据实际路径修改
yearfiles = os.listdir(data_path)

print(yearfiles)
