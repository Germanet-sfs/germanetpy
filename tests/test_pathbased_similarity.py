from pathlib import Path
import sys
import logging
import pytest
from germanetpy.germanet import Germanet
import numpy as np
from lxml import etree as ET
from germanetpy.path_based_relatedness_measures import PathBasedRelatedness
from germanetpy.synset import WordCategory

logger = logging.getLogger('logging_test_semrel')
d = str(Path(__file__).parent.parent) + "/data"
try:
    germanet_data = Germanet(d)
    johannis_wurm = germanet_data.get_synset_by_id("s49774")
    leber_trans = germanet_data.get_synset_by_id("s83979")
    relatedness_nouns = PathBasedRelatedness(germanet=germanet_data, category=WordCategory.nomen, max_len=35,
                                             max_depth=20, synset_pair=(johannis_wurm, leber_trans))
    relatedness_verbs = PathBasedRelatedness(germanet=germanet_data, category=WordCategory.verben)
    relatedness_adj = PathBasedRelatedness(germanet=germanet_data, category=WordCategory.adj)
except ET.ParseError:
    message = ("Unable to load GermaNet data at {0} . Aborting...").format(d)
    logger.error(message,
                 ET.ParseError)
    sys.exit(0)
except IOError:
    message = ("GermaNet data not found at {0} . Aborting...").format(d)
    logger.error(message, IOError)
    sys.exit(0)

unnormalized_path_len_nouns = [
    ('s49774', 's83979', 35),
    ('s49774', 's20560', 35),
    ('s49774', 's20561', 35),
    ('s9439', 's48837', 12),
    ('s39183', 's39496', 5)
]

unnormalized_path_len_adj = [
    ('s91', 's102579', 7),
    ('s5399', 's5427', 4),
    ('s95326', 's95987', 20),
    ('s95326', 's94396', 20),
    ('s94411', 's95987', 20),
    ('s94411', 's94396', 20)

]

unnormalized_path_len_verbs = [
    ('s58565', 's58578', 2),
    ('s57835', 's57328', 5),
    ('s106731', 's123246', 28),
    ('s106731', 's120154', 28),
    ('s106731', 's57534', 28),
    ('s106731', 's123240', 28),
    ('s119463', 's120154', 28),
    ('s119463', 's57534', 28),
    ('s119463', 's123240', 28),
    ('s119463', 's123246', 28)
]

normalized_path_len_nouns = [
    ('s46047', 's45380', 1.0, 0.88571),
    ('s46047', 's45380', 10.0, 8.8571),
    ('s49774', 's83979', 1.0, 0.0),
    ('s49774', 's49774', 1.0, 1.0),
    ('s49774', 's49774', 10.0, 10.0),
    ('s46683', 's46650', 10.0, 8.5714)
]

unnormalized_lch_nouns = [
    ('s46047', 's45380', 0.92428),
    ('s49774', 's49774', 1.62325),
    ('s46683', 's46650', 0.84509),
]

normalized_lch_nouns = [
    ('s46047', 's45380', 10.0, 5.50877),
    ('s49774', 's49774', 10.0, 10.0),
    ('s46683', 's46650', 10.0, 4.99999)
]

unnormalized_lch_verbs = [
    ('s57534', 's119463', 0.04275),
    ('s57534', 's57534', 1.50515),

]

normalized_lch_verbs = [
    ('s57534', 's119463', 10.0, 0.0),
    ('s57534', 's57534', 10.0, 10.0),
]

unnormalized_lch_adj = [
    ('s94396', 's94411', 0.020203),
    ('s94396', 's94396', 1.342423)
]

normalized_lch_adj = [
    ('s94396', 's94411', 10.0, 0.0),
    ('s94396', 's94396', 10.0, 10.0)
]

unnormalized_wup_nouns = [
    ('s46047', 's45380', 0.75),
    ('s49774', 's49774', 1.0),
    ('s46683', 's46650', 0.70588),
]

normalized_wup_nouns = [
    ('s46047', 's45380', 10.0, 7.5),
    ('s49774', 's49774', 10.0, 10.0),
    ('s46683', 's46650', 10.0, 7.0588)
]

unnormalized_wup_verbs = [
    ('s57534', 's119463', 0.0),
    ('s57534', 's57534', 1.0),

]

