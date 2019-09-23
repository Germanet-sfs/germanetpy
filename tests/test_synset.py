from pathlib import Path
import sys
import logging
import pytest
from germanet import Germanet
import numpy as np
from lxml import etree as ET
from synset import ConRel

logger = logging.getLogger('logging_test_synset')
d = str(Path(__file__).parent.parent) + "/data"
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

conceptual_relations = [
    ('s46683', ConRel.has_component_meronym, ['s39494']),
    ('s8813', ConRel.has_component_meronym,
     ['s5731', 's40989', 's6270', 's8925', 's7580', 's6281', 's6377', 's8929', 's6384', 's6383', 's10140', 's25669',
      's9020', 's40988', 's6032', 's8880', 's6385', 's40985', 's6003', 's5998']),
    ('s59726', ConRel.causes, ['s3075']),
    ('s42888', ConRel.is_related_to, ['s84261', 's41336']),
    ('s41689', ConRel.has_component_holonym, ['s42888'])
]
conceptual_incoming_relations = [
    ('s58848', ConRel.causes, ['s56473']),
    ('s41689', ConRel.has_component_meronym, ['s42888']),
    ('s54503', ConRel.entails, ['s54618', 's54339'])
]
all_hypernyms = [
    ('s131', ['s91', 's90', 's0', 's51001']),
    ('s50944',
     ['s27100', 's27099', 's27094', 's27090', 's23307', 's22562', 's47101', 's47083', 's50999', 's50981', 's50980',
      's51001', 's27075', 's27071', 's26979', 's50708', 's50915', 's48805', 's50997', 's50990', 's50986', 's50982',
      's50706', 's50688', 's50687', 's50519', 's50498', 's49812', 's49800', 's48873']),
    ('s57835', ['s57779', 's57714', 's57713', 's57324', 's57318', 's57309', 's60939', 's51001'])
]

paths_between_synsets_nouns = [
    ('s50708', 's48836', ['s50708', 's50915', 's50696', 's48836']),
    ('s50708', 's34063', ['s50708', 's50915', 's48805', 's50997', 's34063']),
    ('s34063', 's8813',
     ['s34063', 's50997', 's50990', 's50986', 's50982', 's50981', 's50999', 's5550', 's5675', 's8702', 's8714', 's8716',
      's8813']),
    ('s42337', 's73124', ['s42337', 's9938', 's9918', 's47083', 's73124'])
]

paths_between_synsets_adj = [
    ('s3', 's158', ['s3', 's79860', 's2246', 's2245', 's51001', 's4452', 's154', 's155', 's158']),
    ('s96631', 's805', ['s96631', 's21', 's2', 's1', 's0', 's10', 's214', 's242', 's805'])
]

paths_between_synsets_verbs = [
    ('s52219', 's52747', ['s52219', 's52202', 's59388', 's51948', 's51946', 's51892', 's52746', 's52747']),
    ('s57835', 's52201',
     ['s57835', 's57779', 's57714', 's57713', 's57324', 's57318', 's57309', 's57310', 's57316', 's57476', 's52201'])
]

path_len_nouns = [
    ('s49774', 's83979', 35),
    ('s49774', 's20560', 35),
    ('s49774', 's20561', 35),
    ('s49774', 's138670', 35),
    ('s9439', 's48837', 12),
    ('s39183', 's39496', 5)
]

path_len_adj = [
    ('s91', 's102579', 7),
    ('s5399', 's5427', 4),
    ('s95326', 's95987', 20),
    ('s95326', 's94396', 20),
    ('s94411', 's95987', 20),
    ('s94411', 's94396', 20)

]

