"""
NOTE: The tests are currently in a very rough shape and they come from old dirty scripts made only
to quickly verify if new features work as expected. Proper tests are planned to be added in future
releases.
"""

# pylint: disable = missing-class-docstring, missing-function-docstring

import sys
from pathlib import Path

sys.path.insert(0, str(Path(Path(__file__).parent.parent, "src").resolve()))

# pylint: disable = wrong-import-position, import-error
from blockie import Block, BlockConfig      # noqa: E402


def compare_files(gen_file: Path, exp_file: Path) -> bool:
    files_match = False
    with open(gen_file, "r", encoding="utf-8") as file_gen, open(exp_file, "r", encoding="utf-8") as file_exp:
        if file_gen.read() == file_exp.read():
            files_match = True
        else:
            print(f"ERROR: File '{gen_file}' does not match the expected file '{exp_file}'.")
    return files_match


def test_lowlevel() -> None:
    Path("data/content_gen.txt").unlink(missing_ok=True)

    blk_file = Block()

    blk_file.load_template("data/content_tmpl.txt")

    blk_simple = blk_file.get_subblock("SIMPLE1")
    blk_simple.clone(force=True)
    blk_simple.clone(force=True)
    blk_simple.clone(force=True)
    blk_simple.set()

    (blk_simple, blk_test1, blk_test2) = blk_file.get_subblock("SIMPLE2", "TEST1", "TEST2")

    blk_simple.template = "<VAL><.>,<^.>.</.>\n<VAL><.>,<^.>.</.>\n\n"
    blk_simple.set_variables(VAL=1)
    blk_simple.clone()
    blk_simple.set_variables(VAL=2)
    blk_simple.clone()
    blk_simple.set_variables(VAL="3")

    blk_val = blk_test1.get_subblock("VAL")
    for i in range(12):
        blk_val.set_variables(ID=i, LABEL="cyclic")
        blk_val.clone()
    blk_val.set()
    blk_test1.clone()

    blk_val.set_variables(ID="333", LABEL="manual1")
    blk_val.clone()
    blk_val.set_variables(ID="4798", LABEL="manual2")
    blk_val.set()

    blk_file.set_subblock(blk_simple, blk_test1)

    blk_val = blk_test2.get_subblock("VAL")
    blk_val.set_variables(ID=(11, 22, 33), LABEL="man")
    blk_test2.set(all_children=True)

    blk_line = blk_file.get_subblock("LINE1")
    blk_val = blk_line.get_subblock("VAL")
    for i in range(31):
        blk_val.set_variables(ID=i)
        blk_val.clone()
        if (i + 1) % 10 == 0:
            blk_val.set()
            blk_line.clone()
    blk_val.set()
    blk_line.set()

    blk_line = blk_file.get_subblock("LINE2")
    blk_val = blk_line.get_subblock("VAL")
    for i in range(32):
        blk_val.clone()
        if (i + 1) % 10 == 0:
            blk_line.set_variables(SEP=20*"_")
            blk_line.clone(set_children=True)
    blk_line.set(all_children=True)

    blk_line = blk_file.get_subblock("LINE3")
    blk_val = blk_line.get_subblock("VAL")
    for i in range(20):
        blk_val.set_variables(ID=f"{i:03d}")
        if i < 10:
            blk_val.get_subblock("DEF").set()
        else:
            blk_val.get_subblock("DEF").set(1)
        blk_val.clone()
        if (i + 1) % 10 == 0:
            blk_line.clone(set_children=True)
    # blk_val.set()   # Not necessary, because there is no remaining blk_val content to be set.
    blk_line.set()

    blk_container = blk_file.get_subblock("CONTAINER")
    blk_line = blk_container.get_subblock("LINE4")
    blk_val = blk_line.get_subblock("VAL")
    blk_val.clone(copies=10)
    blk_line.clone(set_children=True)
    blk_val.clone(copies=10)
    blk_line.set(all_children=True)

    blk_container.clone()
    blk_val.clone(copies=3)
    blk_val.set()
    blk_line.clone()
    blk_val.clone(copies=2)
    blk_container.set(all_children=True)

    blk_prm = blk_file.get_subblock("BLK_PRM")
    blk_prm.set_variables(ARR="", PRM_NAME="PARAM1")
    blk_prm.clear_subblock("NO_ARR")
    blk_arr_def = blk_prm.get_subblock("ARR_DEF")
    blk_arr_def.set_variables(SIZE="10")
    blk_arr_def.set()
    blk_prm.clone()
    blk_prm.set_variables(ARR="", PRM_NAME="PARAM2")
    blk_prm.clear_subblock("NO_ARR")
    blk_arr_def = blk_prm.get_subblock("ARR_DEF")
    blk_arr_def.set_variables(SIZE="11")
    blk_arr_def.set()
    blk_prm.set()

    blk_loop_test = blk_file.get_subblock("LOOP_TEST")
    blk_test = blk_loop_test.get_subblock("TEST")
    blk_test.set_variables(A="a", B="b")
    blk_test.set(0)
    blk_loop_test.clone()
    blk_test.set_variables(A="b")
    blk_test.clear_variables("B")
    blk_test.set(1)
    blk_loop_test.clone()
    blk_test.clear_variables("A", "B")
    blk_test.set(2)
    blk_loop_test.set()

    blk_container = blk_file.get_subblock("MULTI1")
    blk_blk = blk_container.get_subblock("BLK")
    blk_blk.set(0)
    blk_container.clone(force=True)
    blk_blk.set(1)
    blk_container.clone(force=True)
    blk_blk.set(2)
    blk_container.set()

    blk_container = blk_file.get_subblock("MULTI2")
    blk_blk = blk_container.get_subblock("BLK")
    blk_blk.autotags = False
    blk_blk.set_variables(A=123)
    blk_blk.set(0)
    blk_container.clone()
    blk_blk.set_variables(A=123456)
    blk_blk.set(1)
    blk_container.clone()
    blk_blk.set_variables(A=123456789)
    blk_blk.set(2)
    blk_container.set()

    blk_table = blk_file.get_subblock("TABLE")
    blk_row = blk_table.get_subblock("ROW")
    blk_row.set_variables(autoclone=True, A=1, B=23, C=456)
    blk_row.set_variables(autoclone=True, A="def", B="bc", C="a")
    blk_table.set(all_children=True)

    tab_values = (
        ("name", "surname", "age"),
        ("Johnny", "Mnemonic", 35),
        ("Mr.", "Bean", 33),
        ("T-1000", "Terminator", 30))

    blk_html_table = blk_file.get_subblock("HTML_TABLE")
    blk_row = blk_html_table.get_subblock("ROW")
    blk_col = blk_row.get_subblock("COL")
    blk_col.autotags = False
    for row_vals in tab_values:
        blk_col.set_variables(VALUE=row_vals)
        blk_row.clone(set_children=True)
    blk_html_table.set(all_children=True)
    blk_file.save_content(str("data/content_gen.txt"))

    assert compare_files("data/content_gen.txt", "data/content_exp.txt")


