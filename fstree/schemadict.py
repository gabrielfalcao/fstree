from __future__ import unicode_literals

# import traceback

from decimal import Decimal
from collections import defaultdict
from collections import OrderedDict


class InvalidDictionarySchema(Exception):
    pass


class ValueExpectation(object):
    def __init__(self, value):
        self.value = value


class ChildrenFinder(object):
    def __init__(self, members):
        self.members = members

    def traverse(self, parent):
        value = parent
        for key in self.members:
            value = value.get(key)

        return value

    def humanize(self):
        return b'[{}]'.format(']['.join(self.members))


class OpaqueExtractor(object):
    _handlers = OrderedDict()

    @classmethod
    def add_handler(cls, TypeClass, callback=None):
        cls._handlers[TypeClass] = callback or getattr

    @classmethod
    def get_value_handler(cls, value):
        TypeClass = type(value)
        return cls._handlers.get(TypeClass, None)

    @classmethod
    def get_dict(cls, value, path):
        extract = cls.get_value_handler(value)
        if not extract:
            return {}

        return extract(value, path)


class InvalidationReporter(object):
    def __init__(self, target, logger):
        self.target = target
        self.logger = logger
        self.messages = []

    def log(self, message, exception=None):
        self.messages.append(message)
        if not self.logger:
            return

        if exception:
            self.logger.exception(message)
        else:
            self.logger.warning(message)

    def invalidation(self, reason_template, actual_value, finder):
        expected = finder.traverse(self.schema)

        context = {
            b'target': self.target,
            b'path': finder.humanize(),
            b'actual': ValueExpectation(actual_value),
            b'expected': expected,
        }
        reason_message = reason_template.format(**context)
        self.log(reason_message)

    def invalid(self, actual_value, path_members):
        finder = ChildrenFinder(path_members)
        reason_template = (
            b'expected value under {path} to be a '
            '{expected.value} but is {actual.value}'
        )
        return self.invalidation(reason_template, actual_value, finder)


class schemadict(object):
    """simple DSL for declaring "schemas" for python dictionaries.

    features:
    =========

    - keys must be basestrings
    - easily build systems without need to declare complex opaque
      types with custom serialization and validation mechanisms.

    - easily validate API requests without need to resort to
      JSON-schema; or
    - use ``schemadict.from_json_schema()``
    - validate native python dictionaries
    - multiple flexible ways to handle _invalidations_:
      - **`True`/`False`**
      - raising an exception
      - automatic logging with custom level and full traceback.
      - meaningful error messages in all situations
      - callbacks
    - provides "extractor" DSL to simplify and automate serialization
      of opaque native types.
    - recursive validation (aka _nested schemadict_ declarations)
    - AST-based key-evaluation to prevent use of ``eval()`` exploitation

    syntax:
    =======

    - the schema declaration is a dict itself
    - each _key_ must be a primitive type:
      - bool
      - basestring (bytes, str, unicode)
      - int, float, long, complex, Decimal
      - set, list, tuple
    - except for cases below:
      - ``b"__name__"`` **must** have a **unique name**
    - each _value_ must be an instance of``type``:
      - any _primitive_ type
      - any opaque type to which an _extractor_ was previously declared.
    - except for _nested schemadict_ declarations.

    example:
    --------

    .. TODO::

    """

    def __init__(self, declaration, logger=None, raise_error=False, exception=None):
        self.schema_declaration = declaration
        self.logger = logger
        self.raise_error = raise_error
        self.exception = exception if exception is not None else InvalidDictionarySchema

    def ponder_child(self, path, value):
        raise NotImplementedError()
        # return True, value, path

    def ponder_string(self, path, value):
        valid = isinstance(value, basestring)
        return valid, value, path

    def ponder_number(self, path, value):
        valid = isinstance(value, (int, float, long, complex, Decimal))
        return valid, value, path

    def ponder_iterable(self, path, value):
        valid = isinstance(value, (set, list, tuple))
        return valid, value, path

    def ponder_opaque(self, path, value):
        valid = OpaqueExtractor.familiar_with(value)
        value = OpaqueExtractor.get_dict(value, path)
        return valid, value, path

    def ponder_none(self, path, value):
        valid = value is None
        return valid, value, path

    def validate(self, target):
        report = InvalidationReporter(target, self.logger)

        if not isinstance(target, dict):
            report.target(target)

        for key, value in target.iteritems():
            path = [key]

            # test child first, so the first node of the validation
            # tree is a branch, just because

            yield self.validate_member(key, value, path, report)

    def validate_member(self, key, value, path, report):

        TYPE_HANDLERS = [
            ((dict, OrderedDict, defaultdict), self.ponder_child),
            ((type(None), ), self.ponder_none),
            ((basestring, ), self.ponder_string),
            ((int, float, long), self.ponder_number),
            ((set, list, tuple), self.ponder_iterable),
            ((object, ), self.ponder_opaque),
        ]

        for bases, handler in TYPE_HANDLERS:
            if isinstance(value, bases):
                break

        valid, actual_value, path = handler(path, value)

        if not valid:
            report.invalid(value, path, actual_value)

        yield {
            'valid': valid,
            'actual_value': actual_value,
            'path': path,
        }
