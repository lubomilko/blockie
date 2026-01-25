.. _tgt_man_fill:

###################################################################################################
Manual template filling
###################################################################################################

***************************************************************************************************
Block object methods
***************************************************************************************************

The :py:class:`.Block` object allows to perform direct manual operations with the template
:ref:`variables and blocks <tgt_tags>` using its attributes and methods described in the
:ref:`API <tgt_api>` section.

-   :py:class:`.Block` **attributes**:

    -   :py:attr:`.Block.template`: The text template of the block containing other subblocks and
        variables.
    -   :py:attr:`.Block.content`: The text content generated from the template by the
        :py:class:`.Block` methods.
    -   :py:attr:`.Block.name`: The name corresponding to the name of the block tags.

-   :py:class:`.Block` **methods**:

    -   :py:meth:`.Block.fill`: Fills the block template in a semi-automated way using the
        provided input data, as described in the :ref:`Data-driven template filling
        <tgt_data_fill>` section.
    -   :py:meth:`.Block.get_subblock`: Loads a child block from this block's content into another
        :py:class:`.Block` object.
    -   :py:meth:`.Block.set_variables`: Sets the variables within the content of this block to
        the specified values.
    -   :py:meth:`.Block.set` and :py:meth:`.Block.set_subblock`: Sets the finalized block content
        into the content of its parent block.
    -   :py:meth:`.Block.clone`: Duplicates the block template.
    -   :py:meth:`.Block.clear_variables`: Removes the variables from the content of this block.
    -   :py:meth:`.Block.clear`: Removes the content of this block from its parent block content.
    -   :py:meth:`.Block.reset`: Resets the block content to its template.

The following example illustrates the use of :py:class:`.Block` object methods to fill the
template manually.

.. code-block:: python

    template = """
                SHOPPING LIST
      Items                             Quantity
    --------------------------------------------
    <ITEMS>
    <FLAG>IMPORTANT! <^FLAG>MAYBE? </FLAG>
    * <@FLAG><ITEM><+>                  <QTY><UNIT> kg<^UNIT> l</UNIT>
    </ITEMS>
    """

    #   flag, item,               qty, unit
    data = (
        ("",  "apples",           "1", 0),
        ("!", "potatoes",         "2", 0),
        ("",  "rice",             "1", 0),
        ("",  "orange juice",     "1", 1),
        ("?", "cooking magazine", "", -1)
    )

    blk_template = blockie.Block(template)
    blk_items = blk_template.get_subblock("items")
    [blk_flag, blk_unit] = [blk_items.get_subblock(n) for n in ("flag", "unit")]

    for item_data in data:
        blk_items.set_variables(item=item_data[1], qty=item_data[2])
        blk_flag.set(0 if item_data[0] == "!" else 1 if item_data[0] == "?" else -1)
        blk_unit.set(item_data[3])
        blk_items.clone()
    blk_items.set()
    print(blk_template.content)

Output:

.. code-block:: text

                    SHOPPING LIST
      Items                             Quantity
    --------------------------------------------
    * apples                            1 kg
    * IMPORTANT! potatoes               2 kg
    * rice                              1 kg
    * orange juice                      1 l
    * MAYBE? cooking magazine

Filling the templates manually is typically not needed and a :ref:`data-driven approach
<tgt_data_fill>` should be preferred. However, using the :py:class:`.Block` object methods allows
to implement more complex operations and custom :ref:`extensions <tgt_extensions>` that are not
possible with the :py:meth:`.Block.fill` method alone.


.. _tgt_fill_hndl:

***************************************************************************************************
Fill handler
***************************************************************************************************

Template :ref:`blocks <tgt_tags>` filled using the :py:meth:`.Block.fill` method can have a
custom function assigned for performing special :ref:`manual operations <tgt_man_fill>` with the
block content. This function can be assigned within the :ref:`dictionary defining the block
content values <tgt_set_blk_cont>` by the special ``fill_hndl`` key with a value of a function
having the following signature:

.. code-block:: python

    (block: Block, data: dict | object, clone_subidx: int) -> None

The example below shows a simple ``format_date`` fill handler function setting the required
date format based on the format of a month value specified in the input data (i.e., whether the
month is specified using its name or number).

.. code-block:: python

    def format_date(block: blockie.Block, data: dict, _clone_subidx: int) -> None:
        if isinstance(data["month"], str) and not data["month"].isdigit():
            # If month is specified by its name,
            # then make it uppercase and set the date format to: <MONTH> <DAY>
            data["month"] = data["month"].upper()
            block.get_subblock("date").set(vari_idx=1)
        else:
            # Set the date format to: <DAY>.<MONTH>.
            block.get_subblock("date").set(vari_idx=0)
   
    blk = blockie.Block("The date is: <DATE><DAY>.<MONTH>.<^DATE><MONTH> <DAY></DATE>")
    blk.fill({"day": 24, "month": "December", "fill_hndl": format_date})
    print(blk.content)

Output:

.. code-block:: text

    The date is: DECEMBER 24


.. _tgt_extensions:

***************************************************************************************************
Custom extensions
***************************************************************************************************

The following subsections provide examples of useful custom extensions created using the
:ref:`manual filling methods <tgt_man_fill>` and :ref:`fill handler <tgt_fill_hndl>` of the
:py:class:`.Block` object. The examples should serve as an inspiration for further experimentation
and creation of other features.

Template macros
===================================================================================================

.. code-block:: python

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

    def ref_blk_hndl(block: blockie.Block, _data: dict, _clone_subidx: int) -> None:
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

Output:

.. code-block:: text

    PC hardware:
    - case
    - display
    - keyboard
    - mouse

    fruits:
    apple, banana, orange

    vegetables:
    carrot, tomatoe, pepper


.. code-block:: python

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

Output:

.. code-block:: text

    PC hardware:
    - case
    - display
    - keyboard
    - mouse

    fruits:
    apple, banana, orange

    vegetables:
    carrot, tomatoe, pepper


Template extensions
===================================================================================================

.. code-block:: python

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

Output:

.. code-block:: text

    +--------------------------+
    | My list of PC hardware   |
    +--------------------------+

    * case
    * display
    * keyboard
    * mouse

    There are 4 items in total.


.. code-block:: python

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

Output:

.. code-block:: text

    +--------------------------+
    | My list of PC hardware   |
    +--------------------------+

    * case
    * display
    * keyboard
    * mouse

    There are 4 items in total.
