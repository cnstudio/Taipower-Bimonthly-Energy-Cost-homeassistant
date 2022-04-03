"""Constants for TaiPower Bimonthly Energy Cost Integration."""

CONFIG_FLOW_VERSION = 1

DOMAIN = "taipower_cost"
PLATFORMS = ["sensor"]

ATTR_BIMONTHLY_ENERGY = "bimonthly energy source"
ATTR_KWH_COST = "price per kwh"
ATTR_START_DAY = "start day"
ATTR_USED_DAYS = "used days"
UNIT_KWH_COST = "TWD/kWh"
UNIT_TWD = "TWD"
CONF_BIMONTHLY_ENERGY = "bimonthly_energy"
CONF_METER_START_DAY = "meter_start_day"
