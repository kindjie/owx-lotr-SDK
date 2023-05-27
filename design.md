# SDK Design Decisions

- SDK should not deviate drastically from the REST API. This allows developers to draw analogies with
  the documented REST API.
- Developers using an IDE or text editor with LSP should have clear autocomplete support and
  supporting documentation.
- Python type annotations should be provided to support static analysis.

## Core

The API revolves around two core classes:

1.  lotr_sdk.client.LotrClient
2.  lotr_sdk.query.LotrQueryBuilder

LotrClient retains a session, and mimics the REST API. LotrQueryBuilder provides an idiomatic
"ORM-like" interface for constructing query parameters. It allows for pagination, sorting, and
filtering of results.

### LotrClient

The client uses the `requests` package to maintain a session to fetch query results using GET requests.

### LotrQueryBuilder

The `LotrQueryBuilder` class to build queries for the LotR API.

This class provides methods to add various query parameters like page,
limit, offset, sort, and filter.

### Examples

```python
    query_builder = LotrQueryBuilder()
    query_builder.paginate(page=1, limit=10)
    query_builder.add_sort(query.Sort("title", SortOrder.DESCENDING))
    params = query_builder.build()

    query_builder = LotrQueryBuilder() \
        .paginate(page=1, limit=10) \
        .add_sort(query.Sort("title", SortOrder.DESCENDING))
    params = query_builder.build()
```

## Support

There are also several supporting modules:

1.  `lotr_sdk.exceptions` contains custom errors.
2.  `lotr_sdk.models` contains types used in `LotrClient` fetch results.
3.  `lotr_sdk.options` contains enumeration options used in the `LotrQueryBuilder`.

## Process

1. The skeleton of the client and query builder was written first.
2. Next, a quick pass of unit tests was created to try the design.
3. Client and query builder completed up to basic functionality.
4. Then, documentation using Python docstrings was written for key parts.
5. A quick pass of docstrings was generated using the `text-davinci-003` model with the following
   parameters:
   - Temperature: 1
   - Maximum Length: 256
   - Top P: 1
   - Frequency Penalty: 0
   - Presence Penalty: 0
   - Best of: 3
   - And prompts similar to the following:
   > ```python
   > class Log:
   >     def __init__(self, path):
   >         dirname = os.path.dirname(path)
   >         os.makedirs(dirname, exist_ok=True)
   >         f = open(path, "a+")
   >
   >         # Check that the file is newline-terminated
   >         size = os.path.getsize(path)
   >         if size > 0:
   >             f.seek(size - 1)
   >             end = f.read(1)
   >             if end != "\n":
   >                 f.write("\n")
   >         self.f = f
   >         self.path = path
   >
   >     def log(self, event):
   >         event["_event_id"] = str(uuid.uuid4())
   >         json.dump(event, self.f)
   >         self.f.write("\n")
   >
   >     def state(self):
   >         state = {"complete": set(), "last": None}
   >         for line in open(self.path):
   >             event = json.loads(line)
   >             if event["type"] == "submit" and event["success"]:
   >                 state["complete"].add(event["id"])
   >                 state["last"] = event
   >         return state
   > ```
   >
   > """
   >
   > Here's how an expert API developer would document the class using docstrings:
   >
   > ```python
   > class Log:
   >     """A class to represent a Log file. This class is used to write JSON
   >     formatted logs to a file.
   >
   >     Args:
   >         - path (str):
   >             The path of the request.
   >
   >     Examples:
   > ```
6. Generated documentation was then edited.
7. Then the design, implementation, tests, and documentation was iterated on until "good enough".
