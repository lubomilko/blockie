"""
NOTE: The tests are currently in a very rough shape and they come from old dirty scripts made only
to quickly verify if new features work as expected. Proper tests are planned to be added in future
releases.
"""

# pylint: disable = missing-class-docstring, missing-function-docstring
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(Path(__file__).parent.parent, "src").resolve()))
sys.path.insert(0, str(Path(Path(__file__).parent, "data").resolve()))

# pylint: disable = wrong-import-position, import-error
from blockie import Block, BlockConfig      # noqa: E402


def abs_path(path: str | os.PathLike[str]) -> Path:
    return Path(Path(__file__).parent, path).resolve()


def compare_files(gen_file: str | os.PathLike[str], exp_file: str | os.PathLike[str]) -> bool:
    files_match = False
    with (open(abs_path(gen_file), "r", encoding="utf-8") as file_gen,
          open(abs_path(exp_file), "r", encoding="utf-8") as file_exp):
        if file_gen.read() == file_exp.read():
            files_match = True
        else:
            print(f"ERROR: File '{gen_file}' does not match the expected file '{exp_file}'.")
    return files_match


def test_lowlevel() -> None:
    Path("data/content_gen.txt").unlink(missing_ok=True)

    blk_file = Block()

    blk_file.load_template(abs_path("data/content_tmpl.txt"))

    blk_simple = blk_file.get_subblock("SIMPLE1")
    blk_simple.clone(force=True)
    blk_simple.clone(force=True)
    blk_simple.clone(force=True)
    blk_simple.set()

    (blk_simple, blk_test1, blk_test2) = (blk_file.get_subblock(n) for n in ("SIMPLE2", "TEST1", "TEST2"))

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
    blk_blk.config.enable_autotags = False
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
    blk_col.config.enable_autotags = False
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

    blk_file = Block(abs_path("data/fill_tmpl.txt"))
    blk_file.fill(data)
    blk_file.save_content(abs_path("data/fill_gen.txt"))

    assert compare_files("data/fill_gen.txt", "data/fill_exp.txt")


def test_shoplist() -> None:
    template = """
                SHOPPING LIST
  Items                             Quantity
--------------------------------------------
<ITEMS>
<FLAG>IMPORTANT! <^FLAG>MAYBE? </FLAG>
* <@FLAG><ITEM><+>                  <QTY><UNIT> kg<^UNIT> l</UNIT>
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
  Items                             Quantity
--------------------------------------------
* apples                            1 kg
* IMPORTANT! potatoes               2 kg
* rice                              1 kg
* orange juice                      1 l
* MAYBE? cooking magazine


Short list: apples, potatoes, rice, orange juice, cooking magazine
"""


def test_shoplist_custom_cfg() -> None:
    template = """
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
        "---",                      # tag_implct_iter
        "&",                        # autotag_blk_var
        ">>",                       # autotag_align
        "_",                        # autotag_vari
        "-",                        # subref_sep
        8,                          # tab_size
        True,                       # enable_autotags
    )

    blk = Block(template, config=config)
    blk.fill(data)
    assert blk.content == """
                SHOPPING LIST
  Items                             Quantity
--------------------------------------------
* apples                            1 kg
* IMPORTANT! potatoes               2 kg
* rice                              1 kg
* MAYBE? cooking magazine
* orange juice                      1 l


Short list: apples, potatoes, rice, cooking magazine, orange juice
"""


def test_subrefs() -> None:
    template = """
<A>
    <AA><*>,</AA>
    <AB>
        <AB_VA>
        <A.AA><*>+</A.AA>
        <ABA>
            <ABA_VA>
        </ABA>
        <ABA.ABA_VA>
    </AB>
    <AB.ABA><ABA_VA></AB.ABA>
</A>
<B>
    <B_VA>
    <A.AB.AB_VA>
</B>
<VA>
"""

    data = {
        "a": {
            "aa": ["aa_val1", "aa_val2", "aa_val3"],
            "ab": {
                "ab_va": "ab_va_val",
                "aba": {
                    "aba_va": "aba_va_val"
                }
            }
        },
        "b": {
            "b_va": "b_va_val"
        },
        "va": "va_val"
    }

    blk = Block(template)
    blk.fill(data)
    assert blk.content == """
    aa_val1,aa_val2,aa_val3,
        ab_va_val
        aa_val1+aa_val2+aa_val3+
            aba_va_val
        aba_va_val
    aba_va_val
    b_va_val
    ab_va_val
