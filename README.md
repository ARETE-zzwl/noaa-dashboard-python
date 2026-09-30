# NOAA Dashboard Python

[中文](#中文) · [English](#english)

## 中文

一个用 pandas 处理 NOAA GSOD 气象站数据、用 Plotly 绘制全球温度地图的实验脚本。

脚本从最新年度归档中取出站点的最新观测日，再选出该日平均温度最高和最低的各 10 个站点。地图显示站点位置和摄氏温度。它使用历史数据中的最新日期，不提供实时天气。

### 准备环境和数据

需要 Python、Kaggle 账户及已配置的 Kaggle CLI 凭据，以及命令行 `unzip`。Windows 下也需要提供可调用的 `unzip`。

```bash
git clone https://github.com/ARETE-zzwl/noaa-dashboard-python.git
cd noaa-dashboard-python
python -m pip install -r requirements.txt
```

运行前，另行准备 NOAA ISD 站点元数据文件 `isd-history.csv`，放在仓库上一级的 `input/` 目录。脚本会下载 Kaggle 数据集 `noaa/noaa-global-surface-summary-of-the-day`，但不会下载这个元数据文件。

脚本按以下相对路径读取数据：

```text
../input/
  isd-history.csv
  gsod_all_years/
    <yearly archives>
```

年度归档需要符合代码使用的 `tar` → `.op.gz` 布局。若下载包的名称或结构与脚本中的假设不同，需要调整下载、解压和读取路径。

### 运行

从仓库根目录执行：

```bash
python main.py
```

脚本使用 `init_notebook_mode` 和 `iplot` 显示地图，适合在 Jupyter 中查看；普通终端未必会打开图表。`extremes_num` 控制两端各显示多少个站点。

### 当前限制

- 代码使用 `DataFrame.append`，依赖文件因此限定 `pandas<2.0`。
- `year_num=20` 用于选择年度范围和筛选站点，实际解析的是最新年度归档。
- 站点筛选要求记录覆盖所选年份范围；地图上的极值仅代表筛选后可用的站点。
- 下载数据和运行产物不放在仓库中。

仓库未附许可证，代码复用和数据再分发前需分别确认授权。

## English

An experimental script that processes NOAA GSOD station data with pandas and draws a world temperature map with Plotly.

It reads the latest yearly archive, selects the latest observation date available across the retained stations, and maps the 10 stations with the highest and lowest daily mean temperatures. Values are shown in Celsius. This uses the latest date in historical data, not a live weather feed.

### Setup

Use Python, a Kaggle account with CLI credentials configured, and a command-line `unzip` utility. `unzip` must also be available when running on Windows.

```bash
git clone https://github.com/ARETE-zzwl/noaa-dashboard-python.git
cd noaa-dashboard-python
python -m pip install -r requirements.txt
```

Prepare `../input/isd-history.csv` separately. The script downloads `noaa/noaa-global-surface-summary-of-the-day` from Kaggle but does not download station metadata.

It expects yearly archives in `../input/gsod_all_years/`, with a `tar` archive containing `.op.gz` station files. Adjust the hard-coded archive name and paths if the downloaded dataset has a different layout.

### Run and limitations

From the repository root:

```bash
python main.py
```

Plotting uses `init_notebook_mode` and `iplot`, so Jupyter is the intended display environment; a plain terminal may not open the map. Change `extremes_num` to control the number of stations at each end.

The code uses `DataFrame.append`, so requirements pin `pandas<2.0`. `year_num=20` controls the archive range and station coverage filter, but only the latest yearly archive is parsed. Temperature extremes refer to the stations that remain after filtering.

Downloaded data and generated files are not committed. No license is included; confirm permissions for code reuse and dataset redistribution separately.
