# csv2xml.py
# La première ligne contient les entêtes obligatoirement (pour l'instant...)

# TODO
# - en ligne de commande, spécifier si 1ere ligne avec noms ou pas
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

parser.add_argument("-i", "--id", default='', dest="idList", help="colonnes qui forment l'identifiant")

args = parser.parse_args()

if args.dir :
    os.chdir('.')
    csvFiles = glob.glob('*.csv')
else :
    arg = args.csvFile
    if arg.endswith('.csv'):
        csvFiles = [arg]    

if not(args.idList == '') :
    idList = args.idList.split()
    print(idList)
else : idList = [] 

for csvFileName in csvFiles:
    xmlFile = csvFileName[:-4] + '.xml'
    print("Transfortation de "+csvFileName+" en "+xmlFile)
    
    with open(csvFileName, 'r') as csvFile :
        csvReader = csv.DictReader(csvFile)

        with open(xmlFile, 'w') as xmlData :
            xmlData.write('<?xml version="1.0"?>' + "\n")
            xmlData.write('<csv>' + "\n")

            lgn = 0
            for row in csvReader:
                id_ = 'id'
                for c in csvReader.fieldnames :
                    if c.replace(' ', '_') in idList : id_ = id_ + '_' + row[c]
                if id_ != 'id' :
                    xmlData.write('    <lgn xml:id="'+id_+'" no="'+str(lgn)+'">' + "\n")
                else : xmlData.write('    <lgn xml:id="'+id_+str(lgn)+'" no="'+str(lgn)+'">' + "\n")
                for i in csvReader.fieldnames:
                    xmlData.write('        ' + '<' + i.replace(' ', '_') + '>' \
                                  + row[i].replace('<','&lt;').replace('>','&gt;') + '</' + i.replace(' ', '_') + '>' + "\n")
                xmlData.write('    </lgn>' + "\n")
                        
                lgn +=1

            xmlData.write('</csv>' + "\n")