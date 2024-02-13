# topufa
TOol for handling with Pdb-Uniprot-Fasta conversion and Alignment

# Steps #
In a given text file (.txt or .csv), searches for all PDB 4-digit codes
>*in this version only searches for PDB codes using lowercase letters
>*.pdf to be included

Fetch corresponding Uniprot IDs

Fetch corresponding FASTA

Create a blast database with these

Alignment using blastp with your assigned input query fasta file

Output several lists/csv files demonstrating the conversions generated throughout the script execution PLUS output_blastp.txt with the alignment results

# Useful scenarios: #
You want to automatically select several PDB codes mentioned in a text file and compare 'em with a given sequence of yours.

# Place in folder: #
* script1.py 
* your query.fasta
* your text file (txt or csv)
              


> References for installing/using standalone BLASTp: 
> <br />https://blast.ncbi.nlm.nih.gov/doc/blast-help/downloadblastdata.html#downloadblastdata
> <br />https://www.ncbi.nlm.nih.gov/books/NBK52640/
> <br />https://krother.gitbooks.io/biopython-tutorial/content/BLAST.html
