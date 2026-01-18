###################################################################################################
Template tags and operations with them
###################################################################################################

Tags are used to indicate the variable parts of the template intended to be filled with specific
values provided in the input data.

By default, the tags have an XML-like format and they use uppercase letters for names, e.g.,
``<NAME>``. The tag references in the input data and Python filling script can use lowercase
letters that are automatically converted to the uppercase tag names in the template, e.g.,
a ``name`` data attribute is used to set the value of a ``<NAME>`` template tag.

The most straightforward way to work with tags is to use an input data dictionary or an object
with key (or attribute) names corresponding to the template tag names. The data values are then
used to fill the template, i.e., replace the tags with the specified values.

.. important::

    The tag format and automatic uppercase conversion described above is used in almost all
    examples within this document together with a Python dictionary used as a data input.
    However, the tag format is :ref:` configurable <tgt_config>` and the dictionaries can be
    replaced with struct-like objects with attributes corresponding to the dictinary keys.


***************************************************************************************************
Variables
***************************************************************************************************

Variables are the simplest parts of the template consisting of a single tag.

Operations:

- **Set value** using a **basic data type** (``str``, ``int``, ``float``, or ``bool``).
- **Clear value** using a **basic data type** (``str``, ``int``, ``float``, or ``bool``).

.. code-block:: python

    blk = blockie.Block("<WORD1> <WORD2>!")
    blk.fill({"word1": "Hello", "word2": "world"})
    print(blk.content)

prints:

.. code-block:: text

    Hello world!



Clearing a variable
===================================================================================================

A variable can be cleared, i.e., removed, from the generated content by setting its dictionary value to an
**empty string or to none** as shown on the example below removing the variable for a middle name.

.. code-block:: python

    blk = blockie.Block("<NAME> <MIDNAME> <SURNAME>")
    blk.fill({"name": "Patrick", "midname": None, "surname": "Bateman"})
    print(blk.content)

prints:

.. code-block:: text

    Patrick  Bateman

***************************************************************************************************
Blocks
***************************************************************************************************

    Set - non-empty val / Dict
    Clone
    Clear


***************************************************************************************************
Special tags
***************************************************************************************************

    Implicit iterator block variable
    Block variation - vari_idx / integer


***************************************************************************************************
Automatic tags
***************************************************************************************************

    block var
    align
    variation


***************************************************************************************************
Fill handler
***************************************************************************************************
