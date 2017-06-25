#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 The sentence-meter takes TEI documents, removes unnecessary elements from it,
 divides the plain text into sentences, and outputs a graph.
 By Andreas Dittrich, 2017
"""

import re,glob,textwrap,statistics,numpy
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

def splitter(text):
    """ split text in sentences """
    vorpunkt = "(?<!\d\.)(?<!\b\w\.)(?<!Mag\.)(?<!Dr\.)(?<!M[rs]\.)(?<!Mrs\.)(?<!usw\.)(?<!etc\.)(?<!bzw\.)(?<!usf\.)(?<!z\.B\.)(?<!\b[SsPp]\.)(?<!\bca\.)(?<!\bsen\.)(?<!Sep\.)(?<!Sept\.)(?<!Nr\.)(?<!\bmin\.)(?<!\bmind\.)(?<!\bmax\.)"
    s_regex = vorpunkt + "(?<=…|\!|\?|\:|\;|\.|\n|»|«|›|‹) +(?![a-zöäü])"
    sentences = re.split(s_regex,text)
    return sentences

def printlongest(sentences):
    longest= max(sentences, key=len)
    print( "~" * 57)
    print( "Longest sentence ("+str(len(longest.split()))+" words):" )
    print( textwrap.fill( longest , width=57, subsequent_indent="   ") )
    print( "~" * 57)

def printgraph(sentences,filename):
    """ print graph """
    x=range(0,len(sentences))
    y=[len(s.split()) for s in sentences]
    plt.title(re.split("/",filename)[-1])
    plt.ylabel("words")
    # plt.plot(y) # line plot (faster)
    plt.bar(x,y) # bar plot
    plt.show()



######################################################################
## MAIN


# filename=sorted(glob.glob('*.xml'))
filename=sorted(glob.glob('*.xml'))

print("Runnging through divs, counting…")
divcount=0
for file in filename:
    with open(file, "r", encoding="utf-8") as fh:
        soup=BeautifulSoup(fh.read(), "lxml-xml")
        for div in soup.body.find_all("div", type="work"):
        	divcount+=1


counter=0
f, axarr = plt.subplots(divcount, figsize=(15,100), sharex=True, sharey=True)

print("Opening file per file…")
for file in filename:
    with open(file, "r", encoding="utf-8") as fh:
        textinput=re.sub("(\r)?\n","", fh.read())
        textinput=re.sub('<lb break="no"/>',"", textinput)
        textinput=re.sub('<lb/>'," ", textinput)
        soup=BeautifulSoup(textinput, "lxml-xml")
        for div in soup.body.find_all("div", type="work"):
            for match in div.find_all("fw"):
                match.decompose()               # remove fw-tags
            for match in div.find_all("pb"):
                match.decompose()               # remove pb-tags
            for match in div.find_all("speaker"):
                match.decompose()
            for match in div.find_all("stage"):
                match.decompose()
            for match in div.find_all("figure"):
                match.decompose()               # remove figure-tags (paragraphs in it are comments)
            for match in div.find_all("note"):
                match.decompose()               # remove note-tags (footnotes etc)
            for match in div.find_all("lb"):    # remove lb-tags
                try:
                    if match["break"]:
                        match.unwrap()
                except:
                    match.string=" "
                    match.unwrap()

            head=div.find_next("head").get_text()

            text=div.get_text()
            text=re.sub("(\r)?\n+"," ",text)
            text=re.sub(" +"," ",text)

            sentences=splitter( text )
            sentencelengths=list()
            for s in sentences:
                sentencelengths.append(len(s))

            # statistics:
            satzanzahl   =str(  len(sentencelengths) )
            medianlength =str(  statistics.median(sentencelengths) )
            longestlength=str(  max(sentencelengths) )
            
            optitle=re.sub("\W","_", head)

            # plot
            l=satzanzahl+" / "+longestlength+" / "+medianlength
            axarr[counter].bar( range(0,len(sentencelengths)) , sentencelengths , edgecolor='blue', color='blue', label=l)

            axarr[counter].set_title(head)
            axarr[counter].set_xlabel("sentences")
            axarr[counter].set_ylabel("characters")
            
            axarr[counter].legend()

            print("  Done: "+ head)
            counter+=1

f.text(0,0,"Legende: Anzahl der Sätze / Länge des längsten Satzes / durchschnittliche Satzlänge (Median)")
f.tight_layout()
f.savefig("alldivs.pdf")
f.show()