va_val
"""


def test_backrefs() -> None:
    template = """
<A>
    <A_VA>
    <AA>
        <AA_VA>
    </AA>
    <AB>
        <AB_VA>
    </AB>
    <A_VB>
    <A_VC>
</A>
<B>
    <B_VA>
    <B_VB>
    <B_VC>
    <B_VD>
</B>
"""

    data = {
        "a": {
            "a_va": "a_va_val",
            "aa": {"aa_va": "<A.A_VA>"},
            "ab": {"ab_va": "<A.AA.AA_VA>"},
            "a_vb": "<AA.AA_VA>",
            "a_vc": "<A_VB>"
        },
        "b": {
            "b_va": "b_va_val",
            "b_vb": "<B_VA>",
            "b_vc": "<A.A_VA>",
            "b_vd": "<A.AB.AB_VA>"
        },
    }

    blk = Block(template)
    blk.fill(data)
    assert blk.content == """
    a_va_val
        a_va_val
        a_va_val
    a_va_val
    a_va_val
    b_va_val
    b_va_val
    a_va_val
    a_va_val
"""


def test_blk_vars() -> None:
    template = """
<V_LIST>
<A>
numbers
<^A>
lowercase letters
<^A>
uppercase letters
</A>
<V><*><.>, <^.></.></V>
<@A>: <@V><+>                           (<DESC>)
<@V>
</V_LIST>
"""

    data = {
        "v_list": [
            {"v": [1, 2, 3], "a": 0, "desc": "1-3"},
            {"v": ["a", "b", "c"], "a": 1, "desc": "a-c"},
            {"v": ["A", "B", "C", "D", "E"], "a": 2, "desc": "A-E"}
        ]
    }

    blk = Block(template)
    blk.fill(data)
    assert blk.content == """
numbers: 1, 2, 3                        (1-3)
1, 2, 3
lowercase letters: a, b, c              (a-c)
a, b, c
uppercase letters: A, B, C, D, E        (A-E)
A, B, C, D, E
"""


def test_multiline_var() -> None:
    template = """  <TEXT1>
<TEXT2>
        <TEXT3>
    a   <TEXT3>"""
    blk = Block(template)
    blk.fill({
        "text1": "text 1 - line 1\ntext 1 - line 2",
        "text2": "text 2 - line 1\ntext 2 - line 2\ntext 2 - line 3",
        "text3": "text 3 - line 1\ntext 3 - line 2\ntext 3 - line 3"})
    assert blk.content == """  text 1 - line 1
  text 1 - line 2
text 2 - line 1
text 2 - line 2
text 2 - line 3
        text 3 - line 1
        text 3 - line 2
        text 3 - line 3
    a   text 3 - line 1
text 3 - line 2
text 3 - line 3"""


def test_macros_1() -> None:
    template = """
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

    def ref_blk_hndl(block: Block, data: dict, _clone_subidx: int) -> None:
        # Set this block template to the template of a macro block defined in the first part of this block name.
        block.template = block.parent.get_subblock("macros").get_subblock(block.name.split("_")[0]).template

    blk = Block(template)
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
    assert blk.content == """
PC hardware:
- case
- display
- keyboard
- mouse

fruits:
apple, banana, orange

vegetables:
carrot, tomatoe, pepper

"""


def test_macros_2() -> None:
    template = """
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

    def ref_blk_hndl(block: Block, data: dict, _clone_subidx: int) -> None:
        # Set the 'ref_blk' variable value to the template of the block defined by the 'ref' data attribute.
        block.set_variables(ref_blk=block.parent.get_subblock("macros").get_subblock(data.get("ref", "")).template)

    blk = Block(template)
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
    assert blk.content == """
PC hardware:
- case
- display
- keyboard
- mouse

fruits:
apple, banana, orange

vegetables:
carrot, tomatoe, pepper


