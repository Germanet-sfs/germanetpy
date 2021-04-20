from pathlib import Path
import sys
import logging
import pytest
from germanetpy.germanet import Germanet
import numpy as np
from lxml import etree as ET
from germanetpy.icbased_similarity import ICBasedSimilarity
from germanetpy.synset import WordCategory

logger = logging.getLogger('logging_test_semrel')
d = "/Users/bcmpbell/Documents/GN_V160_XML"
frequency_list_nouns = "/Users/bcmpbell/Documents/GN_V160-FreqLists/noun_freqs_decow14_16.txt"
frequency_list_verbs = "/Users/bcmpbell/Documents/GN_V160-FreqLists/verb_freqs_decow14_16.txt"
frequency_list_adj = "/Users/bcmpbell/Documents/GN_V160-FreqLists/adj_freqs_decow14_16.txt"

try:
    germanet_data = Germanet(d)
    relatedness_nouns = ICBasedSimilarity(germanet=germanet_data, wordcategory=WordCategory.nomen,
                                          path=frequency_list_nouns)
    relatedness_verbs = ICBasedSimilarity(germanet=germanet_data, wordcategory=WordCategory.verben,
                                          path=frequency_list_verbs)
    relatedness_adj = ICBasedSimilarity(germanet=germanet_data, wordcategory=WordCategory.adj, path=frequency_list_adj)
except ET.ParseError:
    message = ("Unable to load GermaNet data at {0} . Aborting...").format(d)
    logger.error(message,
                 ET.ParseError)
    sys.exit(0)
except IOError:
    message = ("GermaNet data or not found at {0} or frequency lists not found at {0}. Aborting...").format(d)
    logger.error(message, IOError)
    sys.exit(0)

synset1 = germanet_data.get_synset_by_id('s46683')
synset2 = germanet_data.get_synset_by_id('s46650')
dist = relatedness_nouns.resnik(synset1, synset2)
out = str(dist)
print (out)