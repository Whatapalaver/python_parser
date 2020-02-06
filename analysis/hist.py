import csv
import numpy as np
import numpy.random as random
import matplotlib.pyplot as plt
import pandas as pd
import argparse
import sys

not_used = ['uniqueID', 'museumNumber', 'imageResolution', 'aspects', 'images',
            'recordModificationDate', 'recordCreationDate', 'objectNumber', 'copyNumber']
plot_keys = ['object', 'materialsTechniques', 'productionNote',
             'dimensionsNote', 'creditLine', 'descriptiveLine', 'contentDescription',
             'physicalDescription', 'summary', 'objectHistoryNote', 'historicalContextNote', ]


def compute_histogram_bins(data, desired_bin_size, max_size):
    min_val = np.min(data)
    max_val = max_size or np.max(data)
    min_boundary = -1.0 * (min_val % desired_bin_size - min_val)
    max_boundary = max_val - max_val % desired_bin_size + desired_bin_size
    n_bins = int((max_boundary - min_boundary) / desired_bin_size) + 1
    bins = np.linspace(min_boundary, max_boundary, n_bins)
    return bins


def quantile_bins(data):
    bins = data.quantile([0, .05, 0.1, 0.15, 0.20, 0.25, 0.3, 0.35, 0.40, 0.45,
                          0.5, 0.55, 0.6, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1]).to_list()
    return bins


def parse_args(args):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i", "--input", help="File path and name for input", default="dumps/output.csv")
    parser.add_argument("-f", "--field_name",
                        help="Specific field name for single histogram")

    parser.add_argument("-b", "--bin_size", type=int,
                        help="specify bucket width for bins", default=10)
    parser.add_argument("-m", "--max_size", type=int,
                        help="limit max y-axis, best for single field histogram", default=None)

    return parser.parse_args(args[1:])


def generate_histogram(data, key, bin_size, max_size):
    data_to_plot = data[key]
    bins = compute_histogram_bins(data_to_plot, bin_size, max_size)
    # bins = quantile_bins(data_to_plot)
    print(bins)

    legend = [key]
    plt.hist(data_to_plot[data_to_plot != 0], color=[
        'orange'], bins=bins, alpha=0.5, histtype='stepfilled')
    plt.xlabel("Field Length")
    plt.ylabel("Frequency")
    plt.legend(legend)
    # plt.xticks(range(0, 5))
    # plt.yticks(range(1, 200))
    plt.title('Field Length Distribution across Object API')
    plt.show()


def main(argv):
    args = parse_args(argv)
    print('Args: ', args)
    data = pd.read_csv(args.input)
    # print(type(data))
    if args.field_name:
        generate_histogram(data, args.field_name, args.bin_size, args.max_size)
    else:
        for key in plot_keys:
            generate_histogram(data, key, args.bin_size, args.max_size)


# Run the main() script method
if __name__ == "__main__":
    sys.exit(main(sys.argv))
