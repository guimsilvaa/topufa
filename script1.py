import os
import re
import csv
import pandas as pd
import requests
from tqdm import tqdm

def find_valid_pdb_codes(text):
    pattern = r'\b(?:[a-z][0-9]|[0-9][a-z])[a-z0-9]{2}\b'
    pdb_codes = re.findall(pattern, text)
    return pdb_codes

def retrieve_uniprot_ids(pdb_codes):
    uniprot_ids = {}
    failed_pdb_codes = []
    for code in tqdm(pdb_codes, desc="Fetching UniProt IDs"):
        url = f"https://www.ebi.ac.uk/pdbe/api/mappings/uniprot/{code}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if code in data and "UniProt" in data[code]:
                uniprot_ids[code] = next(iter(data[code]["UniProt"]))  # Get the first (and only) UniProt ID
            else:
                failed_pdb_codes.append(code)
        else:
            failed_pdb_codes.append(code)
    return uniprot_ids, failed_pdb_codes

def retrieve_fasta_content(uniprot_ids):
    fasta_content = ""
    for uniprot_id in tqdm(uniprot_ids.values(), desc="Fetching FASTA"):
        url = f"https://www.uniprot.org/uniprot/{uniprot_id}.fasta"
        response = requests.get(url)
        if response.status_code == 200:
            fasta_content += response.text
    return fasta_content

if __name__ == "__main__":
    # Fetch the current working directory
    current_directory = os.getcwd()
    print("Current working directory:", current_directory)

    # Prompt the user to enter only the file name
    file_name = input("Enter the name of the file (txt or csv) containing PDB codes (e.g. input.txt): ")

    # Join the current directory with the provided file name
    file_path = os.path.join(current_directory, file_name)

    # Print out the constructed file path
    print("File path:", file_path)

    # Verify if the file exists
    if not os.path.exists(file_path):
        print("File does not exist.")
        exit()

    # Read input text from the specified file
    if file_name.endswith('.txt'):
        with open(file_path, "r") as f:
            example_text = f.read()
    elif file_name.endswith('.csv'):
        with open(file_path, "r") as f:
            reader = csv.reader(f)
            example_text = ' '.join([row[0] for row in reader])
    else:
        print("Invalid file format. Please provide a txt or csv file.")
        exit()

    # Prompt the user to enter the name of the query file
    query_file_name = input("Enter the name of the fasta query file (e.g. query.fasta): ")
    query_file_path = os.path.join(current_directory, query_file_name)
    if not os.path.exists(query_file_path):
        print("Query file does not exist.")
        exit()

    # Find valid PDB codes
    valid_pdb_codes = find_valid_pdb_codes(example_text)

    # Remove PDB duplicates
    unique_pdb_codes = list(set(valid_pdb_codes))

    # Retrieve UniProt IDs
    uniprot_ids, failed_pdb_codes = retrieve_uniprot_ids(unique_pdb_codes)

    # Retrieve fasta content
    fasta_content = retrieve_fasta_content(uniprot_ids)

    # Create DataFrame for successful retrievals
    df = pd.DataFrame({'PDB code': list(uniprot_ids.keys()), 'UniProt ID': list(uniprot_ids.values())})

    # Add sequence order
    df['Order'] = range(1, len(df) + 1)

    # Reorder columns
    df = df[['Order', 'PDB code', 'UniProt ID']]

    # Write successful results to CSV
    output_complete_csv_file = "output_full_list.csv"
    df.to_csv(output_complete_csv_file, index=False)
    print(f"\nA total of {len(df)} unique PDB codes and corresponding UniProt IDs have been found and written to {output_complete_csv_file}")

    # Write failed results to CSV
    failed_csv_file = "out_uniprot_failed.csv"
    with open(failed_csv_file, 'w', newline='') as csvfile:
        fieldnames = ['PDB code', 'UniProt ID']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for pdb_code in failed_pdb_codes:
            writer.writerow({'PDB code': pdb_code, 'UniProt ID': 'Failed to retrieve'})
    print(f"A total of {len(failed_pdb_codes)} PDB codes failed to retrieve UniProt IDs and have been written to {failed_csv_file}")

    # Write PDB codes to a second CSV file separated by commas
    out_pdbs_csv_file = "out_pdbs.csv"
    with open(out_pdbs_csv_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(unique_pdb_codes)
    print(f"\nPDB codes have been written to {out_pdbs_csv_file}")

    # Write UniProt IDs to a third CSV file separated by commas
    out_uniprotids_csv_file = "out_uniprotids.csv"
    with open(out_uniprotids_csv_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(uniprot_ids.values())
    print(f"UniProt IDs have been written to {out_uniprotids_csv_file}")

    # Write fasta content to a single output_all.fasta file
    output_all_fasta_file = "output_all.fasta"
    with open(output_all_fasta_file, 'w') as fasta_file:
        fasta_file.write(fasta_content)
    print(f"\nAll FASTA sequences have been concatenated and written to {output_all_fasta_file}")

    # Run BLASTp with the query file and output_all.fasta
    db_path = os.path.join(current_directory, output_all_fasta_file)
    cmd_makeblastdb = f"makeblastdb -in {db_path} -dbtype prot"
    os.system(cmd_makeblastdb)

    # Run BLASTp with the query file and output_all.fasta
    cmd_blastp = f"blastp -query {query_file_path} -db {output_all_fasta_file} -out output_blastp.txt -outfmt 7"
    os.system(cmd_blastp)

    output_blastp = "output_blastp.txt"

    print(f"The alignment using BLASTp was completed successfully. \nPlease check details on {output_blastp} \n\nThank you for using my script! \nAuthor: Dr. Guilherme M. Silva - Harvard Medical School - BIDMC - guimsilva@gmail.com \n ")
    
