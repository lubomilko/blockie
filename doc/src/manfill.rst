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


Filling the whole templates manually is typically not needed and a :ref:`data-driven approach
<tgt_data_fill>` should be preferred. However, the :ref:`block fill handler <tgt_fill_hndl>`
can be utilized to perform more complex manual operations or to implement custom :ref:`extensions
<tgt_extensions>` that are not possible with the :py:meth:`.Block.fill` method alone.

The example below shows the use of :py:meth:`.Block.get_subblock` and :py:meth:`.Block.set`
methods within the :ref:`block fill handler <tgt_fill_hndl>`:

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
    blk.fill({"day": 24, "month": 12, "fill_hndl": format_date})
    print(blk.content)

Output:

.. code-block:: text

    The date is: 24.12.
