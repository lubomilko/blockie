.. _tgt_data_fill:

###################################################################################################
Data-driven template filling
###################################################################################################

In most cases, the template filling logic can be defined purely by the structure of the template
elements and the structure and values of the input data without any explicit custom script-like
instructions in the templates or data values. 

The most straightforward way to fill the whole template is to load it into the primary
:py:class:`.Block` object through its constructor or a :py:attr:`.Block.template` attribute and
to use the :py:meth:`.Block.fill` method with an input data dictionary (``dict``) having keys
corresponding to the template :ref:`tag names <tgt_tags>`. The template tags are then replaced
with the dictionary values in the generated :py:attr:`.Block.content` attribute.

The tag references in the input data and Python filling script can use lowercase letters that
are by default automatically converted to the corresponding uppercase tag names used in the
template.

.. important::

    The tag format and automatic uppercase conversion described above is used in almost all
    examples within this document together with a Python dictionary used as a data input. However,
    the tag format is :ref:`configurable <tgt_config>` and instead of a dictionary, it is also
    possible to use a struct-like object with attributes corresponding to the dictionary keys.

.. note::
    Using the :py:meth:`.Block.fill` method also enables the use of :ref:`additional features
    <tgt_add_features>` described later.


.. _tgt_variable_oper:

***************************************************************************************************
Variable operations
***************************************************************************************************

Setting the variable value
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


Clearing a variable
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


.. _tgt_block_oper:

***************************************************************************************************
Block operations
***************************************************************************************************

.. _tgt_set_blk_cont:

Setting the block content
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


.. _tgt_blk_cont_clone:

Block content cloning
===================================================================================================

It is possible to **clone**, i.e., duplicate, the block template by setting its value to a **list
or tuple of non-empty dictionaries** (``[{...}, {...}, ...]``, ``({...}, {...}, ...)``) with the
inner dictionaries setting the content of other blocks and variables for each block clone.

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
data type** values (``str``, ``int``, ``float``, or ``bool``) without specifying any variable
name or block content dictionary.

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


.. _tgt_set_blk_cont_vari:

Setting the block content variation
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


.. _tgt_clear_blk:

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

A block can be cleared also by setting its :ref:`content variation <tgt_set_blk_cont_vari>` index
(``int``) to a negative value.


.. _tgt_add_features:

***************************************************************************************************
Addtional features
***************************************************************************************************

The :ref:`data-driven template filling <tgt_data_fill>` approach, i.e. usage of the
:py:meth:`.Block.fill` method, also allows to use extended features of :ref:`variables and blocks
<tgt_tags>` described in the subsequent sections.


.. _tgt_fill_hndl:

Block fill handler
===================================================================================================

A block can have a custom handler function assigned for performing special :ref:`data-driven
<tgt_data_fill>` and also :ref:`manual <tgt_man_fill>` operations with the block content.

This custom handler function can be assigned within the dictionary data defining the block content
values using the special ``fill_hndl`` key with a value of a function having the following
signature:

.. code-block:: python

    (block: Block, data: dict | object, clone_subidx: int) -> None

The example below shows a simple ``format_date`` fill handler function setting the required
date format based on the format of a month value specified in the input data (i.e., whether the
month is specified using its name or number).

.. code-block:: python

    def format_date(_block: blockie.Block, data: dict, _clone_subidx: int) -> None:
        if isinstance(data["month"], str) and not data["month"].isdigit():
            # If month is specified by its name,
            # then make it uppercase and set the date format to: <MONTH> <DAY>
            data["month"] = data["month"].upper()
            data["date"] = 1
        else:
            # Set the date format to: <DAY>.<MONTH>.
            data["date"] = 0
   
    blk = blockie.Block("The date is: <DATE><DAY>.<MONTH>.<^DATE><MONTH> <DAY></DATE>")
    blk.fill({"day": 24, "month": "December", "fill_hndl": format_date})
    print(blk.content)

Output:

.. code-block:: text

    The date is: DECEMBER 24


Subelements
===================================================================================================

Variables and blocks in a template can reference input data values defined for nested subblocks
using a ``.`` (dot) operator. For example, a ``<BOOK.AUTHOR.NAME>`` tag is equivalent to
``<BOOK><AUTHOR><NAME></AUTHOR></BOOK>`` template.

.. code-block:: python

    blk = blockie.Block("The date is: <DATE.DAY>.<DATE.MONTH>.")
    blk.fill({"date": {"day": 24, "month": 12}})
    print(blk.content)

Output:

.. code-block:: text

    The date is: 24.12.

It is not possible for subelements to reference data "through" :ref:`cloned blocks
<tgt_blk_cont_clone>`, e.g., a subelement tag ``<BOOK.AUTHORS.NAME>`` would not work in the
example below, since the ``<AUTHORS> ... </AUTHORS>`` block is indended to be cloned and a
``NAME`` reference is not sufficient to indicate the required name instance.

However, a cloned block itself can be referenced, as illustrated by the ``<BOOK.AUTHORS> ...
</BOOK.AUTHORS>`` subblock in the following code.

.. code-block:: python

    blk = blockie.Block("<BOOK.AUTHORS><NAME> <SURNAME>\n</BOOK.AUTHORS>")
    blk.fill({"book": {
        "title": "The C Programming Language",
        "authors": [{"name": "Brian", "surname": "Kernighan"},
                    {"name": "Dennis", "surname": "Ritchie"}],
        "publication": {
            "date": "1988",
            "publisher": "Pearson"
        }}})
    print(blk.content)

Output:

.. code-block:: text

    Brian Kernighan
    Dennis Ritchie

The subelements can always be defined starting from the top (outermost) block in the template
downwards. However, if a subreference is defined within a block content, then that block can
also be considered as a top (outermost) block, as illustrated in the example below with the
``<PUBLICATION.PUBLISHER>`` and ``<PUBLICATION.DATE>`` subvariables using the ``BOOK`` block as
the top block.

.. code-block:: python

    blk = blockie.Block("Publication info: <BOOK><PUBLICATION.PUBLISHER>, <PUBLICATION.DATE></BOOK>")
    blk.fill({"book": {
        "title": "The C Programming Language",
        "authors": [{"name": "Brian", "surname": "Kernighan"},
                    {"name": "Dennis", "surname": "Ritchie"}],
        "publication": {
            "date": "1988",
            "publisher": "Pearson"
        }}})
    print(blk.content)

Output:

.. code-block:: text

    Publication info: Pearson, 1988


Variable templates
===================================================================================================

String data values used for filling the template variables can have a template form themselves,
i.e., the variable values can contain other variable and block :ref:`tags <tgt_tags>` that are
filled automatically if corresponding values are found in the input data for them.

.. code-block:: python

    blk = blockie.Block("<GREETING> Welcome to the world of templating.")
    blk.fill({"name": "John", "greeting": "Hello <NAME>!"})
    print(blk.content)

Output:

.. code-block:: text

    Hello John! Welcome to the world of templating.

The example below shows a more complex template used as a variable value. Although, such a mix of
templates and data can be difficult to maintain.

.. code-block:: python

    blk = blockie.Block("The date is: <DATE_STR>.")
    blk.fill({"date": {"day": "01", "month": "01", "year": "2026"},
              "date_str": "<DATE><DAY>.<MONTH>.<YEAR></DATE>"})
    print(blk.content)

Output:

.. code-block:: text

    The date is: 01.01.2026.
