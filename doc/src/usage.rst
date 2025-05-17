###################################################################################################
Usage
###################################################################################################

The following chapters describe the essential concepts needed for the creation of blockie
templates and for filling them with data to generate an output content.

However, if you are familiar with the basics of template engines and feel confident, then it is
also possible to jump to the :ref:`basic example <tgt_auto_fill_basic_example>` or straight to the
more :ref:`advanced example <tgt_auto_fill_advanced_example>` showing almost all features of
the :ref:`automatic template filling <tgt_auto_fill>` in a very simple way.


***************************************************************************************************
Template tags
***************************************************************************************************

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

Primary tags
===================================================================================================

Variable tag
---------------------------------------------------------------------------------------------------

A *variable* consists of a single tag, e.g., ``<VARIABLE>`` representing a variable named
``VARIABLE`` that can be set to the required value using a simple string replacement.


Block tags
---------------------------------------------------------------------------------------------------

A *block* consists of a start-end tag pair defining a portion - "block" of text within a template.
For example, ``<BLOCK>content</BLOCK>`` represents a block  named ``BLOCK`` having an internal
content consisting of a simple string ``content``. Apart from a constant text, a block can also
contain *variables* and other child *blocks*.

The standard (non-variation) block content can be **cloned**, i.e., duplicated as many times as
needed, and variables in each clone can be filled with different values as illustrated below on
a simple template string with the block named ``PEOPLE`` defining a list of people with each
item containing *variables* for name, surname and age.

.. code-block:: text

    A list of people:
    <PEOPLE>
    - <NAME> <SURNAME>, <AGE>
    </PEOPLE>

.. seealso::
    The description of filling the template with values is
    :ref:`described later <tgt_auto_fill_basic>` after the description of all types of tags.

The whole template itself is considered to be a primary block and its content is not marked by
any start-end tag pair, i.e., the primary template block does not have a name.

A block can also have multiple predefined **content variations** with each variation separated by
a special tag, which by default has a ``<^BLOCK>`` format. The script filling the template with
data can then select a required variation of the predefined content.

The example below illustrates a template with a ``BLOCK`` block having three variations of its
content selectable by the filling script:

.. code-block:: text

    <BLOCK>content 1<^BLOCK>content 2<^BLOCK>content 3</BLOCK>


.. _tgt_auto_tags:

Automatic tags
===================================================================================================

The template can contain special tags that are filled automatically, i.e., without any values
implicitly assigned by the filling script.


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

The automatic template filling is the simplest way to generate a templated content.

To fill the template variables and blocks with data, it is first necessary to load the whole
template into the primary :py:class:`.Block` object. This can be done by setting a template string
text or a text file in the :py:meth:`.Block.__init__` constructor. Alternatively, the
:py:attr:`.Block.template` attribute, or the :py:meth:`.Block.load_template` method can be used.

A template can then be filled using the :py:meth:`.Block.fill` method with the required data
provided as an argument in a Python **dictionary**. The dictionary keys represent the template
:ref:`variable and block tags <tgt_primary_tags>`. The data dictionary needs to 

.. note::
    In reality, the automatic template filling process is, of course, not fully automatic. It is
    necessary to provide the data to fill the template in a correct format matching the template
    structure. However, the filling process is then all done by the :py:meth:`.Block.fill` method,
    unlike with a :ref:`manual approach <tgt_manual_fill>` where the filling script needs to call
    multiple individual :py:class:`.Block` methods to generate the required content.


.. _tgt_auto_fill_basic:

Basic automatic filling
===================================================================================================

The values assigned to the data dictionary keys representing template tags can perform various
operations described in the sections below depending on the data type of the dictionary value.


Setting a variable value
---------------------------------------------------------------------------------------------------

A variable value is set using a **basic data type** (i.e., ``int``, ``float``, ``str``, or
``bool``). 

The example below sets the variables ``word1`` and ``word2`` to the string values ``Hello``,
``World!``:

.. code-block:: python

    blk = blockie.Block("<WORD1> <WORD2>")
    blk.fill({"word1": "Hello", "word2": "world!"})
    print(blk.content)

prints:

.. code-block:: text

    Hello world!


Setting the content of a single block
---------------------------------------------------------------------------------------------------

The content of a block needs to be set by a **dictionary**, as shown in the following example
setting the content of a ``date`` block, specifically setting its child ``day`` and ``month``
variable values:

.. code-block:: python

    blk = blockie.Block("<DATE><DAY> <MONTH></DATE>")
    blk.fill({"date": {"day": 24, "month": "December"}})
    print(blk.content)

prints:

.. code-block:: text

    24 December


.. _tgt_auto_fill_basic_block_clones:

Setting the content of block clones
---------------------------------------------------------------------------------------------------

A block can be cloned, i.e., duplicated, using a **list or a tuple of dictionaries** with each
dictionary corresponding to one clone of a block content. The example below shows setting of
two dates in two clones of a ``date`` block:

