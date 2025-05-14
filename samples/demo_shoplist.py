# pylint: disable = missing-module-docstring, missing-class-docstring, missing-function-docstring
import sys
from dataclasses import dataclass

sys.path.insert(0, f"{sys.path[0]}/../src")

from blockie import Block, BlockConfig    # pylint: disable = wrong-import-position   # noqa E402


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

    blk = Block(template)
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

    blk = Block(template)
    blk.fill(data)
    print(blk.content)


def demo_shoplist() -> None:
    template = """
                            SHOPPING LIST
  Items                                                         Quantity
------------------------------------------------------------------------
<ITEMS>
* <FLAG>IMPORTANT! <^FLAG>MAYBE? </FLAG><ITEM><+>               <QTY><UNIT> kg<^UNIT> l</UNIT>
</ITEMS>


Short list: <ITEMS><ITEM><.>, <^.></.></ITEMS>
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

    blk = Block(template)
    blk.fill(data)
    print(blk.content)


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

    config = BlockConfig(
        lambda name: f"@{name}",    # tag_gen_var
        lambda name: f"@{name}",    # tag_gen_blk_start
        lambda name: f"@!{name}",   # tag_gen_blk_end
        lambda name: f"@~{name}",   # tag_gen_blk_vari
        "*",                        # autotag_align
        "_",                        # autotag_vari
        8                           # tab_size
    )

    blk = Block(template, config=config)
    blk.fill(data)
    print(blk.content)


if __name__ == "__main__":
    demo_shoplist_basic()
    demo_shoplist_basic_obj()
    demo_shoplist()
    demo_shoplist_custom_cfg()
