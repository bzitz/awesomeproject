import csv, json

def WriteListToCSV(csv_file,csv_columns,data_list):
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.writer(csvfile, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(csv_columns)
            for data in data_list:
                writer.writerow(data)
    except IOError as (errno, strerror):
            print("I/O error({0}): {1}".format(errno, strerror))
    return

jsonfile = open('dkplayers.json', "r")
players = json.load(jsonfile)
wanted = [ 
        'Matthew Stafford', 
           'Matt Ryan',
           'Andy Dalton',
           'Matt Ryan',
           'Philip Rivers',
           'Ryan Fitzpatrick',
           'Brian Hoyer',
           "Le'Veon Bell", 
           'Devonta Freeman',
           'Todd Gurley',
           'Charcandrick West',
           'Doug Martin',
           'Danny Woodhead',
           'Chris Johnson',
           'Antonio Andrews',
           'Julio Jones', 
           'Keenan Allen',
           'Mike Evans',
           'Stefon Diggs',
           'DeAndre Hopkins',
           'Calvin Johnson',
           'Jeremy Maclin',
           'Antonio Brown',
           'Martavis Bryant',
           'Alshon Jeffery',
           'Stefon Diggs',
           'Mike Evans',
           'Kendall Wright',
           'Marvin Jones',
           'Brandon Marshall',
           'Ted Ginn Jr.',
           'Tyler Eifert',
           'Ladarius Green',
           'Jacob Tamme',
           'Eric Ebron',
           'Benjamin Watson',
           'Cardinals ', 
           'Falcons ',
           'Rams ',
           'Seahawks ',
           'Panthers '
        ]



csv_columns = ['Name','Team','Position','Salary','Oppurtunity Score','Points/Oppurtunity']
plyrs = []

for x in wanted:
    sal = int(players[x]['Salary'])
    if players[x]['Position'] == "DST":
        plyrs.append([x,players[x]['teamAbbrev'],players[x]['Position'],sal,'NA', 'NA'])
    else:
        plyrs.append([x,players[x]['teamAbbrev'],players[x]['Position'],sal,players[x]['Oppscore'], players[x]['PtsPerOpp']])

WriteListToCSV('/home/scrabbleadmin/awesomeproject/players.csv',csv_columns,plyrs)