"""


def test_extensions_1() -> None:
    template = """
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

    def ext_blk_hndl(block: Block, _data: dict, _clone_subidx: int) -> None:
        # Get the block with extensions from the 'extensions' subblock.
        blk_extensions = block.get_subblock("extensions")
        if isinstance(blk_extensions, Block):
            # Loop through block names defined in the 'EXT_BLKS' block content.
            for ext_blk_name in blk_extensions.get_subblock("ext_blks").content.split(","):
                # Replace the subblocks of this block with the templates of block extensions.
                block.get_subblock(ext_blk_name).template = blk_extensions.get_subblock(ext_blk_name).template

    blk = Block(template)
    blk.fill({
        "fill_hndl": ext_blk_hndl,
        "intro": {"desc": "PC hardware"},
        "items": ["case", "display", "keyboard", "mouse"],
        "outro": {"NUM": 4},
        "extensions": None})
    assert blk.content == """
+--------------------------+
| My list of PC hardware   |
+--------------------------+

* case
* display
* keyboard
* mouse

There are 4 items in total.

"""


def test_extensions_2() -> None:
    template = """
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

    def ext_blk_hndl(block: Block, data: dict, _clone_subidx: int) -> None:
        # Loop through extended block names defined in the 'ext_blk_names' data attribute.
        for name in data.get("ext_blk_names", ""):
            # Replace this block template with the template of a subblock within the 'ext_blks' Block data attrib.
            block.get_subblock(name).template = data.get("ext_blks", Block()).get_subblock(name).template

    blk = Block(template)
    blk.fill({
        "fill_hndl": ext_blk_hndl,
        "ext_blks": Block(extensions),
        "ext_blk_names": ("intro", "items"),
        "intro": {"desc": "PC hardware"},
        "items": ["case", "display", "keyboard", "mouse"],
        "outro": {"NUM": 4}})
    assert blk.content == """
+--------------------------+
| My list of PC hardware   |
+--------------------------+

* case
* display
* keyboard
* mouse

There are 4 items in total.
"""


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

    data = {
        "books":
        [
            {
                "title": {"english": "Robur the Conqueror", "original": "Robur-le-Conquérant"},
                "author":
                {
                    "name": "Jules", "surname": "Verne", "period": {"birth": 1828, "death": 1905},
                    "full_info": "<AUTHOR><NAME> <SURNAME> (<PERIOD.BIRTH>-<PERIOD.DEATH>)</AUTHOR>"
                },
                "genre": "science fiction novel",
                "publication":
                {
                    "isbn": "3750246963", "publisher": "epubli",
                    "date": {"year": 2019, "month": 10, "day": 29},
                    "language": "english", "page_num": 184
                }
            },
            {
                "title": {"english": "I, Robot", "original": ""},
                "author":
                {
                    "name": "Isaac", "surname": "Asimov", "period": {"birth": 1920, "death": 1992},
                    "full_info": "<AUTHOR><NAME> <SURNAME> (<PERIOD.BIRTH>-<PERIOD.DEATH>)</AUTHOR>"
                },
                "genre": "science fiction short stories",
                "publication":
                {
                    "isbn": "0008279551", "publisher": "HarperCollins",
                    "date": {"year": 2018, "month": 5, "day": 1},
                    "language": "english", "page_num": 256
                }
            }
        ]
    }

    for book in data["books"]:
        book["title"]["original_wrap"] = bool(book["title"].get("original", ""))

    blk = Block(template)
    blk.fill(data)
    assert blk.content == """
+------------------------------------------------------------------------------+
| Robur the Conqueror (Robur-le-Conquérant) - Jules Verne (1828-1905)          |
+------------------------------------------------------------------------------+
| Genre     | science fiction novel                                            |
| Published | 29.10.2019                                                       |
| ISBN      | 3750246963                                                       |
| Publisher | epubli                                                           |
| Language  | english                                                          |
| Pages     | 184                                                              |
+------------------------------------------------------------------------------+

+------------------------------------------------------------------------------+
| I, Robot - Isaac Asimov (1920-1992)                                          |
+------------------------------------------------------------------------------+
| Genre     | science fiction short stories                                    |
| Published | 1.5.2018                                                         |
| ISBN      | 0008279551                                                       |
| Publisher | HarperCollins                                                    |
| Language  | english                                                          |
| Pages     | 256                                                              |
+------------------------------------------------------------------------------+

"""


if __name__ == "__main__":
    test_shoplist_custom_cfg()
    test_macros_2()
    test_extensions_2()