normalized_wup_verbs = [
    ('s57534', 's119463', 10.0, 0.0),
    ('s57534', 's57534', 10.0, 10.0),
]

unnormalized_wup_adj = [
    ('s94396', 's94411', 0.0),
    ('s94396', 's94396', 1.0)
]

normalized_wup_adj = [
    ('s94396', 's94411', 10.0, 0.0),
    ('s94396', 's94396', 10.0, 10.0)
]


@pytest.mark.parametrize('id1,id2,pathlength', unnormalized_path_len_nouns)
def test_pathlength_nouns(id1, id2, pathlength):
    """Tests whether the length of the shortest path between two given nouns is correct."""
    synset1 = germanet_data.get_synset_by_id(id1)
    synset2 = germanet_data.get_synset_by_id(id2)
    dist = synset1.shortest_path_distance(synset2)
    np.testing.assert_equal(dist, pathlength)


@pytest.mark.parametrize('id1,id2,pathlength', unnormalized_path_len_adj)
def test_pathlength_adj(id1, id2, pathlength):
    """Tests whether the length of the shortest path between two given adjectives is correct."""
    synset1 = germanet_data.get_synset_by_id(id1)
    synset2 = germanet_data.get_synset_by_id(id2)
    dist = synset1.shortest_path_distance(synset2)
    np.testing.assert_equal(dist, pathlength)


@pytest.mark.parametrize('id1,id2,pathlength', unnormalized_path_len_verbs)
def test_pathlength_verbs(id1, id2, pathlength):
    """Tests whether the length of the shortest path between two given verbs is correct."""
    synset1 = germanet_data.get_synset_by_id(id1)
    synset2 = germanet_data.get_synset_by_id(id2)
    dist = synset1.shortest_path_distance(synset2)
    np.testing.assert_equal(dist, pathlength)


# leacock and chodorow #


@pytest.mark.parametrize('id1,id2,similarity', unnormalized_lch_nouns)
def test_raw_lch_nouns(id1, id2, similarity):
    """Tests whether the unnormalized lch score for nouns is correct."""
    synset1 = germanet_data.get_synset_by_id(id1)
    synset2 = germanet_data.get_synset_by_id(id2)
    sim = relatedness_nouns.leacock_chodorow(synset1=synset1, synset2=synset2, normalize=False)
    np.testing.assert_almost_equal(sim, similarity, decimal=2)


@pytest.mark.parametrize('id1,id2,upper,similarity', normalized_lch_nouns)
def test_normalized_lch_nouns(id1, id2, upper, similarity):
    """Tests whether the normalized lch score for nouns is correct."""
    synset1 = germanet_data.get_synset_by_id(id1)
    synset2 = germanet_data.get_synset_by_id(id2)
    sim = relatedness_nouns.leacock_chodorow(synset1=synset1, synset2=synset2, normalize=True, normalized_max=upper)
    np.testing.assert_almost_equal(sim, similarity, decimal=2)


@pytest.mark.parametrize('id1,id2,similarity', unnormalized_lch_verbs)
def test_unnormalized_lch_verbs(id1, id2, similarity):
    """Tests whether the unnormalized lch score for verbs is correct."""
    synset1 = germanet_data.get_synset_by_id(id1)
    synset2 = germanet_data.get_synset_by_id(id2)
    sim = relatedness_verbs.leacock_chodorow(synset1=synset1, synset2=synset2, normalize=False)
    np.testing.assert_almost_equal(sim, similarity, decimal=2)


@pytest.mark.parametrize('id1,id2,upper,similarity', normalized_lch_verbs)
def test_normalized_lch_verbs(id1, id2, upper, similarity):
    """Tests whether the normalized lch score for verbs is correct."""
    synset1 = germanet_data.get_synset_by_id(id1)
    synset2 = germanet_data.get_synset_by_id(id2)
    sim = relatedness_verbs.leacock_chodorow(synset1=synset1, synset2=synset2, normalize=True, normalized_max=upper)
    np.testing.assert_almost_equal(sim, similarity, decimal=2)


