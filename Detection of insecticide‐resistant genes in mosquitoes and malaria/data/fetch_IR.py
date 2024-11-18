import os
import re
import csv
import sys
import pandas as pd

# Main program
def main():
    if len(sys.argv) != 4:
        print("Usage: python process_vcf.py <vcf_file> <drug_resistance_file> <output_dir>")
        sys.exit(1)

    # Get input file paths and output directory from command line
    vcf_file = sys.argv[1]  # VCF file path
    drug_resistance_file = sys.argv[2]  # Drug resistance gene Excel file path
    output_dir = sys.argv[3]  # Output directory

    # Create the output directory
    os.makedirs(output_dir, exist_ok=True)
    print(f"Created main output directory: {output_dir}")

    # Read the drug resistance gene Excel file using pandas
    gene_info = {}
    drug_resistance_data = pd.read_excel(drug_resistance_file)

    # Iterate through Excel data and store information in a dictionary
    for _, row in drug_resistance_data.iterrows():
        key = f"{row['CHROM']}_{row['POS']}"
        gene_info[key] = {
            "gene_name": row["Gene Name"],
            "drug_resistance": row["Drug Resistance"],
            "marker": row["Marker"]
        }
        print(f"Loaded gene info for {key}: {gene_info[key]}")

    # Read the VCF file and extract sample information
    with open(vcf_file) as f:
        lines = f.readlines()

    # Identify sample names and iterate over all sample columns
    header = [line for line in lines if line.startswith("#CHROM")][0].strip().split("\t")
    sample_names = header[9:]  # Sample names start from the 10th column
    print(f"Samples found: {sample_names}")

    # Regular expression to find amino acid mutation information (e.g., "p.Arg123Ser")
    mutation_pattern = re.compile(r"p\.[A-Za-z][a-z]{2}[0-9]+[A-Za-z][a-z]{2}")

    # Iterate over each sample
    for sample_name in sample_names:
        # Create a folder for each sample
        sample_dir = os.path.join(output_dir, f"{sample_name}_result")
        os.makedirs(sample_dir, exist_ok=True)
        print(f"Created sample directory: {sample_dir}")

        # Iterate over each line in the VCF file (skip the header)
        for line in lines:
            if line.startswith("#"):
                continue
            columns = line.strip().split("\t")
            vcf_chrom, vcf_pos, _, _, _, _, _, info, _, *sample_data = columns[:10 + len(sample_names)]

            # Create a matching key to query the gene information dictionary
            key = f"{vcf_chrom}_{vcf_pos}"
            if key in gene_info:
                gene_details = gene_info[key]
                gene_name = gene_details["gene_name"]
                drug_resistance = gene_details["drug_resistance"]

                # Get mutation data for the current sample
                sample_mutation = sample_data[sample_names.index(sample_name)]

                # If the sample has a mutation (based on amino acid mutation in INFO field)
                mutation_match = mutation_pattern.search(info)
                if mutation_match and sample_mutation != ".":
                    mutation = mutation_match.group(0)
                    print(f"Found mutation {mutation} at CHROM {vcf_chrom}, POS {vcf_pos} for sample {sample_name}")

                    # Create a folder for the gene and record mutation information
                    gene_folder = os.path.join(sample_dir, gene_name)
                    os.makedirs(gene_folder, exist_ok=True)
                    mutation_file = os.path.join(gene_folder, f"{gene_name}_mutations.csv")

                    # If the file is created for the first time, write the header
                    if not os.path.isfile(mutation_file):
                        with open(mutation_file, "w", newline='') as mut_csv:
                            writer = csv.writer(mut_csv)
                            writer.writerow(["CHROM", "POS", "Gene Name", "Drug Resistance", "Mutation"])
                        print(f"Initialized mutation file for {gene_name}: {mutation_file}")

                    # Write mutation details
                    with open(mutation_file, "a", newline='') as mut_csv:
                        writer = csv.writer(mut_csv)
                        writer.writerow([vcf_chrom, vcf_pos, gene_name, drug_resistance, mutation])
                        print(f"Recorded mutation in {mutation_file}: {vcf_chrom},{vcf_pos},{gene_name},{drug_resistance},{mutation}")

    print("Processing complete! Results saved in the result directory.")

# Run main program
if __name__ == "__main__":
    main()
