###################################################################################################
Usage
###################################################################################################

The following chapters describe the essential concepts needed for the creation of templates
and for filling them with data to generate an output content.

However, it is also possible to jump to the :ref:`basic <tgt_auto_fill_basic_example>` or the
:ref:`advanced <tgt_auto_fill_advanced_example>` example to get a quick overview of all the
principles used in the :ref:`automatic template filling <tgt_auto_fill>`.


***************************************************************************************************
Template tags
***************************************************************************************************

Blockie uses templates containing *tags* to indicate variable parts of the template as illustrated
on a simple template string below containing the so-called *block* named ``PEOPLE`` that can
be filled with name, surname and age values of each person assigned to the *variables* ``NAME``,
``SURNAME``, and ``AGE``.

.. code-block:: text

    A list of people:
    <PEOPLE>
    - <NAME> <SURNAME>, <AGE>
    </PEOPLE>

.. important::
    
    By default, the tags have an XML-like form using the uppercase letters for names, e.g.,
    ``<TAG_NAME>`` is a tag named ``TAG_NAME``.

    The tag names in a Python filling script are automatically converted to the uppercase format
    by default, i.e., it is possible to refer to the ``<TAG_NAME>`` tag using the lowercase name
    ``tag_name`` in the script.

    This tag format and automatic uppercase conversion is used in almost all examples within this
    document. However, the tag format is :ref:`configurable <tgt_config>`, as will be described
    later.


.. _tgt_primary_tags:

Primary tags
===================================================================================================

The templates used by the blockie need to use the tags described in the following sections to
represent the essential parts of variable content.

.. seealso::
    :ref:`Tag format configuration <tgt_config>`.


Variable tag
---------------------------------------------------------------------------------------------------

A *variable* consists of a single tag, e.g., ``<VARIABLE>`` representing a variable named
``VARIABLE`` that can be set to the required value using a simple string replacement.


Block tags
---------------------------------------------------------------------------------------------------

A *block* consists of a start-end tag pair, e.g., ``<BLOCK>content</BLOCK>`` representing a block
named ``BLOCK`` having an internal content consisting of a simple string ``content``. Apart from
string constants, a block can also contain *variables* and other child *blocks*.

A block can also have multiple predefined **content variations** with each variation separated by
a special tag, which by default has a ``<^BLOCK>`` format. For example, the
``<BLOCK>content 1<^BLOCK>content 2<^BLOCK>content 3</BLOCK>`` defines a block with three
variations of a content selectable by the filling script.

The standard (non-variation) block content can be **cloned**, i.e., duplicated as many times as
needed, and variables in each clone can be filled with different values.

The whole template is considered to be a primary *block* and its content is not marked by any
start-end tag pair, i.e., the primary template block does not have a name.


.. _tgt_auto_tags:

Automatic tags
===================================================================================================

The template can contain special tags that are filled automatically (i.e., without any values
implicitly assigned by the filling script). These special *autotags* are described in a sections
below.


Alignment autotag
---------------------------------------------------------------------------------------------------

An *alignment autotag* ``<+>``: A special tag useful for the text alignment. It automatically
repeats the first character located right after this tag in the template until a different
character is found. The column position of the different character is kept according to the
template regardless of the length of a generated content located before the alignment autotag.

Example of a template using the alignment autotag:

.. code-block:: text

    <NAME><+>               <SURNAME>

repeats the space character located after the ``<+>`` tag right until the beginning of a surname
(since the character "<" is different from the repeated space character). The surname start column
will remain the same, regardless of the length of the ``NAME`` variable value. So, for example,
filling the template using the name-surname pairs ``John``, ``Connor`` and ``Thomas``,
``Anderson`` results in both surnames aligned to the same column:

.. code-block:: text

    John                    Connor
    Thomas                  Anderson


Variation autotag
---------------------------------------------------------------------------------------------------

A *variation autotag*  in form of a ``<.>`` (dot) block with two, or optionally three
:ref:`content variations <tgt_primary_tags>`: ``<.>standard<^.>last</.>`` or
``<.>standard<^.>last<^.>first</.>``. This autotag is intended to be placed inside another
block that is cloned during the :ref:`template filling <tgt_auto_fill>`. Then the first
clone is (optionally) set to the ``first`` content of the variation autotag, the last clone is
automatically set to the ``last`` content, and the rest of the clones in between are set to
the ``standard`` content.

