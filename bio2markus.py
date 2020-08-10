# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 13:06:45 2020

@author: dongrong
"""

"""
This file reads the tag results of entity recognition and convert them into 
html files with entity highlighted(observable on MARKUS), including regin, year, office & place

txt files in directory 'tag_results' are read
html files output are stored in dictionary "markus"

The Python version of this script is Python 3.7.4

Step1:
    The input should be a document folder named "tag_results" and should be
    put under the same directory with this file
    At the same time, documents in "tag_results" shall be of n.txt form,
    where n is an integer that n>0

Step 2:
    The script reads the txt files and converts the BIO form into xml forms readable
    on Markus

Step3:
    The script outputs the xml files. The output forms will be organized in a 
    document folder named "markus", which will also be put under the same directory

"""

import numpy as np
import pandas as pd
import os
import re


#tags needs to be highlighted in the output xml
B_tag=['B-office_title','B-date_reign','B-date_year','B-place_placename']
I_tag=['I-office_title','I-date_reign','I-date_year','I-place_placename']
#we don't highlight O tags
O_tag=['O']

#in the current task, B-office_voa and I-office_voa are neglected.
neglect=['B-offic_voa','I-office_voa']

#some punctuations are misclassified into I_tags or B_tags(only common puncs are included)
#you are welcomed to add more punctuations into ch_punc according to your need
ch_punc=['，',' ','。','、','！','~','？','；',':']


#map tags to keys in dictionary "mark"
mapping={'B-office_title':'office',
         'B-date_reign':'reign',
         'B-date_year':'year',
         'B-place_placename':'place',
         I_tag[0]:'span',
         I_tag[1]:'span',
         I_tag[2]:'span',
         I_tag[3]:'span'
        }

#the "mark" dictionary contain abbreviations of complex xml 
mark={'span':'</span>',
        'place':'<span class="markup manual unsolved placeName" type="placeName">',
        'reign':'<span class="markup manual unsolved reign" type="reign">',
        'year':'<span class="markup manual unsolved reign_year" type="reign_year">',
        'office':'<span class="markup manual unsolved officialTitle" type="officialTitle">',
        'id':'<span class="markup manual unsolved tempID" type="tempID">',
        'hidchar':r'''<span class="space hiddenChar" contenteditable="false" unselectable="on" onclick="SelectText(event, this);">·'''
        }



#header and rear of the xml file
head=r'''<div class="doc" markupfullname="false" markuppartialname="false" markupnianhao="false" markupofficaltitle="false" markupplacename="false" filename="sample" tag="{&quot;fullName&quot;:{&quot;buttonName&quot;:&quot;&amp;#(22995);&amp;#(21517);&quot;,&quot;visible&quot;:true,&quot;color&quot;:&quot;#d9534f&quot;,&quot;status&quot;:&quot;&quot;},&quot;partialName&quot;:{&quot;buttonName&quot;:&quot;&amp;#(21029);&amp;#(21517);&quot;,&quot;visible&quot;:true,&quot;color&quot;:&quot;#f0ad4e&quot;,&quot;status&quot;:&quot;&quot;},&quot;placeName&quot;:{&quot;buttonName&quot;:&quot;&amp;#(22320);&amp;#(21517);&quot;,&quot;visible&quot;:true,&quot;color&quot;:&quot;#428bca&quot;,&quot;status&quot;:&quot;&quot;},&quot;officialTitle&quot;:{&quot;buttonName&quot;:&quot;&amp;#(23448);&amp;#(21517);&quot;,&quot;visible&quot;:true,&quot;color&quot;:&quot;#5bc0de&quot;,&quot;status&quot;:&quot;&quot;},&quot;timePeriod&quot;:{&quot;buttonName&quot;:&quot;&amp;#(26178);&amp;#(38291);&quot;,&quot;visible&quot;:true,&quot;color&quot;:&quot;green&quot;,&quot;status&quot;:&quot;&quot;},&quot;reign&quot;:{&quot;color&quot;:&quot;#99ccff&quot;,&quot;buttonName&quot;:&quot;&amp;#(24180);&amp;#(34399);&quot;,&quot;visible&quot;:true,&quot;status&quot;:&quot;&quot;},&quot;reign_year&quot;:{&quot;color&quot;:&quot;#993366&quot;,&quot;buttonName&quot;:&quot;&amp;#(24180);&amp;#(34399);&amp;#(24180);&quot;,&quot;visible&quot;:true,&quot;status&quot;:&quot;&quot;},&quot;tempID&quot;:{&quot;color&quot;:&quot;#800000&quot;,&quot;buttonName&quot;:&quot;ID&quot;,&quot;visible&quot;:true,&quot;status&quot;:&quot;noColor&quot;},&quot;comparativeus&quot;:{&quot;buttonName&quot;:&quot;comparativus&quot;,&quot;visible&quot;:true,&quot;color&quot;:&quot;green&quot;,&quot;status&quot;:&quot;&quot;},&quot;dilaPerson&quot;:{&quot;buttonName&quot;:&quot;dilaPerson&quot;,&quot;visible&quot;:true,&quot;color&quot;:&quot;#d6616b&quot;,&quot;status&quot;:&quot;&quot;},&quot;dilaPlace&quot;:{&quot;buttonName&quot;:&quot;dilaPlace&quot;,&quot;visible&quot;:true,&quot;color&quot;:&quot;#6b6ecf&quot;,&quot;status&quot;:&quot;&quot;},&quot;koreanPerson&quot;:{&quot;buttonName&quot;:&quot;KPerson&quot;,&quot;visible&quot;:true,&quot;color&quot;:&quot;#b94a48&quot;,&quot;status&quot;:&quot;&quot;},&quot;koreanBook&quot;:{&quot;buttonName&quot;:&quot;KBook&quot;,&quot;visible&quot;:true,&quot;color&quot;:&quot;#428bca&quot;,&quot;status&quot;:&quot;&quot;},&quot;koreanPlace&quot;:{&quot;buttonName&quot;:&quot;KPlace&quot;,&quot;visible&quot;:true,&quot;color&quot;:&quot;#42ca86&quot;,&quot;status&quot;:&quot;&quot;},&quot;koreanOfficialTitle&quot;:{&quot;buttonName&quot;:&quot;KOfficialTitle&quot;,&quot;visible&quot;:true,&quot;color&quot;:&quot;#17becf&quot;,&quot;status&quot;:&quot;&quot;}}"><pre contenteditable="false">'''
rear='''</pre></div>'''

#generate list of file names with path
#files genrated have formats of "./tag_results/xxx.txt"
#output: a list of files names
def fileNameGen():
    os.makedirs('./markus')
    file_name=os.listdir('./tag_results')
    
    for i in range(0,len(file_name)):
        file_name[i]='./tag_results/'+file_name[i]
    
    
    #regular expression, extract numbers from file names(as the index para to textGen())
    numreg=re.compile(r'(\d)+')
    
    #reindex file_name
    #since the order of file_name acquired above is messy
    indes=[]
    for i in range(0,len(file_name)):
        temp=numreg.search(file_name[i])
        indes.append(int(temp.group()))
    
    df=pd.Series(file_name,index=indes)
    file_name=df.reindex(np.sort(indes))
    file_name=list(file_name)
    
    return file_name

#convert BIO tags to xml mark
#bio receives a pandas frame with 2 series: characters in the bio and their tags
#index is the id of the bio
def textGen(bio,index):
    #characters and tags of bio
    char=bio['char']
    tag=bio['tag']
    
    #add xml markers to related characters
    for i in range(0,len(tag)):
        #if tag[i] is in B_tag, then let char[i] be "<span...>char[i]"
        if tag[i] in B_tag:
            char[i]=mark[mapping[tag[i]]]+char[i]
        #when tag[i] is B or I but not voa
        if tag[i] in B_tag or tag[i] in I_tag:
            #detect if tag[i] is the end of a certain kind of tag
            if i<(len(tag)-1) and not(tag[i+1] in I_tag):
                char[i]=char[i]+mark['span']
            elif i==len(tag)-1:
                char[i]=char[i]+mark['span']
    
    #group all xml markers together    
    text=list(char)
    text=''.join(text)
    head=''.join([mark['id'],str(index),mark['span'],mark['hidchar'],mark['span']])
    text=head+text
 
    
    return text

#some punctuations are misclassified as B or I tags, correct them
def textWash(bio):
    char=bio['char']
    tag=bio['tag']
    
    for i in range(0,len(tag)):
        if not(tag[i] in O_tag) and char[i] in ch_punc:
            tag[i]=O_tag[0]
            if i<len(tag)-1 and tag[i+1]!='O':
                if tag[i+1]=='B-office_voa' or tag[i+1]=='I-office_voa':
                    tag[i+1]='B-office_voa'
                else:
                    tag[i+1]=B_tag[I_tag.index(tag[i+1])]
    
    return bio



#generate xml files
#as the output, file_num files will be generated, each containing bio_num biographies inside
def xmlGen(file_name,file_num,bio_num):
    #regular expression, extract numbers from file names(as the index para to textGen())
    numreg=re.compile(r'(\d)+')
    for k in range(0,file_num):
        f=open(''.join(['./markus/',str(k),'.html']),'w',encoding='utf-8')
        f.write(head)
        f.write('\n')
        for j in range(0,bio_num):
            bio=pd.read_table(file_name[k*bio_num+j])
            bio=textWash(bio)
            index=numreg.search(file_name[k*bio_num+j])
            index=index.group()
            text=textGen(bio,index)
            f.write(text)
            f.write('\n')
        #print(k)
        
    f.write(rear)
    f.close()
 

#you can use the main() down there or you could just import
'''
#main()
if __name__=='__main__':
    
    #Step1: read the files stored in './tag_results'
    file_name=fileNameGen()
    
    #9158=241*38
    file_num=241
    bio_num=38
    
    #Step 2&3: convert bio to xml and store the output in folder './markus'
    xmlGen(file_name,file_num,bio_num)
  '''  
    
    
    
    
    
            
    
        
    
    


    