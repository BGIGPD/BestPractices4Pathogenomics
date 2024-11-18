# 一、Detection of resistance genes in mosquitoes
# Introduction

This course will guide you through detecting resistance genes in mosquitoes. With extensive insecticide use, mosquitoes are developing resistance to common treatments. By identifying and analyzing key resistance genes (such as P450, AChE, and VGSC), we can assess resistance levels in mosquito populations and improve control strategies. This course will introduce the detection workflow and relevant tools, helping you gain essential skills for resistance gene detection in mosquitoes.

**FastD** is a comprehensive platform to analyze insecticide resistance through two main mechanisms:
1. **FastD_TR** detects target-site mutations associated with insecticide resistance from RNA-Seq data.
   - Target genes include: `AChE, VGSC, RyR, nAChR`
![image](https://github.com/user-attachments/assets/78111f51-be80-4819-8fb9-024b56ab6443)

2. **FastD_MR** detects overexpressed detoxification genes associated with insecticide resistance.
   - Target genes include: `P450, GST, CCE`
![image](https://github.com/user-attachments/assets/beab84b7-1d17-4058-b134-f8b122888819)


![image](https://github.com/user-attachments/assets/e9687c42-ccc1-468a-badc-cc881e560b2a)

---

## Step 1: Open Your Server and Set Up Working Directory
```bash
# Make your working directory
mkdir IR_mos
cd IR_mos
```

---

## Step 2: Download FastD
1. [Download FastD](http://www.insect-genome.com/fastd/download/download_software.html). Click on "FastD linux".
![image](https://github.com/user-attachments/assets/6eb12088-7bcc-4845-a530-2751d082347c)

2. Transfer it to the `IR_mos` directory using WinSCP.

Alternatively, you can copy the file from my directory:
```bash
cp /home/liuji/IR/IR_mosq/FastD_v1.0_linux.tar.gz ./
cp /home/liuji/IR/IR_mosq/19BJYW1818.sam ./
tar -xzvf FastD_v1.0_linux.tar.gz
```

---

## Step 3: Set Up the Conda Environment

Activate Conda if it's not already activated:
```bash
source ~/miniconda3/bin/activate
```

### Install Required Software

1. **Create a Conda Environment:**
   ```bash
   conda config --show channels#if you have these three channels,you don't run conda config -add *
   conda config --add channels conda-forge
   conda config --add channels bioconda
   conda config --add channels defaults

   conda create -n mq -c conda-forge r-base#if you have these three channels,just start to run this command
   conda activate mq
   ```

2. **Install Required Packages:**
   ```bash
   conda install -c bioconda bowtie2
   conda install -c conda-forge r-ggplot2 r-ggseqlogo r-deseq2 #if it fails, we can install in R directly.
   ```

### Install R Packages (if needed)
```bash
R
# After entering the R console, run the following command
if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

#Here a number will pop up to select the mirror source, here we select 18
BiocManager::install("DESeq2")
install.packages("ggplot2")
install.packages("ggseqlogo")
```

### Quit and Save the R Environment
```bash
q()
# Save workspace image? [y/n/c]: y
```

---

## Step 4: Input and Output

### Input:
- The raw RNA-Seq reads are aligned to target gene sequences using Bowtie2, and the resulting `.sam` file is used as input.

### Output:
- `result_mutation_scaned*`: Includes mutation detection and frequency in target genes. Each file contains codons corresponding to each mutation site in the reads.

---

## Step 5: Run FastD_TR for Mutation Detection

Run the `FastD_TR.pl` script with the following command:

```bash
perl FastD_v1.0_linux/FastD_TR.pl -s Aedes_albopictus -r VGSC AChE -i 19BJYW1818.sam
```

---

## Step 6: Review Output Files

FastD generates results in the following folders:

1. **Mutation_detected_details**: Contains detailed mutation detection information, including mutation sites, types, and related genes for each sample.
   
2. **Mutation_table**: Summarizes resistance gene mutations in table format, providing an overview of detected mutations for statistical analysis.
   
3. **Mutation_visualization**: Provides visualizations of mutation distributions or proportions across samples.

*Note*: The software may not generate data in the `Mutation_visualization` folder, but the results in the first two folders are the most essential.

# 二、Detection of drug resistance genes in plasmodium

## Introduction

In this tutorial, I will show you how to use a Python script to compare the VCF file with an Excel file that contains mutation site information for malaria resistance genes. The goal is to extract the resistance-related genes present in the samples. This script helps identify resistance mutations and provides detailed information about the mutation sites, gene names, and amino acid changes.

---

## Prerequisites

To run this script, ensure the following prerequisites are in place:

- **Python environment**: Python 3.7 or higher is recommended.
- **Required Python libraries**:
  - `pandas`: for reading and processing Excel files
  - `openpyxl`: for reading `.xlsx` files

### Installing Required Libraries

You can install the necessary libraries using the following commands:

```bash
conda create -n malaria
conda activate malaria
pip install pandas openpyxl
```

---

## Setting Up Your Working Directory

1. Create and navigate to your working directory:

```bash
mkdir ~/IR_mala
cd ~/IR_mala
```

2. Copy the necessary files into your working directory:

```bash
cp /home/liuji/IR/IR_mala/fetch_IR.py ./
cp /home/liuji/IR/IR_mala/test1_pf.vcf.gz ./
cp /home/liuji/IR/IR_mala/snp_marker.xlsx ./
```

3. Unzip the VCF file:

```bash
gunzip test1_pf.vcf.gz
```

---

## Running the Script

Once the files are in place, run the Python script to compare the VCF file with the Excel mutation data. Use the following command:

```bash
python fetch_IR.py test1_pf.vcf snp_marker.xlsx result1
```

This command will execute the script with the `snp_marker.xlsx` file as input and output the results in a folder named `result`.

---

## Output Structure

The output will be structured in the following way:

```
result/
│
├── sample_1_result/              # Folder for each sample's results
│   ├── GeneA/                    # Folder for GeneA
│   │   └── GeneA_mutations.csv   # CSV file containing mutations of GeneA
│   ├── GeneB/                    # Folder for GeneB
│   │   └── GeneB_mutations.csv   # CSV file containing mutations of GeneB
│   └── ...
│
├── sample_2_result/              # Folder for another sample's results
│   ├── GeneA/                    # Folder for GeneA
│   │   └── GeneA_mutations.csv   # CSV file containing mutations of GeneA
│   ├── GeneB/                    # Folder for GeneB
│   │   └── GeneB_mutations.csv   # CSV file containing mutations of GeneB
│   └── ...
│
└── ...
```

In the output directory:

- Each sample's result will be stored in its own folder (e.g., `sample_1_result`).
- Inside each sample folder, there will be separate folders for each gene (e.g., `GeneA`).
- Each gene folder will contain a CSV file (e.g., `GeneA_mutations.csv`) with detailed mutation information.

---
## Exercise Section

### 1. **FastD Exercise**: Detect Overexpressed Genes

For this exercise, you will use the **FastD_MR.pl** tool to detect overexpressed genes related to insecticide resistance, such as **P450**, **GST**, and **CCE**. You will be working with a sam file named `19BJYW1818.sam`. The task is to identify mutations in resistance genes and analyze the overexpression data.

- **Data to Use**: `19BJYW1818.sam` 
- **Genes of Interest**: P450, GST, CCE

### 

Note that FASTD_MR is used differently from FastD_TR, and remember to return to foreword understanding
---

### 2. **Malaria Resistance Gene Detection**: Python Script Exercise

In this exercise, you will use the Python script `fetch_IR.py` to compare a VCF file (`test2_pf.vcf.gz`) with mutation site information stored in the `snp_marker.xlsx` file. The goal is to extract and analyze the resistance-related genes present in the sample.

- **Data to Use**: 
  - `test2_pf.vcf.gz` (VCF file with sample mutation data)
  - `snp_marker.xlsx` (Excel file containing mutation sites and gene information)
The script will output CSV files with mutation details for the relevant genes in the sample.
The result of FastD_MR lists the detoxifying enzyme genes which are selected to be the potential resistance causal genes.
---

These exercises will allow you to practice identifying resistance mutations in malaria samples using both the **FastD_MR.pl** tool and the **Python script**. The exercises will help you understand the mutation sites, gene names, and the amino acid changes related to resistance.

