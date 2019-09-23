from lxml import etree as ET


def convert_to_boolean(attribute):
    if attribute == 'no':
        return False
    if attribute == 'yes':
        return True
    else:
        return "cannot be converted to boolean"


def parse_xml(datadir, f):
    d = '/'.join([datadir, f])
    try:
        tree = ET.parse(d)
    except ET.ParseError:
        print("Unable to load GermaNet data at {0} . Aborting...".format(d))
    else:
        return tree