path_len_verbs = [
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

LCS_between_nouns = [
    ('s50708', 's48836', ['s50915']),
    ('s50708', 's34063', ['s50997']),
    ('s34063', 's8813', ['s50981']),
    ('s42337', 's73124', ['s47083']),
    ('s39494', 's39495', ['s39491']),
    ('s39494', 's46042', ['s50981']),
    ('s50869', 's11106', ['s50981']),
    ('s46665', 's7922', ['s7917']),
    ('s46657', 's46659', ['s46657'])
]

LCS_between_adj = [
    ('s3', 's158', ['s51001']),
    ('s96631', 's805', ['s0']),
    ('s94411', 's94543', ['s0', 's51001']),
    ('s94411', 's94396', ['s51001'])
]

LCS_between_verbs = [
    ('s52219', 's52747', ['s51892']),
    ('s107484', 's61151', ['s52270'])
]


@pytest.mark.parametrize('id,hypernym_ids', all_hypernyms)
def test_all_hypernyms(id, hypernym_ids):
    synset = germanet_data.get_synset_by_id(id)
    hypernyms = synset.all_hypernyms()
    np.testing.assert_equal(sorted([synset.id() for synset in hypernyms]), sorted(hypernym_ids))


def test_root():
    gnroot = 's51001'
    root = germanet_data.get_synset_by_id(gnroot)
    np.testing.assert_equal(root.is_root(), True)
    np.testing.assert_equal(root.is_leaf(), False)


def test_leafs():
    leafs = ['s6675', 's136315', 's10765', 's106594', 's131']
    for leaf in leafs:
        synset = germanet_data.get_synset_by_id(leaf)
        np.testing.assert_equal(synset.is_root(), False)
        np.testing.assert_equal(synset.is_leaf(), True)


def get_shortest_paths(id1, id2):
    syn1 = germanet_data.get_synset_by_id(id1)
    syn2 = germanet_data.get_synset_by_id(id2)
    assert len(syn1.shortest_path(syn2)) == 1, "do not test for synsets with several shortest paths"
    return syn1.shortest_path(syn2)[0]


@pytest.mark.parametrize('id1,id2,expected_path_ids', paths_between_synsets_nouns)
def test_paths_nouns(id1, id2, expected_path_ids):
    path = get_shortest_paths(id1, id2)
    np.testing.assert_equal([synset.id() for synset in path], expected_path_ids)


@pytest.mark.parametrize('id1,id2,expected_path_ids', paths_between_synsets_adj)
def test_paths_adj(id1, id2, expected_path_ids):
    path = get_shortest_paths(id1, id2)
    np.testing.assert_equal([synset.id() for synset in path], expected_path_ids)


@pytest.mark.parametrize('id1,id2,expected_path_ids', paths_between_synsets_verbs)
def test_paths_adj(id1, id2, expected_path_ids):
    path = get_shortest_paths(id1, id2)
    np.testing.assert_equal([synset.id() for synset in path], expected_path_ids)


@pytest.mark.parametrize('id1,id2,pathlength', path_len_nouns)
def test_pathlength_nouns(id1, id2, pathlength):
    synset1 = germanet_data.get_synset_by_id(id1)
    synset2 = germanet_data.get_synset_by_id(id2)
    dist = synset1.shortest_path_distance(synset2)
    np.testing.assert_equal(dist, pathlength)


@pytest.mark.parametrize('id1,id2,pathlength', path_len_adj)
def test_pathlength_adj(id1, id2, pathlength):
    synset1 = germanet_data.get_synset_by_id(id1)
    synset2 = germanet_data.get_synset_by_id(id2)
    dist = synset1.shortest_path_distance(synset2)
    np.testing.assert_equal(dist, pathlength)


@pytest.mark.parametrize('id1,id2,pathlength', path_len_verbs)
def test_pathlength_verbs(id1, id2, pathlength):
    synset1 = germanet_data.get_synset_by_id(id1)
    synset2 = germanet_data.get_synset_by_id(id2)
    dist = synset1.shortest_path_distance(synset2)
    np.testing.assert_equal(dist, pathlength)


@pytest.mark.parametrize('id1,id2,expected_ids', LCS_between_nouns)
def test_lcs_nouns(id1, id2, expected_ids):
    syn1 = germanet_data.get_synset_by_id(id1)
    syn2 = germanet_data.get_synset_by_id(id1)
    lcs = syn1.lowest_common_subsumer(syn2)
    np.testing.assert_equal(sorted([l.id() for l in lcs]), sorted(expected_ids))


@pytest.mark.parametrize('id1,id2,expected_ids', LCS_between_verbs)
def test_lcs_verbs(id1, id2, expected_ids):
    syn1 = germanet_data.get_synset_by_id(id1)
    syn2 = germanet_data.get_synset_by_id(id1)
    lcs = syn1.lowest_common_subsumer(syn2)
    np.testing.assert_equal(sorted([l.id() for l in lcs]), sorted(expected_ids))


@pytest.mark.parametrize('id1,id2,expected_ids', LCS_between_adj)
def test_lcs_adjectives(id1, id2, expected_ids):
    syn1 = germanet_data.get_synset_by_id(id1)
    syn2 = germanet_data.get_synset_by_id(id1)
    lcs = syn1.lowest_common_subsumer(syn2)
    np.testing.assert_equal(sorted([l.id() for l in lcs]), sorted(expected_ids))


@pytest.mark.parametrize('id,conrel,expected_ids', conceptual_relations)
def test_conceptional_relations(id,conrel,expected_ids):
    synset = germanet_data.get_synset_by_id(id)
    related = synset.relations()[conrel]
    np.testing.assert_equal(sorted([syn.id() for syn in related]), sorted(expected_ids))

@pytest.mark.parametrize('id,conrel,expected_ids', conceptual_incoming_relations)
def test_incoming_conceptional_relations(id,conrel,expected_ids):
    synset = germanet_data.get_synset_by_id(id)
    related = synset.incoming_relations()[conrel]
    np.testing.assert_equal(sorted([syn.id() for syn in related]), sorted(expected_ids))