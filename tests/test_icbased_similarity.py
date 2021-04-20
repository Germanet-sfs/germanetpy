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
frequency_list_nouns = str(Path(__file__).parent.parent) + "/data/noun_freqs_decow14_16.txt"
frequency_list_verbs = str(Path(__file__).parent.parent) + "/data/verb_freqs_decow14_16.txt"
frequency_list_adj = str(Path(__file__).parent.parent) + "/data/adj_freqs_decow14_16.txt"

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

raw_resnik_verbs = [
    ('s58565', 's58578', 1.351),
    ('s57835', 's57328', 1.53),
    ('s57534', 's57534', 7.512985163781748)
]

normalized_resnik_verbs = [
    ('s58565', 's58578', 10, 1.357),
    ('s57835', 's57328', 10, 1.536)
]

raw_resnik_nouns = [
    ('s45380', 's45380', 5.182048317402752),
    ('s46047', 's45380', 2.563204597354734),
    ('s46650', 's46683', 2.563204597354734),
    ('s46683', 's46650', 2.563204597354734),
    ('s49774', 's83979', 0.0),
    ('s83979', 's83979', 6.364967952571943)
]

normalized_resnik_nouns = [
    ('s46047', 's45380', 10, 2.602),
    ('s46047', 's46047', 10, 5.512),
    ('s46650', 's46683', 10, 2.602),
    ('s46683', 's46650', 10, 2.602),
    ('s49774', 's49774', 10, 10.0),
    ('s49774', 's83979', 10, 0.0),

]

raw_resnik_adj = [
    ('s94396', 's94411', 0.0),
    ('s94396', 's94396', 6.033336177306553)
]

normalized_resnik_adj = [
    ('s94396', 's94411', 10, 0.0),
    ('s94396', 's94396', 10, 6.47)
]
##lin

raw_lin_verbs = [
    ('s58565', 's58578', 0.342),
    ('s57835', 's57328', 0.405),
    ('s57534', 's57534', 1.0)
]

normalized_lin_verbs = [
    ('s58565', 's58578', 10, 3.424),
    ('s57835', 's57328', 10, 4.054)
]

raw_lin_nouns = [
    ('s45380', 's45380', 1.0),
    ('s46047', 's45380', 0.484),
    ('s46650', 's46683', 0.519),
    ('s46683', 's46650', 0.519),
    ('s49774', 's83979', 0.0),
    ('s83979', 's83979', 1.0)
]

normalized_lin_nouns = [
    ('s46047', 's45380', 10, 4.831),
    ('s46047', 's46047', 10, 10.0),
    ('s46650', 's46683', 10, 5.188),
    ('s46683', 's46650', 10, 5.188),
    ('s49774', 's49774', 10, 10.0),
    ('s49774', 's83979', 10, 0.0),

]

raw_lin_adj = [
    ('s94396', 's94411', 0.0),
    ('s94396', 's94396', 1.0)
]

normalized_lin_adj = [
    ('s94396', 's94411', 10, 0.0),
    ('s94396', 's94396', 10, 10.0)
]

## JCN

raw_jcn_verbs = [
    ('s58565', 's58578', 14.734),
    ('s57835', 's57328', 15.436),
    ('s57534', 's57534', 19.923)
]

normalized_jcn_verbs = [
    ('s58565', 's58578', 10, 7.395),
    ('s57835', 's57328', 10, 7.747)
]

raw_jcn_nouns = [
    ('s45380', 's45380', 19.703),
    ('s46047', 's45380', 14.218),
    ('s46650', 's46683', 14.948),
    ('s46683', 's46650', 14.948),
    ('s49774', 's83979', 3.487),
    ('s83979', 's83979', 19.703)
]

normalized_jcn_nouns = [
    ('s46047', 's45380', 10, 7.217),
    ('s46047', 's46047', 10, 10.0),
    ('s46650', 's46683', 10, 7.587),
    ('s46683', 's46650', 10, 7.587),
    ('s49774', 's49774', 10, 10.0),
    ('s49774', 's83979', 10, 1.77),

]

raw_jcn_adj = [
    ('s94396', 's94411', 6.784),
    ('s94396', 's94396', 18.649)
]

normalized_jcn_adj = [
    ('s94396', 's94411', 10, 3.638),
    ('s94396', 's94396', 10, 10.0)
]


def test_cumfreq():
    """Test whether the total frequency of the Graph corresponds to the number of the current release"""
    np.testing.assert_equal(relatedness_verbs.root_freq, 9159685155)
    np.testing.assert_equal(relatedness_nouns.root_freq, 7102095442)
    np.testing.assert_equal(relatedness_adj.root_freq, 2112150587)


