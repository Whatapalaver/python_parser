import argparse
import sys
import json
import csv
from helpers.extract import extract_objects


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
        "-o", "--output", help="File path and name for output", default="dumps/output.csv")

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


def main(argv):
    args = parse_args(argv)
    print('Args: ', args)

    objects = extract_objects(args)
    # print("first object: ", objects[0])
    csv_header = header(objects[0])

    with open(args.output, "w", newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(csv_header)  # write the header
        # write the actual content line by line
        for object_dump in objects:
            object = object_dump
            line = csv_data(object)
            writer.writerow(line)

    return 0


# Run the main() script method
if __name__ == "__main__":
    sys.exit(main(sys.argv))
