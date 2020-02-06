import csv
import numpy as np
import numpy.random as random
import matplotlib.pyplot as plt
import pandas as pd
import argparse
import sys

not_used = ['uniqueID', 'museumNumber', 'imageResolution', 'aspects', 'images',
            'recordModificationDate', 'recordCreationDate', 'objectNumber', 'copyNumber']
plot_keys = ['object', 'materialsTechniques', 'productionNote', 'artistMakerOrganisation', 'artistMakerPerson',
             'dimensionsNote', 'creditLine', 'descriptiveLine', 'contentDescription', 'artistMakerPeople',
             'physicalDescription', 'summary', 'objectHistoryNote', 'historicalContextNote', 'title']


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
    parser.add_argument("-s", "--subplot_inset", help="Show full scale hist as inset",
                        action='store_true', default=False)

    parser.add_argument("-b", "--bin_size", type=int,
                        help="specify bucket width for bins", default=10)
    parser.add_argument("-m", "--max_size", type=int,
                        help="limit max y-axis, best for single field histogram", default=None)

    return parser.parse_args(args[1:])


def generate_histogram(data, field_name, bin_size, max_size):
    data_to_plot = data[field_name]
    bins = compute_histogram_bins(data_to_plot, bin_size, max_size)
    # bins = quantile_bins(data_to_plot)
    print(bins)

    legend = [field_name]
    plt.hist(data_to_plot[data_to_plot != 0], color=[
        'orange'], bins=bins, alpha=0.5, histtype='stepfilled')
    plt.xlabel("Field Length")
    plt.ylabel("Frequency")
    plt.legend(legend)
    plt.title(
        f"Length Distribution field '{field_name}' across Object API", fontsize="x-large")


def generate_subplot(data, field_name, bin_size, max_size):
    data_to_plot = data[field_name]
    bins_max = compute_histogram_bins(data_to_plot, bin_size, max_size)
    bins_full = compute_histogram_bins(data_to_plot, bin_size, max_size=None)

    # Show inset charts
    fig, axes1 = plt.subplots()
    st = fig.suptitle(
        f"Length Distribution field '{field_name}' across Object API", fontsize="x-large")

    # These are in unitless percentages of the figure size. (0,0 is bottom left)
    left, bottom, width, height = [0.55, 0.5, 0.3, 0.3]
    axes1.hist(data_to_plot[data_to_plot != 0], color=[
        'orange'], bins=bins_max, alpha=0.5, histtype='stepfilled')
    axes2 = plt.axes([left, bottom, width, height])
    axes2.hist(data_to_plot[data_to_plot != 0], color=[
        'green'], bins=bins_full, alpha=0.5, histtype='stepfilled')

    # Add labels
    axes1.set(xlabel="Field Length", ylabel="Frequency")
    axes2.set_title("Full Distribution", fontsize=9)
    axes1.legend([field_name], loc="lower right")


def main(argv):
    args = parse_args(argv)
    print('Args: ', args)
    data = pd.read_csv(args.input)
    # print(type(data))
    # print(data.astype(bool).sum(axis=0))
    print('nonzero', np.count_nonzero(data, axis=0))
    if args.field_name and args.subplot_inset:
        print('Creating subplots for ', args.field_name)
        generate_subplot(data, args.field_name, args.bin_size, args.max_size)
        plt.show()
    elif args.field_name:
        print('Creating histogram for ', args.field_name)
        generate_histogram(data, args.field_name, args.bin_size, args.max_size)
        plt.show()
    else:
        print('Creating multiple histograms')
        for key in plot_keys:
            generate_histogram(data, key, args.bin_size, args.max_size)
            plt.show()


# Run the main() script method
if __name__ == "__main__":
    sys.exit(main(sys.argv))
