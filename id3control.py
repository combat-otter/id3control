import argparse
import json
from weconnect import weconnect

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', required=True)
    parser.add_argument('-p', '--password', required=True)

    args = parser.parse_args()

    print('Connecting...')
    weConnect = weconnect.WeConnect(username=args.username, password=args.password)
    
    for vin, vehicle in weConnect.vehicles.items():

        print(vin)
        print(vehicle.statuses)
    
if __name__ == '__main__':
    main()