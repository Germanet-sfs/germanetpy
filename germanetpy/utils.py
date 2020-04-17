import sys
from lxml import etree as ET


def convert_to_boolean(attribute: str) -> bool:
    """
    Converts the given String into a boolean.
    :param attribute: The attribute that needs to be converted into a boolean
    :return: True, False or an Error message if the attribute doesn't have the right value
    """
    assert attribute == "yes" or attribute == "no", "cannot be converted to boolean"
    if attribute == 'no':
        return False
    if attribute == 'yes':
        return True


def parse_xml(datadir: str, f: str) -> ET:
    """
    Parses an XML file and returns the XML tree
    :param datadir: The directory where the file is located
    :param f: the filename
    :return: The parsed XML tree
    """
    d = '/'.join([datadir, f])
    try:
        tree = ET.parse(d)
    except ET.ParseError:
        print("Unable to load GermaNet data at {0} . Aborting...".format(d))
        sys.exit(0)
    else:
        return tree
