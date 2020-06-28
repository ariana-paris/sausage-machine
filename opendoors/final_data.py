from dataclasses import dataclass


@dataclass
class Author:
    id: int
    name: str
    email: str
    imported: bool
    do_not_import: bool
    to_delete: bool

    def od_insert_sql(self):
        """Insert author into temp table"""
        return """
        INSERT INTO authors
        (id, name, email, imported, do_not_import, to_delete)
        VALUES {}, {}, {}, {}, {}, {}
        """.format(
            self.id, self.name, self.email, self.imported,
            self.do_not_import, self.to_delete)


@dataclass
class Chapter:
    id: int
    position: int
    title: str
    author_id: int
    text: str
    date: str
    story_id: int
    notes: str
    url: str

    def od_insert_sql(self):
        """Insert chapter into temp table"""
        return """
        INSERT INTO chapters
        (id, title, author_id, text, date, story_id, notes, url)
        VALUES {}, {}, {}, {}, {}, {}, {}, {}
        """.format(
            self.id, self.title, self.author_id, self.text, self.date,
            self.story_id, self.notes, self.url)


@dataclass
class Item:
    id: str
    title: str
    summary: str
    notes: str
    author_id: str
    rating: str
    date: str
    updated: str
    categories: str
    tags: str
    warnings: str
    fandoms: str
    characters: str
    relationships: str
    url: str
    imported: bool
    do_not_import: bool
    ao3_url: str
    language_code: str


@dataclass
class Story(Item):
    coauthor_id: int

    def od_insert_sql(self):
        """Insert story into temp table"""
        return """
        INSERT INTO stories
        (id, title, summary, notes, author_id, rating, date, updated,
        categories, tags, warnings, fandoms, characters, relationships,
        url, imported, do_not_import, ao3_url, language_code, coauthor_id)
        VALUES {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {},
        {}, {}, {}, {}, {}, {}
        """.format(
            self.id, self.title, self.summary, self.notes, self.author_id,
            self.rating, self.date, self.updated, self.categories,
            self.tags, self.warnings, self.fandoms, self.characters,
            self.relationships, self.url, self.imported, self.do_not_import,
            self.ao3_url, self.language_code, self.coauthor_id)


@dataclass
class StoryLink(Item):
    broken_link: bool

    def od_insert_sql(self):
        """Insert story into temp table"""
        return """
        INSERT INTO story_links
        (id, title, summary, notes, author_id, rating, date, updated,
        categories, tags, warnings, fandoms, characters, relationships,
        url, imported, do_not_import, ao3_url, language_code, broken_link)
        VALUES {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {},
        {}, {}, {}, {}, {}, {}
        """.format(
            self.id, self.title, self.summary, self.notes, self.author_id,
            self.rating, self.date, self.updated, self.categories,
            self.tags, self.warnings, self.fandoms, self.characters,
            self.relationships, self.url, self.imported, self.do_not_import,
            self.ao3_url, self.language_code, self.broken_link)
