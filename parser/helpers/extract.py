import json
import ndjson


def objects(args):
    if args.json_input:
        return objects_from_file(args.json_input)
    elif args.full:
        return all_api_objects()
    else:
        return modified_api_objects()


def all_api_objects():
    pass


def modified_api_objects():
    pass


def objects_from_file(path):
    with open(path, "r") as f:
        objects_load = ndjson.load(f)
        return objects_load

# Nested field extraction methods


def title(object):
    if not object['title'] or not object['title'][0]:
        return ''
    else:
        return object['title'][0]['title']


def people(object):
    if not object['artistMakerPeople'] or not object['artistMakerPeople'][0]:
        return ''
    else:
        return object['artistMakerPeople'][0]['name']['text']


def person(object):
    if not object['artistMakerPerson'] or not object['artistMakerPerson'][0]:
        return ''
    else:
        return object['artistMakerPerson'][0]['name']['text']


def organisation(object):
    if not object['artistMakerOrganisation'] or not object['artistMakerOrganisation'][0]:
        return ''
    else:
        return object['artistMakerOrganisation'][0]['name']['text']