# resnik measure #

@pytest.mark.parametrize('id1,id2,similarity', raw_resnik_verbs)
def test_raw_resnik_verbs(id1, id2, similarity):
    """Tests unnormalized resnik scores for verbs."""
    synset1 = germanet_data.get_synset_by_id(id1)
    synset2 = germanet_data.get_synset_by_id(id2)
    dist = relatedness_verbs.resnik(synset1, synset2)
    np.testing.assert_array_almost_equal(dist, similarity, decimal=2)


@pytest.mark.parametrize('id1,id2,max,similarity', normalized_resnik_verbs)
def test_normalized_resnik_verbs(id1, id2, max, similarity):
    """Tests normalized resnik scores for verbs."""
    synset1 = germanet_data.get_synset_by_id(id1)
    synset2 = germanet_data.get_synset_by_id(id2)
    dist = relatedness_verbs.resnik(synset1, synset2, normalized_max=max, normalize=True)
    np.testing.assert_array_almost_equal(dist, similarity, decimal=2)


@pytest.mark.parametrize('id1,id2,similarity', raw_resnik_nouns)
def test_raw_resnik_nouns(id1, id2, similarity):
    """Tests unnormalized resnik scores for nouns."""
    synset1 = germanet_data.get_synset_by_id(id1)
    synset2 = germanet_data.get_synset_by_id(id2)
    dist = relatedness_nouns.resnik(synset1, synset2)
    np.testing.assert_array_almost_equal(dist, similarity, decimal=2)


@pytest.mark.parametrize('id1,id2,max,similarity', normalized_resnik_nouns)
def test_normalized_resnik_nouns(id1, id2, max, similarity):
    """Tests normalized resnik scores for nouns."""
    synset1 = germanet_data.get_synset_by_id(id1)
    synset2 = germanet_data.get_synset_by_id(id2)
    dist = relatedness_nouns.resnik(synset1, synset2, normalized_max=max, normalize=True)
    np.testing.assert_array_almost_equal(dist, similarity, decimal=2)


@pytest.mark.parametrize('id1,id2,similarity', raw_resnik_adj)
def test_raw_resnik_adj(id1, id2, similarity):
    """Tests unnormalized resnik scores for adjectives."""
    synset1 = germanet_data.get_synset_by_id(id1)
    synset2 = germanet_data.get_synset_by_id(id2)
    dist = relatedness_adj.resnik(synset1, synset2)
    np.testing.assert_array_almost_equal(dist, similarity, decimal=2)


@pytest.mark.parametrize('id1,id2,max,similarity', normalized_resnik_adj)
def test_normalized_resnik_adj(id1, id2, max, similarity):
    """Tests normalized resnik scores for adjectives."""
    synset1 = germanet_data.get_synset_by_id(id1)
    synset2 = germanet_data.get_synset_by_id(id2)
    dist = relatedness_adj.resnik(synset1, synset2, normalized_max=max, normalize=True)
    np.testing.assert_array_almost_equal(dist, similarity, decimal=2)


# lin measure #

@pytest.mark.parametrize('id1,id2,similarity', raw_lin_verbs)
def test_raw_lin_verbs(id1, id2, similarity):
    """Tests unnormalized lin scores for verbs."""
    synset1 = germanet_data.get_synset_by_id(id1)
    synset2 = germanet_data.get_synset_by_id(id2)
    dist = relatedness_verbs.lin(synset1, synset2)
    np.testing.assert_array_almost_equal(dist, similarity, decimal=2)


@pytest.mark.parametrize('id1,id2,max,similarity', normalized_lin_verbs)
def test_normalized_lin_verbs(id1, id2, max, similarity):
    """Tests normalized lin scores for verbs."""
    synset1 = germanet_data.get_synset_by_id(id1)
    synset2 = germanet_data.get_synset_by_id(id2)
    dist = relatedness_verbs.lin(synset1, synset2, normalized_max=max, normalize=True)
    np.testing.assert_array_almost_equal(dist, similarity, decimal=2)


@pytest.mark.parametrize('id1,id2,similarity', raw_lin_nouns)
def test_raw_lin_nouns(id1, id2, similarity):
    """Tests unnormalized lin scores for nouns."""
    synset1 = germanet_data.get_synset_by_id(id1)
    synset2 = germanet_data.get_synset_by_id(id2)
    dist = relatedness_nouns.lin(synset1, synset2)
    np.testing.assert_array_almost_equal(dist, similarity, decimal=2)


