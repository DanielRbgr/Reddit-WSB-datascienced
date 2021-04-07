"""
This file adds more entries into the csv file.

For this, the csv file is compared with a randomly choosable text file, the code will then add
all posts from the text file into the csv which are created after the newest post of the csv.

"""
import csv

ExistingPosts = []

# little function for sorting purpose
def takeCreationTime(elem):
    return elem[0]


datafile = open("datasets/DumpArchive/WithNames/Dump_17-3-21_30-3-21.txt", "r", encoding="utf-8")

with open("datasets/CSVfiles/datadump_sorted_WithNames.csv", "r", newline='', encoding="utf-8") as csvfile:

    reader = csv.reader(csvfile, delimiter=';')

    # create a list with all current entries in the csv
    for row in reader:
        ExistingPosts.append(row)

    # sort the list by creation date in descending order
    ExistingPosts.sort(key=takeCreationTime, reverse=True)
    print(len(ExistingPosts))

    # search_list = [item for item in ExistingPosts if item[0]=='1613948445']
    # print(search_list)

    # print(ExistingPosts[0][0])

    # remove the first row, which contain the header data
    ExistingPosts.pop(0)

    for line in datafile:
        NewPost = (line.split(';;;')[0][1:], line.split(';;;')[2])
        # if the the new post is more recent then the most recent post in the existing file
        if ExistingPosts[0][0] < NewPost[0]:
            # isExisting.append(True)

            # if the line is not existent yet, add it to the isExisting array
            created_utc = line.split(';;;')[0][1:]
            # print("created_utc:" +created_utc)
            title = line.split(';;;')[1]
            # print("title:" +'"' +title +'"')
            creator = line.split(';;;')[2]
            # print("creator:" +'"' +title +'"')
            url = line.split(';;;')[3][:-2]
            # print("url:" +url)
            row = [created_utc, title, creator, url]
            ExistingPosts.append(row)

    print(len(ExistingPosts))

    ExistingPosts.sort(key=takeCreationTime, reverse=True)

with open("datasets/CSVfiles/datadump_sorted_WithNames.csv", "w", newline='', encoding="utf-8") as csvfile:

    writer = csv.writer(csvfile, delimiter=';')

    # add header
    csvheader = ['utc', 'title', 'author', 'url']
    writer.writerow(csvheader)

    for row in ExistingPosts:
        writer.writerow(row)
    # print(ExistingPosts)

datafile.close()



