[![](https://img.shields.io/github/v/release/cnstudio/Taipower-Bimonthly-Energy-Cost-homeassistant.svg?style=flat-square)](https://github.com/cnstudio/Taipower-Bimonthly-Energy-Cost-homeassistant/releases/latest)

# Taipower-Bimonthly-Energy-Cost-homeassistant
Calculate Taipower (Taiwan Power Company) bi-monthly bill amount from kWh sensor on Home Assistant.  
在 Home Assistant (HA) 內以 kWh sensor (千瓦⋅時 電度 傳感器) 計算每期 (雙月) 電費帳單金額.  
請注意 **`目前只支援 "非時間電價-非營業用的表燈用電" 計費`** 模式. 
** 可支援多次設定, 增加多個台電電表來源分別計算 **

## 1) Install by HACS - 使用 HACS 安裝 (尚未申請, 目前請使用第 2 章節的手動安裝)

###### 1.1) 推薦使用 HACS 安裝 (將在近日申請, 目前 HACS 內應該搜索不到):
請在 HACS 的 `Integrations` 內搜索 `Taipower bimonthly cost` 並安裝後,  
依照 UI 提示安裝即可:  
  
UI 第一行請輸入要引用為電費計算的 "即時 kWh" 的 `utility meter` sensor (請看本說明下方附錄章節了解如何增設 utility meter).  
UI 第二行請輸入本期電費計算周期的第一天的日期 (格式為 YYYY/MM/DD).  
  
之後即可使用 `sensor.<您在設定 UI 第一行輸入的傳感器名稱>.power_cost` 顯示本期電費統計, 
並可使用 `sensor.<您在設定 UI 第一行輸入的傳感器名稱>.kwh_cost` 給 HA 內建的能源面板作為獨立電費單價來源作為個迴路 (設備) 單獨計算電費使用 (請看本說明下方附錄章節).  
(例如您 UI 第一行輸入 "sensor.AA", 完成後可使用 "sensor.AA.power_cost" 與 "sensor.AA.kwh_cost")  
  
  
## 2) Manual Install - 手動安裝 (推薦使用第 1 章節的 HACS 安裝日後更新方便很多)

###### 2.1) 手動安裝 (推薦使用第 1 章節的 HACS 安裝日後更新方便很多):
下載本專案檔案後解壓縮, 拷貝 `custom_components` 到您 Home Assistant 內的 configuration 目錄下 (通常是 `config`),  
目錄結構看起來會像如下:  

```
<config directory>/
|-- custom_components/
|   |-- taipower_bimonthly_cost/
|       |-- __init__.py
|       |-- config_flow.py
|       |-- const.py
|       |-- etc...
|           |-- translations
|           |-- etc...
```
  
###### 2.2) 然後重啟 (reboot) Home Assistant:
接下來請重新啟動 (reboot) HA.  
  
###### 2.3) 於 Home Assistant 內新增整合元件, 
請至 HA 內的 設定 -> 裝置與服務 -> 整合 新增整合(位於右下角的按鈕) -> 於跳出的 設定整合 選單內搜索 `Taipower bimonthly cost` 並安裝.
之後依照 UI 提示進行即可:  
  
UI 第一行請輸入要引用為電費計算的 "即時 kWh" 的 `utility meter` sensor (請看本說明下方附錄章節了解如何增設 utility meter).  
UI 第二行請輸入本期電費計算周期的第一天的日期 (格式為 YYYY/MM/DD).  
  
之後即可使用 `sensor.<您在設定 UI 第一行輸入的傳感器名稱>.power_cost` 顯示本期電費統計, 
並可使用 `sensor.<您在設定 UI 第一行輸入的傳感器名稱>.kwh_cost` 給 HA 內建的能源面板作為獨立電費單價來源作為個迴路 (設備) 單獨計算電費使用 (請看本說明下方附錄章節).  
(例如您 UI 第一行輸入 "sensor.AA", 完成後可使用 "sensor.AA.power_cost" 與 "sensor.AA.kwh_cost")  
  
  
## Appendix I (附錄 I): 如何新增即時 kWh 的 `utility meter` sensor 作為能源計算引用?
請在 `configuration.yaml` 內加入總用電 `utility meter`, 程式碼如下:  

```yaml
utility_meter:
  bimonthly_energy:
    source: sensor.total_power # 這是您想用來計算電費的 kWh 來源傳感器.
```
  
如此即可在設定 UI 的第一行輸入 `sensor.bimonthly_energy` 作為電費計算功能的計算來源.  
  
## Appendix II (附錄 II): How to convert from W to kWh - 如何將 W 轉換為 kWh?  
一般來說大部分的電量偵測硬體是回傳 W (瓦特), 如果想要將 W 轉換為電度 kWh 給 `utility meter` 使用的話,  
可於 `configuration.yaml` 內的 `sensor:` 段落內加入如下的程式碼即可完成轉換工作:

```yaml
  - platform: integration
    source: sensor.your_W_sensor # 這是您原始的用電 "W (瓦特)" 偵測器.
    name: total_power # 這是要交給 utility meter 的名稱.
    unit_prefix: k
    method: right
    round: 3
```

## Appendix III (附錄 III): How to work with new Home Assistant (After 2021.8.0) build-in Energy function?  
從 Home Assistant 2021.8.0 版以後新增了內建的 "能源" 面板功能, 可以分別計算每日用電與每日電費, 配合新增上述 1.2 項次的程式後,  
只要於 HA 內的 設定 -> 能源 -> Grid consumption -> 耗電量 新增項目內選擇 "total_power",  
並選擇 獨立價格實體 後於下拉選單內選擇 sensor.kwh_cost 後按下 儲存即可.  
(注意: 能源面板需要 1~2 個小時後才會開始顯現數值, 給 HA 一點計算時間的耐心)  
