import json
import ndjson


def extract_objects(args):
    if args.json_input:
        return extract_objects_from_file(args.json_input)
    elif args.full:
        return extract_all_api_objects()
    else:
        return extract_modified_api_objects()


def extract_all_api_objects():
    pass


def extract_modified_api_objects():
    pass


def extract_objects_from_file(path):
    with open(path, "r") as f:
        objects_load = ndjson.load(f)
        return objects_load
