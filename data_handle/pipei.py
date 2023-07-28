import glob
import os.path
import numpy as np
import pandas as pd
from datetime import datetime
base_dir_path = "D:/resource/chunmei/data/2020/era5/"
merra_dir_path = "D:/resource/chunmei/data/2020/merra2/"
modis_dir_path = "D:/resource/chunmei/data/2020/modis/"
meic_dir_path = "D:/resource/chunmei/data/2020/MEIC/"

# 获取文件路径
def find_files(dir):
    matching_files = []
    for file_path in glob.glob(os.path.join(dir,'*.csv')):
        # 获取文件名部分
        # file_name = os.path.basename(file_path)
        # print(file_name)

        # 添加文件路径
        matching_files.append(file_path)
    return matching_files

# 读取文件
def read_file(file_path):
    df = pd.read_csv(file_path)
    return df

# 读取时间
def read_time(file_path):
    df = pd.read_csv(file_path)
    if not df.empty:
        if 'ERA5' or 'MERRA2' in file_path:
            read_base_time = df.iloc[:,2]
        if 'MEIC' in file_path:
            read_base_year = df.iloc[:,0]
            read_base_month = df.iloc[:,1]
            # print(type(read_base_year),type(read_base_month))
            read_base_time = pd.to_datetime(read_base_year.astype(str)+'/' + read_base_month.astype(str))
            # print(read_base_time)
    return read_base_time

# 读取经纬度
def read_loc(file_path):
    df = pd.read_csv(file_path)
    if not df.empty:
        if 'ERA5' or 'MERRA2' in file_path:
            read_base_lat = df.iloc[:,3]
            read_base_lon = df.iloc[:,4]
        if 'MEIC' in file_path:
            read_base_lon = df.iloc[:,2]
            read_base_lat = df.iloc[:,3]
    return read_base_lat,read_base_lon


# 处理基表和merra2表
def comper_b (path_a,path_b):
    df_a = read_file(path_a)
    df_b = read_file(path_b)
i = 0
# main函数
if __name__ == "__main__":
    # 获取所有文件路径
    era5_path = find_files(base_dir_path)
    merra_path = find_files(merra_dir_path)
    modis_path = find_files(modis_dir_path)
    meic_path = find_files(meic_dir_path)

    # 作匹配

    for single_file_path in era5_path:
        # print(single_file_path) # D:/resource/chunmei/data/2020/era5\Read_ERA5_2020_01_month_CSJ_1.csv
        base_time_list = read_time(single_file_path)
        base_lat_list, base_lon_list = read_loc(single_file_path)
        for i in range(len(base_time_list)):
            # 获取到基表每一条时间
            base_time = base_time_list[i]
            base_year = base_time[0:4]
            base_month = base_time[5:7]
            # 每一条经纬度
            base_lat = base_lat_list[i]
            base_lon = base_lon_list[i]
            # print(base_time,base_year,base_month,base_lat,base_lon) 2020-01-01 00:00:00 2020 01 33.5 118.0

            # 读取到 待匹配文件
            for meic_file_path in meic_path:
                # print(meic_file_path) D:/resource/chunmei/data/2020/MEIC\merge_MEIC_LATLON.csv
                # meic_year = read_time(meic_file_path) # 2016/01 <class 'pandas.core.series.Series'>
                # meic_month = read_time(meic_file_path)[1] # 2016/01

                # 时间数据
                meic_time = read_time(meic_file_path)
                # 经纬度数据
                meic_lat_list,meic_lon_list = read_loc(meic_file_path)

                for j in range(len(meic_time)):
                    # print(type(time_row)) <class 'pandas._libs.tslibs.timestamps.Timestamp'>
                    meic_time_row = meic_time[j]
                    meic_time_row = meic_time_row.strftime("%Y/%m") # 转成str类型
                    meic_year = meic_time_row[0:4]
                    meic_month = meic_time_row[5:7]
                    meic_lat = meic_lat_list[j]
                    meic_lon = meic_lon_list[j]
                    if base_year == meic_year and base_month == meic_month and base_lat-0.25<=meic_lat and base_lat+0.25>=meic_lat and base_lon-0.25<=meic_lon and base_lon+0.25>=meic_lon:
                        pass

