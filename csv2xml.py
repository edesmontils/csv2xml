# csv2xml.py
# La première ligne contient les entêtes obligatoirement (pour l'instant...)

# TODO
# - paramètres de la ligne de commande avec la lib qui va bien
# - en ligne de commande définir l'id et ajouter l'attribut xml:id
# - mettre en attribut les données "courtes" (comment les identifier ? est-ce que 1ere ligne suffit ?)
# - gérer l'encodage (sans doute utf-8 par défaut)
# - gérer les caractères &, ", ' dans les cdc
# - si grand texte, section CDATA putôt que redéfinition des caractères dangereux.

import csv
import sys
import os
import glob
import argparse


parser = argparse.ArgumentParser(description='csv2xml converter')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-f", "--file", dest="csvFile", help="Nom du fichier CSV")
group.add_argument("-d", "--dir", action="store_true", help="Tous les fichiers CSV du répertoire courant")

args = parser.parse_args()

if args.dir :
    os.chdir('.')
    csvFiles = glob.glob('*.csv')
else :
    arg = args.csvFile
    if arg.endswith('.csv'):
        csvFiles = [arg]    



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