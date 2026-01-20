###################################################################################################
Filling the template tags
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
primary :py:class:`.Block` object through its constructor or a :py:attr:`.Block.template`
attribute and to use the :py:meth:`.Block.fill` method with an input data dictionary having keys
corresponding to the template tag names. The template tags are then replaced with the dictionary
values in the generated :py:attr:`.Block.content` attribute of the :py:class:`.Block` object.

The tag references in the input data and Python filling script can use lowercase letters that
are by default automatically converted to the uppercase tag names in the template, e.g.,
a ``month`` data attribute (dictionary key) is used to set the value of a ``<MONTH>`` variable
in the example below.

.. code-block:: python

    import blockie

    blk = blockie.Block("The date is: <DATE><MONTH> <DAY></DATE>")
    blk.fill({"date": {"day": 24, "month": "December"}})
    print(blk.content)

output:

.. code-block:: text

    The date is: December 24

.. important::

    The tag format and automatic uppercase conversion described above is used in almost all
    examples within this document together with a Python dictionary used as a data input. However,
    the tag format is :ref:`configurable <tgt_config>` and instead of a dictionary, it is also
    possible to use a struct-like object with attributes corresponding to the dictionary keys.


.. _tgt_variables:

***************************************************************************************************
Variables
***************************************************************************************************

Variables are the simplest parts of the template defined by a single tag, e.g., ``<NAME>``.


Setting variable value
===================================================================================================

A variable can be **set** to the required value using a **basic data type** (``str``, ``int``,
``float``, or ``bool``).

.. code-block:: python

    blk = blockie.Block("<WORD1> <WORD2>!")
    blk.fill({"word1": "Hello", "word2": "world"})
    print(blk.content)

Output:

.. code-block:: text

    Hello world!


Clearing variable
===================================================================================================

A variable can be **cleared**, i.e., removed, by setting it to an **empty string or none**
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
Blocks
***************************************************************************************************

Blocks are used for splitting the template into multiple hierarchical parts. A block is defined
by the two start and end tags, e.g., ``<LIST> ... </LIST>`` with a content between them consisting
of constant text, other child blocks and :ref:`variables <tgt_variables>`. The whole template is
considered to be a primary block even without explicitly defined tags.


Setting block content
===================================================================================================

The variables and other subblocks in a block content can be **set** by setting the block value to
a **non-empty dictionary** (``dict``) with keys representing the inner variables and blocks.

.. code-block:: python

    blk = blockie.Block("The date is: <DATE><MONTH> <DAY></DATE>")
    blk.fill({"date": {"day": 24, "month": "December"}})
    print(blk.content)

Output:

.. code-block:: text

        The date is: December 24

The block content can be **set unchanged** into its parent block by setting it to an **essentially
true value of a basic data type** (non-empty ``str``, non-zero ``int``, non-zero ``float``,
``True``).

.. code-block:: python

    blk = blockie.Block("The date is: <DATE>July 2</DATE>")
    blk.fill({"date": True})
    print(blk.content)

Output:

.. code-block:: text

    The date is: July 2


Block content cloning
===================================================================================================

It is possible to **clone**, i.e., duplicate, the block content by setting its value to a **list
or tuple of non-empty dictionaries** (``[{...}, {...}, ...]``, ``({...}, {...}, ...)``) with the
content of dictionaries setting other blocks and :ref:`variables <tgt_variables>` within the block.

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

A block can also be **cloned with an implicit iterator variable** which is a special single-only
variable defined by the ``<*>`` tag that can be set directly using a **list or tuple of basic
data type** values (``str``, ``int``, ``float``, or ``bool``) without specifying any :ref:`variable
<tgt_variables>` name or block content dictionary.

.. code-block:: python

    blk = blockie.Block("<LIST>- <*>\n</LIST>")
    blk.fill({"list": ["gloves", "plastic bags", "duct tape", "shovel"]})
    print(blk.content)

Output:

.. code-block:: text

    - gloves
    - plastic bags
    - duct tape
    - shovel


.. _tgt_set_blk_cont_var:

Setting a block content variation
===================================================================================================

It is possible to define multiple **content variations of a block** using intermediary tags with
a ``<^BLOCK_NAME>`` format inserted between the start and end block tags. The required content
variation can be selected by setting an integer (``int``) index of a variation (starting from 0)
to the special ``vari_idx`` key defined within the block data dictionary.

.. code-block:: python

    blk = blockie.Block("The date is: <DATE><DAY>.<MONTH>.<^DATE><MONTH> <DAY></DATE>")
    blk.fill({"date": {"vari_idx": 0, "day": 24, "month": 12}})
    print(blk.content)

Output:

.. code-block:: text

    The date is: 24.12.

If no variables or subblocks need to be set in a block content, then the content variation can be
selected by directly setting the content variation index integer as a block value.

.. code-block:: python

    blk = blockie.Block("The date is: <DATE>24.12.<^DATE>December 24</DATE>")
    blk.fill({"date": 1})
    print(blk.content)

Output:

.. code-block:: text

    The date is: December 24

.. important::
    The blocks with content variations cannot be cloned. They can, however, be cloned
    indirectly by wrapping them in a standard parent block that can be cloned, e.g.,
    ``<DATE_WRAP><DATE><DAY>.<MONTH>.<^DATE><MONTH> <DAY></DATE><DATE_WRAP>``.


Clearing a block
===================================================================================================

A block can be **cleared**, i.e., removed, by setting it to either an **empty dictionary, list or
tuple** (``{}``, ``[]``, ``()``), or to **none, negative number or false** (``None``, negative
``int``, negative ``float``, ``False``).

.. code-block:: python

    blk = blockie.Block("<NAME> <MIDNAME_WRAP><MIDNAME> </MIDNAME_WRAP><SURNAME>")
    blk.fill({"name": "Thomas", "surname": "Anderson", "midname_wrap": None})
    print(blk.content)

Output:

.. code-block:: text

    Thomas Anderson

A block can be cleared also by setting its :ref:`content variation <tgt_set_blk_cont_var>` index
(``int``) to a negative value.


.. _tgt_auto_block_var:

***************************************************************************************************
Automatic block variable
***************************************************************************************************

block var


.. _tgt_auto_align_var:

***************************************************************************************************
Automatic left-alignment variable
***************************************************************************************************

align


.. _tgt_auto_vari_block:

***************************************************************************************************
Automatic variation block
***************************************************************************************************

variation


.. _tgt_fill_hndl:

***************************************************************************************************
Fill handler
***************************************************************************************************
