import argparse
import json
import datetime
from enum import Enum

from timeit import default_timer as timer

from weconnect import weconnect
from weconnect.elements.control_operation import ControlOperation


class ClimateControl(Enum):
    START = "start"
    STOP = "stop"

    def __str__(self):
        return self.value


"""
expects config.json of the form:

{
    "username":"user@email.com",
    "password":"the_password"
}
"""

IGNORE_ITEMS = ["lvBatteryStatus", "parkingPosition", "capabilityStatus", "rangeStatus"]

CLIMATE_ACTIVE_STATES = ["ventilation","heating"]
CLIMATE_INACTIVE_STATES = ["off"]

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--climate", type=ClimateControl, choices=list(ClimateControl))

    args = parser.parse_args()

    with open("config.json") as f:
        config = json.load(f)

    print("Connecting...")
    connection = weconnect.WeConnect(
        username=config["username"], password=config["password"], updateAfterLogin=False
    )
    connection.updateVehicles()

    # initial dump of status info

    for vin, vehicle in connection.vehicles.items():
        status = vehicle.statuses
        controls = vehicle.controls

    for s in status:
        if s not in IGNORE_ITEMS:
            print(status[s])

    climate_control = controls.climatizationControl

    if args.climate:

        print(f"Applying climate control operation '{args.climate}'")

        climate_control.setValueWithCarTime(ControlOperation.START if args.climate==ClimateControl.START else ControlOperation.STOP)

        start = timer()

        # keep looping until control operation is applied
        while True:
            connection.updateVehicles()
            c_state = status["climatisationStatus"].climatisationState
            c_target = status["climatisationStatus"].target
            c_time = status["climatisationStatus"].remainingClimatisationTime_min

            print(f"progress:{c_target} current:{c_state} remaining:{c_time}min")

            # stop if we reach the desired target state
            if args.climate==ClimateControl.START and str(c_state) in CLIMATE_ACTIVE_STATES:
                break
            elif args.climate==ClimateControl.STOP and str(c_state) in CLIMATE_INACTIVE_STATES:
                break

        end = timer()
        elapsed = (end - start)
        timestamp = datetime.datetime.now()
        print(f"Operation '{args.climate}' took {elapsed} seconds to execute")

        with open("control_log.csv", "a") as file_object:
            file_object.write(f"{timestamp},{args.climate},{elapsed}\r\n")




if __name__ == "__main__":
    main()
