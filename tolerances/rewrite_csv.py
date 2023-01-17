import csv

with open('shafts.csv', 'r', newline='') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='\t')

    headers = next(csv_reader)

    with open('shafts2.csv', 'w', newline='') as new_file:
        csv_writer = csv.writer(new_file, delimiter='\t')

        # first rewrite
        # csv_writer.writerow(['size'] + headers[2:])
        # for line in csv_reader:
        #     csv_writer.writerow([line[0] + '-' + line[1]] + line[2:])

        # second rewrite
        csv_writer.writerow(['size', 'tolerance_gr', 'es', 'ei'])
        for line in csv_reader:
            for i in range(len(line)):
                if i % 2 != 0:
                    csv_writer.writerow([line[0], headers[i], line[i], line[i+1]])
