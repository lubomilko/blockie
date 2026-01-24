.. _tgt_data_fill:

###################################################################################################
Data-driven template filling
###################################################################################################

.. _tgt_principles:

***************************************************************************************************
Basic principles
***************************************************************************************************

The variable elements of the template that can be filled with specific values from the input
data are indicated by tags. By default, the tags have an XML-like format and their names use
uppercase letters. The template consists of two primary elements defined by their corresponding
tags:

-   :ref:`Variables <tgt_variable>` defined by a single tag, e.g., ``<NAME>``.
-   :ref:`Blocks <tgt_block>` defined by the two start and end tags, e.g., ``<LIST> ... </LIST>``,
    with a content between these tags consisting of other blocks and variables. The whole template
    is also considered to be a block despite not having any explicitly defined start and end tags.

Blocks in the template (including the whole template) can be loaded into the :py:class:`.Block`
objects to perform operations with them and with the variables in their content.

In most cases, the **template filling logic can be defined purely by the structure of the template
elements and the structure and values of the input data** without any explicit custom script-like
instructions in the templates or data values.

The most straightforward way to fill the whole template is to load it into the primary
:py:class:`.Block` object through its constructor or a :py:attr:`.Block.template` attribute and
to use the :py:meth:`.Block.fill` method with an input data dictionary (``dict``) having keys
corresponding to the template tag names (see :ref:`Setting block content <tgt_set_blk_cont>`
section). The template tags are then replaced with the dictionary values in the generated
:py:attr:`.Block.content` attribute.

The tag references in the input data and Python filling script can use lowercase letters that
are by default automatically converted to the corresponding uppercase tag names used in the
template.

.. important::

    The tag format and automatic uppercase conversion described above is used in almost all
    examples within this document together with a Python dictionary used as a data input. However,
    the tag format is :ref:`configurable <tgt_config>` and instead of a dictionary, it is also
    possible to use a struct-like object with attributes corresponding to the dictionary keys.


.. _tgt_variable:

***************************************************************************************************
Variable
***************************************************************************************************

Variables are the simplest modifiable parts of the template defined by a single tag, e.g.,
``<NAME>``.


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


.. _tgt_block:

***************************************************************************************************
Block
***************************************************************************************************

Blocks are used for splitting the template into multiple hierarchical parts. A block is defined
by the two start and end tags, e.g., ``<LIST> ... </LIST>`` with a content between them consisting
of constant text, other child blocks and :ref:`variables <tgt_variable>`. The whole template is
considered to be a primary block even without explicitly defined tags.


.. _tgt_set_blk_cont:

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


.. _tgt_blk_cont_clone:

Block content cloning
===================================================================================================

