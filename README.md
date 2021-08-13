# Taipower-Bimonthly-Energy-Cost-homeassistant
Calculate Taipower (Taiwan Power Company) bi-monthly bill amount from kWh sensor on Home Assistant.  
在 Home Assistant (HA) 內以 kWh sensor (千瓦⋅時 電度 傳感器) 計算每期 (雙月) 電費帳單金額.  
請注意 **`目前只支援 "非時間電價-非營業用的表燈用電" 計費`** 模式.

## 1) Install - 安裝

###### 1.1) 以從 1月 18 日抄錶開始的雙月帳單週期為例, 
先在 `configuration.yaml` 內加入每兩個月 18 日自動歸零的總用電 `utility meter`, 程式碼如下

```yaml
utility_meter:
  bimonthly_energy:
    source: sensor.total_power # 這是您想用來計算電費的 kWh 來源傳感器.
    cycle: bimonthly
    offset:
      days: 18
      hours: 0
      minutes: 0
```
      
###### 1.2) 依照 2021 年 5 月 1 日由台灣電力公司發佈的最新電價表, 
於 `configuration.yaml` 內加入電費計算傳感器 (template sensor), 程式碼如下

```yaml
sensor:
  - platform: template
    sensors:
      kwh_cost:
        value_template: >
          {% if now().month in [6,7,8,9] %}
            {% if states("sensor.bimonthly_energy") | float < 240 %}
              {{1.63}}
            {% elif states("sensor.bimonthly_energy") | float >= 240  and states("sensor.bimonthly_energy") | float < 660 %}
              {{2.38}}
            {% elif states("sensor.bimonthly_energy") | float >= 660  and states("sensor.bimonthly_energy") | float < 1000 %}
              {{3.52}}
            {% elif states("sensor.bimonthly_energy") | float >= 1000  and states("sensor.bimonthly_energy") | float < 1400 %}
              {{4.8}}
            {% elif states("sensor.bimonthly_energy") | float >= 1400  and states("sensor.bimonthly_energy") | float < 2000 %}
              {{5.66}}
            {% elif states("sensor.bimonthly_energy") | float >= 2000 %}
              {{6.41}}
            {% endif %}
          {% else %}
            {% if states("sensor.bimonthly_energy") | float < 240 %}
              {{1.63}}
            {% elif states("sensor.bimonthly_energy") | float >= 240  and states("sensor.bimonthly_energy") | float < 660 %}
              {{2.1}}
            {% elif states("sensor.bimonthly_energy") | float >= 660  and states("sensor.bimonthly_energy") | float < 1000 %}
              {{2.89}}
            {% elif states("sensor.bimonthly_energy") | float >= 1000  and states("sensor.bimonthly_energy") | float < 1400 %}
              {{3.94}}
            {% elif states("sensor.bimonthly_energy") | float >= 1400  and states("sensor.bimonthly_energy") | float < 2000 %}
              {{4.6}}
            {% elif states("sensor.bimonthly_energy") | float >= 2000 %}
              {{5.03}}
            {% endif %}
          {% endif %}
        friendly_name: "目前電度單價"
        unit_of_measurement: "TWD"
        device_class: monetary

  - platform: template
    sensors:
      power_cost:
        value_template: >
          {% if now().month in [6,7,8,9] %}
            {% if states("sensor.bimonthly_energy") | float < 240 %}
              {{(states("sensor.bimonthly_energy") | float * states("sensor.kwh_cost") | float) | round(0)}}
            {% elif states("sensor.bimonthly_energy") | float >= 240  and states("sensor.bimonthly_energy") | float < 660 %}
              {{(((states("sensor.bimonthly_energy") | float - 240) * states("sensor.kwh_cost") | float) + 391.2) | round(0)}}
            {% elif states("sensor.bimonthly_energy") | float >= 660  and states("sensor.bimonthly_energy") | float < 1000 %}
              {{(((states("sensor.bimonthly_energy") | float - 660) * states("sensor.kwh_cost") | float) + 1390.8) | round(0)}}
            {% elif states("sensor.bimonthly_energy") | float >= 1000  and states("sensor.bimonthly_energy") | float < 1400 %}
              {{(((states("sensor.bimonthly_energy") | float - 1000) * states("sensor.kwh_cost") | float) + 2587.6) | round(0)}}
            {% elif states("sensor.bimonthly_energy") | float >= 1400  and states("sensor.bimonthly_energy") | float < 2000 %}
              {{(((states("sensor.bimonthly_energy") | float - 1400) * states("sensor.kwh_cost") | float) + 4507.6) | round(0)}}
            {% elif states("sensor.bimonthly_energy") | float >= 2000 %}
              {{(((states("sensor.bimonthly_energy") | float - 2000) * states("sensor.kwh_cost") | float) + 7903.6) | round(0)}}
            {% endif %}
          {% else %}
            {% if states("sensor.bimonthly_energy") | float < 240 %}
              {{(states("sensor.bimonthly_energy") | float * states("sensor.kwh_cost") | float) | round(0)}}
            {% elif states("sensor.bimonthly_energy") | float >= 240  and states("sensor.bimonthly_energy") | float < 660 %}
              {{(((states("sensor.bimonthly_energy") | float - 240) * states("sensor.kwh_cost") | float) + 391.2) | round(0)}}
            {% elif states("sensor.bimonthly_energy") | float >= 660  and states("sensor.bimonthly_energy") | float < 1000 %}
              {{(((states("sensor.bimonthly_energy") | float - 660) * states("sensor.kwh_cost") | float) + 1273.2) | round(0)}}
            {% elif states("sensor.bimonthly_energy") | float >= 1000  and states("sensor.bimonthly_energy") | float < 1400 %}
              {{(((states("sensor.bimonthly_energy") | float - 1000) * states("sensor.kwh_cost") | float) + 2255.8) | round(0)}}
            {% elif states("sensor.bimonthly_energy") | float >= 1400  and states("sensor.bimonthly_energy") | float < 2000 %}
              {{(((states("sensor.bimonthly_energy") | float - 1400) * states("sensor.kwh_cost") | float) + 3831.8) | round(0)}}
            {% elif states("sensor.bimonthly_energy") | float >= 2000 %}
              {{(((states("sensor.bimonthly_energy") | float - 2000) * states("sensor.kwh_cost") | float) + 6591.8) | round(0)}}
            {% endif %}
          {% endif %}
        friendly_name: "目前總電費"
        unit_of_measurement: "TWD"
        device_class: monetary
```
        
## 2) 重啟 (Reboot) Home Assistant,
之後即可使用 `sensor.power_cost` 顯示目前的電費總金額.

## Appendix I: How to convert from W to kWh - 如何將 W 轉換為 kWh ?  
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

## Appendix II: How to work with new Home Assistant (After 2021.8.0) build-in Energy function?  
從 Home Assistant 2021.8.0 版以後新增了內建的 "能源" 面板功能, 可以分別計算每日用電與每日電費, 配合新增上述 1.2 項次的程式後,  
只要於 HA 內的 設定 -> 能源 -> Grid consumption -> 耗電量 新增項目內選擇 "total_power",  
並選擇 獨立價格實體 後於下拉選單內選擇 sensor.kwh_cost 後按下 儲存即可.  
(注意: 能源面板需要 1~3 個小時後才會開始顯現數值, 給 HA 一點計算時間的耐心)
