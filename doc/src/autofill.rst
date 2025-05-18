.. _tgt_auto_fill:

###################################################################################################
Automatic template filling
###################################################################################################

The automatic template filling is the simplest way to generate a templated content. To fill the
template variables and blocks with data, it is first necessary to load the whole template into
the primary :py:class:`.Block` object. This can be done by setting a template string text or a
text file in the :py:meth:`.Block.__init__` constructor. Alternatively, the
:py:attr:`.Block.template` attribute, or the :py:meth:`.Block.load_template` method can be used.

A template can then be filled using the :py:meth:`.Block.fill` method with the required data
provided as an argument in a Python **dictionary**. The dictionary keys represent the template
:ref:`variable and block tags <tgt_primary_tags>`. The data dictionary needs to 

.. note::
    In reality, the automatic template filling process is, of course, not fully automatic. It is
    necessary to provide the data to fill the template in a correct format matching the template
    structure. However, the filling process is then all done by the :py:meth:`.Block.fill` method,
    unlike with a :ref:`manual approach <tgt_manual_fill>`, where the filling script needs to call
    the individual :py:class:`.Block` methods to generate the required content.


.. _tgt_auto_fill_basic:

***************************************************************************************************
Basic automatic filling
***************************************************************************************************

The values assigned to the data dictionary keys representing template tags can perform various
operations described in the sections below depending on the data type of the dictionary value.


Setting a variable value
===================================================================================================

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


Setting a block content
===================================================================================================

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


Cloning a block and setting its content
===================================================================================================

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


.. important::
    The blocks having multiple :ref:`content variations <tgt_primary_tags_content_vari>` cannot
    be cloned directly. They can, however, be cloned indirectly by "wrapping" them in a standard
    parent block that can be cloned, e.g.,
    ``<DATE_WRAP><DATE><DAY>.<MONTH>.<^DATE><DAY> <MONTH></DATE><DATE_WRAP>``, where the
    ``DATE_WRAP`` block content can be cloned and each clone would contain a new ``DATE`` block
    having two content variations.

    Note that the process of
    :ref:`setting the selected block content variation <tgt_auto_fill_advanced_set_block_vari>`
    is described later.


.. _tgt_auto_fill_basic_example:

Example
===================================================================================================

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

***************************************************************************************************
Advanced automatic filling
***************************************************************************************************

Similarly to the :ref:`basic operations <tgt_auto_fill_basic>`, the values in a data dictionary
can also perform additional operations described in the following sections.


Setting a block content as is
===================================================================================================

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


.. _tgt_auto_fill_advanced_set_block_vari:

Setting a block content variation
===================================================================================================

A specific content from a block with multiple content variations can be selected using a
**special** ``vari_idx`` **key with a numeric value** defined in a *dictionary* corresponding to
the block. The value of a number assigned to the ``vari_idx`` key defines one of the operations
below:

-   A value equal to zero or higher (*>=0*) selects the block content variation with an index
    corresponding to the provided value.
-   A negative value (*<0*) removes the entire block from the generated content.
-   A boolean value can be used, where ``True`` has the same effect as the value zero and
    ``False`` has the same effect as a negative value.

.. note::
    Note that removing a block using a ``vari_idx`` key set to a negative value is only the
    secondary purpose of the ``vari_idx`` key. The primary method of a
    :ref:`block removal <tgt_auto_fill_remove_block>` is described later.

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
    the filling script, since the blockie templates are logicless.


Setting a handler for manual filling
===================================================================================================

.. note::
    The manual filling process is only needed in very special use cases, so in vast majority of
    common applications this section can be skipped.

The automatic method of filling the block template can be partially suplemented by the
:ref:`manual method <tgt_manual_fill>` using a **special** ``fill_hndl`` **key with a handler
function value** defined in a *dictionary* corresponding to the block. The function assigned to
the ``fill_hndl`` key defines a handler called when a block is being filled. The handler function
can call the :py:class:`.Block` methods to perform special low-level operations if needed.

The handler function must use the following declaration:

.. code-block:: python

    func(block: Block, data: dict | object, clone_subidx: int) -> None

where:

*   ``block``: A :py:class:`.Block` object corresponding to the template block for which the
    handler has been called.
*   ``data``: The dictionary (or optionally a custom object) used for filling the content of a
    block.
*   ``clone_subidx``: An index of a cloned content being filled. Only applicable if the block is
    being cloned during the automatic filling process.

The example below illustrates the use of a manual filling handler for making the ``MONTH``
variable value using uppercase letters if it is a string and then setting the content variation
of the ``DATE`` block using the :py:meth:`.Block.set` method:

.. code-block:: python

    def format_month(block: blockie.Block, data: dict, _clone_subidx: int) -> None:
        if isinstance(data["month"], str):
            data["month"] = data["month"].upper()
            block.get_subblock("date").set(vari_idx=1)
        else:
            block.get_subblock("date").set(vari_idx=0)

    blk = blockie.Block("<DATE><DAY>.<MONTH>.<^DATE><DAY> <MONTH></DATE>")
    blk.fill({"day": 24, "month": "December", "fill_hndl": format_month})
    print(blk.content)

prints:

.. code-block:: text

    24 DECEMBER


Removing a variable
===================================================================================================

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
===================================================================================================

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

Example
===================================================================================================

The filling script below expands the :ref:`basic automatic filling concepts <tgt_auto_fill_basic>`
using the advanced operations described above. The script uses a template loaded from a text file
and data to fill it are loaded from a JSON file. The generated content is then saved into the
output text file.

The template input file *shoplist_tmpl.txt*:

.. code-block:: text

                                    SHOPPING LIST
      Items                                                         Quantity
    ------------------------------------------------------------------------
    <ITEMS>
    * <FLAG>IMPORTANT! <^FLAG>MAYBE? </FLAG><ITEM><+>               <QTY><UNIT> kg<^UNIT> l</UNIT>
    </ITEMS>


    Short list: <ITEMS><ITEM><.>, <^.></.></ITEMS>

The input data file *shoplist_data.json*:

.. code-block:: json

    {
        "items": [
            {"item": "apples", "qty": "1", "unit": 0},
            {"item": "potatoes", "qty": "2", "unit": 0},
            {"item": "rice", "qty": "1", "unit": 0},
            {"item": "orange juice", "qty": "1", "unit": 1},
            {"item": "cooking magazine", "qty": null, "unit": null}
        ]
    }

The script code:

.. code-block:: python

    import json
    from blockie import Block

    important_items = ("potatoes", "rice")
    maybe_items = ("cooking magazine",)

    with open("shoplist_data.json", encoding="utf-8") as file:
        data = json.load(file)

        for item in data["items"]:
            item["flag"] = 0 if item["item"] in important_items else \
                1 if item["item"] in maybe_items else None

        blk = blockie.Block()
        blk.load_template("shoplist_tmpl.txt")
        blk.fill(data)
        blk.save_content("shoplist_gen.txt")

.. note::
    Notice that the value of the ``FLAG`` variable in the template is defined by the script
    setting the ``flag`` key value into the input dictionary data. This is done to illustrate
    how to     control the template filling logic within the script, since the Blockie templates
    are logicless.

The generated output file *shoplist_gen.txt*:

.. code-block:: text

                                SHOPPING LIST
      Items                                                         Quantity
    ------------------------------------------------------------------------
    * apples                                                        1 kg
    * IMPORTANT! potatoes                                           2 kg
    * IMPORTANT! rice                                               1 kg
    * orange juice                                                  1 l
    * MAYBE? cooking magazine                                       


    Short list: apples, potatoes, rice, orange juice, cooking magazine
