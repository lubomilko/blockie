###################################################################################################
Usage
###################################################################################################

***************************************************************************************************
Template tags
***************************************************************************************************

Tags are used to indicate the variable parts of the template intended to be filled with specific
values provided in the input data.

By default, the tags have an XML-like format and their names use uppercase letters. The template
consists of two primary elements:

-   :ref:`Variables <tgt_variables>` defined by a single tag, e.g., ``<NAME>``.
-   :ref:`Blocks <tgt_blocks>` defined by the two start and end tags, e.g., ``<LIST> ... </LIST>``,
    with a content consisting of other blocks and variables between these tags. The whole template
    is also considered to be a block despite not having any explicitly defined start and end tags.


***************************************************************************************************
Template filling
***************************************************************************************************

The most straightforward way to fill the template with values is to load the template into the
:py:class:`.Block` object through its constructor or a :py:attr:`.Block.template` attribute and
to use the :py:meth:`.Block.fill` method with an input data dictionary having keys
corresponding to the template tag names. The template tags are then replaced with the dictionary
values in the generated :py:attr:`.Block.content` attribute of the :py:class:`.Block` object.

The tag references in the input data and Python filling script can use lowercase letters that
are by default automatically converted to the uppercase tag names in the template, e.g.,
a ``name`` data attribute is used to set the value of a ``<NAME>`` template tag.

.. important::

    The tag format and automatic uppercase conversion described above is used in almost all
    examples within this document together with a Python dictionary used as a data input. However,
    the tag format is :ref:`configurable <tgt_config>` and instead of a dictionary, it is also
    possible to use a struct-like object with attributes corresponding to the dictinary keys.


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
