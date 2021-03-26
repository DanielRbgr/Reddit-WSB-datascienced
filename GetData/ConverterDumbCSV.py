"""
This file changes the format of the data from the dump-files into a csv

Format before (achieved by the dump):
[created_utc;;;title;;;URL]

Format in CSV:
created_utc;"title";url

"""
import csv, TextFunctions

datafile = open("datasets/DumpArchive/WithNames/Dump_1-11-20_25-2-21.txt", "r", encoding="utf-8")

with open("datasets/CSVfiles/datadump_sorted_WithNames.csv", "w", newline='', encoding="utf-8") as csvfile:

    spamwriter = csv.writer(csvfile, delimiter=';')
    for line in datafile:
        created_utc = line.split(';;;')[0][1:]
        #print("created_utc:" +created_utc)
        title = line.split(';;;')[1]
        #print("title:" +'"' +title +'"')
        creator = line.split(';;;')[2]
        # print("creator:" +'"' +title +'"')
        url = line.split(';;;')[3][:-2]
        #print("url:" +url)
        row = [created_utc, title, creator, url]
        #print(row)
        spamwriter.writerow(row)

datafile.close()



