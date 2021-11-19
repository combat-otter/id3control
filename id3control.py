import argparse
import json
from weconnect import weconnect

IGNORE_ITEMS = ["lvBatteryStatus", "parkingPosition", "capabilityStatus", "rangeStatus"]

def main():

    with open ("config.json") as f:
        config = json.load(f)

    
    print('Connecting...')
    weConnect = weconnect.WeConnect(username=config["username"], password=config["password"])
    
    for vin, vehicle in weConnect.vehicles.items():

        print(vin)
        
        status = vehicle.statuses
        for s in status:
            if s not in IGNORE_ITEMS:
                print(status[s])

    
if __name__ == '__main__':
    main()