import re
from typing import Pattern

# exactly two leading underscores, exactly two trailing underscores
# since we enforce one non-underscore after the two leading underscores,
# we put the rest in an optional group
RE_SPECIAL: Pattern = re.compile(r"^__[^_]([\w_]*[^_])?__$")

# at least two leading underscores, at most one trailing underscore
# since we enforce one non-underscore before the last,
# we make the previous characters optional with an asterisk
RE_CLASS_PRIVATE: Pattern = re.compile(r"^__[\w_]*[^_]_?$")

# at most one leading underscore, then whatever
RE_PRIVATE: Pattern = re.compile(r"^_[^_][\w_]*$")

NAME_SPECIAL = ("special", lambda n: bool(RE_SPECIAL.match(n)))
NAME_CLASS_PRIVATE = ("class-private", lambda n: bool(RE_CLASS_PRIVATE.match(n)))
NAME_PRIVATE = ("private", lambda n: bool(RE_PRIVATE.match(n)))