def test_dictfill() -> None:
    Path("data/fill_gen.txt").unlink(missing_ok=True)
    data = {
        "to_set": 1,
        "to_clear": -1,
        "struct_name": "SOME_STRUCT_T",
        "members": (
            {"type": {"vari_idx": 0, "t": "UNSIGNED8"}, "name": "u8Var", "arr": None},
            {"type": {"vari_idx": 1, "t": "UNSIGNED16"}, "name": "au16Var", "arr": {"size": 10}},
            {"type": {"vari_idx": 2, "t": "SIGNED8"}, "name": "ps8Var", "arr": None},
            {"type": {"vari_idx": 3, "t": "SIGNED16"}, "name": "aps16Var", "arr": {"size": 20}},
            {"type": {"vari_idx": -1}, "name": "InvalidVar1", "arr": None},
            {"type": {"vari_idx": False}, "name": "InvalidVar2", "arr": None},
            {"type": "", "name": "InvalidVar3", "arr": None},
            {"type": {}, "name": "InvalidVar4", "arr": None}),
        "text": ["line one", "line two", "line three"]
    }

    blk_file = Block("data/fill_tmpl.txt")
    blk_file.fill(data)
    blk_file.save_content("data/fill_gen.txt")

    assert compare_files("data/fill_gen.txt", "data/fill_exp.txt")


def test_shoplist() -> None:
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
            {"flag": 1, "item": "cooking magazine", "qty": None, "unit": None},
        ]
    }

    blk = Block(template)
    blk.fill(data)
    assert blk.content == """
                            SHOPPING LIST
  Items                                                         Quantity
------------------------------------------------------------------------
* apples                                                        1 kg
* IMPORTANT! potatoes                                           2 kg
* rice                                                          1 kg
* orange juice                                                  1 l
* MAYBE? cooking magazine


Short list: apples, potatoes, rice, orange juice, cooking magazine
"""


def test_shoplist_custom_cfg() -> None:
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
            {"flag": True, "item": "potatoes", "qty": "2", "unit": 0},
            {"flag": None, "item": "rice", "qty": "1", "unit": 0},
            {"flag": {"vari_idx": 1}, "item": "cooking magazine", "qty": None, "unit": None},
            {"flag": None, "item": "orange juice", "qty": "1", "unit": 1}
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
    assert blk.content == """
                            SHOPPING LIST
  Items                                                         Quantity
------------------------------------------------------------------------
* apples                                                        1 kg
* IMPORTANT! potatoes                                           2 kg
* rice                                                          1 kg
* MAYBE? cooking magazine
* orange juice                                                  1 l


Short list: apples, potatoes, rice, cooking magazine, orange juice
"""


if __name__ == "__main__":
    test_shoplist_custom_cfg()
