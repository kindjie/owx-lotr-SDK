import os

import pytest
import requests_mock

from lotr_sdk import exceptions
from lotr_sdk import client
from lotr_sdk import models
from lotr_sdk import options
from lotr_sdk import query

API_KEY = os.environ.get("THE_ONE_API_KEY")

BOOKS = [
    models.Book({
        "_id": "5cf5805fb53e011a64671582",
        "name": "The Fellowship Of The Ring"
    }),
    models.Book({
        "_id": "5cf58077b53e011a64671583",
        "name": "The Two Towers"
    }),
    models.Book({
        "_id": "5cf58080b53e011a64671584",
        "name": "The Return Of The King"
    })
]

CHAPTERS = [
    models.Chapter({
        '_id': '6091b6d6d58360f988133b8b',
        'chapterName': 'A Long-expected Party'
    }),
    models.Chapter({
        '_id': '6091b6d6d58360f988133b8c',
        'chapterName': 'The Shadow of the Past'
    }),
    models.Chapter({
        '_id': '6091b6d6d58360f988133b8d',
        'chapterName': 'Three is Company'
    })
]

MOVIES = [
    models.Movie({
        "_id": "5cd95395de30eff6ebccde56",
        "name": "The Lord of the Rings Series",
        "runtimeInMinutes": 558,
        "budgetInMillions": 281,
        "boxOfficeRevenueInMillions": 2917,
        "academyAwardNominations": 30,
        "academyAwardWins": 17,
        "rottenTomatoesScore": 94
    }),
    models.Movie({
        "_id": "5cd95395de30eff6ebccde57",
        "name": "The Hobbit Series",
        "runtimeInMinutes": 462,
        "budgetInMillions": 675,
        "boxOfficeRevenueInMillions": 2932,
        "academyAwardNominations": 7,
        "academyAwardWins": 1,
        "rottenTomatoesScore": 66.33333333
    }),
    models.Movie({
        "_id": "5cd95395de30eff6ebccde58",
        "name": "The Unexpected Journey",
        "runtimeInMinutes": 169,
        "budgetInMillions": 200,
        "boxOfficeRevenueInMillions": 1021,
        "academyAwardNominations": 3,
        "academyAwardWins": 1,
        "rottenTomatoesScore": 64
    })
]

QUOTES = [
    models.Quote({
        "_id": "5cd96e05de30eff6ebcce9b8",
        "dialog": "Sauron's wrath will be terrible, his retribution swift.",
        "movie": "5cd95395de30eff6ebccde5b",
        "character": "5cd99d4bde30eff6ebccfea0",
        "id": "5cd96e05de30eff6ebcce9b8"
    }),
    models.Quote({
        "_id": "5cd96e05de30eff6ebcce9b9",
        "dialog": "The battle for Helm's Deep is over."
        "The battle for Middle-earth is about to begin.",
        "movie": "5cd95395de30eff6ebccde5b",
        "character": "5cd99d4bde30eff6ebccfea0",
        "id": "5cd96e05de30eff6ebcce9b9"
    }),
    models.Quote({
        "_id": "5cd96e05de30eff6ebcce9ba",
        "dialog": "All our hopes now lie with two little Hobbits...",
        "movie": "5cd95395de30eff6ebccde5b",
        "character": "5cd99d4bde30eff6ebccfea0",
        "id": "5cd96e05de30eff6ebcce9ba"
    })
]

CHARACTER_QUOTES = [
    models.Quote({
        "_id": "5cd96e05de30eff6ebcce80b",
        "dialog": "Now come the days of the King. May they be blessed.",
        "movie": "5cd95395de30eff6ebccde5d",
        "character": "5cd99d4bde30eff6ebccfea0",
        "id": "5cd96e05de30eff6ebcce80b"
    }),
    models.Quote({
        "_id": "5cd96e05de30eff6ebcce82a",
        "dialog": "Hobbits!",
        "movie": "5cd95395de30eff6ebccde5d",
        "character": "5cd99d4bde30eff6ebccfea0",
        "id": "5cd96e05de30eff6ebcce82a"
    }),
    models.Quote({
        "_id": "5cd96e05de30eff6ebcce832",
        "dialog": "Be careful. Even in defeat, Saruman is dangerous.",
        "movie": "5cd95395de30eff6ebccde5d",
        "character": "5cd99d4bde30eff6ebccfea0",
        "id": "5cd96e05de30eff6ebcce832"
    })
]

