# pylint: disable = missing-module-docstring, missing-class-docstring, missing-function-docstring
import sys

sys.path.insert(0, f"{sys.path[0]}/../src")

import blockie      # pylint: disable = wrong-import-position   # noqa E402


def demo_set_var() -> None:
    blk = blockie.Block("<WORD1> <WORD2>!")
    blk.fill({"word1": "Hello", "word2": "world"})
    print(blk.content)
    # prints:
    # Hello world!


def demo_set_var_multiline() -> None:
    template = """  <TEXT1>
<TEXT2>
        <TEXT3>"""
    blk = blockie.Block(template)
    blk.fill({
        "text1": "text 1 - line 1\ntext 1 - line 2",
        "text2": "text 2 - line 1\ntext 2 - line 2\ntext 2 - line 3",
        "text3": "text 3 - line 1\ntext 3 - line 2\ntext 3 - line 3"})
    print(blk.content)
    # prints:
    #   text 1 - line 1
    #   text 1 - line 2
    # text 2 - line 1
    # text 2 - line 2
    # text 2 - line 3
    #         text 3 - line 1
    #         text 3 - line 2
    #         text 3 - line 3


def demo_set_block() -> None:
    blk = blockie.Block("The date is: <DATE><MONTH> <DAY></DATE>")
    blk.fill({"date": {"day": 24, "month": "December"}})
    print(blk.content)
    # prints:
    # The date is: December 24


def demo_set_block_clones() -> None:
    blk = blockie.Block("* <EVENTS><EVENT>: <MONTH> <DAY>\n</EVENTS>")
    blk.fill({"events": [
        {"event": "Christmas", "day": 24, "month": "December"},
        {"event": "New Year's Eve", "day": 31, "month": "December"},
        {"event": "New Year's Day", "day": 1, "month": "January"}]})
    print(blk.content)
    # prints:
    # * Christmas: December 24
    # * New Year's Eve: December 31
    # * New Year's Day: January 1


def demo_set_implct_iter() -> None:
    blk = blockie.Block("<LIST>- <*>\n</LIST>")
    blk.fill({"list": ["gloves", "plastic bags", "duct tape", "shovel"]})
    print(blk.content)
    # prints:
    # - gloves
    # - plastic bags
    # - duct tape
    # - shovel


def demo_set_block_as_is() -> None:
    blk = blockie.Block("The date is: <DATE>July 2</DATE>")
    blk.fill({"date": True})
    print(blk.content)
    # prints:
    # The date is: July 2


def demo_set_block_vari_1() -> None:
    blk = blockie.Block("The date is: <DATE><DAY>.<MONTH>.<^DATE><MONTH> <DAY></DATE>")
    blk.fill({"date": {"vari_idx": 0, "day": 24, "month": 12}})
    print(blk.content)
    # prints:
    # The date is: 24.12.


def demo_set_block_vari_2() -> None:
    date_dict = {"day": 24, "month": "December"}
    date_dict["vari_idx"] = 0 if isinstance(date_dict["month"], int) else 1

    blk = blockie.Block("The date is: <DATE><DAY>.<MONTH>.<^DATE><MONTH> <DAY></DATE>")
    blk.fill({"date": date_dict})
    print(blk.content)
    # prints:
    # The date is: December 24


def demo_set_block_vari_3() -> None:
    blk = blockie.Block("The date is: <DATE>24.12.<^DATE>December 24</DATE>")
    blk.fill({"date": 1})
    print(blk.content)
    # prints:
    # The date is: December 24


def demo_set_block_fill_hndl() -> None:
    def format_month(block: blockie.Block, data: dict, _clone_subidx: int) -> None:
        if isinstance(data["month"], str):
            data["month"] = data["month"].upper()
            block.get_subblock("date").set(vari_idx=1)
        else:
            block.get_subblock("date").set(vari_idx=0)

    blk = blockie.Block("The date is: <DATE><DAY>.<MONTH>.<^DATE><MONTH> <DAY></DATE>")
    blk.fill({"day": 24, "month": "December", "fill_hndl": format_month})
    print(blk.content)
    # prints:
    # The date is: DECEMBER 24


def demo_clear_var() -> None:
    blk = blockie.Block("<NAME> <MIDNAME> <SURNAME>")
    blk.fill({"name": "Thomas", "midname": None, "surname": "Anderson"})
    print(blk.content)
    # prints:
    # Thomas  Anderson


def demo_clear_block() -> None:
    blk = blockie.Block("<NAME> <MIDNAME_WRAP><MIDNAME> </MIDNAME_WRAP><SURNAME>")
    blk.fill({"name": "Thomas", "surname": "Anderson", "midname_wrap": None})
    print(blk.content)
    # prints:
    # Thomas Anderson


