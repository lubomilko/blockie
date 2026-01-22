###################################################################################################
Basic principles
###################################################################################################

***************************************************************************************************
Template elements overview
***************************************************************************************************

The variable elements of the template intended to be filled with specific values from the input
data are indicated by tags. By default, the tags have an XML-like format and their names use
uppercase letters. The template consists of two primary elements defined by their corresponding
tags:

-   :ref:`Variables <tgt_variables>` defined by a single tag, e.g., ``<NAME>``.
-   :ref:`Blocks <tgt_blocks>` defined by the two start and end tags, e.g., ``<LIST> ... </LIST>``,
    with a content consisting of other blocks and variables between these tags. The whole template
    is also considered to be a block despite not having any explicitly defined start and end tags.


***************************************************************************************************
Template filling essentials
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