It is possible to **clone**, i.e., duplicate, the block template by setting its value to a **list
or tuple of non-empty dictionaries** (``[{...}, {...}, ...]``, ``({...}, {...}, ...)``) with the
inner dictionaries setting the content of other blocks and :ref:`variables <tgt_variable>` for
each block clone.

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
<tgt_variable>` name or block content dictionary.

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


***************************************************************************************************
Automatic variables and blocks
***************************************************************************************************

Automatic variables and blocks are filled automatically without any values specified in the
input data. The automatic elements typically help with the formatting of the generated content.


.. _tgt_auto_align_var:

Automatic left-alignment variable
===================================================================================================

A left-alignment automatic variable has a ``<+>`` tag and can be used to maintain the
left-alignment of a text within the template having :ref:`variables <tgt_variable>` filled with
values of different character lengths.

Blockie automatically scans the first character located right after this tag and counts the number
of consecutive occurrences of this character until a different character is found. Then it
maintains the column position of the different character regardless of the content generated
on the line before this character.

.. code-block:: python

    template = """
    Name        Surname     Role
    ----------------------------
    <CHARACTERS>
    <NAME><+>   <SNAME><+>  <ROLE>
    </CHARACTERS>"""

    blk = blockie.Block(template)
    blk.fill({"characters": [
        {"name": "Dave", "sname": "Bowman", "role": "astronaut 1"},
        {"name": "Frank", "sname": "Poole", "role": "astronaut 2"},
        {"name": "Heywood", "sname": "Floyd", "role": "chairman of the US National Council of Astronautics"},
        {"name": "HAL", "sname": "9000", "role": "broken computer that can kill, but can't lie"}]})
    print(blk.content)

Output:

.. code-block:: text

    Name        Surname     Role
    ----------------------------
    Dave        Bowman      astronaut 1
    Frank       Poole       astronaut 2
    Heywood     Floyd       chairman of the US National Council of Astronautics
    HAL         9000        broken computer that can kill, but can't lie

.. code-block:: python

    template = """
    Name            Phone number
    ----------------------------
    <PEOPLE>
    <NAME><+>.......<PHONE>
    </PEOPLE>"""

    blk = blockie.Block(template)
    blk.fill({"people": [
        {"name": "Dave", "phone": "0940 123 456"},
        {"name": "Frank", "phone": "0933 987 654"},
        {"name": "Heywood", "phone": "0911 111 111"}]})
    print(blk.content)

Output:

.. code-block:: text

    Name            Phone number
    ----------------------------
    Dave............0940 123 456
    Frank...........0933 987 654
    Heywood.........0911 111 111


.. _tgt_auto_block_var:

Automatic block variable
===================================================================================================

A :ref:`block <tgt_block>` content can be :ref:`set <tgt_set_blk_cont>` into a different location
than its original location, or into multiple different locations within the template using a
special tag having a ``<@BLOCK_NAME>`` format. This so-called *block variable* acts as a target
for a block content, while the original block is :ref:`cleared <tgt_clear_blk>`.

The block variable can be useful for repeating the referenced content multiple times or for
maintaining the :ref:`left-alignment <tgt_auto_align_var>` as illustrated in the example below.

.. code-block:: python

    template = """
    <LIST>
    <IDX>a)<^IDX>b)<^IDX>c)<^IDX>d)<^IDX>e)<^IDX>f)</IDX>
    <@IDX> <ITEM><+>        <QTY>
    </LIST>
    """

    blk = blockie.Block(template)
    blk.fill({"list": [
        {"idx": 0, "item": "first", "qty": 1},
        {"idx": 1, "item": "second", "qty": 2},
        {"idx": 2, "item": "third", "qty": 3}]})
    print(blk.content)

Output:

.. code-block:: text

    a) first                1
    b) second               2
    c) third                3

.. note::
    The block variable tag(s) must be located within the parent block of a referenced block.


.. _tgt_auto_vari_block:

Automatic variation block
===================================================================================================

With :ref:`cloned block contents <tgt_blk_cont_clone>` it is often useful to have some part of the
block content to be different in the first and/or the last clone. An *automatic variation block*
can be used to define such part of the content using a special ``<.>`` block tag having either two
or three :ref:`content variations <tgt_set_blk_cont_vari>`:

- ``<.>standard content<^.>last content</.>``
- ``<.>standard content<^.>last content<^.>first content</.>``

Where the ``standard content`` is used in the second and second to last clones of a parent block,
the ``last content`` is used in the last clone, and the ``first content`` is used in the first
parent block content.

.. code-block:: python

    blk = blockie.Block("Characters: <CHARACTERS><NAME> <SURNAME><.>, <^.></.></CHARACTERS>.")
    blk.fill({"characters": [
        {"name": "Dave", "surname": "Bowman"},
        {"name": "Frank", "surname": "Poole"},
        {"name": "Heywood", "surname": "Floyd"},
        {"name": "HAL", "surname": "9000"}]})
    print(blk.content)

Output:

.. code-block:: text

    Characters: Dave Bowman, Frank Poole, Heywood Floyd, HAL 9000.

.. code-block:: python

    template = """
    <CHARACTERS>
    <.>
    | <NAME><+>     <SURNAME><+> |
    <^.>
    | <NAME><+>     <SURNAME><+> |
    +----------------------------+
    <^.>
    +----------------------------+
    | <NAME><+>     <SURNAME><+> |
    </.>
    </CHARACTERS>"""

    blk = blockie.Block(template)
    blk.fill({"characters": [
        {"name": "Dave", "surname": "Bowman"},
        {"name": "Frank", "surname": "Poole"},
        {"name": "Heywood", "surname": "Floyd"},
        {"name": "HAL", "surname": "9000"}]})
    print(blk.content)

Output:

.. code-block:: text

    +----------------------------+
    | Dave          Bowman       |
    | Frank         Poole        |
    | Heywood       Floyd        |
    | HAL           9000         |
    +----------------------------+