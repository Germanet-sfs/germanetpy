import os
from collections import defaultdict
import progressbar
from utils import parse_xml
from synsetLoader import load_lexunits
from iliLoader import load_ili
from wictionaryLoader import load_wiktionary
from relationLoader import load_relations
from frames import Frames


class Germanet:

    def __init__(self, datadir, addiliRecords=True, addWictionary=True):
        """
        The Germanet object is initialized with the directory where the Germanet data is stored. The data is loaded
        when Germanet is initialized.
        :param datadir: [String] The path to the directory where the Germanet data is stored
        :param addiliRecords: a boolean, denotes whether the iliRecords should also be loaded into the Germanet
        object, default: True
        :param addWictionary: a boolean, denotes whether the wictionary files should also be loaded into the Germanet
        object, default: True
        """
        self.datadir = datadir
        self.addiliRecords = addiliRecords
        self.addWictionary = addWictionary

        # Dictionary: lexunit id - lexunit object
        self._lexunits = {}

        # Dictionary: synset id - synset object
        self._synsets = {}

        # Dictionary: any orthform (all variants) - lexunit id
        self._ortform2lexid = defaultdict(set)

        # Dictionary: main orthform - lexunit id
        self._mainOrtform2lexid = defaultdict(set)

        # Dictionary: lower cased orht form (all variants) - lexunit id
        self._lowercasedform2lexid = defaultdict(set)

        # Dictionary: Wordcategory - set of lexunit ids
        self._wordcat2lexid = defaultdict(set)

        # Dictionary: Wordclass - set of lexunit ids
        self._wordclass2lexid = defaultdict(set)

        # Set if synsets (that are compounds)
        self._compounds = set()

        # Dictionary: Frame - Lexunit objects
        self._frames2lexunits = defaultdict(set)

        # List: wictionary entries
        self._wiktionary_entries = []

        # List: ili Records
        self._ili_records = []

        self.load_data()

        self._frames = Frames(self._frames2lexunits)

    def get_synsets_by_orthform(self, form, ignorecase=False):
        if ignorecase:
            lexunit_ids = self._lowercasedform2lexid[form.lower()]
        else:
            lexunit_ids = self._ortform2lexid[form]
        return [self._lexunits[id].synset() for id in lexunit_ids]

    def get_synsets_by_wordcategory(self, category):
        lexunit_ids = self._wordcat2lexid[category.name]
        return [self._lexunits[id].synset() for id in lexunit_ids]

    def get_synsets_by_wordclass(self, wordclass):
        lexunit_ids = self._wordclass2lexid[wordclass.name]
        return [self._lexunits[id].synset() for id in lexunit_ids]

    def get_synset_by_id(self, id):
        assert id in self._synsets, "the given synset id is not in GermaNet"
        return self._synsets[id]

    def get_lexunit_by_id(self, id):
        assert id in self._lexunits, "the given lexunit id is not in GermaNet"
        return self._lexunits[id]

    def get_lexunits_by_orthform(self, form, ignorecase=False):
        if ignorecase:
            lexunit_ids = self._lowercasedform2lexid[form.lower()]
            return [self._lexunits[id] for id in lexunit_ids]
        lexunit_ids = self._ortform2lexid[form]
        return [self._lexunits[id] for id in lexunit_ids]

    def get_lexunits_by_wordclass(self, wordclass):
        lexunit_ids = self._wordclass2lexid[wordclass.name]
        return [self._lexunits[id] for id in lexunit_ids]

    def get_lexunits_by_wordcategory(self, category):
        lexunit_ids = self._wordcat2lexid[category.name]
        return [self._lexunits[id] for id in lexunit_ids]

    def get_synsets_by_frame(self, frame):
        synset_ids = self._frames2lexunits[frame]
        return [self._synsets[id] for id in synset_ids]

    def get_number_of_senses(self, lexunits):
        senses = [unit.sense for unit in lexunits]
        return max(senses)

    def load_data(self):
        files = os.listdir(self.datadir)
        wikifiles = [f for f in files if "wiktionary" in f and "xml" in f]
        lexentries = [f for f in files if f.startswith("nomen") or f.startswith("verben") or f.startswith("adj")]
        ilifiles = [f for f in files if "interLingua" in f]

        with progressbar.ProgressBar(max_value=len(files)) as bar:
            counter = 0
            for f in lexentries:
                counter += 1
                tree = parse_xml(self.datadir, f)
                load_lexunits(germanet=self, tree=tree)
                bar.update(counter)
            tree = parse_xml(self.datadir, "gn_relations.xml")
            load_relations(germanet=self, tree=tree)
            if self.addWictionary:
                for f in wikifiles:
                    counter += 1
                    tree = parse_xml(self.datadir, f)
                    load_wiktionary(germanet=self, tree=tree)
                    bar.update(counter)
            if self.addiliRecords:
                for f in ilifiles:
                    counter += 1
                    tree = parse_xml(self.datadir, f)
                    load_ili(germanet=self, tree=tree)
                    bar.update(counter)

    def lexunits(self):
        return self._lexunits

    def synsets(self):
        return self._synsets

    def orthform2lexid(self):
        return self._ortform2lexid

    def main_orthform2lexid(self):
        return self._mainOrtform2lexid

    def lowercasedform2lexid(self):
        return self._lowercasedform2lexid

    def wordcat2lexid(self):
        return self._wordcat2lexid

    def wordclass2lexid(self):
        return self._wordclass2lexid

    def compounds(self):
        return self._compounds

    def frames2id(self):
        return self._frames2lexunits

    def wiktionary_entries(self):
        return self._wiktionary_entries

    def ili_records(self):
        return self._ili_records

    def frames(self):
        return self._frames

    def root(self):
        root = self.get_synset_by_id('s51001')
        return root