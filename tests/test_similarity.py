from pathlib import Path
import sys
import logging
from lxml import etree as ET
import pytest
from germanet import Germanet
from pathbased_similarity import PathBasedSimilarity
import numpy as np

logger = logging.getLogger('logging_test_similarity')
d = str(Path(__file__).parent.parent) + "/data"
try:
    germanet_data = Germanet(d)
    sim = PathBasedSimilarity(germanet_data)
except ET.ParseError:
    message = ("Unable to load GermaNet data at {0} . Aborting...").format(d)
    logger.error(message,
                 ET.ParseError)
    sys.exit(0)
except IOError:
    message = ("GermaNet data not found at {0} . Aborting...").format(d)
    logger.error(message, IOError)
    sys.exit(0)

path_similarity_nouns = [
    ('s74611', 's39544', 0.74),
    ('s39183', 's39544', 0.86),
    ('s39183', 's39197', 0.97),

]

wup_similarity_nouns = [
    ('s74611', 's39544', 0.0),
    ('s39183', 's39544', 0.62),
    ('s39183', 's39197', 0.92),
]

lch_similarity_nouns = [
    ('s74611', 's39544', 1.41),
    ('s39183', 's39544', 1.92),
    ('s39183', 's39197', 3.02),
]

@pytest.mark.parametrize('id,other_id,similarity', path_similarity_nouns)
def test_path_similarity(id, other_id, similarity):
    synset = germanet_data.get_synset_by_id(id)
    other = germanet_data.get_synset_by_id(other_id)
    path_sim = np.round(sim.path(synset, other), decimals=2)
    np.testing.assert_almost_equal(path_sim, similarity)

@pytest.mark.parametrize('id,other_id,similarity', wup_similarity_nouns)
def test_wup_similarity(id, other_id, similarity):
    synset = germanet_data.get_synset_by_id(id)
    other = germanet_data.get_synset_by_id(other_id)
    wup_sim = np.round(sim.wup(synset, other), decimals=2)
    np.testing.assert_almost_equal(wup_sim, similarity)

@pytest.mark.parametrize('id,other_id,similarity', lch_similarity_nouns)
def test_lch_similarity(id, other_id, similarity):
    synset = germanet_data.get_synset_by_id(id)
    other = germanet_data.get_synset_by_id(other_id)
    lch_sim = np.round(sim.lch(synset, other), decimals=2)
    np.testing.assert_almost_equal(lch_sim, similarity)