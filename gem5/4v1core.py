import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate

def convert_str_to_num(s):
    """Convert string to either float or int"""
    try:
        return int(s)
    except ValueError:
        return float(s)

def get_metrics(lines):
    metrics = {}
    for line in lines:
        line_lowercase = line.lower()
        if "cache" not in line_lowercase:
            continue
        if "miss" in line.lower() or "hit" in line.lower():
            # the line is interesting to us. extract the first and second non-whitespace words
            words = line.split()
            metric = words[0]
            value = words[1]
            if metric not in metrics:
                metrics[metric] = convert_str_to_num(words[1])

    return metrics


def get_per_core_metrics(metric, metrics):
    # take metric, find it in metrics, and get the avg of all the results\
    metric_vals = []
    for m in metrics.keys():
        # get the last word in the key -- this is actually the metric we are looking for
        if m.split(".")[-1] == metric:
            metric_vals.append(metrics[m])

    return sum(metric_vals) / len(metric_vals)
        



def get_percent_diff(a, b):
    # return the percent difference between a and b
    # ensure that the first number is greater than the second
    if a < b:
        a, b = b, a
    try:
        percent_diff = (a - b) / a
        return percent_diff
    except ZeroDivisionError:
        return 0

all_compressors = [
    'BaseCacheCompressor', 'BaseDictionaryCompressor',
    'Base64Delta8', 'Base64Delta16', 'Base64Delta32',
    'Base32Delta8', 'Base32Delta16', 'Base16Delta8',
    'CPack', 'FPC', 'FPCD', 'FrequentValuesCompressor', 'MultiCompressor',
    'PerfectCompressor', 'RepeatedQwordsCompressor', 'ZeroCompressor']

stats = []

for compressor in all_compressors:
    f_core_file = f"./benchmarks/results/baseline/FFT/4/{compressor}/stats.txt"
    o_core_file = f"./benchmarks/results/baseline/FFT/2/{compressor}/stats.txt"
    with open(f_core_file, "r") as f:
        f_core_vals = f.readlines()
    with open(o_core_file, "r") as f:
        o_core_vals = f.readlines()

    f_core_metrics = get_metrics(f_core_vals)
    # print(f"F_core_metrics: {f_core_metrics}")
    o_core_metrics = get_metrics(o_core_vals)
    # print(f"o_core_metrics: {o_core_metrics}")

    # print(f_core_metrics)

    # print(f_core_file)
    # print(o_core_file)

    rows = []
    
    for metric in f_core_metrics:

        # TODO: avg out same stat for each core

        if metric not in o_core_metrics:
            # print("Metric not in benchmark")
            continue
        compressed_val = f_core_metrics[metric]
        no_compress_val = o_core_metrics[metric]
        percent_diff = get_percent_diff(compressed_val, no_compress_val)
        percent_diff = round(percent_diff * 100, 3)
        rows.append((metric, compressed_val, no_compress_val, percent_diff))
        # print("here")
        # if args.plot:
        #     # save a bar plot of compressed_val vs no_compress_val with the title as the metric
        #     plt.bar(["compressed", "no-compressed"], [compressed_val, no_compress_val])
        #     plt.title(metric)
        #     plt.show()

    # print(rows)

    stats.append(rows)

print(stats)
