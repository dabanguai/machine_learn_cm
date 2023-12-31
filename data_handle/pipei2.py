import glob
import os.path

import numpy as np
import pandas as pd
base_dir_path = "D:/resource/chunmei/data/2020/era5/"
merra_dir_path = "D:/resource/chunmei/data/2020/merra2/"
modis_dir_path = "D:/resource/chunmei/data/2020/modis/"
meic_dir_path = "D:/resource/chunmei/data/2020/MEIC/"

def find_files(dir):
    matching_files = []
    for file_path in glob.glob(os.path.join(dir,'*.csv')):
        # 添加文件路径
        matching_files.append(file_path)
    return matching_files

def read_file(file_path):
    df = pd.read_csv(file_path)
    return df

if __name__ == "__main__":
    # 获取文件路径
    era5_path = find_files(base_dir_path)
    merra_path = find_files(merra_dir_path)
    modis_path = find_files(modis_dir_path)
    meic_path = find_files(meic_dir_path)
    row_avr_TOTANGSTR = []
    row_avr_TOTEXTTAU = []
    row_avr_TOTSCATAU = []

    for single_file_path in era5_path:
        # 一个基表对应一个表(前提是匹配的文件只有一个)，所以每添加完一个基表就应该让列表清空
        con_avr_TOTANGSTR = []
        con_avr_TOTEXTTAU = []
        con_avr_TOTSCATAU = []
        con_avr_ndvi = []
        con_avr_ndvi_1 = []
        df = read_file(single_file_path)
        base_filename = os.path.basename(single_file_path)
        for index,row in df.iterrows():
            # print(type(row)) <class 'str'>
            base_time = row[2]
            base_year = base_time[0:4] # <class 'str'>
            base_month = base_time[5:7]
            base_lat = row[3] #<class 'float'>
            base_lon = row[4]
            # print(type(base_year), type(base_month), base_lat, base_lon)

            time_a = pd.to_datetime(base_time,format='%Y/%m/%d %H:%M:%S')
            # merra2 b表
            # for single_merra_path in merra_path:
            #     df_merra = read_file(single_merra_path)
            #     output_data = pd.DataFrame(columns=['MERRA2_TOTANGSTR', 'MERRA2_TOTEXTTAU', 'MERRA2_TOTSCATAU'])
            #     for index,row in df_merra.iterrows():
            #         merra_time = row[2]
            #         time_b = pd.to_datetime(merra_time,format='%Y/%m/%d %H:%M:%S')
            #         # merra_year = merra_time[0:4]  # <class 'str'>
            #         # merra_month = merra_time[5:7]
            #         merra_lat = row[3]  # <class 'float'>
            #         merra_lon = row[4]
            #         merra_TOTANGSTR = row[5]
            #         merra_TOTEXTTAU = row[6]
            #         merra_TOTSCATAU = row[7]
            #         # 进行匹配比较
            #         if time_b == time_a + pd.Timedelta(minutes=30) & base_lat - 0.25 <= merra_lat & base_lat + 0.25 >= merra_lat & base_lon - 0.25 <= merra_lon & base_lon + 0.25  >= merra_lon:
            #             row_avr_TOTANGSTR.append(merra_TOTANGSTR)
            #             row_avr_TOTEXTTAU.append(merra_TOTEXTTAU)
            #             row_avr_TOTSCATAU.append(merra_TOTSCATAU)
            #
            #     #   单个文件匹配结束
            #     con_avr_TOTANGSTR.append(np.mean(row_avr_TOTANGSTR))
            #     con_avr_TOTEXTTAU.append(np.mean(row_avr_TOTEXTTAU))
            #     con_avr_TOTSCATAU.append(np.mean(row_avr_TOTSCATAU))
            #     row_avr_TOTANGSTR.clear()
            #     row_avr_TOTEXTTAU.clear()
            #     row_avr_TOTSCATAU.clear()
            #     break
            # break

            # mod13c1 c表 只有单表
            # for single_modis_path in modis_path:
            #     df_modis = read_file(single_modis_path)
            df_modis = read_file(modis_path[0])
            row_avr_ndvi = []
            row_avr_ndvi_1 = []
            for index,row_modis in df_modis.iterrows():
                modis_time = row_modis[1]
                modis_year = modis_time[0:4]
                modis_month = modis_time[5:7]
                time_c = pd.to_datetime(modis_year + '/' + modis_month)
                time_c = pd.to_datetime(time_c, format='%Y/%m/%d %H:%M:%S')
                modis_lon = row_modis[3] # <class 'numpy.float64'>
                modis_lat = row_modis[2]
                modis_ndvi = row_modis[4]
                modis_ndvi_1 = row_modis[5]
                # print(modis_year,modis_month,modis_lat,modis_lon)
                # 进行匹配比较
                if (time_c == time_a + pd.Timedelta(days=8)) & (base_lat - 0.25 <= modis_lat) & (base_lat + 0.25 >= modis_lat) & (base_lon - 0.25 <= modis_lon) & (base_lon + 0.25  >= modis_lon):
                    row_avr_ndvi.append(modis_ndvi)
                    row_avr_ndvi_1.append(modis_ndvi_1)
            if len(row_avr_ndvi) != 0:
                con_avr_ndvi.append(np.mean(row_avr_ndvi))
            elif len(row_avr_ndvi_1) != 0:
                con_avr_ndvi_1.append(np.mean(row_avr_ndvi_1))
            row_avr_ndvi.clear()
            row_avr_ndvi_1.clear()
        merge_file = pd.concat([con_avr_ndvi][con_avr_ndvi_1],axis=1)
        merge_file.to_csv(modis_dir_path+'01',index=False)
        break
            # #   meic d表
            # for single_meic_path in meic_path:
            #     df_meic = read_file(single_meic_path)
            #     for index,row_meic in df_meic.iterrows():
            #         meic_year = row_meic[0].astype(str)
            #         meic_year = meic_year[0:4]
            #         meic_month = row_meic[1]
            #         meic_month = "{:0>2}".format(int(meic_month))
            #         meic_lon = row_meic[2] # <class 'numpy.float64'>
            #         meic_lat = row_meic[3]


# 判断当前行和下一行的值是否相同
# if index + 1 < len(df_meic):
#     next_row = df_meic.iloc[index + 1]
#     next_year = next_row[0]
#     break
# break