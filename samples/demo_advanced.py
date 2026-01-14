# pylint: disable = missing-module-docstring, missing-class-docstring, missing-function-docstring
import sys
import json
from dataclasses import dataclass

sys.path.insert(0, f"{sys.path[0]}/../src")

import blockie      # pylint: disable = wrong-import-position   # noqa E402


def demo_shoplist_basic() -> None:
    template = """demo_shoplist_basic:
                SHOPPING LIST
  Items                             Quantity
--------------------------------------------
<ITEMS>
* <ITEM><+>                         <QTY>
</ITEMS>


Short list: <ITEMS><ITEM><.>, <^.></.></ITEMS>
"""

    data = {
        "items": [
            {"item": "apples", "qty": "1 kg"},
            {"item": "potatoes", "qty": "2 kg"},
            {"item": "rice", "qty": "1 kg"},
            {"item": "orange juice", "qty": "1 l"},
            {"item": "cooking magazine", "qty": 1},
        ]
    }

    blk = blockie.Block(template)
    blk.fill(data)
    print(blk.content)


def demo_shoplist_basic_obj() -> None:
    template = """demo_shoplist_basic_obj:
                SHOPPING LIST
  Items                             Quantity
--------------------------------------------
<ITEMS>
* <ITEM><+>                         <QTY>
</ITEMS>


Short list: <ITEMS><ITEM><.>, <^.></.></ITEMS>
"""

    @dataclass
    class ItemAttribs:
        item: str = ""
        qty: str | int = ""

    @dataclass
    class Data:
        items: list[ItemAttribs] | None = None

    data = Data(
        [
            ItemAttribs("apples", "1 kg"),
            ItemAttribs("potatoes", "2 kg"),
            ItemAttribs("rice", "1 kg"),
            ItemAttribs("orange juice", "1 l"),
            ItemAttribs("cooking magazine", 1)
        ]
    )

    blk = blockie.Block(template)
    blk.fill(data)
    print(blk.content)


def demo_shoplist_advanced_1() -> None:
    template = """demo_shoplist_advanced_1:
                SHOPPING LIST
  Items                             Quantity
--------------------------------------------
<ITEMS>
<FLAG>IMPORTANT! <^FLAG>MAYBE? </FLAG>
* <@FLAG><ITEM><+>                  <QTY><UNIT> kg<^UNIT> l</UNIT>
</ITEMS>


Short list: <ITEMS><ITEM><.>, <^.></.></ITEMS>
"""

    important_items = ("potatoes", "rice")
    maybe_items = ("cooking magazine",)

    data = {
        "items": [
            {"item": "apples", "qty": "1", "unit": 0},
            {"item": "potatoes", "qty": "2", "unit": 0},
            {"item": "rice", "qty": "1", "unit": 0},
            {"item": "orange juice", "qty": "1", "unit": 1},
            {"item": "cooking magazine", "qty": None, "unit": None}
        ]
    }

    for item in data["items"]:
        item["flag"] = 0 if item["item"] in important_items else 1 if item["item"] in maybe_items else None

    blk = blockie.Block(template)
    blk.fill(data)
    print(blk.content)


def demo_shoplist_advanced_custom_cfg() -> None:
    template = """demo_shoplist_advanced_custom_cfg:
                SHOPPING LIST
  Items                             Quantity
--------------------------------------------
@items
@flagIMPORTANT! @~flagMAYBE? @!flag
* @&flag@item@>>                    @qty@unit kg@~unit l@!unit
@!items


Short list: @items@item@_, @~_@!_@!items
"""

    data = {
        "items": [
            {"flag": None, "item": "apples", "qty": "1", "unit": True},
            {"flag": True, "item": "potatoes", "qty": "2", "unit": {"vari_idx": 0}},
            {"flag": None, "item": "rice", "qty": "1", "unit": {"vari_idx": 0}},
            {"flag": None, "item": "orange juice", "qty": "1", "unit": {"vari_idx": 1}},
            {"flag": {"vari_idx": 1}, "item": "cooking magazine", "qty": None, "unit": None},
        ]
    }

    config = blockie.BlockConfig(
        lambda name: f"@{name}",    # tag_gen_var
        lambda name: f"@{name}",    # tag_gen_blk_start
        lambda name: f"@!{name}",   # tag_gen_blk_end
        lambda name: f"@~{name}",   # tag_gen_blk_vari
        "---",                      # tag_implct_iter
        "&",                        # autotag_blk_var
        ">>",                       # autotag_align
        "_",                        # autotag_vari
        "-",                        # subref_sep
        8,                          # tab_size
        True,                       # enable_autotags
    )

    blk = blockie.Block(template, config=config)
    blk.fill(data)
    print(blk.content)


