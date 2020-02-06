import argparse
import sys
import os
import json
import csv
from helpers.extract import extract_objects, extract_objects_from_file


flat_keys = ['object', 'uniqueID', 'museumNumber', 'imageResolution', 'materialsTechniques', 'productionNote', 'copyNumber',
             'dimensionsNote', 'creditLine', 'descriptiveLine', 'contentDescription', 'recordModificationDate',
             'recordCreationDate', 'physicalDescription', 'summary', 'objectHistoryNote', 'historicalContextNote']
array_keys = ['objectNumber', 'aspects', 'images']
object_keys = ['productionType', 'collectionCode']
unknowns = ['contentOther', 'contentPlace', 'contentConcept', 'contentLiteraryRefs', 'contentPeople', 'contentEvent',
            'labelsAndDate', 'contentOrganisation', 'style', 'associatedPlace', 'associatedPerson', 'associatedEvent', 'associatedOrganisation', 'associatedPeople']
nested_keys = ['dimensions', 'artistMakerPeople', 'galleryLocation', 'placeOfOrigin', 'categories', 'date', 'marksAndInscriptions',
               'artistMakerOrganisation', 'title', 'techniques', 'contentPerson', 'artistMakerPerson', 'materials', 'bibliographicReferences']


def parse_args(args):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-o", "--output", help="File path and name for output", default="dumps/")
    parser.add_argument("-m", "--multifile_output",
                        help="Multiple output files", action='store_true', default=False)

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("-a", "--api", help="Use SSL API",
                       action='store_true', default=False)
    group.add_argument("-j", "--json_input", help="JSON file to import")

    return parser.parse_args(args[1:])


def flat_key_lengths(object_data):
    # print([key for key in object_data.keys() if key in flat_keys])
    return [len(object_data[key]) for key in object_data.keys() if key in flat_keys]


def flat_key_headers(object_data):
    return [key for key in object_data.keys() if key in flat_keys]


def object_key_lengths(object_data):
    # print([key for key in object_data.keys() if key in flat_keys])
    return [len(object_data[key]['text']) for key in object_data.keys() if key in object_keys]


def array_key_headers(object_data):
    return [key + ": item_count" for key in object_data.keys() if key in array_keys]


def array_key_lengths(object_data):
    # print([key for key in object_data.keys() if key in flat_keys])
    return [len(object_data[key]) for key in object_data.keys() if key in array_keys]


def object_key_headers(object_data):
    return [key for key in object_data.keys() if key in object_keys]


def header(object_data):
    header = flat_key_headers(object_data) + array_key_headers(object_data) + \
        object_key_headers(object_data)
    header.insert(0, 'UniqueID')
    return header


def object_counts(object_data):
    return flat_key_lengths(object_data) + array_key_lengths(object_data) + \
        object_key_lengths(object_data)


def csv_data(object_data):

    list = object_counts(object_data)
    list.insert(0, object_data['uniqueID'])
    return list


def output_filename(file):
    without_ext = file.split('.')[:-1]
    s = '-'
    return 'output' + s + s.join(without_ext)


def main(argv):
    args = parse_args(argv)
    print('Args: ', args)

    if args.json_input:
        if args.multifile_output:
            # output multiple files
            for dirpath, dirnames, files in os.walk(args.json_input, topdown=False):
                print(f'Found directory: {dirpath}')
                for input_file_name in files:
                    print('Filename: ', input_file_name)
                    objects = extract_objects_from_file(
                        dirpath+input_file_name)
                    # print("first object: ", objects[0])
                    csv_header = header(objects[0])
                    output_file = args.output + \
                        output_filename(input_file_name) + '.csv'

                    with open(output_file, "w", newline='') as f:
                        writer = csv.writer(f, delimiter=',')
                        writer.writerow(csv_header)  # write the header
                        # write the actual content line by line
                        for object_dump in objects:
                            line = csv_data(object_dump)
                            writer.writerow(line)
        else:
            # output single file
            output_file = args.output + 'output.csv'
            # Headers need amending if I amend what gets processed
            csv_header = ['UniqueID', 'descriptiveLine', 'copyNumber', 'creditLine', 'historicalContextNote',
                          'objectHistoryNote', 'object', 'summary', 'productionNote', 'recordCreationDate', 'uniqueID',
                          'physicalDescription', 'materialsTechniques', 'dimensionsNote', 'imageResolution', 'contentDescription',
                          'recordModificationDate', 'museumNumber', 'aspects: item_count', 'images: item_count',
                          'objectNumber: item_count', 'collectionCode', 'productionType']
            with open(output_file, "w", newline='') as f:
                writer = csv.writer(f, delimiter=',')
                writer.writerow(csv_header)  # write the header
                for dirpath, dirnames, files in os.walk(args.json_input, topdown=False):
                    for input_file_name in files:
                        print('Processing filename: ', input_file_name)
                        objects = extract_objects_from_file(
                            dirpath+input_file_name)
                        # write the actual content line by line
                        for object_dump in objects:
                            line = csv_data(object_dump)
                            writer.writerow(line)

    return 0


# Run the main() script method
if __name__ == "__main__":
    sys.exit(main(sys.argv))
