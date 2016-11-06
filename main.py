#Construct Local DNS
#Author: etopiei

import csv, sqlite3, os, sys, socket

listOfIPs = list()

output_file = open('vivaldi_history.csv', 'wb')
csv_writer = csv.writer(output_file)
headers = ('URL', 'IP')
csv_writer.writerow(headers)

def writeToFile(url,IP):

    row = (url,IP)
    csv_writer.writerow(row)

def checkForDuplicate(IP):
    if IP in listOfIPs:
        return 0
    else:
        return 1

def cleanURL(url):

    locationstart = url.find("www")
    locationend1 = url.find("/", locationstart)
    locationend2 = url.find("&", locationstart)
    locationend3 = url.find("%",locationstart)

    if locationend1 == -1:
        locationend1 = 9000
    if locationend2 == -1:
        locationend2 = 9001
    if locationend3 == -1:
        locationend3 = 9002

    if locationend1 > locationend2:
        if locationend2 > locationend3:
            locationend = locationend3
        else:
            locationend = locationend2

    elif locationend2 > locationend1:
        if locationend3 > locationend1:
            locationend = locationend1
        else:
            locationend = locationend3

    elif locationend3 > locationend1:
        if locationend2 > locationend1:
            locationend = locationend1
        else:
            locationend = locationend2


    clean = url[locationstart: locationend]

    if ("http" not in clean) and (clean is not None):
        return clean
    else:
        cleanURL(clean)

def fixString(url):

    if "www" not in url:
        return "Nope"
    else:
        return cleanURL(url)

def getIpOfUrl(url , n):

    new = fixString(url)
    if new != "Nope" and new is not None:
        IP = socket.gethostbyname(new)
        if checkForDuplicate(IP) != 0:
            listOfIPs.append(IP)
            writeToFile(new,IP)
            return 1

def run():

    print('Gathering History...')
    print('This could take a few minutes, please wait...')

    connectionString = sys.argv[1]
    connection = sqlite3.connect(connectionString)
    connection.text_factory = str
    cur = connection.cursor()

    n = 0
    for row in (cur.execute('select url from urls')):
        row = list(row)
        if getIpOfUrl(row[0], n) == 1:
            n = n+1

    print('Done.')

run()
