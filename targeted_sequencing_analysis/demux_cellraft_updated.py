import gzip
import pandas as pd
import os
import glob
from Bio import SeqIO

my_barcode_assignments = {'ACAAGT': '130',
                       'AAGCAA': '131',
                       'TCCTGT': '145',
                       'TGGTCC': '133',
                       'ATGACC': '142',
                       'CAGCTT': '143',
                       'GGATAC': '144',
                       'GGCTTG': '132',
                       'other': 'other'}

my_barcodes = ['ACAAGT', 'AAGCAA', 'TCCTGT', 'TGGTCC',
            'ATGACC', 'CAGCTT', 'GGATAC', 'GGCTTG', 'other']

my_barcode_counts = {'other':0, 'ACAAGT':0, 'AAGCAA':0, 'GGCTTG':0, 'TGGTCC':0,
                   'ATGACC':0, 'CAGCTT':0, 'GGATAC':0, 'TCCTGT':0}


def get_sample_id(sample):
    """
    gets name of sample from full path to fastq. Splitting on underscore
    :param sample: full path to sample to analyze
    :return: name split on underscore
    """
    name = os.path.basename(sample).split("_")[0]
    return name


def hamming_distance(s1, s2):
    """
    calculate hamming distance between two strings (must be same length)
    :param s1: first string
    :param s2: second string
    :return: number of mismatches between strings (if not same length, returns 100)
    """
    if len(s1) != len(s2):
        return 100
    else:
        return sum(ch1 != ch2 for ch1, ch2 in zip(s1, s2))


def find_index_match(index, barcodes):
    """

    :param index: 6bp index to match (allowing hamming distance of 1)
    :param barcodes: list of barcodes to look for
    :return: barcode that matches (allowing up to 1 mismatch)
    """
    for barcode in barcodes:
        if hamming_distance(index, barcode) < 2:
            return barcode


def trim_read_from_barcode(read, barcodes):
    """
    matches the first 6bp to a barcode and trims the read. If no barcode is found, returns the whole read.
    :param read: sequencing read starting with index as first 6 bp
    :param barcodes: list of barcodes
    :return: barcode assignment, sequencing read with barcode trimmed
    """
    index = read[:6]
    assigned = find_index_match(index, barcodes)
    if assigned is None:
        assigned = 'other'
    else:
        read = read[6:]

    return assigned, read


def demux_fastq(fastq, output_dir, barcodes=my_barcodes, barcode_assignments=my_barcode_assignments):

    barcode_counter = {'other':0, 'ACAAGT':0, 'AAGCAA':0, 'GGCTTG':0, 'TGGTCC':0,
                   'ATGACC':0, 'CAGCTT':0, 'GGATAC':0, 'TCCTGT':0}

    """

    :param fastq:
    :param barcodes:
    :param barcode_counter:
    :param output_dir:
    :return:
    """
    sample_name = get_sample_id(fastq)
    write_files = {}

    for barcode in barcodes:
        file = output_dir+sample_name+"_"+barcode_assignments[barcode]+".fastq"
        write_files[barcode_assignments[barcode]] = open(file, 'w')

    handle = gzip.open(fastq, 'rt')
    for record in SeqIO.parse(handle, "fastq"):
        name = record.name
        seq = record.seq
        read_length = len(seq)
        quality = record.format("fastq")[-read_length-1:].rstrip("\n")
        plus = '+'
        
        index, short_read = trim_read_from_barcode(seq, barcodes)
        barcode_counter[index] += 1
        
        if index != 'other':
            quality = quality[6:]
            
        entry = '@'+name+"\n"+str(short_read)+"\n"+plus+"\n"+quality+"\n"
        
        write_files[barcode_assignments[index]].write(entry)
        
    
    for barcode in barcodes:
        write_files[barcode_assignments[barcode]].close()

    return barcode_counter

def format_and_save_barcode_counter(barcode_counts, output_dir, fastq):
    """

    :param barcode_counter: result of demux_fastq
    :param output_dir: save directory
    :param fastq: fastq file to demux (gzipped)
    :return:saves barcode metrics file in output directory
    """
    sample_name = get_sample_id(fastq)
    df = pd.DataFrame.from_dict(barcode_counts, orient='index')
    df.rename(columns={0: "count"}, inplace=True)
    df.to_csv(output_dir+sample_name+"_barcode_metrics.csv")


def summarize_metrics(output_dir, barcode_assignments=my_barcode_assignments):
    """
    combines all metrics file into one dataframe
    :param output_dir: directory where metrics files are being saved
    :param barcode_assignments: name with barcode string
    :return: saves new dataframe
    """

    files = glob.glob(output_dir+"*_metrics.csv")
    dfs = []

    for sample in files:
        name = os.path.basename(sample).split("_")[0]
        df = pd.read_csv(sample, index_col=0)
        df.rename(columns = {"count": name}, inplace=True)
        dfs.append(df)

    result = pd.concat(dfs, axis=1)
    result.reset_index(inplace=True)
    result['barcode_name'] = result['index'].map(barcode_assignments)
    result.set_index('index', inplace=True)
    result.to_csv(output_dir+"all_metrics_summary.csv")


def master(fastq_files, output_dir, barcodes=my_barcodes):
    for fastq in fastq_files:
        counter_new = demux_fastq(fastq, output_dir, barcodes)
        format_and_save_barcode_counter(counter_new, output_dir, fastq)
    summarize_metrics(output_dir)