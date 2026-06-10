class Example(str):
    """
    Represents an example belonging to a lexical unit.

    Example subclasses str so existing code that treated lexunit.examples as a
    list of strings continues to work, while the object also exposes optional
    frame and LLM provenance metadata.
    """

    def __new__(cls, text: str = "", frame: str = None, llm_model: str = None,
                llm_version: str = None, date_created: str = None, edited: bool = False):
        obj = str.__new__(cls, text or "")
        obj._frame = frame
        obj._llm_model = llm_model
        obj._llm_version = llm_version
        obj._date_created = date_created
        obj._edited = edited
        return obj

    def __repr__(self):
        return (f'Example(text={str.__repr__(self)}, frame={self._frame!r}, '
                f'llmModel={self._llm_model!r}, llmVersion={self._llm_version!r}, '
                f'edited={self._edited!r})')

    @property
    def text(self):
        return str(self)

    @property
    def frame(self):
        return self._frame

    @property
    def exframe(self):
        return self._frame

    @property
    def llm_model(self):
        return self._llm_model

    @property
    def llmModel(self):
        return self._llm_model

    @property
    def llm_version(self):
        return self._llm_version

    @property
    def llmVersion(self):
        return self._llm_version

    @property
    def date_created(self):
        return self._date_created

    @property
    def dateCreated(self):
        return self._date_created

    @property
    def edited(self):
        return self._edited