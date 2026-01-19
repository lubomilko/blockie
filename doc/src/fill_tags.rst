###################################################################################################
Filling the template tags
###################################################################################################

.. _tgt_variables:

***************************************************************************************************
Variable tags
***************************************************************************************************

Variables are the simplest parts of the template defined by a single tag, e.g., ``<NAME>``.

-   A variable can be **set** to the required value using a **basic data type** (``str``, ``int``,
    ``float``, or ``bool``).

    .. code-block:: python

        blk = blockie.Block("<WORD1> <WORD2>!")
        blk.fill({"word1": "Hello", "word2": "world"})
        print(blk.content)

    Output:

    .. code-block:: text

        Hello world!

-   A variable can be **cleared**, i.e., removed, by setting it to an **empty string or none**
    (``""``, ``None``).

    .. code-block:: python

        blk = blockie.Block("<NAME> <MIDNAME> <SURNAME>")
        blk.fill({"name": "Thomas", "midname": None, "surname": "Anderson"})
        print(blk.content)

    Output:

    .. code-block:: text

        Thomas  Anderson


.. _tgt_blocks:

***************************************************************************************************
Block tags
***************************************************************************************************

Blocks are used for splitting the template into multiple hierarchical parts. A block is defined
by the two start and end tags, e.g., ``<LIST> ... </LIST>`` with a content between them consisting
of constant text, other child blocks and :ref:`variables <tgt_variables>`. The whole template is
considered to be a primary block even without explicitly defined tags.

-   The variables and other subblocks in a block content can be **set** by setting the
    block value to a **non-empty dictinary** (``dict``).

    .. code-block:: python

        blk = blockie.Block("The date is: <DATE><MONTH> <DAY></DATE>")
        blk.fill({"date": {"day": 24, "month": "December"}})
        print(blk.content)

    Output:

    .. code-block:: text

        The date is: December 24

-   The block content can be **set unchanged** into its parent block by setting it to an
    **essentially true value of a basic data type** (non-empty ``str``, non-zero ``int``,
    non-zero ``float``, ``True``).

    .. code-block:: python

        blk = blockie.Block("The date is: <DATE>July 2</DATE>")
        blk.fill({"date": True})
        print(blk.content)

    Output:

    .. code-block:: text

        The date is: July 2

-   It is possible to **clone**, i.e., duplicate, the block content by setting its value to
    a **list or tuple of non-empty dictionaries** (``[{...}, {...}, ...]``,
    ``({...}, {...}, ...)``).

    .. code-block:: python

        blk = blockie.Block("* <EVENTS><EVENT>: <MONTH> <DAY>\n</EVENTS>")
        blk.fill({"events": [
            {"event": "Christmas", "day": 24, "month": "December"},
            {"event": "New Year's Eve", "day": 31, "month": "December"},
            {"event": "New Year's Day", "day": 1, "month": "January"}]})
        print(blk.content)

    Output:

    .. code-block:: text
    
        * Christmas: December 24
        * New Year's Eve: December 31
        * New Year's Day: January 1

-   A block can be **cleared**, i.e., removed, by setting it to either an **empty dictionary,
    list or tuple** (``{}``, ``[]``, ``()``), or to **none, negative number or false** (``None``,
    negative ``int``, negative ``float``, ``False``).

    .. code-block:: python

        blk = blockie.Block("<NAME> <MIDNAME_WRAP><MIDNAME> </MIDNAME_WRAP><SURNAME>")
        blk.fill({"name": "Thomas", "surname": "Anderson", "midname_wrap": None})
        print(blk.content)

    Output:

    .. code-block:: text

        Thomas Anderson

.. _tgt_special_tags:

***************************************************************************************************
Special tags
***************************************************************************************************

-   I Implicit iterator block variable

    Block variation - vari_idx / integer


.. _tgt_autotags:

***************************************************************************************************
Automatic tags
***************************************************************************************************

    block var
    align
    variation


.. _tgt_fill_hndl:

***************************************************************************************************
Fill handler
***************************************************************************************************
