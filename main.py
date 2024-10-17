import numpy as np
import pandas as pd
from plotly.offline import iplot, init_notebook_mode
import plotly.graph_objs as go
import tarfile
import gzip
import re
import os
import datetime as dt
import kaggle  # 添加Kaggle接口的库

# 初始化 Plotly
init_notebook_mode(connected=True)

# year_num: 考虑的过去年份数量，extremes_num: 显示的最热和最冷的站点数
year_num = 20
extremes_num = 10

# 使用Kaggle API从Kaggle上下载 NOAA GSOD 数据集
os.system('kaggle datasets download -d noaa/noaa-global-surface-summary-of-the-day')
os.system('unzip noaa-global-surface-summary-of-the-day-gsod.zip -d ../input/gsod_all_years')

# 获取所有年份的数据文件并排序，只取最近 year_num 年的数据
yearfiles = os.listdir("../input/gsod_all_years")
yearfiles.sort()
yearfiles = yearfiles[-year_num:]
years = [int(re.findall('\d+', yearfile)[0]) for yearfile in yearfiles]

# 读取站点的位置信息
station_loc = pd.read_csv('../input/isd-history.csv')
station_loc = station_loc.replace([0.0, -999.0, -999.9], np.nan)
station_loc = station_loc[pd.notnull(station_loc['LAT']) & pd.notnull(station_loc['LON'])]
station_loc = station_loc[[int(re.findall('^\d{4}', str(end_year))[0]) == max(years) for end_year in station_loc['END']]]
station_loc = station_loc[[int(re.findall('^\d{4}', str(beg_year))[0]) <= min(years) for beg_year in station_loc['BEGIN']]]
station_loc['LBL'] = station_loc[['STATION NAME', 'STATE', 'CTRY']].apply(lambda x: x.str.cat(sep=', '), axis=1)
station_loc['ELEV_LBL'] = station_loc['ELEV(M)'].apply(lambda x: 'Elevation: ' + str(x) + ' m' if ~np.isnan(x) else np.nan)
station_loc['LBL'] = station_loc[['LBL', 'ELEV_LBL']].apply(lambda x: x.str.cat(sep='<br>'), axis=1)
station_loc = station_loc.drop(['STATION NAME', 'STATE', 'ELEV_LBL', 'ICAO', 'BEGIN', 'END'], axis=1)

df = pd.DataFrame([])
df_day = pd.DataFrame([])

# 预处理站点文件内容的函数
def preprocess_station_file_content(content):
    headers = content.pop(0)
    headers = [headers[ind] for ind in [0, 1, 2, 3, 4, 8, 11, 12]]
    for d in range(len(content)):
        content[d] = [content[d][ind] for ind in [0, 1, 2, 3, 5, 13, 17, 18]]
    content = pd.DataFrame(content, columns=headers)
    content.rename(columns={'STN---': 'USAF'}, inplace=True)
    content['MAX'] = content['MAX'].apply(lambda x: re.sub("\\*$", "", x))
    content['MIN'] = content['MIN'].apply(lambda x: re.sub("\\*$", "", x))
    content[['WBAN', 'TEMP', 'DEWP', 'WDSP', 'MAX', 'MIN']] = content[['WBAN', 'TEMP', 'DEWP', 'WDSP', 'MAX', 'MIN']].apply(pd.to_numeric)
    content['YEARMODA'] = pd.to_datetime(content['YEARMODA'], format='%Y%m%d', errors='ignore')
    content['YEAR'] = pd.DatetimeIndex(content['YEARMODA']).year
    content['MONTH'] = pd.DatetimeIndex(content['YEARMODA']).month
    content['DAY'] = pd.DatetimeIndex(content['YEARMODA']).day
    return content

# 读取最新一年的数据文件
yearfile = yearfiles[-1]
print(yearfile)
i = 0
tar = tarfile.open("../input/gsod_all_years/" + yearfile, "r")
print(len(tar.getmembers()[1:]))

