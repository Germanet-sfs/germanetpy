from pathlib import Path
import sys
import logging
import numpy as np
from lxml import etree as ET
import pytest
from germanetpy.germanet import Germanet
from germanetpy.filterconfig import Filterconfig
from germanetpy.lexunit import OrthFormVariant
from germanetpy.synset import WordCategory, WordClass

logger = logging.getLogger('logging_test_filter')
d = "/Users/bcmpbell/Data/GermaNetForApiUnitTesting/R19/XML-Valid"
try:
    germanet_data = Germanet(d)
except ET.ParseError:
    message = "Unable to load GermaNet data at {0} . Aborting...".format(d)
    logger.error(message,
                 ET.ParseError)
    sys.exit(0)
except IOError:
    message = "GermaNet data not found at {0} . Aborting...".format(d)
    logger.error(message, IOError)
    sys.exit(0)

allOrthForms_lex = [
    ('Spitz', True, ['l72040', 'l3733', 'l7447'], None, None),
    ('Spitz', False, ['l72040'], None, None),
    ('spitz', True, ['l72040', 'l3733', 'l7447'], None, None),
    ('spitz', False, ['l3733', 'l7447'], None, None)
]

allOrthForms_syn = [
    ('Spitz', True, ['s50936', 's2433', 's4983'], None, None),
    ('Spitz', False, ['s50936'], None, None),
    ('spitz', True, ['s50936', 's2433', 's4983'], None, None),
    ('spitz', False, ['s2433', 's4983'], None, None)
]

differentWordCategories_lex = [
    ('Recht', True, ['l45139', 'l18689', 'l18690', 'l145344'], [WordCategory.nomen], None),
    ('recht', True, ['l45139', 'l18689', 'l18690', 'l145344'], [WordCategory.nomen], None),
    ('Recht', False, ['l45139', 'l18689', 'l18690', 'l145344'], [WordCategory.nomen], None),

    ('recht', False, [], [WordCategory.nomen], None),
    ('Recht', True, ['l435', 'l1963', 'l3535', 'l132285'], [WordCategory.adj], None),
    ('recht', True, ['l45139', 'l18689', 'l18690', 'l145344', 'l435', 'l1963', 'l3535', 'l132285'],
     [WordCategory.nomen, WordCategory.adj], None),

    ('Recht', False, [], [WordCategory.verben], None),
    ('schiffahrt', True, ['l26447'], [WordCategory.nomen], None),
    ('schiffahrt', True, ['l26447'], [WordCategory.nomen, WordCategory.adj], None),
    ('schiffahrt', True, [], [WordCategory.adj], None),
    ('schloß', True, ['l62042', 'l8893'], [WordCategory.nomen], None)

]

differentWordCategories_syn = [
    ('Recht', True, ['s32782', 's13474', 's13475', 's28213'], [WordCategory.nomen], None),
    ('recht', True, ['s32782', 's13474', 's13475', 's28213'], [WordCategory.nomen], None),
    ('Recht', False, ['s32782', 's13474', 's13475', 's28213'], [WordCategory.nomen], None),

    ('recht', False, [], [WordCategory.nomen], None),
    ('Recht', True, ['s273', 's1182', 's2311', 's99446'], [WordCategory.adj], None),
    ('recht', True, ['s273', 's1182', 's2311', 's99446', 's32782', 's13474', 's13475', 's28213'],
     [WordCategory.nomen, WordCategory.adj], None),

    ('Recht', False, [], [WordCategory.verben], None),
    ('schiffahrt', True, ['s19109'], [WordCategory.nomen], None),
    ('schiffahrt', True, ['s19109'], [WordCategory.nomen, WordCategory.adj], None),
    ('schiffahrt', True, [], [WordCategory.adj], None),
    ('schloß', True, ['s6011', 's42555'], [WordCategory.nomen], None)

]

differentOrthCat_lex = [
    ('Schloß', True, [], [WordCategory.nomen], [OrthFormVariant.orthForm]),
    ('Schloß', True, ['l8893', 'l62042'], [WordCategory.nomen], [OrthFormVariant.oldOrthForm]),
    ('panter', True, [], [WordCategory.nomen], [OrthFormVariant.orthForm]),
    ('panter', True, ['l71762'], [WordCategory.nomen], [OrthFormVariant.orthVar]),
    ('panter', True, [], [WordCategory.nomen],
     [OrthFormVariant.orthForm, OrthFormVariant.oldOrthForm, OrthFormVariant.oldOrthVar])

]

