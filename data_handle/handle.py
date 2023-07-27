import csv
import os
import re
import glob

import pandas as pd

# 获取文件
def find_files(dir):
    matching_files = []
    base_file = []
    # 遍历目录中的所有以“*.csv”为后缀的文件
    for file_path in glob.glob(os.path.join(dir, '*.csv')):
        # 获取文件名部分
        filename = os.path.basename(file_path)
        # 使用正则表达式匹配文件名
        if '_pipei' in filename:
            matching_files.append(file_path)
    return matching_files

# 获取基准文件
def find_base_files(dir):
    base_file = []
    # 遍历目录中的所有以“*.csv”为后缀的文件
    for file_path in glob.glob(os.path.join(dir, '*.csv')):
        # 获取文件名部分
        filename = os.path.basename(file_path)
        # 使用正则表达式匹配文件名
        if 'merge' in filename:
            base_file.append(file_path)
    return base_file
#  年份匹配
def extract_year(value):
    match = re.search(r'\d{4}', value)  # 匹配四位数字，即年份部分
    if match:
        return match.group()
    else:
        return None

# 读取文件
def read_file(file_path):
    df = pd.read_csv(file_path)
    return df

# 读取年份
def read_year(filename):
    if not filename.empty:
        read_column = filename.iloc[:, 0]
        years = read_column.apply(lambda x:extract_year(x))
        return years
# 读取经纬度
def read_loc(filename):
    if not filename.empty:
        lon = filename.iloc[:, 1]
        lat = filename.iloc[:, 2]
        return lon,lat
if __name__ == "__main__":
    dir_path = 'D:/resource/chunmei/data/'
    # 获取匹配的文件
    compare_files = find_files(dir_path)
    base_file_path = find_base_files(dir_path)[0]
    base_file = read_file(base_file_path)
    base_year = base_file.iloc[:, 0]
    base_lon = base_file.iloc[:, 2]
    base_lat = base_file.iloc[:, 3]
    for file_path in compare_files:
        # 待匹配的文件和年份
        com_file = read_file(file_path)
        com_years = read_year(com_file)
        com_lon,com_lat = read_loc(com_file)

        # print(com_file)
        print(com_lon,com_lat)
    # 获取基准文件

    # print(base_file_path)
    # print(base_file)
    # print(base_year)
    # print(base_lon)
    # print(base_lat)