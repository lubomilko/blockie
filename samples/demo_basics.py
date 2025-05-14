# pylint: disable = missing-module-docstring, missing-class-docstring, missing-function-docstring
import sys

sys.path.insert(0, f"{sys.path[0]}/../src")

import blockie      # pylint: disable = wrong-import-position   # noqa E402


def demo_hello() -> None:
    blk = blockie.Block("<WORD> ")
    blk.fill({"word": "Hello!"})
    print(blk.content)


def demo_hello_world() -> None:
    blk = blockie.Block("<WORD1> <WORD2>")
    blk.fill({"word1": "Hello", "word2": "world!"})
    print(blk.content)


def demo_sententce_hello_world() -> None:
    blk = blockie.Block("<SENTENCE><WORD> </SENTENCE>")
    blk.fill({"sentence": [{"word": "Hello"}, {"word": "world!"}]})
    print(blk.content)


def demo_date_single() -> None:
    blk = blockie.Block("<DATE><DAY> <MONTH></DATE>")
    blk.fill({"date": {"day": 24, "month": "December"}})
    print(blk.content)


def demo_date_multi() -> None:
    blk = blockie.Block("<DATE><DAY> <MONTH>\n</DATE>")
    blk.fill({"date": [{"day": 24, "month": 12}, {"day": 25, "month": 12}]})
    print(blk.content)


if __name__ == "__main__":
    demo_hello()
    demo_hello_world()
    demo_sententce_hello_world()
    demo_date_single()
    demo_date_multi()
