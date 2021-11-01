# csv2xml.py
# La première ligne contient les entêtes obligatoirement (pour l'instant...)

# TODO
# - paramètres de la ligne de commande avec la lib qui va bien
# - en ligne de commande définir l'id et ajouter l'attribut xml:id
# - mettre en attribut les données "courtes" (comment les identifier ? est-ce que 1ere ligne suffit ?)
# - gérer l'encodage (sans doute utf-8 par défaut)
# - gérer les caractères &, ", ' dans mes cdc
# - si grand texte, section CDATA putôt que redéfinition des caractères dangereux.

import csv
import sys
import os
import glob

# the optional command-line argument maybe a CSV file or a folder
if len(sys.argv) == 2:
    arg = sys.argv[1].lower()
    if arg.endswith('.csv'): # if a CSV file then convert only that file
        csvFiles = [arg]
    else: # if a folder path then convert all CSV files in the that folder
        os.chdir(arg)
        csvFiles = glob.glob('*.csv')
# if no command-line argument then convert all CSV files in the current folder
elif len(sys.argv) == 1:
    csvFiles = glob.glob('*.csv')
else:
    os._exit(1)


for csvFileName in csvFiles:
    xmlFile = csvFileName[:-4] + '.xml'
    print("Transfortation de "+csvFileName+" en "+xmlFile)
    
    with open(csvFileName, 'r') as csvFile :
        csvReader = csv.reader(csvFile)

        with open(xmlFile, 'w') as xmlData :
            xmlData.write('<?xml version="1.0"?>' + "\n")
            xmlData.write('<csv>' + "\n")

            lgn = 0
            for row in csvReader:
                if lgn == 0:
                    tags = row
                    for i in range(len(tags)):
                        tags[i] = tags[i].replace(' ', '_')
                else: 
                    xmlData.write('    <lgn no="'+str(lgn)+'">' + "\n")
                    for i in range(len(tags)):
                        xmlData.write('        ' + '<' + tags[i] + '>' \
                                      + row[i].replace('<','&lt;').replace('>','&gt;') + '</' + tags[i] + '>' + "\n")
                    xmlData.write('    </lgn>' + "\n")
                        
                lgn +=1

            xmlData.write('</csv>' + "\n")