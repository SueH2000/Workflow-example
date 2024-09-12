# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 14:48:48 2023

@author: MingHeng Hsiung

 The parser
 Task:
     This program is specifically written to be the parser that reads the
     GeneticData_1.txt file and outputs two fasta files, one for mtDNA
     and one for the Y chromosome.
 Usage:
     python FastaParser.py text_file(GenecticData) output_fasta
     """


#%% 0.Set the arguments.
import sys
from pathlib import Path
if len(sys.argv) == 4 and Path(sys.argv[1]).is_file():#if use a self-defined output file name
# Save each file to a variable
    infile = sys.argv[1]
    outfile_mtDNA = sys.argv[2]
    outfile_Y = sys.argv[3]
#The outfile don't have to exist, it will be created when the file is open as writeable "w".
elif len(sys.argv) == 2 and Path(sys.argv[1]).is_file():#if use a default output file name
    infile = sys.argv[1]
    outfile_mtDNA = "mtDNA.fna"
    outfile_Y = "Y.fna"
else: #if the number of argv is wrong
    raise IndexError("Incorroct number of Argument!/n""Usage: python FastaParser.py input_txt")    


#%% 1.The parser. Parse through the file and print out the targeted ID and the sequences into fasta file.

#initialize a variable for sequence (needed for lines in fasta)
fasta_mtDNA = ""
fasta_Y = ""
#Initialize a ID variable
ID = None

#Open the input file as reading mode and 2 output files 
with open(infile, "r",  encoding='cp950', errors='replace') as data, open(outfile_mtDNA,"w", encoding='utf-8') as mtDNA_output, open(outfile_Y,"w", encoding='utf-8') as Y_output:
#noted in this file, there is a sign that cannot recognized by utf-8, so here we use cp950 encoding and replace the error part(that stange sign)
    data = data.read() #read the data
    data = data.replace('\n\n\n','\n\n') #To make sure each paragraph have same \n
    data = data.replace('>','')#remove extra marks
    paragraphs = data.strip().split('\n\n') #Split the paragraph by empty line between them
    
    #print(paragraphs) #Just to check the paragraph were separated correctly
    for paragraph in paragraphs: #parse through each paragraph
        lines = paragraph.split('\n') #split the paragraph with \n
        ID = lines[0] #take the first index as ID 
# find the position of specific element in the list        
        index1 = None #initializing the index1 (position)
        index2 = None #initializing index2 (position)

        for i, element in enumerate(lines): #parsethrough the lines
            if element == "mtDNA": #if find the specific element
                index1 = i #record the position of that element
            if element == "Y chromosome":#if find the specific element
                index2 = i #record the position of that element
                break #go out of this loop

        # After with got the position of the specific elements, we can get the sequence after that variable
        if index1 is not None and index1 < len(lines) - 1: #if the index exist and witin the whole list
            mtseq = lines[index1 + 1] #take the next item as sequence
            fasta_mtDNA += f">{ID}\n{mtseq}\n" #make it a fasta format
                  
        if index2 is not None and index2 < len(lines) - 1:#if the index exist and witin the whole lists
            Yseq = lines[index2 + 1] #take the next item as sequence
            fasta_Y += f">{ID}\n{Yseq}\n" #make it a fasta format
    print(fasta_mtDNA, file = mtDNA_output)   #print the result into outputfile
    #print(fasta_mtDNA)
    print(fasta_Y, file = Y_output)  #print the result into outputfile
    #print(fasta_Y)      
    
