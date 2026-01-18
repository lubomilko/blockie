###################################################################################################
Filling the template tags
###################################################################################################

.. _tgt_variables:

***************************************************************************************************
Variable tags
***************************************************************************************************

Variables are the simplest parts of the template consisting of a single tag, e.g., ``<NAME>``.

*Operations*:

-   **Set**: A variable can be set to the specified value of a **basic data type** (``str``,
    ``int``, ``float``, or ``bool``).

    .. code-block:: python

        blk = blockie.Block("<WORD1> <WORD2>!")
        blk.fill({"word1": "Hello", "word2": "world"})
        print(blk.content)

    prints::

        Hello world!

-   **Clear**: A variable can be cleared, i.e., removed, by setting it to an **empty string or
    none** (``""``, ``None``).

    .. code-block:: python

        blk = blockie.Block("<NAME> <MIDNAME> <SURNAME>")
        blk.fill({"name": "Patrick", "midname": None, "surname": "Bateman"})
        print(blk.content)

    prints::

        # Patrick  Bateman


.. _tgt_blocks:

***************************************************************************************************
Block tags
***************************************************************************************************

    Set - non-empty val / Dict
    Clone
    Clear


.. _tgt_special_tags:

***************************************************************************************************
Special tags
***************************************************************************************************

    Implicit iterator block variable
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
