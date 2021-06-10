import logging
import sys
from germanetpy.germanet import Germanet
from lxml import etree as ET
import numpy as np
from pathlib import Path

logger = logging.getLogger('logging_test_germanet')
d = "/Users/bcmpbell/Documents/GN_V160_XML"
try:
    germanet_data = Germanet(d)
except ET.ParseError:
    message = ("Unable to load GermaNet data at {0} . Aborting...").format(d)
    logger.error(message,
                 ET.ParseError)
    sys.exit(0)
except IOError:
    message = ("GermaNet data not found at {0} . Aborting...").format(d)
    logger.error(message, IOError)
    sys.exit(0)


def test_number_of_instances():
    """Test whether the total numbers of synsets, lexunits, compounds, ili records, wictionary entries corresponds to
    the numbers for the current release"""
    number_synsets = len(germanet_data.synsets)
    number_lexunits = len(germanet_data.lexunits)
    number_compounds = len(germanet_data.compounds)
    number_ili_records = len(germanet_data.ili_records)
    number_wiktionary = len(germanet_data.wiktionary_entries)
    np.testing.assert_equal(number_synsets, 151843)
    np.testing.assert_equal(number_lexunits, 195000)
    np.testing.assert_equal(number_compounds, 109544)
    np.testing.assert_equal(number_ili_records, 28564)
    np.testing.assert_equal(number_wiktionary, 29547)