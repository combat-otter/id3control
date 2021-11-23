import argparse
import json
from enum import Enum
from weconnect import weconnect

from weconnect.elements.control_operation import ControlOperation

class ClimateControl(Enum):
    START = 'start'
    STOP = 'stop'
    
    def __str__(self):
        return self.value


'''
expects config.json of the form:

{
    "username":"user@email.com",
    "password":"the_password"
}
'''

IGNORE_ITEMS = ["lvBatteryStatus", "parkingPosition", "capabilityStatus", "rangeStatus"]

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--climate', type=ClimateControl, choices=list(ClimateControl))
    
    args = parser.parse_args()

    with open ("config.json") as f:
        config = json.load(f)
    
    print('Connecting...')
    connection = weconnect.WeConnect(username=config["username"], password=config["password"], updateAfterLogin=False)
    connection.updateVehicles()

    # initial dump of status info   

    for vin, vehicle in connection.vehicles.items():
        status = vehicle.statuses
        controls = vehicle.controls
        
    for s in status:
        if s not in IGNORE_ITEMS:
            print(status[s])

    climate_control = controls.climatizationControl

    if args.climate==ClimateControl.START:

        target_temp = status["climatisationSettings"].targetTemperature_C.value
        print(f"Activating climate control, target temperature = {target_temp}")
        
        climate_control.setValueWithCarTime(ControlOperation.START)

        while True:
            connection.updateVehicles()
            c_state = status["climatisationStatus"].climatisationState
            c_target = status["climatisationStatus"].target
            c_time = status["climatisationStatus"].remainingClimatisationTime_min

            print(f"progress:{c_target} current:{c_state} remaining:{c_time}min")

            if str(c_state)=="ventilation" or str(c_state)=="heating":
                break
            
    elif args.climate==ClimateControl.STOP:

        target_temp = status["climatisationSettings"].targetTemperature_C.value
        print(f"Stopping climate control")
        
        climate_control.setValueWithCarTime(ControlOperation.STOP)

        while True:
            connection.updateVehicles()
            c_state = status["climatisationStatus"].climatisationState
            c_target = status["climatisationStatus"].target
            c_time = status["climatisationStatus"].remainingClimatisationTime_min

            print(f"progress:{c_target} current:{c_state} remaining:{c_time}min")

            if str(c_state)=="off":
                break


if __name__ == '__main__':
    main()