# 遍历文件成员（气象站数据）
for member in tar.getmembers()[1:]:
    name_parts = re.sub("\.op\.gz$", "", re.sub("^\./", "", member.name)).split("-")
    usaf = name_parts[0]
    wban = int(name_parts[1])
    # 过滤只保留在站点位置信息中的气象站
    if station_loc[(station_loc['USAF'] == usaf) & (station_loc['WBAN'] == wban)].shape[0] != 0:
        i = i + 1
        f = tar.extractfile(member)
        f = gzip.open(f, 'rb')
        content = [re.sub(" +", ",", line.decode("utf-8")).split(",") for line in f.readlines()]
        content = preprocess_station_file_content(content)
        df_day = df_day.append(content[content['YEARMODA'] == content['YEARMODA'].max()])
        content = content.groupby(['USAF', 'WBAN', 'YEAR', 'MONTH']).agg('median').reset_index()
        df = df.append(content)
tar.close()

day = df_day['YEARMODA'].max()
df_day = df_day[df_day['YEARMODA'] == day]

# 读取过去年份的数据文件
df_loc = pd.merge(df, station_loc, how='inner', on=['USAF', 'WBAN'])
df_day_loc = pd.merge(df_day, station_loc, how='inner', on=['USAF', 'WBAN'])

# 增加温度标签（单位转换为摄氏度）
df_loc['ADD_LBL'] = df_loc['TEMP'].apply(lambda x: 'Temperature: ' + str(np.round((x - 32) * 5 / 9, 1)) + ' C')
df_loc['LBL'] = df_loc[['LBL', 'ADD_LBL']].apply(lambda x: x.str.cat(sep='<br>'), axis=1)
df_loc = df_loc.drop('ADD_LBL', axis=1)

df_day_loc['ADD_LBL'] = df_day_loc['TEMP'].apply(lambda x: 'Temperature: ' + str(np.round((x - 32) * 5 / 9, 1)) + ' C')
df_day_loc['LBL_TRACE'] = df_day_loc['LBL']
df_day_loc['LBL'] = df_day_loc[['LBL', 'ADD_LBL']].apply(lambda x: x.str.cat(sep='<br>'), axis=1)
df_day_loc = df_day_loc.drop('ADD_LBL', axis=1)

# 寻找当天最热和最冷的站点
extremes = pd.DataFrame([])
extremes = extremes.append(df_day_loc[df_day_loc['YEARMODA'] == day].sort_values(by="TEMP", ascending=False).head(extremes_num))
extremes = extremes.append(df_day_loc[df_day_loc['YEARMODA'] == day].sort_values(by="TEMP", ascending=False).tail(extremes_num))

# 可视化极端温度的站点
scl = [
    [0, "rgb(150,0,90)"], [0.125, "rgb(0, 0, 200)"], [0.25, "rgb(0, 25, 255)"],
    [0.375, "rgb(0, 152, 255)"], [0.5, "rgb(44, 200, 150)"],
    [0.75, "rgb(255, 234, 0)"], [0.875, "rgb(255, 111, 0)"], [1, "rgb(255, 0, 0)"]
]

# 构建极端温度的地图
data = [dict(
    type='scattergeo',
    text=extremes['LBL'],
    lat=extremes['LAT'],
    lon=extremes['LON'],
    marker=dict(
        color=(extremes['TEMP'] - 32) * 5 / 9,
        colorscale=scl,
        cmin=-50,
        cmax=50,
        size=5,
        colorbar=dict(
            thickness=10,
            titleside="right",
            outlinecolor="rgba(68, 68, 68, 0)",
            tickvals=[-50, -30, -15, 0, 15, 30, 50],
            ticks="outside",
            ticklen=3,
            ticksuffix=" C",
            showticksuffix="all"
        )
    )
)]

layout = dict(
    geo=dict(
        scope='world',
        showland=True,
        landcolor="rgb(212, 212, 212)",
        showlakes=True,
        lakecolor="rgb(255, 255, 255)",
        showsubunits=False,
        showcountries=False,
        showcoastlines=False,
        resolution=110
    ),
)
fig = dict(data=data, layout=layout)

# 打印最热和最冷站点的信息
print("Top 10 hottest and top 10 coldest stations in the world on:")
print(dt.date.strftime(day, '%Y-%m-%d'))
iplot(fig)
