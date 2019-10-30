from collections import Counter
import numpy as np
import os
import pandas as pd
import statistics
from Bio import SeqIO


after_guide = 'gttttagagctaGAAAtagcaagtt'.upper()
before_guide = 'TTCTTGTGGAAAGGACGAAACACCG'


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


def count_guides(sample_fastq, front_seq=before_guide, back_seq=after_guide):
    """

    :param sample_fastq: demuxed fastq file to count guides
    :param front_seq: sequence before guide
    :param back_seq: sequence after guide
    :return: Counter of everything detected in between
    """

    gRNA_counts = Counter()
    read_count = 0
    good_read_count = 0
      
    handle = open(sample_fastq, 'rt')
    for record in SeqIO.parse(handle, "fastq"):
        seq = record.seq
        
        read_count += 1
        
        start_position = seq.find(front_seq)+len(front_seq)                
        end_position = seq.find(back_seq)

        if (start_position != (-1+len(front_seq))) & (end_position != -1):

            gRNA = str(seq[start_position: end_position])
            gRNA_counts[gRNA] += 1
            good_read_count += 1

        else:

            gRNA_counts['None'] += 1

    return gRNA_counts, read_count, good_read_count


def assign_guides(gRNA_counts):

    cutoff = statistics.mean(gRNA_counts.values())*5

    to_keep = dict()

    for item in gRNA_counts.keys():
        count = gRNA_counts[item]
        if count > cutoff:
            to_keep[item] = count

    return to_keep


def make_summary_df(read_count, good_read_count, to_keep, demuxed_fastq):
    rows = []
    name = os.path.basename(demuxed_fastq).split("_")[0]
    index = os.path.basename(demuxed_fastq).split("_")[1].rstrip(".fastq")
    row_1 = [name, index, 'total_reads', read_count]
    row_2 = [name, index, 'reads_with_guide', good_read_count]
    rows.append(row_1)
    rows.append(row_2)

    if len(to_keep) > 0:
        for item in to_keep.keys():
            row = [name, index, item, to_keep[item]]
            rows.append(row)

    df = pd.DataFrame(rows)

    return df


def process_all_samples(sample_manifest, demux_dir, front_seq=before_guide, back_seq=after_guide):
    """
    Processes all libraries to call gRNAs
    :param sample_manifest:
    :param demux_dir:
    :param front_seq:
    :param back_seq:
    :return:
    """

    manifest_df = pd.read_csv(sample_manifest, sep="\t")

    dfs = []

    for library in manifest_df.iterrows():
        lib = library[1]['Sample']
        indices = library[1]['Index'].split(",")
        for index in indices:
            fastq = demux_dir+"{}_{}.fastq".format(lib, index)
            gRNA_counts, read_count, reads_with_guide = count_guides(fastq, front_seq=front_seq, back_seq=back_seq)
            to_keep = assign_guides(gRNA_counts)
            df = make_summary_df(read_count, reads_with_guide, to_keep, fastq)
            dfs.append(df)

    summary = pd.concat(dfs)
    summary.columns = ['library', 'index', 'type', 'read_count']

    return summary
