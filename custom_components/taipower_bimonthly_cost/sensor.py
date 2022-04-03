"""Support for TaiPower Energy Cost service."""
from datetime import datetime

from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import (
    ATTR_ENTITY_ID,
    DEVICE_CLASS_MONETARY
)
from homeassistant.helpers.typing import ConfigType

from .const import (
    ATTR_BIMONTHLY_ENERGY,
    ATTR_KWH_COST,
    ATTR_START_DAY,
    ATTR_USED_DAYS,
    CONF_BIMONTHLY_ENERGY,
    CONF_METER_START_DAY,
    DOMAIN,
    UNIT_KWH_COST,
    UNIT_TWD
)

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigType, async_add_entities
) -> None:
    """Set up the energy cost sensor."""
    async_add_entities(
        [
            EnergyCostSensor(hass, entry.options)
        ]
    )


class EnergyCostSensor(SensorEntity):
    """Implementation of a energy cost sensor."""
    def __init__(self, hass, entry_data):
        self._hass = hass
        self._energy_entity = entry_data[CONF_BIMONTHLY_ENERGY]
        self._reset_day = datetime.strptime(
            entry_data[CONF_METER_START_DAY], "%Y/%m/%d")
        self._kwh_cost = None

    async def reset_utility_meter(self, sensor):
        """Send a command."""
        service_data = {
            'value': '0.000',
            ATTR_ENTITY_ID: sensor
        }

        await self._hass.services.async_call(
            'utility_meter', 'calibrate', service_data)

    @property
    def name(self):
        """Return the name of the sensor."""
        return "power_cost"

    @property
    def unique_id(self):
        """Return the unique of the sensor."""
        return "power_cost"

    @property
    def state(self):
        """Return the state of the sensor."""
        now = datetime.now()
        value = None

        if self._hass.states.get(self._energy_entity):
            state = self._hass.states.get(self._energy_entity).state
            if isinstance(state, str):
                state = float(state)
            if isinstance(state, (float, int)):
                state = float(state)
                if now.month in [6, 7, 8, 9]:
                    if state < 240.0:
                        kwh_cost = 1.63
                        value = state * kwh_cost
                    elif 240.0 <= state <= 660.0:
                        kwh_cost = 2.38
                        value = ((state - 240.0) * kwh_cost) + 391.2
                    elif 660.0 <= state < 1000.0:
                        kwh_cost = 3.52
                        value = ((state - 660.0) * kwh_cost) + 1390.8
                    elif 1000.0 <= state < 1400.0:
                        kwh_cost = 4.8
                        value = ((state - 1000.0) * kwh_cost) + 2587.6
                    elif 1400.0 <= state < 2000.0:
                        kwh_cost = 5.66
                        value = ((state - 1400.0) * kwh_cost) + 4507.6
                    elif state >= 2000.0:
                        kwh_cost = 6.41
                        value = ((state - 2000.0) * kwh_cost) + 7903.6
                else:
                    if state < 240.0:
                        kwh_cost = 1.63
                        value = state * kwh_cost
                    elif 240.0 <= state <= 660.0:
                        kwh_cost = 2.1
                        value = ((state - 240.0) * kwh_cost) + 391.2
                    elif 660.0 <= state < 1000.0:
                        kwh_cost = 2.89
                        value = ((state - 660.0) * kwh_cost) + 1273.2
                    elif 1000.0 <= state < 1400.0:
                        kwh_cost = 3.94
                        value = ((state - 1000.0) * kwh_cost) + 2255.8
                    elif 1400.0 <= state < 2000.0:
                        kwh_cost = 4.6
                        value = ((state - 1400.0) * kwh_cost) + 3831.8
                    elif state >= 2000.0:
                        kwh_cost = 5.03
                        value = ((state - 2000.0) * kwh_cost) + 6591.8
                self._kwh_cost = kwh_cost
        if ((now - self._reset_day).days % 60) == 59:
            if now.hour == 23 and now.minute == 59 and 0 < now.second <= 59:
                if (self._hass.states.get(self._energy_entity) and
                        self._hass.states.get(self._energy_entity).state != "unknown"):
                    self.reset_utility_meter(self._energy_entity)
        return value

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return UNIT_TWD

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return DEVICE_CLASS_MONETARY

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the device."""
        now = datetime.now()
        return {
            ATTR_BIMONTHLY_ENERGY: self._energy_entity,
            ATTR_KWH_COST: "{} {}".format(self._kwh_cost, UNIT_KWH_COST),
            ATTR_START_DAY: self._reset_day,
            ATTR_USED_DAYS: (now - self._reset_day).days % 60,
        }