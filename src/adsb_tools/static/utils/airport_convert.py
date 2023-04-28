input_file = 'airports.txt'
output_file = 'airports.csv'

with open(input_file, 'r') as in_file, open(output_file, 'w') as out_file:
    # Write header row to CSV
    out_file.write('ICAO Code,IATA Code,Airport Name,City/Town,Country,Latitude Degrees,Latitude Minutes,Latitude Seconds,Latitude Direction,Longitude Degrees,Longitude Minutes,Longitude Seconds,Longitude Direction,Altitude,Latitude Decimal Degrees,Longitude Decimal Degrees\n')
    
    # Process each line in input file
    for line in in_file:
        # Replace colons with commas
        line = line.replace(':', ',')
        
        # Write modified line to output file
        out_file.write(line)