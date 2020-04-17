import os
from collections import defaultdict
from tqdm import trange
from germanetpy.utils import parse_xml
from germanetpy.synsetLoader import load_lexunits
from germanetpy.iliLoader import load_ili
from germanetpy.wictionaryLoader import load_wiktionary
from germanetpy.relationLoader import load_relations
from germanetpy.frames import Frames


class Germanet:

    def __init__(self, datadir: str, add_ilirecords: bool = True, add_wictionary: bool = True):
        """
        The GermaNet object is initialized with the directory where the GermaNet data is stored. The data is loaded
        when GermaNet is initialized.
        :param datadir: The path to the directory where the GermaNet data is stored
        :param addiliRecords: a boolean, denotes whether the iliRecords should also be loaded into the GermaNet
        object, default: True
        :param addWictionary: a boolean, denotes whether the wictionary files should also be loaded into the GermaNet
        object, default: True
        """
        self._datadir = datadir
        self._add_ilirecords = add_ilirecords
        self._add_wictionary = add_wictionary

        # Dictionary: lexunit id - lexunit object
        self._lexunits = {}

        # Dictionary: synset id - synset object
        self._synsets = {}

        # Dictionary: any orthform (all variants) - lexunit id
        self._orthform2lexid = defaultdict(set)

        # Dictionary: main orthform - lexunit id
        self._mainOrtform2lexid = defaultdict(set)

        # Dictionary: lower cased orthographic form (all variants) - lexunit id
        self._lowercasedform2lexid = defaultdict(set)

        # Dictionary: Wordcategory - set of lexunit ids
        self._wordcat2lexid = defaultdict(set)

        # Dictionary: Wordclass - set of lexunit ids
        self._wordclass2lexid = defaultdict(set)

        # Set of synsets (that are compounds)
        self._compounds = set()

        # Dictionary: Frame - Lexunit objects
        self._frames2lexunits = defaultdict(set)

        # List: wictionary entries
        self._wiktionary_entries = []

        # List: ili Records
        self._ili_records = []

        # the Frames object, storing all frame information from GermaNet
        self._frames = Frames(self._frames2lexunits)

        # load data when GermaNet is initialized
        self._load_data()

    def get_synsets_by_orthform(self, form: str, ignorecase: bool = False) -> list:
        """
        This method returns a list of synsets that match the given input search string
        :param form: a word that can be looked up in the GermaNet
        :param ignorecase: whether the case of the word should be ignored (default = False)
        :return: a list of synsets
        """
        if ignorecase:
            form = form.lower()
            lexunit_ids = self.lowercasedform2lexid[form]
        else:
            lexunit_ids = self.orthform2lexid[form]
        return [self.lexunits[id].synset for id in lexunit_ids]

    def get_synsets_by_wordcategory(self, category) -> list:
        """
        Returns a list of synsets that belong to the specified word category
        :type category: WordCategory
        :param category: The word category of interest
        :return: A list of Synsets that belong to the specified word category
        """
        lexunit_ids = self.wordcat2lexid[category.name]
        return [self.lexunits[id].synset for id in lexunit_ids]

    def get_synsets_by_wordclass(self, wordclass) -> list:
        """
        Returns a list of synsets that belong to the specified word class
        :type wordclass: WordClass
        :param wordclass: The word category of interest
        :return: A list of Synsets that belong to the specified word class
        """
        lexunit_ids = self.wordclass2lexid[wordclass.name]
        return [self.lexunits[id].synset for id in lexunit_ids]

    def get_synset_by_id(self, id: str):
        """
        Returns a Synset by a specified identifier (if that exists, otherwise raises an Error)
        :rtype: Synset
        :param id: a Synset identifier
        :return: The matching Synset object
        """
        assert id in self.synsets, "the given Synset id is not in GermaNet"
        return self.synsets[id]

    def get_lexunit_by_id(self, id: str):
        """
        Returns a lexical unit by a specified identifier (if that exists, otherwise raises an Error)
        :rtype: Lexunit
        :param id: a Lexunit identifier
        :return: The matching Lexunit object
        """
        assert id in self.lexunits, "the given lexical unit id is not in GermaNet"
        return self.lexunits[id]

    def get_lexunits_by_orthform(self, form: str, ignorecase: bool = False) -> list:
        """
        This method returns a list of lexical units that match the given input search string
        :param form: a word that can be looked up in the GermaNet
        :param ignorecase: whether the case of the word should be ignored (default = False)
        :return: a list of lexical units that match the given input query
        """
        if ignorecase:
            form = form.lower()
            lexunit_ids = self.lowercasedform2lexid[form]
            return [self.lexunits[id] for id in lexunit_ids]
        lexunit_ids = self.orthform2lexid[form]
        return [self.lexunits[id] for id in lexunit_ids]

    def get_lexunits_by_wordclass(self, wordclass) -> list:
        """
        Returns a list of lexical units that belong to the specified word class
        :type wordclass: WordClass
        :param wordclass: The word category of interest
        :return: A list of lexical units that belong to the specified word class
        """
        lexunit_ids = self.wordclass2lexid[wordclass.name]
        return [self.lexunits[id] for id in lexunit_ids]

    def get_lexunits_by_wordcategory(self, category) -> list:
        """
        Returns a list of lexical units that belong to the specified word category
        :type category: WordCategory
        :param category: The word category of interest
        :return: A list of lexical units that belong to the specified word category
        """
        lexunit_ids = self.wordcat2lexid[category.name]
        return [self.lexunits[id] for id in lexunit_ids]

    def get_synsets_by_frame(self, frame: str) -> list:
        """
        Returns a list of Synsets that match a specified frame
        :param frame: a frame that describes the argument structure of a verb (e.g. 'NN.AN' specifies that a
        verb can take a subject and accusative object as arguments.)
        :return: a list of Synsets that match the given frame. If the frame is not valid an Assertion
        Error will be raised
        """
        assert frame in self.frames2lexunits, "the specified frame is not in GermaNet"
        synset_ids = self.frames2lexunits[frame]
        return [self.synsets[id] for id in synset_ids]

    def _load_data(self):
        """
        Protected method to load the GermaNet data. The Data has to be stored in self.datadir.
        """
        files = os.listdir(self.datadir)
        wikifiles = [f for f in files if "wiktionary" in f and "xml" in f]
        lexentries = [f for f in files if f.startswith("nomen") or f.startswith("verben") or f.startswith("adj")]
        ilifiles = [f for f in files if "interLingua" in f]
        pbar = trange(100, desc='Load GermaNet data...', leave=True)
        for i in range(len(lexentries)):
            f = lexentries[i]
            tree = parse_xml(self.datadir, f)
            load_lexunits(germanet=self, tree=tree)
            pbar.update(100 / len(lexentries))
        tree = parse_xml(self.datadir, "gn_relations.xml")
        load_relations(germanet=self, tree=tree)
        pbar.close()
        pbar = trange(100, desc='Load Wictionary data...', leave=True)
        if self.add_wictionary:
            for i in range(len(wikifiles)):
                tree = parse_xml(self.datadir, wikifiles[i])
                load_wiktionary(germanet=self, tree=tree)
                pbar.update(100 / len(wikifiles))
        pbar.close()
        pbar = trange(100, desc='Load Ili records...', leave=True)
        if self.add_ilirecords:
            for i in range(len(ilifiles)):
                tree = parse_xml(self.datadir, ilifiles[i])
                load_ili(germanet=self, tree=tree)
                pbar.update(100 / len(ilifiles))
        pbar.close()

    @property
    def lexunits(self):
        return self._lexunits

    @property
    def synsets(self):
        return self._synsets

    @property
    def orthform2lexid(self):
        return self._orthform2lexid

    @property
    def mainOrtform2lexid(self):
        return self._mainOrtform2lexid

    @property
    def lowercasedform2lexid(self):
        return self._lowercasedform2lexid

    @property
    def wordcat2lexid(self):
        return self._wordcat2lexid

    @property
    def wordclass2lexid(self):
        return self._wordclass2lexid

    @property
    def compounds(self):
        return self._compounds

    @property
    def frames2lexunits(self):
        return self._frames2lexunits

    @property
    def wiktionary_entries(self):
        return self._wiktionary_entries

    @property
    def ili_records(self):
        return self._ili_records

    @property
    def frames(self):
        return self._frames

    @property
    def root(self):
        root = self.get_synset_by_id('s51001')
        return root

    @property
    def datadir(self):
        return self._datadir

    @property
    def add_ilirecords(self):
        return self._add_ilirecords

    @property
    def add_wictionary(self):
        return self._add_wictionary
