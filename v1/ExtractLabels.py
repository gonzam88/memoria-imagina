import csv

# Open csv file. Then get the lables row

labels = ["label"]

with open('kinetics700-large.csv', 'r') as file:
    csv_reader = csv.reader(file)
    kinetics = [row for row in csv_reader]
    
    index = 0
    while(index < len(kinetics)):
        label = kinetics[index][0]
        if label not in labels:
            labels.append(label)
        index += 1
    
    with open('labels.txt', 'w') as file:
        # Convert the array elements to strings and join them with commas
        data = ','.join(map(str, labels))
        
        # Write the comma-separated data to the file
        file.write(data)