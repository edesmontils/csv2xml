# csv2xml

## Utilisation

```
usage: csv2xml.py [-h] (-f CSVFILE | -d) [-i IDLIST] [-n NAME] [-r ROOT] [-k]

csv2xml : permet de convertir un document CSV en XML

optional arguments:
  -h, --help            show this help message and exit
  -f CSVFILE, --file CSVFILE
                        Nom du fichier CSV
  -d, --dir             Tous les fichiers CSV du répertoire courant
  -s DELIMITER, --sep DELIMITER
                        délimiteur de colonnes ("," par défaut)
  -i IDLIST, --id IDLIST
                        colonnes qui forment l'identifiant sous la forme “c1
                        c2..." (remplacer les espaces par des _)
  -g GROUPLIST, --group GROUPLIST
                        colonnes qui sont "id" à regrouper sous la forme “pref
                        c1 c2..." (remplacer les espaces par des _)
  -n NAME, --name NAME  Nom des éléments ("lgn" par défaut)
  -r ROOT, --root ROOT  Nom de la racine ("csv" par défaut)
  -k                    Les éléments vides ne sont pas mis.
  -dd                   Suppression des lignes successives identiques.
```

## Librairies utiles et Python

Ce programme utilise les librairies "argparse", "csv", "os", "sys" et "glob". Il a été testé avec Python 3.6.10.

## Exemple

### Document CSV "test.csv" :

```csv
c1,c2,c3
1,2,3
2,3,4
3,4,5
6,,8
9,10,11
```

### Commande :

```shell
python csv2xml.py -f test.csv -r toto -n ltl -k
```

### Résultat "test.xml" :

```xml
<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<!DOCTYPE toto [
   <!ELEMENT toto (ltl)* >
   <!ELEMENT ltl (c1?, c2?, c3?) >
   <!ATTLIST ltl xml:id ID #REQUIRED no CDATA #REQUIRED >
   <!ELEMENT c1 (#PCDATA) >
   <!ELEMENT c2 (#PCDATA) >
   <!ELEMENT c3 (#PCDATA) >
]>
<toto>
    <ltl xml:id="id0" no="0">
        <c1>1</c1>
        <c2>2</c2>
        <c3>3</c3>
    </ltl>
    <ltl xml:id="id1" no="1">
        <c1>2</c1>
        <c2>3</c2>
        <c3>4</c3>
    </ltl>
    <ltl xml:id="id2" no="2">
        <c1>3</c1>
        <c2>4</c2>
        <c3>5</c3>
    </ltl>
    <ltl xml:id="id3" no="3">
        <c1>6</c1>
        <c3>8</c3>
    </ltl>
    <ltl xml:id="id4" no="4">
        <c1>9</c1>
        <c2>10</c2>
        <c3>11</c3>
    </ltl>
</toto>
```

## Copyright

GNU General Public License (GNU GPL) v3.0



© E. Desmontils, Université de Nantes, Novembre 2021

