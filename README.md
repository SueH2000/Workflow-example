# Workflow-example
 Fasta parser and Multiple sequence alignments
Created on Thu Oct 19 22:11:07 2023
@author: MingHeng Hsiung

 The Fasta parser
     This is a program that writes a parser that reads the GeneticData –1.txt file and outputs two fasta files, one for mtDNA and one for the Y chromosome.
 Usage:
     python FastaParser.py text_file output_fasta_file
     
The results will show as follows:

![image](https://github.com/user-attachments/assets/4f75cde2-2c33-434e-91d9-033aa79039ea)


Multiple sequence alignments
    This is a program that 
    1. Reads an aligned fasta file.
    2. Evaluate the alignment and output two measures of the alignment quality: 
        the identity score and the alignment score of all possible pairs. 
    3. It also allows the user to determine the weight matrix. 
       
Usage:
    python MSA.py -f fasta_file(change the name according to the input data) -p weight_parameters(input from the user) -o output_file(don't forget to change name   according to the infile')

The results will show as follows:

![image](https://github.com/user-attachments/assets/87438ba9-ec4b-4fb7-865f-73e62b31296d)