CHARACTERS = [
    models.Character({
        '_id': '5cd99d4bde30eff6ebccfbbe',
        'height': '',
        'race': 'Human',
        'gender': 'Female',
        'birth': '',
        'spouse': 'Belemir',
        'death': '',
        'realm': '',
        'hair': '',
        'name': 'Adanel',
        'wikiUrl': 'http://lotr.wikia.com//wiki/Adanel'
    }),
    models.Character({
        '_id': '5cd99d4bde30eff6ebccfbbf',
        'height': '',
        'race': 'Human',
        'gender': 'Male',
        'birth': 'Before ,TA 1944',
        'spouse': '',
        'death': 'Late ,Third Age',
        'realm': '',
        'hair': '',
        'name': 'Adrahil I',
        'wikiUrl': 'http://lotr.wikia.com//wiki/Adrahil_I'
    }),
    models.Character({
        '_id': '5cd99d4bde30eff6ebccfbc0',
        'height': '',
        'race': 'Human',
        'gender': 'Male',
        'birth': 'TA 2917',
        'spouse': 'Unnamed wife',
        'death': 'TA 3010',
        'realm': '',
        'hair': '',
        'name': 'Adrahil II',
        'wikiUrl': 'http://lotr.wikia.com//wiki/Adrahil_II'
    })
]

COMPARED_MOVIES = [
    models.Movie({
        "_id": "5cd95395de30eff6ebccde56",
        "name": "The Lord of the Rings Series",
        "runtimeInMinutes": 558,
        "budgetInMillions": 281,
        "boxOfficeRevenueInMillions": 2917,
        "academyAwardNominations": 30,
        "academyAwardWins": 17,
        "rottenTomatoesScore": 94
    }),
    models.Movie({
        "_id": "5cd95395de30eff6ebccde5b",
        "name": "The Two Towers",
        "runtimeInMinutes": 179,
        "budgetInMillions": 94,
        "boxOfficeRevenueInMillions": 926,
        "academyAwardNominations": 6,
        "academyAwardWins": 2,
        "rottenTomatoesScore": 96
    }),
    models.Movie({
        "_id": "5cd95395de30eff6ebccde5c",
        "name": "The Fellowship of the Ring",
        "runtimeInMinutes": 178,
        "budgetInMillions": 93,
        "boxOfficeRevenueInMillions": 871.5,
        "academyAwardNominations": 13,
        "academyAwardWins": 4,
        "rottenTomatoesScore": 91
    })
]


@requests_mock.Mocker(kw="mock")
class TestLotrClientUnit:

    def setup_class(self):
        self.lotr = client.LotrClient(API_KEY)

    def test_init(self, **kwargs):
        with pytest.raises(exceptions.InvalidAPIKeyError):
            client.LotrClient("")

    def test_get_books(self, **kwargs):
        kwargs["mock"].get("https://the-one-api.dev/v2/book",
                           json={"docs": [{
                               "_id": "1"
                           }]})
        assert self.lotr.get_books() == [models.Book({"_id": "1"})]

    def test_get_chapters(self, **kwargs):
        kwargs["mock"].get("https://the-one-api.dev/v2/book/1/chapter",
                           json={"docs": [{
                               "_id": "1"
                           }]})
        assert self.lotr.get_chapters("1") == [models.Chapter({"_id": "1"})]
        kwargs["mock"].get("https://the-one-api.dev/v2/book/1/chapter",
                           json={"docs": [{
                               "_id": "1"
                           }]})
        assert self.lotr.get_chapters("1") == [models.Chapter({"id": "1"})]

    def test_get_chapter(self, **kwargs):
        kwargs["mock"].get("https://the-one-api.dev/v2/chapter/1",
                           json={"docs": [{
                               "_id": "1"
                           }]})
        assert self.lotr.get_chapter("1") == models.Chapter({"_id": "1"})

    def test_get_movies(self, **kwargs):
        kwargs["mock"].get("https://the-one-api.dev/v2/movie",
                           json={"docs": [{
                               "_id": "1"
                           }]})
        assert self.lotr.get_movies() == [models.Movie({"_id": "1"})]

    def test_get_movie(self, **kwargs):
        kwargs["mock"].get("https://the-one-api.dev/v2/movie/1",
                           json={"docs": [{
                               "_id": "1"
                           }]})
        assert self.lotr.get_movie("1") == models.Movie({"_id": "1"})

    def test_get_quotes(self, **kwargs):
        kwargs["mock"].get("https://the-one-api.dev/v2/movie/1/quote",
                           json={"docs": [{
                               "_id": "1"
                           }]})
        assert self.lotr.get_quotes("1") == [models.Quote({"_id": "1"})]

    def test_get_quote(self, **kwargs):
        kwargs["mock"].get("https://the-one-api.dev/v2/quote/1",
                           json={"docs": [{
                               "_id": "1"
                           }]})
        assert self.lotr.get_quote("1") == models.Quote({"_id": "1"})

    def test_get_characters(self, **kwargs):
        kwargs["mock"].get("https://the-one-api.dev/v2/character",
                           json={"docs": [{
                               "_id": "1"
                           }]})
        assert self.lotr.get_characters() == [models.Character({"_id": "1"})]

    def test_get_character(self, **kwargs):
        kwargs["mock"].get("https://the-one-api.dev/v2/character/1",
                           json={"docs": [{
                               "_id": "1"
                           }]})
        assert self.lotr.get_character("1") == models.Character({"_id": "1"})

    def test_get_character_quotes(self, **kwargs):
        kwargs["mock"].get("https://the-one-api.dev/v2/character/1/quote",
                           json={"docs": [{
                               "_id": "1"
                           }]})
        assert self.lotr.get_character_quotes("1") == [
            models.Quote({"_id": "1"})
        ]


