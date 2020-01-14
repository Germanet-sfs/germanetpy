import fastenum
from collections import defaultdict


class LexRel(fastenum.Enum):
    has_synonym = 'has_synonym'
    has_antonym = 'has_antonym'
    has_pertainym = 'has_pertainym'
    has_participle = 'has_participle'
    has_active_usage = 'has_active_usage'
    has_occasion = 'has_occasion'
    has_attribute = 'has_attribute'
    has_appearance = 'has_appearance'
    has_construction_method = 'has_construction_method'
    has_container = 'has_container'
    is_container_for = 'is_container_for'
    has_consistency_of = 'has_consistency_of'
    has_component = 'has_component'
    has_owner = 'has_owner'
    is_owner_of = 'is_owner_of'
    has_function = 'has_function'
    has_manner_of_functioning = 'has_manner_of_functioning'
    has_origin = 'has_origin'
    has_production_method = 'has_production_method'
    has_content = 'has_content'
    has_no_property = 'has_no_property'
    has_habitat = 'has_habitat'
    has_location = 'has_location'
    is_location_of = 'is_location_of'
    has_measure = 'has_measure'
    is_measure_of = 'is_measure_of'
    has_material = 'has_material'
    has_member = 'has_member'
    is_member_of = 'is_member_of'
    has_diet = 'has_diet'
    is_diet_of = 'is_diet_of'
    has_eponym = 'has_eponym'
    has_user = 'has_user'
    has_product = 'has_product'
    is_product_of = 'is_product_of'
    has_prototypical_holder = 'has_prototypical_holder'
    is_prototypical_holder_for = 'is_prototypical_holder_for'
    has_prototypical_place_of_usage = 'has_prototypical_place_of_usage'
    has_relation = 'has_relation'
    has_raw_product = 'has_raw_product'
    has_other_property = 'has_other_property'
    is_storage_for = 'is_storage_for'
    has_specialization = 'has_specialization'
    has_part = 'has_part'
    is_part_of = 'is_part_of'
    has_topic = 'has_topic'
    is_caused_by = 'is_caused_by'
    is_cause_for = 'is_cause_for'
    is_comparable_to = 'is_comparable_to'
    has_usage = 'has_usage'
    has_result_of_usage = 'has_result_of_usage'
    has_purpose_of_usage = 'has_purpose_of_usage'
    has_goods = 'has_goods'
    has_time = 'has_time'
    is_access_to = 'is_access_to'
    has_ingredient = 'has_ingredient'
    is_ingredient_of = 'is_ingredient_of'


class OrthFormVariant(fastenum.Enum):
    orthForm = 'orthForm'
    orthVar = 'orthVar'
    oldOrthForm = 'oldOrthForm'
    oldOrthVar = 'oldOrthVar'


class Lexunit:
    """
    This class holds the lexical unit object of GermaNet. A lexical unit is a concrete word that is part of a synset.
    """

    def __init__(self, id, synset, sense, source, named_entity, style_marking, artificial,
                 compound_info=None, orthform=None, old_orthform=None, orthvar=None, old_orthvar=None):
        """
        :param id: A unique String identifier
        :param synset: The lexical unit belongs to one (and only one) synset object.
        :param sense: The sense number of the lexical unit
        :param source:
        :param named_entity: True if this unit is a named entity, otherwise False
        :param style_marking: True if the term is colloquial
        :param artificial: true if this term was introduced into GermaNet as an artificial node (e.g to construct the
        adjective hierachy, the term "zeitspezifisch" was introduced
        :param compound_info: a compound info object if the lexical unit is a compound
        :param orthform: the main orthform (that is mainly used in today's written German)
        :param old_orthform: The orthform that was used in written German in former times
        :param orthvar: The orth variant (e.g Delfin / Delphin are both legal orth variants)
        :param old_orthvar: The orth variant that was used in written German in former times
        """
        self._id = id
        self._synset = synset
        self._sense = sense

        self._orthform = orthform
        self._orthvar = orthvar
        self._old_orthform = old_orthform
        self._old_orthvar = old_orthvar

        self._source = source
        self._named_entity = named_entity
        self._styleMarking = style_marking
        self._artificial = artificial

        self._frames = []
        self._frames2examples = defaultdict(set)
        self._examples = []
        self._ili_records = []
        self._wiktionary_paraphrases = []
        self._compound_info = compound_info

        self._relations = defaultdict(set)
        self._incoming_relations = defaultdict(set)

    def get_orthform_variant(self, orthform_variant):
        """
        :param orthform_variant: one of the four orthform_variants
        :return: the string of the requested orthform variant or the main orthform, if the requested orthform doesn't
        exist.
        """
        if orthform_variant == OrthFormVariant.oldOrthVar:
            return self.old_orthvar
        elif orthform_variant == OrthFormVariant.oldOrthForm and self.old_orthform:
            return self.old_orthform
        elif orthform_variant == OrthFormVariant.orthVar and self.orthvar:
            return self.orthvar
        else:
            return self.orthform

    def __repr__(self):
        return f'Lexunit(id={self._id}, orthform={self._orthform}, synset_id={self._synset.id})'

    def get_all_orthforms(self):
        """
        :return: A list<String> of all existing orthform variants of the current lexunit.
        """
        forms = set()
        for orthformvariant in OrthFormVariant:
            form = self.get_orthform_variant(orthformvariant)
            if form:
                forms.add(form)
        return forms

    @property
    def id(self):
        return self._id

    @property
    def synset(self):
        return self._synset

    @property
    def sense(self):
        return self._sense

    @property
    def orthform(self):
        return self._orthform

    @property
    def orthvar(self):
        return self._orthvar

    @property
    def old_orthform(self):
        return self._old_orthform

    @property
    def old_orthvar(self):
        return self._old_orthvar

    @property
    def frames(self):
        return self._frames

    @property
    def examples(self):
        return self._examples

    @property
    def ili_records(self):
        return self._ili_records

    @property
    def frames2examples(self):
        return self._frames2examples

    @property
    def wiktionary_paraphrases(self):
        return self._wiktionary_paraphrases

    @property
    def compound_info(self):
        return self._compound_info

    @property
    def relations(self):
        return self._relations

    @property
    def incoming_relations(self):
        return self._incoming_relations
