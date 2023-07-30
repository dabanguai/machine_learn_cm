# 为了简化逻辑，选择不循环文件夹，而是手动添加文件
import pandas as pd
import numpy as np
# 基础的文件夹路径
base_dir_path = "D:/resource/chunmei/data/2020/era5/"
merra_dir_path = "D:/resource/chunmei/data/2020/merra2/"
modis_dir_path = "D:/resource/chunmei/data/2020/modis/"
meic_dir_path = "D:/resource/chunmei/data/2020/MEIC/"

if __name__ == "__main__":
    # 获取单个文件路径
    base_file_01 = base_dir_path+"Read_ERA5_2020_01_month_CSJ_1.csv"
    merra_file_01 = merra_dir_path+"merge_MERRA2_202001.csv"

    # 读取文件
    df_base = pd.read_csv(base_file_01)
    df_merra = pd.read_csv(merra_file_01)

    # 创建空列表，以存储匹配并处理后的数据
    # 每个基表文件 都需要 生成单个对应的表
    con_avr_TOTANGSTR = []
    con_avr_TOTEXTTAU = []
    con_avr_TOTSCATAU = []
    con_avr_ndvi = []
    con_avr_ndvi_1 = []
    row_avr_TOTANGSTR = []
    row_avr_TOTEXTTAU = []
    row_avr_TOTSCATAU = []

    #对基表进行遍历，进行for循环的嵌套，使基表单条数据可以匹配整个待匹配文件
    for index, row in df_base.iterrows():
        # print(type(row)) <class 'str'>
        # 针对不同的待匹配表，需要对 “时间” 做不同处理
        # 当匹配表 b,c时，需要以datetime 匹配d表时，需要把年月分开成两个条件匹配
        base_time = row[2]
        base_year = base_time[0:4]  # <class 'str'>
        base_month = base_time[5:7]
        base_lat = row[3]  # <class 'float'>
        base_lon = row[4]
        time_base = pd.to_datetime(base_time, format='%Y/%m/%d %H:%M:%S')
        for index, row_merra in df_merra.iterrows():
            merra_time = row_merra[2]
            time_merra = pd.to_datetime(merra_time,format='%Y/%m/%d %H:%M:%S')
            # merra_year = merra_time[0:4]  # <class 'str'>
            # merra_month = merra_time[5:7]
            merra_lat = row_merra[3]  # <class 'float'>
            merra_lon = row_merra[4]
            merra_TOTANGSTR = row_merra[5]
            merra_TOTEXTTAU = row_merra[6]
            merra_TOTSCATAU = row_merra[7]
            # print(row_merra)
            # print(time_merra,merra_lat,merra_lon,merra_TOTANGSTR,merra_TOTEXTTAU,merra_TOTSCATAU)
            # print(type(time_merra),type(time_base),type(base_lat),type(merra_lat),type(base_lon),type(merra_lon))
            # 进行匹配比较
            if (time_merra == time_base + pd.Timedelta(minutes=30)) & (base_lat - 0.25 <= merra_lat) & (base_lat + 0.25 >= merra_lat) & (base_lon - 0.25 <= merra_lon) & (base_lon + 0.25  >= merra_lon):
                row_avr_TOTANGSTR.append(merra_TOTANGSTR)
                row_avr_TOTEXTTAU.append(merra_TOTEXTTAU)
                row_avr_TOTSCATAU.append(merra_TOTSCATAU)
            # print(row_avr_TOTSCATAU)
        #  基表单条匹配结束 基表一条可能对应待匹配表中多条数据，需要取平均值再加到另一个列表中
        # 可能出现 基表单条 匹配不到数据，不可以做取平均值处理。
        if len(row_avr_TOTANGSTR) != 0:
            con_avr_TOTANGSTR.append(np.mean(row_avr_TOTANGSTR))
        elif len(row_avr_TOTEXTTAU) != 0:
            con_avr_TOTEXTTAU.append(np.mean(row_avr_TOTEXTTAU))
        elif len(row_avr_TOTSCATAU) != 0:
            con_avr_TOTSCATAU.append(np.mean(row_avr_TOTSCATAU))
        # print(con_avr_TOTSCATAU)
        row_avr_TOTANGSTR.clear()
        row_avr_TOTEXTTAU.clear()
        row_avr_TOTSCATAU.clear()
    merge_file = pd.concat([con_avr_TOTANGSTR][con_avr_TOTEXTTAU],[con_avr_TOTSCATAU], axis=1)
    merge_file.to_csv(base_file_01+"ed", index=False)
    print("finished")