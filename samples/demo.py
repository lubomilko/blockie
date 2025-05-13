# pylint: disable = missing-module-docstring, missing-class-docstring, missing-function-docstring

import sys
from pathlib import Path


sys.path.insert(0, str(Path(Path(__file__).parent.parent, "src").resolve()))

from blockie import Block    # pylint: disable = wrong-import-position   # noqa E402


def demo_item_list_essential() -> None:
    # Define template string.
    tmpl_str = "\n".join((
        "List of items:",
        "<ITEMS>",
        "* <ITEM>",
        "</ITEMS>"))

    # Define the main Block object and set its template string.
    blk_main = Block()
    blk_main.template = tmpl_str
    # Define anothe Block object corresponding to the template block marked by the ITEMS tags.
    # From now on the Block objects are referred to only as "blocks".
    blk_items = blk_main.get_subblock("ITEMS")

    for item_name in ("apples", "oranges", "bananas"):
        # Set value for a template variable marked by the ITEM tag.
        blk_items.set_variables(ITEM=item_name)
        # Clone the content of the ITEMS Block object to allow setting of another ITEM variable.
        blk_items.clone()
    # Set the filled ITEMS block into its parent main block.
    blk_items.set()

    # Print the main block content with filled ITEMS block. Outputs the following string:
    # List of items:
    # * apples
    # * oranges
    # * bananas
    print(f"{blk_main.content}")


def demo_item_lists() -> None:
    item_names = (
        ("red apples", "green apples"),
        ("oranges",),
        ("carrots", "peppers", "tomatoes"),
        ("eggs",),
        ("pen", "pencil"))

    item_numbers = ("2 kg each", 5, "", 10, "")

    blk_file = Block(template="samples/template_item_lists.txt")

    blk_items = blk_file.get_subblock("ITEMS_1")
    blk_items_row = blk_items.get_subblock("ITEMS_ROW")
    for row_names in item_names:
        for name in row_names:
            blk_items_row.set_variables(autoclone=True, ITEM=name)
        blk_items_row.set()
        blk_items.clone()
    blk_items.set()

    blk_items = blk_file.get_subblock("ITEMS_2")
    blk_items_row = blk_items.get_subblock("ITEMS_ROW")
    for row_names in item_names:
        for name in row_names:
            blk_items_row.set_variables(autoclone=True, ITEM=name)
        blk_items_row.set()
        blk_items.clone()
    blk_items.set()

    blk_items = blk_file.get_subblock("ITEMS_3")
    blk_items_row = blk_items.get_subblock("ITEMS_ROW")
    for (i, row_names) in enumerate(item_names):
        for name in row_names:
            blk_items_row.set_variables(autoclone=True, ITEM=name)
        blk_items_row.set()
        blk_items.set_variables(NUM=item_numbers[i])
        blk_items.clone()
    blk_items.set()

    blk_items = blk_file.get_subblock("ITEMS_4")
    blk_items_row = blk_items.get_subblock("ITEMS_ROW")
    blk_items_row.set_variables(ITEM="ITEM NAME")
    blk_items_row.set()
    blk_items.set_variables(NUM="NUMBER")
    blk_items.clone()
    for (i, row_names) in enumerate(item_names):
        for name in row_names:
            blk_items_row.set_variables(autoclone=True, ITEM=name)
        blk_items_row.set()
        blk_items.set_variables(SEP=f"{32*' .'}", NUM=item_numbers[i])
        blk_items.clone()
    blk_items.set()

    blk_file.save_content("samples/generated_item_lists.txt")


def demo_dict_fill() -> None:
    blk_data = {
        "to_set": 1,
        "to_clear": 0,
        "struct_name": "SOME_STRUCT_T",
        "members": (
            {"type": {"vari_idx": 0, "t": "UNSIGNED8"}, "name": "u8Var", "arr": None},
            {"type": {"vari_idx": 1, "t": "UNSIGNED16"}, "name": "au16Var", "arr": {"size": 10}},
            {"type": {"vari_idx": 2, "t": "SIGNED8"}, "name": "ps8Var", "arr": None},
            {"type": {"vari_idx": 3, "t": "SIGNED16"}, "name": "aps16Var", "arr": {"size": 20}},
            {"type": {"vari_idx": -1}, "name": "InvalidVar1", "arr": None},
            {"type": {"vari_idx": False}, "name": "InvalidVar2", "arr": None},
            {"type": None, "name": "InvalidVar3", "arr": None},
            {"type": {}, "name": "InvalidVar4", "arr": None})}

    blk_file = Block(template="samples/template_dict_fill.txt")
    blk_file.fill(blk_data)
    blk_file.save_content("samples/generated_dict_fill.txt")


def main() -> None:
    demo_item_list_essential()
    demo_item_lists()
    demo_dict_fill()


if __name__ == "__main__":
    main()