@pytest.mark.parametrize('id1,id2,similarity', unnormalized_lch_adj)
def test_unnormalized_lch_adj(id1, id2, similarity):
    """Tests whether the unnormalized lch score for adjectives is correct."""
    synset1 = germanet_data.get_synset_by_id(id1)
    synset2 = germanet_data.get_synset_by_id(id2)
    sim = relatedness_adj.leacock_chodorow(synset1=synset1, synset2=synset2, normalize=False)
    np.testing.assert_almost_equal(sim, similarity, decimal=2)


@pytest.mark.parametrize('id1,id2,upper,similarity', normalized_lch_adj)
def test_normalized_lch_adj(id1, id2, upper, similarity):
    """Tests whether the normalized lch score for adjectives is correct."""
    synset1 = germanet_data.get_synset_by_id(id1)
    synset2 = germanet_data.get_synset_by_id(id2)
    sim = relatedness_adj.leacock_chodorow(synset1=synset1, synset2=synset2, normalize=True, normalized_max=upper)
    np.testing.assert_almost_equal(sim, similarity, decimal=2)


# wu and palmer #


@pytest.mark.parametrize('id1,id2,similarity', unnormalized_wup_nouns)
def test_raw_wup_nouns(id1, id2, similarity):
    """Tests whether the unnormalized wup score for nouns is correct."""
    synset1 = germanet_data.get_synset_by_id(id1)
    synset2 = germanet_data.get_synset_by_id(id2)
    sim = relatedness_nouns.wu_and_palmer(synset1=synset1, synset2=synset2, normalize=False)
    np.testing.assert_almost_equal(sim, similarity, decimal=2)


@pytest.mark.parametrize('id1,id2,upper,similarity', normalized_wup_nouns)
def test_normalized_wup_nouns(id1, id2, upper, similarity):
    """Tests whether the normalized wup score for nouns is correct."""
    synset1 = germanet_data.get_synset_by_id(id1)
    synset2 = germanet_data.get_synset_by_id(id2)
    sim = relatedness_nouns.wu_and_palmer(synset1=synset1, synset2=synset2, normalize=True, normalized_max=upper)
    np.testing.assert_almost_equal(sim, similarity, decimal=2)


@pytest.mark.parametrize('id1,id2,similarity', unnormalized_wup_verbs)
def test_unnormalized_wup_verbs(id1, id2, similarity):
    """Tests whether the unnormalized wup score for verbs is correct."""
    synset1 = germanet_data.get_synset_by_id(id1)
    synset2 = germanet_data.get_synset_by_id(id2)
    sim = relatedness_verbs.wu_and_palmer(synset1=synset1, synset2=synset2, normalize=False)
    np.testing.assert_almost_equal(sim, similarity, decimal=2)


@pytest.mark.parametrize('id1,id2,upper,similarity', normalized_wup_verbs)
def test_normalized_wup_verbs(id1, id2, upper, similarity):
    """Tests whether the normalized wup score for verbs is correct."""
    synset1 = germanet_data.get_synset_by_id(id1)
    synset2 = germanet_data.get_synset_by_id(id2)
    sim = relatedness_verbs.wu_and_palmer(synset1=synset1, synset2=synset2, normalize=True, normalized_max=upper)
    np.testing.assert_almost_equal(sim, similarity, decimal=2)


@pytest.mark.parametrize('id1,id2,similarity', unnormalized_wup_adj)
def test_unnormalized_wup_adj(id1, id2, similarity):
    """Tests whether the unnormalized wup score for adjectives is correct."""
    synset1 = germanet_data.get_synset_by_id(id1)
    synset2 = germanet_data.get_synset_by_id(id2)
    sim = relatedness_adj.wu_and_palmer(synset1=synset1, synset2=synset2, normalize=False)
    np.testing.assert_almost_equal(sim, similarity, decimal=2)


@pytest.mark.parametrize('id1,id2,upper,similarity', normalized_wup_adj)
def test_normalized_wup_adj(id1, id2, upper, similarity):
    """Tests whether the normalized wup score for adjectives is correct."""
    synset1 = germanet_data.get_synset_by_id(id1)
    synset2 = germanet_data.get_synset_by_id(id2)
    sim = relatedness_adj.wu_and_palmer(synset1=synset1, synset2=synset2, normalize=True, normalized_max=upper)
    np.testing.assert_almost_equal(sim, similarity, decimal=2)
