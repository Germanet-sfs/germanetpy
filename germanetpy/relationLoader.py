from germanetpy.lexunit import LexRel
from germanetpy.synset import ConRel

NAME = 'name'
FROM_NODE = 'from'
TO_NODE = 'to'
DIRECTION = 'dir'
INVERSE = 'inv'
LEX_REL = 'lex_rel'
CON_REL = 'con_rel'


def get_relation_attributes(attributes) -> (str, str, str, str):
    """
    :type attributes: XML attribute
    :param attributes: The XML attributes the information can be extracted from
    :return: The information as Strings or None if the information is not present. The name of the relation,
    the id of the start node, the id of the end node, the type of direction and if
    the relation is inverse
    """
    relation = attributes[NAME]
    from_node = attributes[FROM_NODE]
    to_node = attributes[TO_NODE]
    direction = attributes[DIRECTION]
    inverse_relation = attributes.get(INVERSE)
    return relation, from_node, to_node, direction, inverse_relation


def load_relations(germanet, tree):
    """
    Loads the information about the related synsets ans lexunits from the data and adds the edges between the objects.
    :type tree: Element Tree
    :type germanet: Germanet
    :param germanet: The Germanet object that is populated with Synsets and Lexunits
    :param tree: The XML tree of the relation data.
    """
    root = tree.getroot()
    for child in root:
        tag = child.tag
        if tag == LEX_REL:
            relation, from_node, to_node, direction, inverse_relation = get_relation_attributes(child.attrib)
            lexunit1 = germanet.lexunits[from_node]
            lexunit2 = germanet.lexunits[to_node]
            lexunit1.relations[LexRel[relation]].add(lexunit2)
            lexunit2.incoming_relations[LexRel[relation]].add(lexunit1)
            if inverse_relation is not None:
                lexunit2.relations[LexRel[inverse_relation]].add(lexunit1)

        elif tag == CON_REL:
            relation, from_node, to_node, dir, inverse_relation = get_relation_attributes(child.attrib)
            synset1 = germanet.synsets[from_node]
            synset2 = germanet.synsets[to_node]
            synset1.relations[ConRel[relation]].add(synset2)
            synset2.incoming_relations[ConRel[relation]].add(synset1)
            if inverse_relation is not None:
                synset2.relations[ConRel[inverse_relation]].add(synset1)
