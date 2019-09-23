from lexunit import LexRel
from synset import ConRel

NAME = 'name'
FROM_NODE = 'from'
TO_NODE = 'to'
DIRECTION = 'dir'
INVERSE = 'inv'
LEX_REL = 'lex_rel'
CON_REL = 'con_rel'


def get_relation_attributes(attributes):
    relation = attributes[NAME]
    from_node = attributes[FROM_NODE]
    to_node = attributes[TO_NODE]
    direction = attributes[DIRECTION]
    inverse_relation = attributes.get(INVERSE)

    return relation, from_node, to_node, direction, inverse_relation


def load_relations(germanet, tree):
    root = tree.getroot()
    for child in root:
        tag = child.tag
        if tag == LEX_REL:
            relation, from_node, to_node, direction, inverse_relation = get_relation_attributes(child.attrib)
            lexunit1 = germanet._lexunits[from_node]
            lexunit2 = germanet._lexunits[to_node]
            lexunit1._relations[LexRel[relation]].add(lexunit2)
            lexunit2._incoming_relations[LexRel[relation]].add(lexunit1)
            if inverse_relation is not None:
                lexunit2._relations[LexRel[inverse_relation]].add(lexunit1)

        elif tag == CON_REL:
            relation, from_node, to_node, dir, inverse_relation = get_relation_attributes(child.attrib)
            synset1 = germanet._synsets[from_node]
            synset2 = germanet._synsets[to_node]
            synset1._relations[ConRel[relation]].add(synset2)
            synset2._incoming_relations[ConRel[relation]].add(synset1)
            if inverse_relation is not None:
                synset2._relations[ConRel[inverse_relation]].add(synset1)
