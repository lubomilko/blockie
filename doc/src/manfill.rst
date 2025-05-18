.. _tgt_manual_fill:

###################################################################################################
Manual template filling
###################################################################################################

.. note::
    Filling the templates manually is not needed in a vast majority of common use cases and an
    :ref:`automated process <tgt_auto_fill>` described before should be preferred.

    The manual template filling process also requires a deeper knowledge of blockie and a
    description of all aspects of this process is beyond the current scope of this document.
    However, the examples in this chapter show some of the basic principles and further reading
    of the :ref:`API <tgt_api>` and experimentation is encouraged.

The manual generation of content provides more low-level control over the way the data are being
filled into the template and allows to perform certain special operations that are otherwise not
possible. It relies on a manual execution of mainly the following :py:class:`.Block` methods
in a template filling script:

*   :py:meth:`.Block.get_subblock`: Loading a block from a template into the :py:class:`.Block`
    object.
*   :py:meth:`.Block.set_variables`: Setting variable values. 
*   :py:meth:`.Block.set` and :py:meth:`.Block.set_subblock`: Setting the content of blocks into
    the generated content.
*   :py:meth:`.Block.clone`: Cloning the content of a block.
*   :py:meth:`.Block.clear_variables`: Removing variable from the generated content.
*   :py:meth:`.Block.clear` and :py:meth:`.Block.clear_subblock`: Removing blocks from the
    generated content.


***************************************************************************************************
Examples
***************************************************************************************************

The following examples briefly illustrate the manual template filling process.

Example 1
===================================================================================================

.. code-block:: python

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

Generated content output:

.. code-block:: text

                                SHOPPING LIST
      Items                                                         Quantity
    ------------------------------------------------------------------------
    * apples                                                        1 kg
    * IMPORTANT! potatoes                                           2 kg
    * rice                                                          1 kg
    * orange juice                                                  1 l
    * MAYBE? cooking magazine


Example 2
===================================================================================================

.. code-block:: python

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

Generated content output:

.. code-block:: text

                                SHOPPING LIST
      Items                                                         Quantity
    ------------------------------------------------------------------------
    * apples                                                        1 kg
    * potatoes                                                      2 kg
    * rice                                                          1 kg
    * orange juice                                                  1 l
    * cooking magazine


Example 3
===================================================================================================

.. code-block:: python

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

Generated content output:

.. code-block:: text

                                SHOPPING LIST
      Items                                                         Quantity
    ------------------------------------------------------------------------
    * apples                                                        1 kg
    * potatoes                                                      2 kg
    * rice                                                          1 kg
    * orange juice                                                  1 l
    * cooking magazine