differentOrthCat_syn = [
    ('Schloß', True, [], [WordCategory.nomen], [OrthFormVariant.orthForm]),
    ('Schloß', True, ['s6011', 's42555'], [WordCategory.nomen], [OrthFormVariant.oldOrthForm]),
    ('panter', True, [], [WordCategory.nomen], [OrthFormVariant.orthForm]),
    ('panter', True, ['s50699'], [WordCategory.nomen], [OrthFormVariant.orthVar]),
    ('panter', True, [], [WordCategory.nomen],
     [OrthFormVariant.orthForm, OrthFormVariant.oldOrthForm, OrthFormVariant.oldOrthVar])

]

differentRegex_syn = [
    (".*en.*brot.*", True, ['s39184', 's39185', 's39189', 's39193', 's39196', 's39962', 's40274', 's40282', 's44982',
                            's71879', 's117435', 's118466', 's132900', 's146785', 's146808', 's146806', 's143623',
                            's146861', 's150543', 's155998', 's159828', 's160534', 's164927', 's168808'], [WordCategory.nomen], []),
    (".*en.*brot.*", True, ['s44982', 's71879'], [WordCategory.nomen], [WordClass.Pflanze]),
    ("Musik.*f{2,}.*", True, ['s7064', 's115983', 's126175', 's137462'], [WordCategory.nomen], []),
    ("Musi.*k{2,}.*n{2,}.*", True, ['s135050'], [WordCategory.nomen], []),
    ("musi.*k{2,}.*n{2,}.*", False, [], [WordCategory.nomen], []),
    ("Musik.*(rr|st).*", True, ['s29972', 's29990', 's30067'], [WordCategory.nomen], [WordClass.Kommunikation]),
    ("unver.*bar", True,
     ['s218', 's488', 's1004', 's1013', 's1226', 's3605', 's3721', 's3748', 's3752', 's4008', 's4798', 's94410',
      's128930'], [WordCategory.adj], []),
    (".*un$", True, ['s57352', 's57394', 's151850', 's177631'], [WordCategory.verben], [WordClass.Lokation])
]

levenshtein_distance_syn = [
    ("Unver.*barkeit", True, True,
     [OrthFormVariant.orthForm, OrthFormVariant.oldOrthForm, OrthFormVariant.oldOrthVar, OrthFormVariant.orthVar], 3,
     ['s13953', 's13966', 's13969', 's14004', 's101032', 's108169', 's122501', 's125332']),
    ("Unver.*barkeit", False, True,
     [OrthFormVariant.orthForm, OrthFormVariant.oldOrthForm, OrthFormVariant.oldOrthVar, OrthFormVariant.orthVar],
     3, ['s13953', 's13966', 's13969', 's14004', 's101032', 's108169', 's122501', 's125332']),
    ("unver.*barkeit", True, True,
     [OrthFormVariant.orthForm, OrthFormVariant.oldOrthForm, OrthFormVariant.oldOrthVar, OrthFormVariant.orthVar], 5,
     ['s13953', 's13966', 's13969', 's14004', 's101032', 's108169', 's122501', 's125332']),
    ("Unvertretbarkeit", True, False,
     [OrthFormVariant.orthForm, OrthFormVariant.oldOrthForm, OrthFormVariant.oldOrthVar, OrthFormVariant.orthVar], 4,
     ['s13943', 's13952', 's13953', 's13966', 's13969', 's14004', 's108169', 's122501', 's218']),
    ("Unvertretbarkeit", False, False,
     [OrthFormVariant.orthForm, OrthFormVariant.oldOrthForm, OrthFormVariant.oldOrthVar, OrthFormVariant.orthVar], 4,
     ['s13943', 's13952', 's13953', 's13966', 's13969', 's14004', 's108169', 's122501']),
    ("Schloß", True, False, [OrthFormVariant.oldOrthForm], 2,
     ['s28692', 's6011', 's42555', 's51189', 's80636', 's21276', 's21263', 's112175', 's17941', 's16118']),
    ("Schloß", False, False, [OrthFormVariant.oldOrthForm], 2,
     ['s28692', 's6011', 's42555', 's51189', 's80636', 's21276', 's21263', 's112175', 's17941', 's16118']),
    ("schloß", True, False, [OrthFormVariant.oldOrthForm], 2,
     ['s28692', 's6011', 's42555', 's51189', 's80636', 's21276', 's21263', 's112175', 's17941', 's16118']),
    ("schloß", False, False, [OrthFormVariant.oldOrthForm], 2, ['s28692', 's6011', 's42555', 's51189']),
]


def apply_lexFilters(orthForm, ignoreCase, word_categories, orthvariants):
    "Auxiliary function to apply a filter for retrieving lexical units."
    config = Filterconfig(orthForm, ignore_case=ignoreCase)
    if word_categories is not None:
        config.word_categories = word_categories
    if orthvariants is not None:
        config.orth_variants = orthvariants

    return config.filter_lexunits(germanet_data)


