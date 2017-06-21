#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 The sentence-meter takes TEI documents, removes unnecessary elements from it,
 divides the plain text into sentences, and outputs a graph.
 By Andreas Dittrich, 2017
"""
import re,textwrap
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

def teiextractor(inp):
    """ extract not needed TEI-elements """
    for match in inp.find_all("fw"):
        match.decompose()               # remove fw-tags
    for match in inp.find_all("pb"):
        match.decompose()               # remove pb-tags
    # remove linebreaks etc.
    for match in inp.find_all("speaker"):
        match.decompose()
    for match in inp.find_all("stage"):
        match.decompose()
    for match in inp.find_all("figure"):
        match.decompose()               # remove figure-tags (paragraphs in it are comments)
    for match in inp.find_all("note"):
        match.decompose()               # remove note-tags (footnotes etc)
    for match in inp.find_all("lb"):    # remove lb-tags
        try:
            if match["break"]:
                match.unwrap()
        except:
            match.string=" "
            match.unwrap()
    return inp

def readingtext(filename):
    """ reads text from filename, extracts text and returns plain text """
    with open(filename, "r", encoding="utf-8") as fh:
        soup=BeautifulSoup(fh.read(), "lxml-xml")
        text=teiextractor(soup.body).get_text()
        text=re.sub("\n+"," ",text)
        text=re.sub(" +"," ",text)
        return text

def splitter(text):
    """ split text in sentences """
    vorpunkt = "(?<!\d\.)(?<!\b\w\.)(?<!Mag\.)(?<!Dr\.)(?<!M[rs]\.)(?<!Mrs\.)(?<!usw\.)(?<!etc\.)(?<!bzw\.)(?<!usf\.)(?<!z\.B\.)(?<!\b[SsPp]\.)(?<!\bca\.)(?<!\bsen\.)(?<!Sep\.)(?<!Sept\.)(?<!Nr\.)(?<!\bmin\.)(?<!\bmind\.)(?<!\bmax\.)"
    s_regex = vorpunkt + "(?<=…|\!|\?|\:|\;|\.|\n|»|«|›|‹) +(?![a-zöäü])"
    sentences = re.split(s_regex,text)
    return sentences

def printlongest(sentences):
    print( "~" * 57)
    print( "Longest sentence ("+str(len(sentences))+" words):" )
    print( textwrap.fill( max(sentences, key=len) , width=57, subsequent_indent="   ") )
    print( "~" * 57)

def printgraph(sentences,filename):
    """ print graph """
    x=range(0,len(sentences))
    y=[len(l) for l in sentences]
    plt.title(re.split("/",filename)[-1])
    plt.plot(x,y)
    plt.show()

def showsentences(sentences):
    for s in sentences:
        print("- ", s)

def main(filename, choice):
    sentences=splitter( readingtext(filename) )
    if choice=="1":
        printgraph(    sentences , filename)
    if choice=="2":
        printlongest(  sentences )
    if choice=="3":
        showsentences( sentences )


# Print menu
def print_menu():
    print( 20 * "~" , " SENCTENCE METER " , 20 * "~")
    print( "0. Enter other filename / path" )
    print( "1. print graph of sentence lengths")
    print( "2. print longest sentence")
    print( "3. print all sentences")
    print( "4. exit")
    print( 57 * "~")
filename=input("Please enter filename or path to file: ")
loop=True
while loop:
    print_menu()
    choice = input("Enter your choice [0-4]: ")
    if choice=="0":
        filename=input("Please enter filename or path to file: ")
    if choice=="1":
        main(filename, "1")
    if choice=="2":
        main(filename, "2")
    if choice=="3":
        main(filename, "3")
    elif choice=="4" or choice=="x" or choice=="q":
        loop=False
    else:
        continue
