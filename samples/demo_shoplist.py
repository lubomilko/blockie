# pylint: disable = missing-module-docstring, missing-class-docstring, missing-function-docstring
import sys
import json
from dataclasses import dataclass

sys.path.insert(0, f"{sys.path[0]}/../src")

import blockie      # pylint: disable = wrong-import-position   # noqa E402


def demo_shoplist_basic() -> None:
    template = """
                            SHOPPING LIST
  Items                                                         Quantity
------------------------------------------------------------------------
<ITEMS>
* <ITEM><+>                                                     <QTY>
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
    template = """
                            SHOPPING LIST
  Items                                                         Quantity
------------------------------------------------------------------------
<ITEMS>
* <ITEM><+>                                                     <QTY>
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


def demo_shoplist() -> None:
    with open("samples/shoplist_data.json", encoding="utf-8") as file:
        data = json.load(file)

        blk = blockie.Block()
        blk.load_template("samples/shoplist_tmpl.txt")
        blk.fill(data)
        blk.save_content("samples/shoplist_gen.txt")


def demo_shoplist_custom_cfg() -> None:
    template = """
                            SHOPPING LIST
  Items                                                         Quantity
------------------------------------------------------------------------
@items
* @flagIMPORTANT! @~flagMAYBE? @!flag@item@*                    @qty@unit kg@~unit l@!unit
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
        "*",                        # autotag_align
        "_",                        # autotag_vari
        8                           # tab_size
    )

    blk = blockie.Block(template, config=config)
    blk.fill(data)
    print(blk.content)


def demo_shoplist_manual_1() -> None:
    template = """
                            SHOPPING LIST
  Items                                                         Quantity
------------------------------------------------------------------------
<ITEMS>
* <FLAG>IMPORTANT! <^FLAG>MAYBE? </FLAG><ITEM><+>               <QTY><UNIT> kg<^UNIT> l</UNIT>
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
    [blk_flag, blk_unit] = blk_items.get_subblock("flag", "unit")

    for data_item in data:
        blk_items.set_variables(item=data_item[1], qty=data_item[2])
        blk_flag.set(data_item[0])
        blk_unit.set(data_item[3])
        blk_items.clone()
    blk_items.set()
    print(blk_template.content)


def demo_shoplist_manual_2() -> None:
    template = """
                            SHOPPING LIST
  Items                                                         Quantity
------------------------------------------------------------------------
<ITEMS>
* <ITEM><+>                                                     <QTY>
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


def demo_shoplist_manual_3() -> None:
    template = """
                            SHOPPING LIST
  Items                                                         Quantity
------------------------------------------------------------------------
<ITEMS>
* <ITEM><+>                                                     <QTY>
</ITEMS>
"""

    data_item = ("apples", "potatoes", "rice", "orange juice", "cooking magazine")
    data_qty = ("1 kg", "2 kg", "1 kg", "1 l", "")

    blk_template = blockie.Block(template)
    blk_items = blk_template.get_subblock("items")

    blk_items.set_variables(item=data_item, qty=data_qty)
    blk_items.set()
    print(blk_template.content)


if __name__ == "__main__":
    demo_shoplist_basic()
    demo_shoplist_basic_obj()
    demo_shoplist()
    demo_shoplist_custom_cfg()
    demo_shoplist_manual_1()
    demo_shoplist_manual_2()
    demo_shoplist_manual_3()