def demo_shoplist_advanced_manual_1() -> None:
    template = """demo_shoplist_advanced_manual_1:
                SHOPPING LIST
  Items                             Quantity
--------------------------------------------
<ITEMS>
<FLAG>IMPORTANT! <^FLAG>MAYBE? </FLAG>
* <@FLAG><ITEM><+>                  <QTY><UNIT> kg<^UNIT> l</UNIT>
</ITEMS>
"""

    #   flag,   item,               qty,    unit
    data = (
        (-1,    "apples",           "1",    0),
        (0,     "potatoes",         "2",    0),
        (-1,    "rice",             "1",    0),
        (-1,    "orange juice",     "1",    1),
        (1,     "cooking magazine", "",     -1)
    )

    blk_template = blockie.Block(template)
    blk_items = blk_template.get_subblock("items")
    [blk_flag, blk_unit] = [blk_items.get_subblock(n) for n in ("flag", "unit")]

    for data_item in data:
        blk_items.set_variables(item=data_item[1], qty=data_item[2])
        blk_flag.set(data_item[0])
        blk_unit.set(data_item[3])
        blk_items.clone()
    blk_items.set()
    print(blk_template.content)


def demo_shoplist_advanced_manual_2() -> None:
    template = """demo_shoplist_advanced_manual_2:
                SHOPPING LIST
  Items                             Quantity
--------------------------------------------
<ITEMS>
* <ITEM><+>                         <QTY>
</ITEMS>
"""

    #   item,                   qty
    data = (
        ("apples",              "1 kg"),
        ("potatoes",            "2 kg"),
        ("rice",                "1 kg"),
        ("orange juice",        "1 l"),
        ("cooking magazine",    "")
    )

    blk_template = blockie.Block(template)
    blk_items = blk_template.get_subblock("items")

    for data_item in data:
        blk_items.set_variables(autoclone=True, item=data_item[0], qty=data_item[1])
    blk_items.set()
    print(blk_template.content)


def demo_shoplist_advanced_manual_3() -> None:
    template = """demo_shoplist_advanced_manual_3:
                SHOPPING LIST
  Items                             Quantity
--------------------------------------------
<ITEMS>
* <ITEM><+>                         <QTY>
</ITEMS>
"""

    data_item = ("apples", "potatoes", "rice", "orange juice", "cooking magazine")
    data_qty = ("1 kg", "2 kg", "1 kg", "1 l", "")

    blk_template = blockie.Block(template)
    blk_items = blk_template.get_subblock("items")

    blk_items.set_variables(item=data_item, qty=data_qty)
    blk_items.set()
    print(blk_template.content)


def demo_macros_1() -> None:
    template = """demo_macros_1:
<VLIST_A>
</VLIST_A>

<HLIST_A>
</HLIST_A>

<HLIST_B>
</HLIST_B>

<MACROS>
<VLIST>
<DESC>:
<ITEMS>
- <*>
</ITEMS>
</VLIST>

<HLIST>
<DESC>:
<ITEMS><*><.>, <^.></.></ITEMS>
</HLIST>
</MACROS>
"""

    def ref_blk_hndl(block: blockie.Block, data: dict, _clone_subidx: int) -> None:
        # Set this block template to the template of a macro block defined in the first part of this block name.
        block.template = block.parent.get_subblock("macros").get_subblock(block.name.split("_")[0]).template

    blk = blockie.Block(template)
    blk.fill({
        "vlist_a": {
            "fill_hndl": ref_blk_hndl,
            "desc": "PC hardware",
            "items": ["case", "display", "keyboard", "mouse"]},
        "hlist_a": {
            "fill_hndl": ref_blk_hndl,
            "desc": "fruits",
            "items": ["apple", "banana", "orange"]},
        "hlist_b": {
            "fill_hndl": ref_blk_hndl,
            "desc": "vegetables",
            "items": ["carrot", "tomatoe", "pepper"]},
        "macros": None})
    print(blk.content)
    # prints:
    # PC hardware:
    # - case
    # - display
    # - keyboard
    # - mouse
    #
    # fruits:
    # apple, banana, orange
    #
    # vegetables:
    # carrot, tomatoe, pepper


def demo_macros_2() -> None:
    template = """demo_macros_2:
<LISTS>
<REF_BLK>

</LISTS>

<MACROS>
<VLIST>
<DESC>:
<ITEMS>
- <*>
</ITEMS>
</VLIST>

<HLIST>
<DESC>:
<ITEMS><*><.>, <^.></.></ITEMS>
</HLIST>
</MACROS>
"""

    def ref_blk_hndl(block: blockie.Block, data: dict, _clone_subidx: int) -> None:
        # Set the 'ref_blk' variable value to the template of the block defined by the 'ref' data attribute.
        block.set_variables(ref_blk=block.parent.get_subblock("macros").get_subblock(data.get("ref", "")).template)

    blk = blockie.Block(template)
    blk.fill({
        "lists": [
            {
                "fill_hndl": ref_blk_hndl,
                "ref": "vlist",
                "desc": "PC hardware",
                "items": ["case", "display", "keyboard", "mouse"]},
            {
                "fill_hndl": ref_blk_hndl,
                "ref": "hlist",
                "desc": "fruits",
                "items": ["apple", "banana", "orange"]},
            {
                "fill_hndl": ref_blk_hndl,
                "ref": "hlist",
                "desc": "vegetables",
                "items": ["carrot", "tomatoe", "pepper"]}],
        "macros": None})
    print(blk.content)
    # prints:
    # PC hardware:
    # - case
    # - display
    # - keyboard
    # - mouse
    #
    # fruits:
    # apple, banana, orange
    #
    # vegetables:
    # carrot, tomatoe, pepper