This autoblock can be useful, for example, for the comma-separation of variables within a
cloned block as illustrated below where the *standard* content is set to a comma ``, ``
and the *last* content is set to an empty string ````:

.. code-block:: text

    <NUM_LIST><NUM><.>, <^.></.></NUM_LIST>

Cloning the ``NUM_LIST`` block with values ``1``, ``2``, ``3``, ``4`` set to the ``NUM``
variable in each cloned content will result in a following string (notice that the last
value ``4`` is not followed by a comma):

.. code-block:: text

    1, 2, 3, 4

.. seealso::
    .

.. seealso::
    See the :ref:`code example <tgt_auto_fill_basic_example>` using both of the automatic tags.

    The symbols used for the automatic tags can also be configured by the
    :ref:`configuration object <tgt_config>`.


.. _tgt_auto_fill:

***************************************************************************************************
Automatic template filling
***************************************************************************************************

The automatic template filling is the simplest way to generate a templated content. The data used
for setting the values in a template is defined by a Python dictionary with keys representing the
template :ref:`variable and block tag names <tgt_primary_tags>`.

To fill the template variables and blocks with data, it is first necessary to load the whole
template into the primary :py:class:`.Block` object. This can be done by setting a template string
text or a text file in the :py:meth:`.Block.__init__` constructor. Alternatively, the
:py:attr:`.Block.template` attribute, or the :py:meth:`.Block.load_template` method can be used.


.. _tgt_auto_fill_basic:

Basic automatic filling
===================================================================================================

The template can be filled by the :py:meth:`.Block.fill` method with the required data
**dictionary** provided as an argument.

The dictionary values can perform one of the operations in the sections below depending on the
data type of the dictionary value.


Setting a variable value
---------------------------------------------------------------------------------------------------

A variable value must be set using a **basic data type** (i.e., ``int``, ``float``, ``str``,
and ``bool``). For example, the key-value dictionary pair ``name: "John"`` sets the variable
``name`` to the value ``John``.


Setting the content of a single block
---------------------------------------------------------------------------------------------------

