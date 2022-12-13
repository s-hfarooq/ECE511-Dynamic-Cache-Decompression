import argparse
import pandas as pd


BASE_DIR = "/home/timot/Classes/ece511/ECE511-Dynamic-Cache-Decompression/results/" # change to your dir



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


def get_file_lines(file):
    with open(file, "r") as f:
        lines = f.readlines()
    return lines

    

def get_same_metrics_singlecore(df):
    # metrics are in the order 
    # system.cpu.<metric we are interested in>
    # we want to get the metrics that are the same for all cores
    # so we can compare them
    # we will assume that the first core is the same as the rest
    

    # get the first core
    first_core = df.loc[df.index.str.startswith("system.cpu.") | df.index.str.startswith("system.l3.")]
    print(first_core)
    # get the metrics that are the same for all cores
    first_core.index = first_core.index.str.replace("system.cpu.", "")
    # l3
    first_core.index = first_core.index.str.replace("system.l3", "l3")
    
    return first_core

def get_same_metrics_multicore(df, num_cores, avg=False):
    # metrics are in the order 
    # system.cpu[num for cpu core].<metric we are interested in>
    # we want to get the metrics that are the same for all cores
    # so we can compare them
    # we will assume that the first core is the same as the rest
    

    cores = [f"system.cpu{i}." for i in range(num_cores)]
    core_metric_dfs = []
    # get the first core
    for core in cores:
        core_df = df.loc[df.index.str.startswith(core)]
        # get the metrics that are the same for all cores
        core_df.index = core_df.index.str.replace(core, "")
        core_metric_dfs.append(core_df)

    # append all the core metric dfs together
    # on append, add the metrics that are the same for all cores
    # to the same row
    
    metrics = {}
    for core_df in core_metric_dfs:
        for metric in core_df.index:
            if metric in metrics:
                metrics[metric] += (core_df.loc[metric])
            else:
                metrics[metric] = core_df.loc[metric]

    # convert the metrics to a dataframe
    if avg:
        for metric in metrics:
            metrics[metric] /= num_cores


    # get l3 metrics
    l3 = df.loc[df.index.str.startswith("system.l3.")]
    l3.index = l3.index.str.replace("system.l3", "l3")

    for metric in l3.index:
        if metric in metrics:
            metrics[metric] += (l3.loc[metric])
        else:
            metrics[metric] = l3.loc[metric]

    metrics_df = pd.DataFrame.from_dict(metrics, orient="index")
    return metrics_df
                


    

if __name__ == "__main__":
    

    parser = argparse.ArgumentParser(description="Compare CPU usage")

    # file1 = parser.add_argument("--file1", help="File 1", required=True)
    # file4 = parser.add_argument("--file4", help="File 4", required=True)

    file1 = BASE_DIR + "riscv/FFT/1/Base16Delta8/stats.txt"
    file4 = BASE_DIR + "riscv/FFT/4/Base16Delta8/stats.txt"

    file1_lines = get_file_lines(file1)
    file4_lines = get_file_lines(file4)

    file1_metrics = get_metrics(file1_lines)
    file4_metrics = get_metrics(file4_lines)


    file1_df = pd.DataFrame.from_dict(file1_metrics, orient="index")
    cpu1core = get_same_metrics_singlecore(file1_df)
    file4_df = pd.DataFrame.from_dict(file4_metrics, orient="index")
    cpu4core = get_same_metrics_multicore(file4_df, 4, avg=True)


    print(cpu1core)

    # print matching metrics
    # for metric in cpu1core.index:
    #     if metric in cpu4core.index:
    #         print(f"{metric}: {cpu1core.loc[metric].values[0]} vs {cpu4core.loc[metric].values[0]}")
    #         percent_diff = get_percent_diff(cpu1core.loc[metric].values[0], cpu4core.loc[metric].values[0])
    #         if over_threshold(percent_diff, 0.05):
    #             print(f"Percent difference: {percent_diff}")
    #             print("Over threshold")
    #         else:
    #             print("Under threshold")
    #         print()


    # get the data frame from file1 and file4


    

    