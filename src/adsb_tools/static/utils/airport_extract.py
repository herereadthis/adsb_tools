import csv

input_file = 'airports.csv'
output_file = 'airports_new.csv'

# Open the input file and create a reader object
with open(input_file, 'r') as infile:
    reader = csv.reader(infile)
    
    # Create a list to hold the rows that will be written to the new file
    output_rows = []
    
    # Loop through each row in the reader object
    for row in reader:
        # Skip row if column 2 or 3 are 'N/A'
        if row[1] == 'N/A' or row[2] == 'N/A':
            continue
        
        # Get the first 5 columns and convert columns 3 and 4 to title case
        abbreviated_countries = ['USA']
        row4 = row[4] if row[4] in abbreviated_countries else row[4].title()

        new_row = [row[0], row[1], row[2].title(), row[3].title(), row4]
        
        # Add the new row to the output list
        output_rows.append(new_row)

# Open the output file and create a writer object
with open(output_file, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    
    # Write the output rows to the new file
    writer.writerows(output_rows)
