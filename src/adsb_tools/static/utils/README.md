# Utils for Static files

## Global Airport Database

Columns

```
ICAO Code
IATA Code
Airport Name
City/Town
Country
Latitude Degrees
Latitude Minutes
Latitude Seconds
Latitude Direction
Longitude Degrees
Longitude Minutes
Longitude Seconds
Longitude Direction
Altitude
Latitude Decimal Degrees
Longitude Decimal Degrees
```

Download DB from 

* https://www.partow.net/miscellaneous/airportdatabase/
* Direct Link: [The Global Airport Database (version 0.0.2)](https://www.partow.net/downloads/GlobalAirportDatabase.zip)

Then run `airport_convert.py` on the file
Then run `airport_extract.py` on the new .CSV file