ya\_jsonapi
===========

`ya_jsonapi` is yet another implementation of jsonapi client for Python. I
started writing this library as I wanted to have a library that supports asyncio
and gives explicit control over performed http requests, and writing one from
scratch appears to be easier than than modifying any of the existing ones.

Design goals
============
* Decoupling from the fetch process. Only generate links and process received
  data, actual data fetching (any any exception handling) should be implemented
  by the user. `requests` or `aiohttp` implementations should be trivial.
* Explicit control over requests. No implicit ORM, explicit fetching and
  posting data. Convenience tools for ORM-like traversal of fetched data.
* Access to keyed attributes via dicts, no \_\_getattr\_\_ magic, to keep things
  simple and unambiguous.

Roadmap
=======

No target dates. Hopefully won't run out of motivation before the library is at
least partially complete.

Absolute basics
---------------

1. (__DONE__) Parsing json responses. Translating them into exactly
   corresponding entities - Document, (resource) Object, Relationship etc.
   Wherever the spec has arbitrary dicts, we should use dict access only,
   attribute acces would be incomplete and unnecessary.
   
   Validate jsonapi with its jsonspec first, then turn it into a Document
   object with attributes forming a tree analogous to the response.

2. Performing requests. Do not offer code that fetches things for us, instead
   only offer code that generates the URL. Classes that prepare parameters for
   filtering, inclusion and pagination, allow subclassing to generate custom
   queries. Combined with actual addresses like usual GET parameters.
   TODO: figure out what to do with ContentType/other requirements.


First improvements
------------------

3. Introduce Context class. Context is a collection of jsonapi Objects, it's
   used to keep results of multiple related queries together. All objects from
   a request are put in a context (existing one if we pass it in, newly created
   one if we don't). Context is used to access objects based on object
   identifiers.

4. Shortcuts in the Document. Allow direct attribute access on objects and
   relationships where applicable to access fields and related objects directly.
   Use the Context for that (each object should know which context it belongs
   to).

More improvments
----------------

5. Allow specifying a Getter class for the Context. The class is used by Context
   to fetch data through a get method, however it sees fit and with whatever
   exceptions.

5. Creating links out of objects / relationships. Logic for figuring out which
   link is the 'self' link of the object. Possibly a helper function on an
   object to get the document and put it in the context if it's not an error.

6. Introduce pagination objects. If a link collection supports pagination, you
   can make a Page out of it. Once created, a page is a list of object
   identifiers (so you can always use it to show the same items, even when you
   only have the context without the document). Give them a 'next' and
   'previous' link that you can use to fetch appropriate documents (and perhaps
   also analogous pages inside them? Seems non-trivial).

7. Async calls. Add async\_get to context getter, give functions that use the
   getter async versions (perhaps via a parameter on the Context?)

Even more improvements
----------------------

8. Type checking support. Allow to define types of objects, with allowed names
   of fields and relations. Give a different error if trying to access a field
   ot specified in the type.

9. Default endpoints for paths, perhaps? In case an object does not have a
   'self' link, allow for checking a default endpoint of its type (via binding
   to the Context, probably).

10. Creating, updating and deleting resources. Keep it simple - no ORM. Creating
    / updating happens via lists of partially filled in objects - what's in them
    gets turned into json and sent out.
    Updating relationships uses identifiers only. Deleting takes nothing, just a
    link.

11. Expose adding / updating / deleting through objects only, with appropriate
    functions (add, update, delete etc.). We don't always want to update the
    whole object state, so figure out a way (via copying, or attributes) how to
    limit that.
