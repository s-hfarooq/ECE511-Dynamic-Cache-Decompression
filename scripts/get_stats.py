import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate
import argparse


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


def over_threshold(percent, threshold):
    # return True if the percent difference between a and b is greater than the threshold
    # ensure that the first number is greater than the second
    return abs(percent) > threshold


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="get_stats.py",
        description='Compare cache statistics between compressed and uncompressed CPU traces. \
            The script expects two files as input: the first file is the compressed trace, and \
            the second file is the uncompressed trace. The script will output a table of cache \
            statistics of "interesting" metrics (those that are over a certain threshold, which \
                defaults to 5%).',
    )
    parser.add_argument("-c", "--compressed", type=str, help="path to compressed stats.txt")
    parser.add_argument("-n", "--no-compressed", type=str, help="path to no-compression stats.txt")
    parser.add_argument(
        "-t",
        "--threshold",
        type=float,
        default=0.05,
        help="threshold for percent difference",
    )
    parser.add_argument(
        "-s",
        "--sort",
        type=str,
        default="percent",
        choices=["percent", "metric"],
        help="sort by percent or metric",
    )
    parser.add_argument("-f", "--file", type=str, default="results.csv",help="path to output file")
    parser.add_argument("-p", "--plot", action="store_true", help="plot the results")
    args = parser.parse_args()

    with open(args.compressed, "r") as f:
        compressed = f.readlines()
    with open(args.no_compressed, "r") as f:
        no_compressed = f.readlines()

    compressed_metrics = get_metrics(compressed)
    no_compressed_metrics = get_metrics(no_compressed)

    # list of tuples (metric, compressed value, no-compressed value, percent difference)
    rows = []

    print("PRINTING COMPRESSED VS NON_COMPRESSED")
    print("======================================")

    for metric in compressed_metrics:
        if metric not in no_compressed_metrics:
            continue
        compressed_val = compressed_metrics[metric]
        no_compress_val = no_compressed_metrics[metric]
        percent_diff = get_percent_diff(compressed_val, no_compress_val)
        if over_threshold(percent_diff, args.threshold):
            percent_diff = round(percent_diff * 100, 3)
            rows.append((metric, compressed_val, no_compress_val, percent_diff))
            if args.plot:
                # save a bar plot of comperssed_val vs no_compress_val with the title as the metric
                plt.bar(["compressed", "no-compressed"], [compressed_val, no_compress_val])
                plt.title(metric)
                plt.show()
                

    if args.sort.lower() == "percent":
        # x[3] = percent difference
        rows.sort(key=lambda x: x[3], reverse=True)
    elif args.sort.lower() == "metric":
        # x[0] = metric
        rows.sort(key=lambda x: x[0])

    col_names = ["metric", "compressed", "no-compressed", "percent difference"]
    df = pd.DataFrame(rows, columns=col_names)

    print(tabulate(df, headers="keys", tablefmt="psql"))
    # save to args.file
    df.to_csv(args.file, index=False)

    # save all as a bar chart 
    