The content of a block needs to be set by a **dictionary** (i.e., ``{...}``. For example, the
``date: {day: 24, month: December}`` sets the ``date`` block content with a template containing
two variables ``day`` and ``month`` set to values ``24`` and ``December`` respectively.


Setting the content of block clones
---------------------------------------------------------------------------------------------------

A block can be cloned, i.e., duplicated, using a **list or a tuple of dictionaries** with each
dictionary corresponding to one clone of a block content. As an example, the
``date: [{day: 24, month: 12}, {day: 25, month: 12}]`` key-value pair creates and sets two clones
of a ``date`` block with the ``day`` and ``month`` variables in each block  clone set to the
values ``24``, ``12`` in the first clone and to the ``25``, ``12`` in the second clone.


.. _tgt_auto_fill_basic_example:

The following filling script example shows all simple concepts described above, i.e., the template
containing the :ref:`basic tags <tgt_primary_tags>` and also :ref:`automatic tags <tgt_auto_tags>`
filled using the :ref:`basic principles <tgt_auto_fill_basic>` of automatic filling. The template
is defined directly by the ``template`` string and the data to fill the template with are defined
by the ``data`` dictionary.

.. code-block:: python

    from blockie import Block


    template = """
                                SHOPPING LIST
      Items                                                         Quantity
    ------------------------------------------------------------------------
    <ITEMS>
    * <ITEM><+>                                                     <QTY>
    </ITEMS>


    Short list: <ITEMS><ITEM><.>, <^.></.></ITEMS>
    """

    data = {
        "items": [
            {"item": "apples", "qty": "1 kg"},
            {"item": "potatoes", "qty": "2 kg"},
            {"item": "rice", "qty": "1 kg"},
            {"item": "orange juice", "qty": "1 l"},
            {"item": "cooking magazine", "qty": 1},
        ]
    }

    blk = Block(template)
    blk.fill(data)
    print(blk.content)


The script prints the following generated content:

.. code-block:: text

                                SHOPPING LIST
      Items                                                         Quantity
    ------------------------------------------------------------------------
    * apples                                                        1 kg
    * potatoes                                                      2 kg
    * rice                                                          1 kg
    * orange juice                                                  1 l
    * cooking magazine                                              1


    Short list: apples, potatoes, rice, orange juice, cooking magazine

.. note::
    Notice that the template contains two ``ITEMS`` blocks containing the variable ``ITEM`` and
    that both blocks are automatically filled by the same data, since they have the same name.


.. _tgt_auto_fill_advanced:

Advanced automatic filling
===================================================================================================

Similarly to the :ref:`basic operations <tgt_auto_fill_basic>`, the values in a data dictionary
can also perform additional operations described in the following list:


Setting a block content as is
---------------------------------------------------------------------------------------------------

A single block can be set to the generated content as is, i.e., without setting any of its child
elements, by setting the block value to a simple **non-empty value**, which can be a *non-empty
string, non-zero numeric value or a boolean true*. As an example, the key-value pairs
``date: "anything"``, ``date: 1``, ``date: True`` all set the content of a block named ``date``
into the final generated output without explicitly setting any of its internal values or other
subblocks (it is expected that the block is either constant, i.e., without variables, or the
variables have been already set).


Setting a block content variation
---------------------------------------------------------------------------------------------------

A specific content from a block with multiple content variations can be selected using a
**special** ``vari_idx`` **key** defined in a *dictionary* corresponding to the block.
The ``vari_idx`` key can be set to a *numeric or  boolean* value with the following meaning:

-   A numeric value zero or higher sets the variation of a content corresponding to the specified
    index, e.g.
    ``date: {"vari_idx": 1}`` sets the second content variation of a ``date`` block (value 0
    corresponds to the first variation).
-   A numeric value below zero removes the block, e.g. ``date: {"vari_idx": -1}`` removes the
    ``date`` block from the generated content.
-   A boolean ``True`` has the same effect as the value zero (i.e., sets the first content
    variation) and boolean ``False`` has the same effect as any negative value (i.e., removes
    the block).


Removing a variable
---------------------------------------------------------------------------------------------------

A variable can be removed from the generated content by setting its dictionary value to an
**empty string or to none**, i.e., ``name: ""`` or ``name: None`` key-value pairs both remove the
``name`` variable from the generated content.


Removing a block
---------------------------------------------------------------------------------------------------

A block can be removed from the content by setting its dictionary value to an **empty value**,
which can be an *empty dictionary, empty list, none, zero, or boolean false*, i.e., ``date: {}``,
``date: []``, ``date: None``, ``date: 0``, ``date: False`` all remove the ``date`` block from the
generated content.


.. _tgt_auto_fill_advanced_example:

The filling script below expands the :ref:`basic automatic filling concepts <tgt_auto_fill_basic>`
using the advanced operations described above. The template is defined directly by the
``template`` string and the data to fill the template with are defined by the ``data`` dictionary.

.. code-block:: python

    from blockie import Block


    template = """
                                SHOPPING LIST
      Items                                                         Quantity
    ------------------------------------------------------------------------
    <ITEMS>
    * <FLAG>IMPORTANT! <^FLAG>MAYBE? </FLAG><ITEM><+>               <QTY><UNIT> kg<^UNIT> l</UNIT>
    </ITEMS>


    Short list: <ITEMS><ITEM><.>, <^.></.></ITEMS>
    """

    data = {
        "items": [
            {"flag": None, "item": "apples", "qty": "1", "unit": True},
            {"flag": True, "item": "potatoes", "qty": "2", "unit": {"vari_idx": 0}},
            {"flag": None, "item": "rice", "qty": "1", "unit": {"vari_idx": 0}},
            {"flag": None, "item": "orange juice", "qty": "1", "unit": {"vari_idx": 1}},
            {"flag": {"vari_idx": 1}, "item": "cooking magazine", "qty": None, "unit": None},
        ]
    }

    blk = Block(template)
    blk.fill(data)
    print(blk.content)

The script prints the following generated content:

.. code-block:: text

                                SHOPPING LIST
    Items                                                           Quantity
    ------------------------------------------------------------------------
    * apples                                                        1 kg
    * IMPORTANT! potatoes                                           2 kg
    * rice                                                          1 kg
    * orange juice                                                  1 l
    * MAYBE? cooking magazine
