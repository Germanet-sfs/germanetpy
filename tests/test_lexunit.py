from pathlib import Path
import sys
import logging
import pytest
from germanetpy.germanet import Germanet
import numpy as np
from lxml import etree as ET
from germanetpy.lexunit import LexRel
from germanetpy.compoundInfo import CompoundProperty, CompoundCategory

logger = logging.getLogger('logging_test_lexunit')
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

lexical_relations = [
    ('l66160', LexRel.has_part, ['l9112']),
    ('l81451', LexRel.has_synonym, ['l81448', 'l81449', 'l81450']),
    ('l12419', LexRel.has_synonym, ['l97249', 'l12418', 'l12420', 'l12421', 'l12422', 'l12423', 'l122141']),
    ('l2825', LexRel.has_antonym, ['l2847'])
]

lexical_incoming_relations = [
    ('l66183', LexRel.is_part_of, ['l66955', 'l66960']),
    ('l66183', LexRel.has_habitat, ['l71123']),
    ('l66183', LexRel.has_topic, ['l25890']),
    ('l62003', LexRel.has_member, ['l124229']),

]

# Relation, Equivalent, pwn20Id, pwn30Id, synonyms, pwn20paraphrase, source
iliRecords = [
    ('l37670', 'synonym', 'hearing', 'ENG20-05331473-n', 'ENG30-05657718-n',
     ['audition', 'auditory sense', 'sense of hearing', 'auditory modality'],
     'the ability to hear; the auditory faculty; "his hearing was impaired"', 'extension2'),
    ('l41587', 'synonym', 'newsletter', 'ENG20-06270913-n', 'ENG30-06681976-n', ['newssheet'],
     'report or open letter giving informal or confidential news of interest to a special group', 'extension2')
]

# modifier, head, modifier1Property, modifier1Category, modifier2, modifier2Property, modifier2Category, headProperty
compound_info = [
    ('l66936', 'Apfel', 'Baum', None, CompoundCategory.Nomen, None, None, None, None),
    ('l57979', 'Him', 'Beere', CompoundProperty.opaquesMorphem, None, None, None, None, None),
    ('l23978', 'Kegel', 'Tour', None, CompoundCategory.Nomen, 'kegeln', None, CompoundCategory.Verb, None),
    ('l23312', 'Spiel', 'Ausgang', None, CompoundCategory.Nomen, 'spielen', None, CompoundCategory.Verb, None),
    ('l17119', 'mikro', 'Chip', CompoundProperty.Konfix, None, None, None, None, None)

]

# lexunit, wiktionaryId, wiktionarySenseId, wiktionarySense, edited
wiktionary = [("l76274", "w74102", 0,
               "wird im Vergleich zu benutzen regional verschieden gewertet, von synonym bis in Nuancen entwertenden "
               "Touch: verwenden, aus etwas Nutzen ziehen, ausnutzen, zum Vorteil anwenden, brauchen, gebrauchen",
               False),
              ('l101788', 'w29023', 2, 'der Unterhaltung dienendes  Gebäude, Etablissement', False),
              ('l173', 'w136562', 2, 'großartig, unglaublich (Ausdruck der Bewunderung), sagenhaft', False)]


@pytest.mark.parametrize('id,lexrel,expected_ids', lexical_relations)
def test_lexical_relations(id, lexrel, expected_ids):
    """Test whether the given lexunit contains the correct lexical relations"""
    lexunit = germanet_data.lexunits[id]
    related = lexunit.relations[lexrel]
    np.testing.assert_equal(sorted([lex.id for lex in related]), sorted(expected_ids))


@pytest.mark.parametrize('id,lexrel,expected_ids', lexical_incoming_relations)
def test_incoming_lexical_relations(id, lexrel, expected_ids):
    """Test whether the given lexunit contains the correct incoming lexical relations."""
    lexunit = germanet_data.lexunits[id]
    related = lexunit.incoming_relations[lexrel]
    np.testing.assert_equal(sorted([lex.id for lex in related]), sorted(expected_ids))


@pytest.mark.parametrize(
    'id,modifier, head, modifier1Property, modifier1Category, modifier2, modifier2Property, modifier2Category, '
    'headProperty',
    compound_info)
def test_compoundInfo(id, modifier, head, modifier1Property, modifier1Category, modifier2, modifier2Property,
                      modifier2Category,
                      headProperty):
    """Test if a compound info is stored correctly."""
    lexunit = germanet_data.lexunits[id]
    compoundinfo = lexunit.compound_info
    np.testing.assert_equal(compoundinfo.modifier1, modifier)
    np.testing.assert_equal(compoundinfo.head, head)
    np.testing.assert_equal(compoundinfo.modifier1_property == modifier1Property, True)
    np.testing.assert_equal(compoundinfo.modifier1_category == modifier1Category, True)
    np.testing.assert_equal(compoundinfo.modifier2 == modifier2, True)
    np.testing.assert_equal(compoundinfo.modifier2_property == modifier2Property, True)
    np.testing.assert_equal(compoundinfo.modifier2_category == modifier2Category, True)
    np.testing.assert_equal(compoundinfo.head_property == headProperty, True)


@pytest.mark.parametrize('id, relation, english_equivalent, pwn20Id, pwn30Id, pwn20synonyms, pwn20paraphrase, source',
                         iliRecords)
def test_iliRecords(id, relation, english_equivalent, pwn20Id, pwn30Id, pwn20synonyms, pwn20paraphrase, source):
    """Test if an ili record is stored correctly."""
    lexunit = germanet_data.lexunits[id]
    ilirecord = lexunit.ili_records[0]
    np.testing.assert_equal(ilirecord.relation, relation)
    np.testing.assert_equal(ilirecord.english_equivalent, english_equivalent)
    np.testing.assert_equal(ilirecord.pwn20id, pwn20Id)
    np.testing.assert_equal(ilirecord.pwn30id, pwn30Id)
    np.testing.assert_equal(ilirecord.pwn20synonyms, pwn20synonyms)
    np.testing.assert_equal(ilirecord.pwn20paraphrase, pwn20paraphrase)
    np.testing.assert_equal(ilirecord.source, source)


@pytest.mark.parametrize('id, wiktionaryId, wiktionarySenseId, wiktionarySense, edited', wiktionary)
def test_wiktionary(id, wiktionaryId, wiktionarySenseId, wiktionarySense, edited):
    """Test if a wiktionary paraphrase is stored correctly."""
    lexunit = germanet_data.lexunits[id]
    wiktionary = lexunit.wiktionary_paraphrases[0]
    np.testing.assert_equal(wiktionary.wiktionary_id, wiktionaryId)
    np.testing.assert_equal(wiktionary.wiktionary_sense_id, wiktionarySenseId)
    np.testing.assert_equal(wiktionary.wiktionary_sense, wiktionarySense)
    np.testing.assert_equal(wiktionary.edited, edited)