class TestLotrClientIntegration:
    BOOK_ID = "5cf5805fb53e011a64671582"
    CHAPTER_ID = "6091b6d6d58360f988133b8b"
    MOVIE_ID = "5cd95395de30eff6ebccde5b"
    CHARACTER_ID = "5cd99d4bde30eff6ebccfea0"
    QUOTE_ID = "5cd96e05de30eff6ebcce9ba"

    def setup_class(self):
        self.lotr = client.LotrClient(API_KEY)
        self.params = query.LotrQueryBuilder().add(query.Limit(3))

    def test_get_books(self):
        expected_response = BOOKS[:3]
        assert self.lotr.get_books(self.params.build()) == expected_response

    def test_get_book(self):
        expected_response = BOOKS[0]

        assert self.lotr.get_book(self.BOOK_ID,
                                  self.params.build()) == expected_response

    def test_get_chapters(self):
        expected_response = CHAPTERS[:3]
        assert self.lotr.get_chapters(self.BOOK_ID,
                                      self.params.build()) == expected_response

    def test_get_chapter(self):
        expected_response = CHAPTERS[0]

        assert self.lotr.get_chapter(self.CHAPTER_ID) == expected_response

    def test_get_movies(self):
        expected_response = MOVIES[:3]
        assert self.lotr.get_movies(self.params.build()) == expected_response

    def test_get_movie(self):
        expected_response = MOVIES[0]
        assert self.lotr.get_movie(self.MOVIE_ID) == expected_response

    def test_get_quotes(self):
        expected_response = QUOTES[:3]
        assert self.lotr.get_quotes(self.MOVIE_ID,
                                    self.params.build()) == expected_response

    def test_get_quote(self):
        expected_response = QUOTES[0]
        assert self.lotr.get_quote(self.QUOTE_ID) == expected_response

    def test_get_characters(self):
        expected_response = CHARACTERS[:3]
        assert self.lotr.get_characters(
            self.params.build()) == expected_response

    def test_get_character(self):
        expected_response = CHARACTERS[0]
        assert self.lotr.get_character(self.CHARACTER_ID) == expected_response

    def test_get_character_quotes(self):
        expected_response = CHARACTER_QUOTES[:3]
        assert self.lotr.get_character_quotes(
            self.CHARACTER_ID, self.params.build()) == expected_response

    def test_sort_params(self):
        self.params.add(query.Sort("name"))

        assert self.lotr.get_books(self.params.build()) == BOOKS[:3]

    def test_compare_params(self):
        self.params.add(
            query.Compare("academyAwardWins", options.Comparator.GREATER_THAN,
                          1))

        assert self.lotr.get_movies(self.params.build()) == COMPARED_MOVIES[:3]


class TestLotrQueryBuilder:

    def setup_method(self):
        self.query = query.LotrQueryBuilder()

    def test_sort(self):
        self.query.add(query.Sort("name"))
        assert self.query.build() == {options.QueryOption.SORT: "name:asc"}

    def test_sort_asc(self):
        self.query.add(query.Sort("name", options.SortOrder.ASCENDING))
        assert self.query.build() == {options.QueryOption.SORT: "name:asc"}

    def test_sort_desc(self):
        self.query.add(query.Sort("name", options.SortOrder.DESCENDING))
        assert self.query.build() == {options.QueryOption.SORT: "name:desc"}

    def test_sort_multiple(self):
        with pytest.raises(exceptions.InvalidClauseError):
            self.query.add(query.Sort("name"))
            self.query.add(query.Sort("age", options.SortOrder.DESCENDING))

    def test_page(self):
        page = query.Page(10)
        self.query.add(page)
        assert self.query.build() == {options.QueryOption.PAGE: 10}

    def test_limit(self):
        self.query.add(query.Limit(10))
        assert self.query.build() == {options.QueryOption.LIMIT: 10}

    def test_offset(self):
        self.query.add(query.Offset(10))
        assert self.query.build() == {options.QueryOption.OFFSET: 10}

    def test_match(self):
        self.query.add(query.Match("name", "Gandalf"))
        assert self.query.build() == {
            options.QueryOption.FILTER: ["name=Gandalf"]
        }

    def test_match_multiple(self):
        self.query.add(query.Match("name", "Gandalf"))
        self.query.add(query.Match("age", 100))
        assert self.query.build() == {
            options.QueryOption.FILTER: ["name=Gandalf", "age=100"]
        }

    def test_match_multiple_same_key(self):
        with pytest.raises(exceptions.InvalidClauseError):
            self.query.add(query.Match("name", "Gandalf"))
            self.query.add(query.Match("name", "Sauron"))
