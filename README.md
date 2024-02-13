# topufa
TOol for handling with Pdb-Uniprot-Fasta conversion and Alignment

# Steps #

1) In a given text file (.txt or .csv), searches for all PDB 4-digit codes
>*in this version only searches for PDB codes using lowercase letters
>
>*.pdf to be included

2) Fetch corresponding Uniprot IDs

3) Fetch corresponding FASTA

4) Create a BLAST database with these

5) BLASTp alignment between this database and your assigned input-query fasta file

6) Output several lists/csv files demonstrating the conversions generated throughout the script execution PLUS output_blastp.txt with the alignment results

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
