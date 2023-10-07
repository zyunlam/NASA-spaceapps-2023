import requests
import re
import hjson
import datetime
import csv

def read_satellite(planet, start_date: datetime.datetime, end_date):
    # Parse week by week
    # add a week to start_date
    current_date = start_date
    orbit_data = []
    while current_date < end_date:
        old_date = current_date
        current_date += datetime.timedelta(weeks=4)
        # Parse the line
        payload = {
            "format": "json",
            "EPHEM_TYPE": "VECTOR",
            "COMMAND": planet,
            "START_TIME": old_date.strftime("%Y-%m-%d"),
            "STOP_TIME": current_date.strftime("%Y-%m-%d"),
            "STEP_SIZE": "10m",
            "OBJ_DATA": "NO",
            "CENTER": 3
        }
        api = requests.get("https://ssd.jpl.nasa.gov/api/horizons.api", payload)
        res = str(api.json()["result"])
        res = res.replace("\\n", "\n")
        params = (res[res.find("$$SOE") + len("$$SOE") + 1:res.find("$$EOE")])
        params2 = params.split("\n")
        params2 = list(zip(params2[::4], params2[1::4], params2[2::4], params2[3::4]))
        # Get the time or something
        for param in params2:
            # Get time from the first line
            # The first line is formatted like this: "2458849.500000000 = A.D. 2020-Jan-01 00:00:00.0000 TDB "
            # We need to get the first part of the string, and then convert it to a datetime object
            time = param[0].split(" = ")[1]
            try:
                t = datetime.datetime.strptime(time, "A.D. %Y-%b-%d %H:%M:%S.%f TDB ")
            except ValueError:

                continue
            orbital_params = {}
            orbital_params["Time"] = t
            for p2 in param[1:]:
                for start in re.finditer("=", p2):
                    id = p2[start.start() - 2 : start.start()].strip()
                    if id == "0":
                        continue
                    orb_param = float(p2[start.end() : start.end() + 22].strip())
                    orbital_params[id] = float(orb_param)
            orbit_data.append(orbital_params)
    with open(f'{planet}.csv', 'w') as f:
        w = csv.DictWriter(f, orbit_data[0].keys(), lineterminator='\n')
        w.writeheader()
        w.writerows(orbit_data)

read_satellite("DSCOVR", datetime.datetime(year=2015, month=6, day=8), datetime.datetime(year=2023, month=1, day=1))
