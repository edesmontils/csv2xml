#!/usr/bin/env python3.7
# coding: utf8

# La première ligne contient les entêtes obligatoirement (pour l'instant...)

import csv
import sys
import os
import glob
import argparse


parser = argparse.ArgumentParser(description='csv2xml : permet de convertir un document CSV en XML')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-f", "--file", dest="csvFile", help="Nom du fichier CSV")
group.add_argument("-d", "--dir", action="store_true", help="Tous les fichiers CSV du répertoire courant")

parser.add_argument("-i", "--id", default='', dest="idList", help='colonnes qui forment l\'identifiant sous la forme “c1 c2..." (remplacer les espaces par des _)')
parser.add_argument("-g", "--group", default='', dest="groupList", help='colonnes qui sont "id" à regrouper sous la forme “pref c1 c2..." (remplacer les espaces par des _)')

parser.add_argument("-n", "--name", default='lgn', dest="name", help='Nom des éléments ("lgn" par défaut)')
parser.add_argument("-r", "--root", default='csv', dest="root", help='Nom de la racine ("csv" par défaut)')

parser.add_argument("-k", action="store_true", help="Les éléments vides ne sont pas mis")

args = parser.parse_args()

if args.dir :
    os.chdir('.')
    csvFiles = glob.glob('*.csv')
else :
    arg = args.csvFile
    if arg.endswith('.csv'):
        csvFiles = [arg]    

if not(args.groupList == '') :
    groupList = args.groupList.split()
    prefix = groupList[0]
    groupList = groupList[1:]
    print(groupList)
else : 
    groupList = [] 
    prefix = ''

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

            # Génération de l'entête
            xmlData.write('<?xml version="1.0" encoding="utf-8" standalone="yes"?>' + "\n")

            # Génération de la DTD
            xmlData.write('<!DOCTYPE '+args.root+' ['+ "\n")

            if groupList == [] :
                xmlData.write('   <!ELEMENT '+args.root+' ('+args.name+')* >'+ "\n" )
            else: 
                xmlData.write('   <!ELEMENT '+args.root+' ('+'group'+')* >'+ "\n" )
                xmlData.write('   <!ELEMENT '+'group'+' ('+args.name+')* >'+ "\n" )
                xmlData.write('   <!ATTLIST '+'group xml:id ID #REQUIRED'+" >\n" )

            xmlData.write('   <!ELEMENT '+args.name+' (')
            if args.k: xmlData.write(csvReader.fieldnames[0]+'?' )
            else: xmlData.write(csvReader.fieldnames[0] )
            for ele in csvReader.fieldnames[1:] :
                xmlData.write(', '+ele)
                if args.k: xmlData.write('?' )
            xmlData.write(') >'+ "\n")
            xmlData.write('   <!ATTLIST '+args.name+ "\n" )
            xmlData.write('           xml:id ID #REQUIRED'+ "\n" )
            xmlData.write('           no CDATA #REQUIRED'+ "\n" )
            xmlData.write('   >'+ "\n" )
            for ele in csvReader.fieldnames :
                xmlData.write('   <!ELEMENT '+ele+ ' (#PCDATA) >'+ "\n")

            xmlData.write(']>'+ "\n")

            # Génération du corps
            xmlData.write('<'+args.root+'>' + "\n")

            lgn = 0
            noGrp = ''
            tab = 1
            for row in csvReader:
                id_ = args.name

                newGrp = ''
                for e in groupList :
                    newGrp = newGrp + row[e]

                if noGrp != newGrp :
                    if noGrp != '' : xmlData.write('    </'+'group'+'>' + "\n")
                    xmlData.write('    <'+'group'+' xml:id="'+prefix+newGrp+'">' + "\n")

                for c in csvReader.fieldnames :
                    if c.replace(' ', '_') in idList : id_ = id_ + '.' + row[c]
                if id_ != args.name :
                    xmlData.write('       <'+args.name+' xml:id="'+id_+'" no="'+str(lgn)+'">' + "\n")
                else : xmlData.write('       <'+args.name+' xml:id="'+id_+str(lgn)+'" no="'+str(lgn)+'">' + "\n")


                for i in csvReader.fieldnames:
                    if not(args.k and row[i] == '') : 
                        xmlData.write('           ' + '<' + i.replace(' ', '_') + '>' \
                                  + row[i].replace('<','&lt;').replace('>','&gt;') + '</' + i.replace(' ', '_') + '>' + "\n")
                xmlData.write('       </'+args.name+'>' + "\n")


                noGrp = newGrp
                lgn +=1

            if noGrp != '' : xmlData.write('    </'+'group'+'>' + "\n")
            xmlData.write('</'+args.root+'>' + "\n")
print('Fin')