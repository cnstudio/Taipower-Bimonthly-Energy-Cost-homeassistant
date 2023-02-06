"""Constants for TaiPower Bimonthly Energy Cost Integration."""
from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)

CONFIG_FLOW_VERSION = 1

DOMAIN = "taipower_bimonthly_cost"
PLATFORMS = ["sensor"]

ATTR_BIMONTHLY_ENERGY = "bimonthly energy source"
ATTR_KWH_COST = "price per kwh"
ATTR_START_DAY = "start day"
ATTR_USED_DAYS = "used days"
UNIT_KWH_COST = "TWD/kWh"
UNIT_TWD = "TWD"
CONF_BIMONTHLY_ENERGY = "bimonthly_energy"
CONF_METER_START_DAY = "meter_start_day"


@dataclass
class TaiPowerCostSensorDescription(
    SensorEntityDescription
):
    """Class to describe an TaiPower Energy Cost sensor."""


COST_SENSORS: tuple[TaiPowerCostSensorDescription, ...] = (
    TaiPowerCostSensorDescription(
        key="kwh_cost",
        name="Price Per kWh",
        native_unit_of_measurement=UNIT_KWH_COST,
        device_class=SensorDeviceClass.MONETARY,
        #state_class=SensorStateClass.MEASUREMENT,
        #Try to workaround HA 2023.2.1 sensor class warning issue
    ),
    TaiPowerCostSensorDescription(
        key="power_cost",
        name="Power Cost",
        native_unit_of_measurement=UNIT_TWD,
        device_class=SensorDeviceClass.MONETARY,
        #state_class=SensorStateClass.MEASUREMENT,
        #Try to workaround HA 2023.2.1 sensor class warning issue
    )
)
