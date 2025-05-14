# pylint: disable = missing-module-docstring, missing-class-docstring, missing-function-docstring
import sys

sys.path.insert(0, f"{sys.path[0]}/../src")

from blockie import Block       # pylint: disable = wrong-import-position   # noqa E402


def demo_hello() -> None:
    blk = Block("<WORD> ")
    blk.fill({"word": "Hello!"})
    print(blk.content)


def demo_hello_world() -> None:
    blk = Block("<WORD1> <WORD2>")
    blk.fill({"word1": "Hello", "word2": "world!"})
    print(blk.content)


def demo_hello_world_alt() -> None:
    blk = Block("<WORD> ")
    blk.fill({"word": ["Hello", "world!"]})
    print(blk.content)


def demo_sententce_hello_world() -> None:
    blk = Block("<SENTENCE><WORD> </SENTENCE>")
    blk.fill({"sentence": [{"word": "Hello"}, {"word": "world!"}]})
    print(blk.content)


def demo_sententce_hello_world_alt1() -> None:
    blk = Block("<SENTENCE><WORD> </SENTENCE>")
    blk.fill({"sentence": {"word": ["Hello", "world!"]}})
    print(blk.content)


def demo_sententce_hello_world_alt2() -> None:
    blk = Block("<SENTENCE><WORD1> <WORD2></SENTENCE>")
    blk.fill({"sentence": {"word1": "Hello", "word2": "world!"}})
    print(blk.content)


if __name__ == "__main__":
    demo_hello()
    demo_hello_world()
    demo_hello_world_alt()
    demo_sententce_hello_world()
    demo_sententce_hello_world_alt1()
    demo_sententce_hello_world_alt2()