def apply_synFilters(orthForm, ignoreCase, word_categories, orthvariants):
    """Auxiliary function to apply a filter for retrieving synsets"""
    config = Filterconfig(orthForm, ignore_case=ignoreCase)
    if word_categories is not None:
        config.word_categories = word_categories
    if orthvariants is not None:
        config.orth_variants = orthvariants

    return config.filter_synsets(germanet_data)


@pytest.mark.parametrize('orthForm,ignoreCase,expected_ids,word_categories,orthvariants', allOrthForms_lex)
def test_allOrthForms(orthForm, ignoreCase, expected_ids, word_categories, orthvariants):
    """Test whether a filter can be used to retrieve lexical units based on all orthographical variants."""
    result = apply_lexFilters(orthForm, ignoreCase, word_categories, orthvariants)
    np.testing.assert_equal(sorted([unit.id for unit in result]), sorted(expected_ids))


@pytest.mark.parametrize('orthForm,ignoreCase,expected_ids,word_categories,orthvariants', differentWordCategories_lex)
def test_differentWordCategories(orthForm, ignoreCase, expected_ids, word_categories, orthvariants):
    """Test whether lexical units can be retrieved based on specific word categories."""
    result = apply_lexFilters(orthForm, ignoreCase, word_categories, orthvariants)
    np.testing.assert_equal(sorted([unit.id for unit in result]), sorted(expected_ids))


@pytest.mark.parametrize('orthForm,ignoreCase,expected_ids,word_categories,orthvariants', differentOrthCat_lex)
def test_differentOrthVariants(orthForm, ignoreCase, expected_ids, word_categories, orthvariants):
    """Test whether lexical units can be retrieved specifying different orthographical variants. """
    result = apply_lexFilters(orthForm, ignoreCase, word_categories, orthvariants)
    np.testing.assert_equal(sorted([unit.id for unit in result]), sorted(expected_ids))


@pytest.mark.parametrize('orthForm,ignoreCase,expected_ids,word_categories,orthvariants', allOrthForms_syn)
def test_allOrthForms_synsets(orthForm, ignoreCase, expected_ids, word_categories, orthvariants):
    """Test whether a filter can be used to retrieve synsets based on all orthographical variants."""
    result = apply_synFilters(orthForm, ignoreCase, word_categories, orthvariants)
    np.testing.assert_equal(sorted([unit.id for unit in result]), sorted(expected_ids))


@pytest.mark.parametrize('orthForm,ignoreCase,expected_ids,word_categories,orthvariants', differentWordCategories_syn)
def test_differentWordCategories_synsets(orthForm, ignoreCase, expected_ids, word_categories, orthvariants):
    """Test whether synsets can be retrieved based on specific word categories."""
    result = apply_synFilters(orthForm, ignoreCase, word_categories, orthvariants)
    np.testing.assert_equal(sorted([unit.id for unit in result]), sorted(expected_ids))


@pytest.mark.parametrize('orthForm,ignoreCase,expected_ids,word_categories,orthvariants', differentOrthCat_syn)
def test_differentOrthVariants_synsets(orthForm, ignoreCase, expected_ids, word_categories, orthvariants):
    """Test whether synsets can be retrieved specifying different orthographical variants. """
    result = apply_synFilters(orthForm, ignoreCase, word_categories, orthvariants)
    np.testing.assert_equal(sorted([unit.id for unit in result]), sorted(expected_ids))


@pytest.mark.parametrize('regex,ignoreCase,expected_ids,word_categories,wordclasses', differentRegex_syn)
def test_regex_synsets(regex, ignoreCase, expected_ids, word_categories, wordclasses):
    """Test whether synsets can be retrieved with regular expressions"""
    config = Filterconfig(regex, ignore_case=ignoreCase, regex=True)
    config.word_categories = word_categories
    if wordclasses:
        config.word_classes = wordclasses
    result = config.filter_synsets(germanet_data)
    np.testing.assert_equal(sorted([unit.id for unit in result]), sorted(expected_ids))


@pytest.mark.parametrize('query,ignoreCase,regex,orthvariants,distance,expected_ids', levenshtein_distance_syn)
def test_levenshtein_synsets(query, ignoreCase, regex, orthvariants, distance, expected_ids):
    """Test whether synsets can be retrieved based on a specified levenshtein distance."""
    config = Filterconfig(query, ignore_case=ignoreCase, regex=regex, levenshtein_distance=distance)
    config.orth_variants = orthvariants
    result = config.filter_synsets(germanet_data)
    np.testing.assert_equal(sorted([unit.id for unit in result]), sorted(expected_ids))
