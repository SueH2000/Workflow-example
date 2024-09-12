# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 22:11:07 2023

@author: MingHeng Hsiung
Task:
    Multiple sequence aligner
    This is a program that 
    1.reads an aligned fasta file.
    2.evaluates the alignment and outputs two measures of the alignment quality: 
        the identity score and the alignment score of all possible pairs. 
    3. It also allow the user to determine the weight matrix. 
       
Usage:python MSA.py -f fasta_file(change the name according to the input data) -p weight_parameters(input from the user) -o output_file(don't forget to change name according to the infile')
"""

#%% 0. argparse
# Setting up argparse, handling inputs from command line.
import argparse
import re
import os
#set how we should enter in the commandline to run the program
parser = argparse.ArgumentParser(prog='MSA_para',
                                 #usage='%(prog)s -f INPUT [-o] OUTPUT [-p] PARAMETER-FILE',
                                 description="""Scores alignments made based
                                 on an input fasta file containing aligned sequences.
                                 """)
#we should get a fasta file as input that start with -f
parser.add_argument('--fasta', '-f', required=True,
                    help='file containing aligned sequences to be scored.')
#a parameter file as scoring parameters should start with -p or --parameter
parser.add_argument('--parameter', '-p', type=str,
                    help="Custom parameters for alignment scores. Allowed \
                    keywords are match, gap, transition and transversion [score]. \
                    Please seperate keywords (string) from values (integers or floats) \
                    with spaces, tabs or =. If a keyword appears several times, the first valid \
                    occuring score will be used. If any keyword cannot be found, the script uses the \
                    default parameter for that keyword instead.")
#a output file should start with -o                       
parser.add_argument('--output', '-o', type=str, default ="output_parameters.txt",
                    help="""output file containing alignment scores per id pair.""")

#shorten the calling 
args = parser.parse_args()


#%% 1. definition setting.
# Define transition and transversion with setting dictionary
transition = {'A':'G', 'G':'A', 'T':'C', 'C':'T'}  #The nucleotides are both pyrimidines or both purines so this is a transition
transversion = {'A':('T','C'), 'G':('T','C'), 'T':('A','G'), 'C':('A','G')} #Change in different chemical classes is a transversion

def alignment_score(x, y): # define the scoring of the alignment
    # x, y -- sequences.
    # set up score
    #Use custom parameters if given,
    if args.parameter:
        parameters=param_file_dict
    #otherwise use default value
    else:
        parameters=default_par
    #Go through the bases in the sequences
    score = 0   # the initial score is zero
    for i, j in zip(x,y): # x,y are 2 sequence, use zip() to make an iterator that aggregates elements from each of the iterables.
    # Returns an iterator of tuples, where the i-th tuple contains the i-th of the element from each of the argument sequence.
        # calculate the score, followings show when each kinds of score counts
        if (i != "?") or (j != "?"):# Check if both characters are not '?'
            
            if  (i =="-") or (j =="-"): # if gaps apear in weather x or y sequence
                score+=parameters["gap"]# count as gap score
            
            elif i == j: # if the element match
                score+=parameters["match"] # count as match scorei != j: # if the elements are different
                
            elif i in transition and j == transition[i]: # if it fit in the transition dictionary
                score+=parameters["transition"] # count as transition score
            elif i in transversion and j in transversion[i]:  # if it fit in the transversion dictionary
                score+=parameters["transversion"] # count as transversion score
    return score

def alignment_identity_p(x, y):# define the ideneity percentage of the alignment
    identity = 0 # initial identity is zero
    for i, j in zip(x,y): 
        if (i != "?") or (j != "?"):# Check if both characters are not '?'
            if (i != "-") or (j != "-"):# Check if both characters are not '-'
                if  i == j: # if the element match
                    identity += 1 # identity counts
                    # set the output format
    Identity_p ='{:.1f}%'.format((identity/len(x))*100)  #len(x) is to count the length of the sequence
    return Identity_p
#%% 2. Error Exceptions.

#Check if the given input files exist?
output=args.output
while True: #if all the files exist 
    try: #account for error
        #check fasta file
        if not os.path.isfile(args.fasta): 
            problematic_file=args.fasta #count as problematic file
            raise FileNotFoundError
        #check parameter if given
        if args.parameter:
            if not os.path.isfile(args.parameter):
                problematic_file=args.parameter #count as problematic file
                raise FileNotFoundError
        
        #If output file is given, check if it already exists:
        if os.path.isfile(output):
            #If it does, ask user if they want to overwrite the output.
            answer=str(input("The output file "+ args.output+ " already exists. Would you like to overwrite it? (Y/N) "))
            if answer.upper()=="Y": #if the user type Y, rewrite it and go out of this loop
                break
            elif answer.upper()=="N":#if the user type N, ask them to give a name for the output file
                new_output=str(input("Please enter a new output name: "))
                if all([e in [" ", "", "\t", "\n"] for e in new_output]):#check if there is invalid word in output name
                    print("This is not a valid output name. Lets try this again.")
                else:
                    output=new_output
                    
            else:#if the user give input other than Y or N
                print("This is not a valid response. Please answer with Y (yes) or N (no).") 
                
        #Break the while loop so that it doesnt run infinitely in case of no output file.
        else:
            break
    except FileNotFoundError: #report the error to tell the user which file is missing
        print("The input file "+ problematic_file + " cannot be found. Please check your spelling and working directory and try again.")
        quit()

#Check if the input file is empty.
if os.stat(args.fasta).st_size==0:
    print("The fasta file is empty. Please check your fasta file and try again.")
    quit()
#%% 3. Get the weigh-parameter from the parameter file


#Default Parameters for Alignment Score. Used if no parameter file is given.

default_par={'gap':-1, 'transition': -1, 'transversion': -2, 'match': 1} 


#If the user gives a parameter file, read off the parameters for scoring.
if args.parameter:
    #initialize parameter file dictionary
    param_file_dict={"match":False, "gap":False, "transition":False, "transversion":False}
    #And a list for potentially not found keys
    problematic_keys=[]
    with open(args.parameter, "r") as param:
        lines="".join(param.readlines()) #reads in file as one string
        for key in list(param_file_dict.keys()): #if we find the key in the string
            #search for keywords for scoring in the file string. Assigns next number (integer or float) as score.
            match = re.search(key + r"[a-z]*[\ +|\t+]*\w*[\ +|\t+]*=?[\ +|\t+]*=?(-?\d+[\.|,]*\d*)", lines)
            if match:#if we find the score after the key
                 #overwrite the current score if it is not a number.
                if type(param_file_dict[key]) not in [int, float]:#extract a numeric value from the string representation of the value 
                    param_file_dict[key]= float(match.group(1)) # the first match
                
            else:
                #If any of the keys cannot be found, raise an error.
                problematic_keys.append(key)
        if len(problematic_keys)!=0: #if there is a error in parameter file
            if len(problematic_keys)==1: #if there is one score missing, use the default score for that key
                print("For "+ key+ """ no score can be found in the given parameter file. We will use the default score """+ str(default_par[key])+ " instead." )
            else: #if there is more than one score missing, use the default score for keys counted in the problematic keys
                scores=[] #initialize the score
                for key in problematic_keys:
                    scores.append(str(default_par[key]))#add score from default score and tell the user what keys are using default score
                print("For the "+ ", ".join(problematic_keys)+ 
                      " no score could be found in the parameter file. The default scores " + ", ".join(scores)+ " will be used respectively.")
            print("For another run please make sure that for match, gap, transition and transversion there are scores \
available in the file. Also make sure that the key word and score are seperated \
only by spaces, = or tabs. If a key is several times in the parameter file, the first \
valid occurence is used.")
            for key in problematic_keys:
                param_file_dict[key]=default_par[key]
#%%Get the input data from the fna file, align the sequrnces with pairs and print out the Identity, Identity percentage, Gaps, Gaps percnetage and total score
# Check if you have the required number of arguments
#import sys
#from pathlib import Path
#if len(sys.argv) == 3 and Path(sys.argv[1]).is_file():#if use a self-defined output file name
# Save each file to a variable
    #infile = sys.argv[1]
    #outfile = sys.argv[2]
# The outfile don't have to exist, it will be created when the file is open as writeable "w".
#elif len(sys.argv) == 2 and Path(sys.argv[1]).is_file():#if use a default output file name
    #infile = sys.argv[1]
    #outfile = "parameters.txt"
#else: #if the number of argv is wrong
    #raise IndexError("Incorroct number of Argument!/n""Usage: python FastaAligner.py input_fasta.fna parameters.txt") 
#if sys.argv == 3 and Path(sys.argv[1]).is_file():

    #infile = sys.argv[1]
# this is the  argument you pass in the terminal (score.extra.fna), which here will be the outfile.
    #outfile = sys.argv[2]
   
       
# The outfile don't have to exist, it will be created when the C:\Users\sueba\AppData\Local\Temp\3871976e-7b08-49a5-bda2-d6cca64df079_RE2_part2.zip.079\RE2_part2\amino_count.pyfile is open as writeable "w".
#else:
    
    #infile = "mtDNA.txt"
    #outfile = "mtDNA_parameters.txt"
#%% 4. Read the infile and print out the score 
#score_gap = float(input("Enter score for a gap (or press Enter to use default, -1): ") or -1)
#score_match = float(input("Enter score for a match (or press Enter to use default, 1): ") or 1)
#score_transition = float(input("Enter score for a transition (or press Enter to use default, -1): ") or -1)
#score_transversion = float(input("Enter score for a transversion (or press Enter to use default, -2): ") or -2)

#allowed characters in the aligned sequences.
allowed_bases=['A','C','G','T','-','?'] 

dic_seq = {} # built a empty dictionary for ID and Sequence
ID = "" # The initial ID is none
Sequence = "" #The initial Sequence is empty
#Initialize invalid sequence Flag
invalid_sequence=False
#If someone gives a nonsense file, put a stop after a few errors.
invalid_counter=0
# open the fna file as reading mode
with open(args.fasta, "r") as seq:
    for line in seq: #parse through the line
        if line.startswith(">"): #find the line start witn">"
            if Sequence!="" and invalid_sequence==False and ID not in dic_seq: #If the sequence is not invalid sequence and the ID didn't exist in the dic alreadly
                dic_seq[ID]=Sequence #the ID be the key and the sequence will be the value correspondingly
            ID=line.strip("\n").strip(">") # remove the">" sign
            Sequence=""  # reset current sequence
            invalid_sequence=False #reset the invalid sequence
        else:
            #check for invalid nucleotides, those sequences are excluded from alignment.
            try:
                for nucleotide in line.strip("\n"): #parse through element in the line 
                    if nucleotide.upper() not in allowed_bases: #make all rhe sequence uppercase and if the sequence have basese that are not allowed
                        raise ValueError #error
            except ValueError:#if there is a value error
                invalid_counter+=1 #count as invalid counter
                if ID!="": #if there is a ID corresponding with the sequence, print out the notice for the user about which ID has invalid sequence
                    print("The aligned sequence with ID "+ ID +""" contained an invalid nucleotides. The id and its corresponding sequence will be excluded from the alignment scores. To have it included, make sure the sequence only contains characters A, G, T, C and - (not case sensitive). \n Note that this could be due to a header missing a ">" at the beginning of its line.""")
                #set flag, to not save sequence and ID in dictionary
                invalid_sequence=True
                if invalid_counter>5: #if there are over 5 invalid sequences
                    print("This file contains too many lines with invalid nucleotides. Are you sure this is a fasta file? Do the headers start with >, and the sequences contain only A, G, T, C and -?")
                    print("Please try again with a valid fasta file.")
                    quit()
            Sequence+=line.strip("\n") #remove the "\n" from sequence line
    
    # Add the last sequence(if there is one) and if it is not count as invalid sequence 
    if Sequence!="" and invalid_sequence==False:
        dic_seq[ID]=Sequence
#print(dic_seq) #If necessary,just to check whether the dictionary is in the correct form we want.

             
# Arrange the sequence in pairs by ID for sequence score 
dic_keys = list(dic_seq.keys()) # make the ID(keys) in the dictionary a list
with open(output, "w") as output: #open the output file as writing mode      
    output.write("SampleA\tSampleB\tIdentityScore\tScore\n") #write the header that was separated with tab            
    for i in range(0,len(dic_keys)): # chose one id in list
        for j in range(i+1,len(dic_keys)): # and another id in list
           #If sequences have different lengths, meaning that they are not aligned and will be excluded from alignment scoring.
           if len(dic_seq[dic_keys[i]])!=len(dic_seq[dic_keys[j]]):
               print("The alignment between the sequences with ids " + dic_keys[i] + " and " +dic_keys[j]+ " could not be scored as they have different lengths.")
               continue
            #score valid alignments
           identity_p = alignment_identity_p(dic_seq[dic_keys[i]],dic_seq[dic_keys[j]])
           score = alignment_score(dic_seq[dic_keys[i]],dic_seq[dic_keys[j]])
            #Write scored alignments into output file with separqtion with tab.
           output.write('{}\t{}\t{}\t{}\n'.format(dic_keys[i], dic_keys[j], identity_p, score))
    