def demo_extensions_1() -> None:
    template = """demo_extensions_1:
<INTRO>This is a list of <DESC>:</INTRO>
<ITEMS>
- <*>
</ITEMS>

<OUTRO>There are <NUM> items in total.</OUTRO>

<EXTENSIONS>
<EXT_BLKS>INTRO,ITEMS</EXT_BLKS>
<INTRO>
+--------------------------+
| My list of <DESC><+>     |
+--------------------------+
</INTRO>

<ITEMS>
* <*>
</ITEMS>
</EXTENSIONS>
"""

    def ext_blk_hndl(block: blockie.Block, _data: dict, _clone_subidx: int) -> None:
        # Get the block with extensions from the 'extensions' subblock.
        blk_extensions = block.get_subblock("extensions")
        if isinstance(blk_extensions, blockie.Block):
            # Loop through block names defined in the 'EXT_BLKS' block content.
            for ext_blk_name in blk_extensions.get_subblock("ext_blks").content.split(","):
                # Replace the subblocks of this block with the templates of block extensions.
                block.get_subblock(ext_blk_name).template = blk_extensions.get_subblock(ext_blk_name).template

    blk = blockie.Block(template)
    blk.fill({
        "fill_hndl": ext_blk_hndl,
        "intro": {"desc": "PC hardware"},
        "items": ["case", "display", "keyboard", "mouse"],
        "outro": {"NUM": 4},
        "extensions": None})
    print(blk.content)
    # prints:
    # +--------------------------+
    # | My list of PC hardware   |
    # +--------------------------+
    #
    # * case
    # * display
    # * keyboard
    # * mouse
    #
    # There are 4 items in total.


def demo_extensions_2() -> None:
    template = """demo_extensions_2:
<INTRO>This is a list of <DESC>:</INTRO>
<ITEMS>
- <*>
</ITEMS>

<OUTRO>There are <NUM> items in total.</OUTRO>
"""

    extensions = """
<INTRO>
+--------------------------+
| My list of <DESC><+>     |
+--------------------------+
</INTRO>

<ITEMS>
* <*>
</ITEMS>
"""

    def ext_blk_hndl(block: blockie.Block, data: dict, _clone_subidx: int) -> None:
        # Loop through extended block names defined in the 'ext_blk_names' data attribute.
        for name in data.get("ext_blk_names", ""):
            # Replace this block template with the template of a subblock within the 'ext_blks' Block data attrib.
            block.get_subblock(name).template = data.get("ext_blks", blockie.Block()).get_subblock(name).template

    blk = blockie.Block(template)
    blk.fill({
        "fill_hndl": ext_blk_hndl,
        "ext_blks": blockie.Block(extensions),
        "ext_blk_names": ("intro", "items"),
        "intro": {"desc": "PC hardware"},
        "items": ["case", "display", "keyboard", "mouse"],
        "outro": {"NUM": 4}})
    print(blk.content)
    # prints:
    # +--------------------------+
    # | My list of PC hardware   |
    # +--------------------------+
    #
    # * case
    # * display
    # * keyboard
    # * mouse
    #
    # There are 4 items in total.


def demo_references() -> None:
    template = """
<BOOKS>
<TITLE><ENGLISH><ORIGINAL_WRAP> (<ORIGINAL>)</ORIGINAL_WRAP></TITLE>
+------------------------------------------------------------------------------+
| <@TITLE> - <AUTHOR.FULL_INFO><+>                                             |
+------------------------------------------------------------------------------+
| Genre     | <GENRE><+>                                                       |
| Published | <PUBLICATION.DATE><DAY>.<MONTH>.<YEAR></PUBLICATION.DATE><+>     |
| ISBN      | <PUBLICATION.ISBN><+>                                            |
| Publisher | <PUBLICATION.PUBLISHER><+>                                       |
| Language  | <PUBLICATION.LANGUAGE><+>                                        |
| Pages     | <PUBLICATION.PAGE_NUM><+>                                        |
+------------------------------------------------------------------------------+

</BOOKS>
"""

    blk = blockie.Block(template)

    # Load data from a JSON file and add an 'original_wrap' attribute to each 'book' needed for
    # setting the 'ORIGINAL_WRAP' block.
    with open("samples/data_books.json", encoding="utf-8") as file:
        data = json.load(file)
        for book in data["books"]:
            book["title"]["original_wrap"] = bool(book["title"].get("original", ""))

    blk.fill(data)
    print(blk.content)


if __name__ == "__main__":
    demo_shoplist_basic()
    demo_shoplist_basic_obj()
    demo_shoplist_advanced_1()
    demo_shoplist_advanced_custom_cfg()
    demo_shoplist_advanced_manual_1()
    demo_shoplist_advanced_manual_2()
    demo_shoplist_advanced_manual_3()
    demo_macros_1()
    demo_macros_2()
    demo_extensions_1()
    demo_extensions_2()
    demo_references()
