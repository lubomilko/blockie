# pylint: disable = missing-module-docstring, missing-class-docstring, missing-function-docstring
import sys

sys.path.insert(0, f"{sys.path[0]}/../src")

import blockie      # pylint: disable = wrong-import-position   # noqa E402


def demo_hello() -> None:
    blk = blockie.Block("<WORD> ")
    blk.fill({"word": "Hello!"})
    print(blk.content)


def demo_set_var() -> None:
    blk = blockie.Block("<WORD1> <WORD2>")
    blk.fill({"word1": "Hello", "word2": "world!"})
    print(blk.content)


def demo_set_block() -> None:
    blk = blockie.Block("<DATE><DAY> <MONTH></DATE>")
    blk.fill({"date": {"day": 24, "month": "December"}})
    print(blk.content)


def demo_set_block_clones() -> None:
    blk = blockie.Block("<DATE><DAY> <MONTH>\n</DATE>")
    blk.fill({"date": [{"day": 24, "month": 12}, {"day": 25, "month": 12}]})
    print(blk.content)


def demo_set_block_as_is() -> None:
    blk = blockie.Block("<DATE>24 December</DATE>")
    blk.fill({"date": True})
    print(blk.content)


def demo_set_block_vari_1() -> None:
    date_dict = {"day": 24, "month": "December"}
    date_dict["vari_idx"] = 0 if isinstance(date_dict["month"], int) else 1

    blk = blockie.Block("<DATE><DAY>.<MONTH>.<^DATE><DAY> <MONTH></DATE>")
    blk.fill({"date": date_dict})
    print(blk.content)


def demo_set_block_vari_2() -> None:
    blk = blockie.Block("<DATE>24.12.<^DATE>24 December</DATE>")
    blk.fill({"date": 1})
    print(blk.content)


def demo_set_block_fill_hndl() -> None:
    def format_month(block: blockie.Block, data: dict, _clone_subidx: int) -> None:
        if isinstance(data["month"], str):
            data["month"] = data["month"].upper()
            block.get_subblock("date").set(vari_idx=1)
        else:
            block.get_subblock("date").set(vari_idx=0)

    blk = blockie.Block("<DATE><DAY>.<MONTH>.<^DATE><DAY> <MONTH></DATE>")
    blk.fill({"day": 24, "month": "December", "fill_hndl": format_month})
    print(blk.content)


def demo_remove_var() -> None:
    blk = blockie.Block("<NAME> <MIDNAME> <SURNAME>")
    blk.fill({"name": "Patrick", "midname": None, "surname": "Bateman"})
    print(blk.content)


def demo_remove_block() -> None:
    blk = blockie.Block("<NAME> <MIDNAME_WRAP><MIDNAME> </MIDNAME_WRAP><SURNAME>")
    blk.fill({"name": "Patrick", "surname": "Bateman", "midname_wrap": None})
    print(blk.content)


if __name__ == "__main__":
    demo_hello()
    demo_set_var()
    demo_set_block()
    demo_set_block_clones()
    demo_set_block_as_is()
    demo_set_block_vari_1()
    demo_set_block_vari_2()
    demo_set_block_fill_hndl()
    demo_remove_var()
    demo_remove_block()