.. code-block:: python

    blk = blockie.Block("<DATE><DAY> <MONTH>\n</DATE>")
    blk.fill({"date": [{"day": 24, "month": 12}, {"day": 25, "month": 12}]})
    print(blk.content)

prints:

.. code-block:: text

    24 12
    25 12


.. _tgt_auto_fill_basic_example:

Basic example
---------------------------------------------------------------------------------------------------

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
can also perform additional operations described in the following sections.


Setting a block content as is
---------------------------------------------------------------------------------------------------

A single block can be set to the generated content as is, i.e., without setting any of its child
elements, by setting the block value to a simple **non-empty value**, which can be a *non-empty
string, zero or positive number or a boolean true*. It is expected that the block content is
either constant, or the variables inside have been already set. The example below shows setting
a ``date`` block having a constant content into the final generated output just by setting it to
boolean true:

.. code-block:: python

    blk = blockie.Block("<DATE>24 December</DATE>")
    blk.fill({"date": True})
    print(blk.content)

prints:

.. code-block:: text

    24 December


Setting a block content variation
---------------------------------------------------------------------------------------------------

A specific content from a block with multiple content variations can be selected using a
**special** ``vari_idx`` **key with a numeric value** defined in a *dictionary* corresponding to
the block. The value of a number assigned to the ``vari_idx`` key defines one of the operations
below:

-   A value equal to zero or higher (*>=0*) selects the block content variation with an index
    corresponding to the provided value.
-   A negative value (*<0*) removes the entire block from the generated content.
-   A boolean value can be used, where ``True`` has the same effect as the value zero and
    ``False`` has the same effect as a negative value.

Alternatively, if a block has a constant content, it is possible to select one of its constant
content variations by directly setting a numeric value representing the content index to its key
in a data dictionary, as shown in the second example below:

.. code-block:: python

    date_dict = {"day": 24, "month": "December"}
    date_dict["vari_idx"] = 0 if isinstance(date_dict["month"], int) else 1

    blk = blockie.Block("<DATE><DAY>.<MONTH>.<^DATE><DAY> <MONTH></DATE>")
    blk.fill({"date": date_dict})
    print(blk.content)

prints:

.. code-block:: text

    24 December

.. code-block:: python

    blk = blockie.Block("<DATE>24.12.<^DATE>24 December</DATE>")
    blk.fill({"date": 1})
    print(blk.content)

prints:

.. code-block:: text

    24 December

.. important::
    As illustrated on the first example, the block variations can be used for a conditional
    content selection. However, the logic of selecting the right content must be defined within
    the filling script, since the blockie templates themselves are logicless.

.. note::
    Note that removing a block using a ``vari_idx`` key set to a negative value is only the
    secondary purpose of the ``vari_idx`` key. The primary method of a
    :ref:`block removal <tgt_auto_fill_remove_block>` is described later.


Removing a variable
---------------------------------------------------------------------------------------------------

A variable can be removed from the generated content by setting its dictionary value to an
**empty string or to none** as shown on the example below removing the variable for a middle name.

.. code-block:: python

    blk = blockie.Block("<NAME> <MIDNAME> <SURNAME>")
    blk.fill({"name": "Patrick", "midname": None, "surname": "Bateman"})
    print(blk.content)

prints:

.. code-block:: text

    Patrick  Bateman


.. _tgt_auto_fill_remove_block:

Removing a block
---------------------------------------------------------------------------------------------------

A block can be removed from the content by setting it to an **empty value**, which can be an
*empty dictionary, empty list or tuple, none, negative number, or boolean false*. The following
example uses a ``None`` object to remove the wrapper block ``MIDNAME_WRAP`` defining a content
with the variable for a middle name inside:

.. code-block:: python

    blk = blockie.Block("<NAME> <MIDNAME_WRAP><MIDNAME> </MIDNAME_WRAP><SURNAME>")
    blk.fill({"name": "Patrick", "surname": "Bateman", "midname_wrap": None})
    print(blk.content)

prints:

.. code-block:: text

    Patrick Bateman

.. note::
    Notice how using a wrapper block allows a better control over the parts removed from the
    generated content. In the example above, it it allows to remove the variable for a middle
    name and also the space character that would otherwise remain in the generated content.


.. _tgt_auto_fill_advanced_example:

Advanced example
---------------------------------------------------------------------------------------------------

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
      Items                                                         Quantity
    ------------------------------------------------------------------------
    * apples                                                        1 kg
    * IMPORTANT! potatoes                                           2 kg
    * rice                                                          1 kg
    * orange juice                                                  1 l
    * MAYBE? cooking magazine


    Short list: apples, potatoes, rice, orange juice, cooking magazine


.. _tgt_manual_fill:

***************************************************************************************************
Manual template filling
***************************************************************************************************