@pytest.mark.parametrize('id1,id2,max,similarity', normalized_lin_nouns)
def test_normalized_lin_nouns(id1, id2, max, similarity):
    """Tests normalized lin scores for nouns."""
    synset1 = germanet_data.get_synset_by_id(id1)
    synset2 = germanet_data.get_synset_by_id(id2)
    dist = relatedness_nouns.lin(synset1, synset2, normalized_max=max, normalize=True)
    np.testing.assert_array_almost_equal(dist, similarity, decimal=2)


@pytest.mark.parametrize('id1,id2,similarity', raw_lin_adj)
def test_raw_lin_adj(id1, id2, similarity):
    """Tests unnormalized lin scores for adjectives."""
    synset1 = germanet_data.get_synset_by_id(id1)
    synset2 = germanet_data.get_synset_by_id(id2)
    dist = relatedness_adj.lin(synset1, synset2)
    np.testing.assert_array_almost_equal(dist, similarity, decimal=2)


@pytest.mark.parametrize('id1,id2,max,similarity', normalized_lin_adj)
def test_normalized_lin_adj(id1, id2, max, similarity):
    """Tests normalized lin scores for adjectives."""
    synset1 = germanet_data.get_synset_by_id(id1)
    synset2 = germanet_data.get_synset_by_id(id2)
    dist = relatedness_adj.lin(synset1, synset2, normalized_max=max, normalize=True)
    np.testing.assert_array_almost_equal(dist, similarity, decimal=2)


# jiang and conrath measure #

@pytest.mark.parametrize('id1,id2,similarity', raw_jcn_verbs)
def test_raw_jcn_verbs(id1, id2, similarity):
    """Tests unnormalized jcn scores for verbs."""
    synset1 = germanet_data.get_synset_by_id(id1)
    synset2 = germanet_data.get_synset_by_id(id2)
    dist = relatedness_verbs.jiang_and_conrath(synset1, synset2)
    np.testing.assert_array_almost_equal(dist, similarity, decimal=2)


@pytest.mark.parametrize('id1,id2,max,similarity', normalized_jcn_verbs)
def test_normalized_jcn_verbs(id1, id2, max, similarity):
    """Tests normalized jcn scores for verbs."""
    synset1 = germanet_data.get_synset_by_id(id1)
    synset2 = germanet_data.get_synset_by_id(id2)
    dist = relatedness_verbs.jiang_and_conrath(synset1, synset2, normalized_max=max, normalize=True)
    np.testing.assert_array_almost_equal(dist, similarity, decimal=2)


@pytest.mark.parametrize('id1,id2,similarity', raw_jcn_nouns)
def test_raw_jcn_nouns(id1, id2, similarity):
    """Tests unnormalized jcn scores for nouns."""
    synset1 = germanet_data.get_synset_by_id(id1)
    synset2 = germanet_data.get_synset_by_id(id2)
    dist = relatedness_nouns.jiang_and_conrath(synset1, synset2)
    np.testing.assert_array_almost_equal(dist, similarity, decimal=2)


@pytest.mark.parametrize('id1,id2,max,similarity', normalized_jcn_nouns)
def test_normalized_jcn_nouns(id1, id2, max, similarity):
    """Tests normalized jcn scores for nouns."""
    synset1 = germanet_data.get_synset_by_id(id1)
    synset2 = germanet_data.get_synset_by_id(id2)
    dist = relatedness_nouns.jiang_and_conrath(synset1, synset2, normalized_max=max, normalize=True)
    np.testing.assert_array_almost_equal(dist, similarity, decimal=2)


@pytest.mark.parametrize('id1,id2,similarity', raw_jcn_adj)
def test_raw_jcn_adj(id1, id2, similarity):
    """Tests unnormalized jcn scores for adjectives."""
    synset1 = germanet_data.get_synset_by_id(id1)
    synset2 = germanet_data.get_synset_by_id(id2)
    dist = relatedness_adj.jiang_and_conrath(synset1, synset2)
    np.testing.assert_array_almost_equal(dist, similarity, decimal=2)


@pytest.mark.parametrize('id1,id2,max,similarity', normalized_jcn_adj)
def test_normalized_jcn_adj(id1, id2, max, similarity):
    """Tests normalized jcn scores for adjectives."""
    synset1 = germanet_data.get_synset_by_id(id1)
    synset2 = germanet_data.get_synset_by_id(id2)
    dist = relatedness_adj.jiang_and_conrath(synset1, synset2, normalized_max=max, normalize=True)
    np.testing.assert_array_almost_equal(dist, similarity, decimal=2)
