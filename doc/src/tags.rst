###################################################################################################
Template tags
###################################################################################################

Blockie uses templates containing *tags* to indicate variable parts of the template intended to
be filled with specific values by the Python script.

.. important::
    
    By default, the tags have an XML-like form using the uppercase letters for names, e.g.,
    ``<TAG_NAME>`` is a tag named ``TAG_NAME``.

    The tag names in a Python filling script are automatically converted to the uppercase format
    by default, i.e., it is possible to refer to the ``<TAG_NAME>`` tag using a lowercase name
    ``tag_name`` in the script.

    This tag format and automatic uppercase conversion is used in almost all examples within this
    document. However, the :ref:`tag format is configurable <tgt_config>`, as will be described
    later.


.. _tgt_primary_tags:

***************************************************************************************************
Primary tags
***************************************************************************************************

Variable tag
===================================================================================================

A *variable* consists of a single tag, e.g., ``<VARIABLE>`` representing a variable named
``VARIABLE`` that can be set to the required value using a simple string replacement.


Block tag
===================================================================================================

A *block* consists of a start-end tag pair defining a portion, i.e., block, of text within a
template. For example, ``<BLOCK>content</BLOCK>`` represents a block  named ``BLOCK`` having an
internal content consisting of a simple string ``content``. Apart from a constant text, a block
can also contain *variables* and other child *blocks*.

The whole template itself is considered to be a *primary block*. However, it is not marked by any
start-end tag pair, i.e., the primary template block does not have a name.

The block content can be **cloned**, i.e., duplicated as many times as needed, with variables in
each clone filled with different values. For example, the simple template string below contains
a block named ``PEOPLE`` that can be used to define a list with each row containing information
about a different person:

Template:

.. code-block:: text

    A list of people:
    <PEOPLE>
    - <NAME> <SURNAME>, <AGE>
    </PEOPLE>

.. seealso::
    The description of filling the template with values is
    :ref:`described later <tgt_auto_fill_basic>` after the description of all types of tags.


.. _tgt_primary_tags_content_vari:

Block variation tag
===================================================================================================

A block can have multiple predefined **content variations**, with each variation separated by
a special tag, which by default has a ``<^BLOCK>`` format, where the ``BLOCK`` is a block name.
The script filling the template with data can then select a required variation of the predefined
content.

The example below illustrates a template with a ``BLOCK`` block having three variations of its
content selectable by the filling script:

.. code-block:: text

    <BLOCK>content 1<^BLOCK>content 2<^BLOCK>content 3</BLOCK>


.. _tgt_auto_tags:

***************************************************************************************************
Secondary - automatic tags
***************************************************************************************************

The special secondary *autotags* are filled automatically, i.e., without any values explicitly
assigned by the filling script.


Alignment autotag
===================================================================================================

An *alignment autotag* ``<+>`` is special tag useful for the text alignment. It automatically
repeats the first character located right after this tag in the template until a different
character is found. The column position of the different character is kept according to the
template regardless of the length of a generated content located before the alignment autotag.

Example of a template using the alignment autotag:

.. code-block:: text

    <NAME><+>               <SURNAME>

repeats the space character located after the ``<+>`` tag right until the beginning of a surname
(since the character "<" at the beginning of the ``<SURNAME>`` tag is different from the repeated
space character). The surname start column will remain the same, regardless of the length of the
``NAME`` variable value. So, for example, filling the template using the name-surname pairs
``John``, ``Connor`` and ``Thomas``, ``Anderson`` results in both surnames aligned to the same
column:

.. code-block:: text

    John                    Connor
    Thomas                  Anderson


Variation autotag
===================================================================================================

A *variation autotag* has a form of a ``<.>`` (dot) block with two, or optionally three
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
    See the :ref:`code example <tgt_auto_fill_basic_example>` using both of the automatic tags.
