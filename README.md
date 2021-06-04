# Taipower-Bimonthly-Energy-Cost-homeassistant
Calculate Taipower (Taiwan Power Company) bi-monthly bill amount from kWh sensor on Home Assistant.
在 Home Assistant 內以 kWh sensor (千瓦⋅時 電度 傳感器) 計算每期 (雙月) 電費帳單金額.
請注意目前只支援 "非時間電價-非營業用的表燈用電" 計費模式.

1) Install - 安裝

1.1) 以從 1月 18 日抄錶開始的雙月帳單週期為例, 
先在 configuration.yaml 內加入每兩個月 18 日自動歸零的總用電 "utility meter", 程式碼如下

utility_meter:
  bimonthly_energy:
    source: sensor.total_power
    cycle: bimonthly
    offset:
      days: 18
      hours: 0
      minutes: 0
      
1.2) 依照 2021 年 5 月 1 日由台灣電力公司發佈的最新電價表, 
於 configuration.yaml 內加入電費計算傳感器 (template sensor), 程式碼如下

sensor:
  - platform: template
    sensors:
      power_cost:
        value_template: >
          {% if now().month in [6,7,8,9,10] %}
            {% if states("sensor.bimonthly_energy") | float < 240 %}
              {{(states("sensor.bimonthly_energy") | float * 1.63) | round(0)}}
            {% elif states("sensor.bimonthly_energy") | float >= 240  and states("sensor.bimonthly_energy") | float < 660 %}
              {{(((states("sensor.bimonthly_energy") | float - 240) * 2.38) + 391.2) | round(0)}}
            {% elif states("sensor.bimonthly_energy") | float >= 660  and states("sensor.bimonthly_energy") | float < 1000 %}
              {{(((states("sensor.bimonthly_energy") | float - 660) * 3.52) + 1390.8) | round(0)}}
            {% elif states("sensor.bimonthly_energy") | float >= 1000  and states("sensor.bimonthly_energy") | float < 1400 %}
              {{(((states("sensor.bimonthly_energy") | float - 1000) * 4.8) + 2587.6) | round(0)}}
            {% elif states("sensor.bimonthly_energy") | float >= 1400  and states("sensor.bimonthly_energy") | float < 2000 %}
              {{(((states("sensor.bimonthly_energy") | float - 1400) * 5.66) + 4507.6) | round(0)}}
            {% elif states("sensor.bimonthly_energy") | float >= 2000 %}
              {{(((states("sensor.bimonthly_energy") | float - 2000) * 6.41) + 7903.6) | round(0)}}
            {% endif %}
          {% else %}
            {% if states("sensor.bimonthly_energy") | float < 240 %}
              {{(states("sensor.bimonthly_energy") | float * 1.63) | round(0)}}
            {% elif states("sensor.bimonthly_energy") | float >= 240  and states("sensor.bimonthly_energy") | float < 660 %}
              {{(((states("sensor.bimonthly_energy") | float - 240) * 2.1) + 391.2) | round(0)}}
            {% elif states("sensor.bimonthly_energy") | float >= 660  and states("sensor.bimonthly_energy") | float < 1000 %}
              {{(((states("sensor.bimonthly_energy") | float - 660) * 2.89) + 1273.2) | round(0)}}
            {% elif states("sensor.bimonthly_energy") | float >= 1000  and states("sensor.bimonthly_energy") | float < 1400 %}
              {{(((states("sensor.bimonthly_energy") | float - 1000) * 3.94) + 2255.8) | round(0)}}
            {% elif states("sensor.bimonthly_energy") | float >= 1400  and states("sensor.bimonthly_energy") | float < 2000 %}
              {{(((states("sensor.bimonthly_energy") | float - 1400) * 4.6) + 3831.8) | round(0)}}
            {% elif states("sensor.bimonthly_energy") | float >= 2000 %}
              {{(((states("sensor.bimonthly_energy") | float - 2000) * 5.03) + 6591.8) | round(0)}}
            {% endif %}
          {% endif %}
        friendly_name: "目前總電費"
        unit_of_measurement: "NTD"
        
2) 重啟 (Reboot) Home Assistant,
之後即可使用 "sensor.power_cost" 顯示目前的電費總金額.

