class Person:
    def __init__(self, name, scopusId):
        self.name = name
        self.scopusId = scopusId


class PersonFullInfo(Person):
    def __init__(self, person, document_count, cited_by_count, citation_count):
        super().__init__(person.name, person.scopusId)
        self.document_count = document_count
        self.cited_by_count = cited_by_count
        self.citation_count = citation_count