def demo_ref_var() -> None:
    blk = blockie.Block("<GREETING> Welcome to the world of templating.")
    blk.fill({"name": "John", "greeting": "Hello <NAME>!"})
    print(blk.content)
    # prints:
    # Hello John! Welcome to the world of templating.


def demo_ref_block() -> None:
    blk = blockie.Block("The date is: <DATE_STR>.")
    blk.fill({"date": {"day": "01", "month": "01", "year": "2026"}, "date_str": "<DATE><DAY>.<MONTH>.<YEAR></DATE>"})
    print(blk.content)
    # prints:
    # The date is: 01.01.2026.


def demo_subref_var() -> None:
    blk = blockie.Block("The date is: <DATE.DAY>.<DATE.MONTH>.")
    blk.fill({"date": {"day": 24, "month": 12}})
    print(blk.content)
    # prints:
    # The date is: 24.12.


def demo_subref_block() -> None:
    blk = blockie.Block("<BOOK.AUTHORS><NAME> <SURNAME>\n</BOOK.AUTHORS>")
    blk.fill({"book": {
        "title": "The C Programming Language",
        "authors": [{"name": "Brian", "surname": "Kernighan"}, {"name": "Dennis", "surname": "Ritchie"}],
        "date": "1988"}})
    print(blk.content)
    # prints:
    # Brian Kernighan
    # Dennis Ritchie


def demo_autotag_align() -> None:
    template = """
<CHARACTERS>
<NAME><+>       <SURNAME>
</CHARACTERS>"""

    blk = blockie.Block(template)
    blk.fill({"characters": [
        {"name": "Dave", "surname": "Bowman"},
        {"name": "Frank", "surname": "Poole"},
        {"name": "Heywood", "surname": "Floyd"},
        {"name": "HAL", "surname": "9000"}]})
    print(blk.content)
    # prints:
    # Dave            Bowman
    # Frank           Poole
    # Heywood         Floyd
    # HAL             9000


def demo_autotag_vari_1() -> None:
    blk = blockie.Block("Characters: <CHARACTERS><NAME> <SURNAME><.>, <^.></.></CHARACTERS>.")
    blk.fill({"characters": [
        {"name": "Dave", "surname": "Bowman"},
        {"name": "Frank", "surname": "Poole"},
        {"name": "Heywood", "surname": "Floyd"},
        {"name": "HAL", "surname": "9000"}]})
    print(blk.content)
    # prints:
    # Characters: Dave Bowman, Frank Poole, Heywood Floyd, HAL 9000.


def demo_autotag_vari_2() -> None:
    template = """
<CHARACTERS>
<.>
| <NAME><+>     <SURNAME><+> |
<^.>
| <NAME><+>     <SURNAME><+> |
+----------------------------+
<^.>
+----------------------------+
| <NAME><+>     <SURNAME><+> |
</.>
</CHARACTERS>"""

    blk = blockie.Block(template)
    blk.fill({"characters": [
        {"name": "Dave", "surname": "Bowman"},
        {"name": "Frank", "surname": "Poole"},
        {"name": "Heywood", "surname": "Floyd"},
        {"name": "HAL", "surname": "9000"}]})
    print(blk.content)
    # prints:
    # +----------------------------+
    # | Dave          Bowman       |
    # | Frank         Poole        |
    # | Heywood       Floyd        |
    # | HAL           9000         |
    # +----------------------------+


def demo_autotag_block_var() -> None:
    template = """
<LIST>
<IDX>a)<^IDX>b)<^IDX>c)<^IDX>d)<^IDX>e)<^IDX>f)</IDX>
<@IDX> <ITEM><+>        <QTY>
</LIST>
"""

    blk = blockie.Block(template)
    blk.fill({"list": [
        {"idx": 0, "item": "first", "qty": 1},
        {"idx": 1, "item": "second", "qty": 2},
        {"idx": 2, "item": "third", "qty": 3}]})
    print(blk.content)
    # prints:
    # a) first                1
    # b) second               2
    # c) third                3


if __name__ == "__main__":
    demo_set_var()
    demo_set_var_multiline()
    demo_set_block()
    demo_set_block_clones()
    demo_set_implct_iter()
    demo_set_block_as_is()
    demo_set_block_vari_1()
    demo_set_block_vari_2()
    demo_set_block_vari_3()
    demo_set_block_fill_hndl()
    demo_clear_var()
    demo_clear_block()
    demo_ref_var()
    demo_ref_block()
    demo_subref_var()
    demo_subref_block()
    demo_autotag_align()
    demo_autotag_vari_1()
    demo_autotag_vari_2()
    demo_autotag_block_var()
