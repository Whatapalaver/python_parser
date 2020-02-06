import csv
import numpy as np
import numpy.random as random
import matplotlib.pyplot as plt
import pandas as pd

not_used = ['uniqueID', 'museumNumber', 'imageResolution',
            'recordModificationDate', 'recordCreationDate', 'objectNumber', 'copyNumber']
plot_keys = ['object', 'materialsTechniques', 'productionNote',
             'dimensionsNote', 'creditLine', 'descriptiveLine', 'contentDescription',
             'physicalDescription', 'summary', 'objectHistoryNote', 'historicalContextNote', 'aspects', 'images']
# x = np.random.random_integers(1, 100, 5)
# print(x)
# plt.hist(x, bins=20)
# plt.ylabel('No of times')
# plt.show()


def compute_histogram_bins(data, desired_bin_size):
    min_val = np.min(data)
    max_val = np.max(data)
    min_boundary = -1.0 * (min_val % desired_bin_size - min_val)
    max_boundary = max_val - max_val % desired_bin_size + desired_bin_size
    n_bins = int((max_boundary - min_boundary) / desired_bin_size) + 1
    bins = np.linspace(min_boundary, max_boundary, n_bins)
    return bins


if __name__ == '__main__':
    data = pd.read_csv('dumps/output.csv')
    # print(type(data))
    for key in plot_keys:
        data_to_plot = data[key]
        bins = compute_histogram_bins(data_to_plot, 10.0)
        print(bins)

        legend = [key]
        # summary = data['summary']
        plt.hist(data_to_plot[data_to_plot != 0], color=['orange'], bins=bins)
        plt.xlabel("Field Length")
        plt.ylabel("Frequency")
        plt.legend(legend)
        # plt.xticks(range(0, 5))
        # plt.yticks(range(1, 200))
        plt.title('Field Length Distribution across Object API')
        plt.show()
