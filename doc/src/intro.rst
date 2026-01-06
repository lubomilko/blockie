###################################################################################################
Introduction
###################################################################################################

`Blockie <https://github.com/lubomilko/blockie>`_ is a lightweight, universal and easy to use
Python-based template engine. It can generate various types of text-based content including a
standard text, markup language content, source code in any language and various data files.

Blockie is an alternative to the existing popular template engines that are often bulky and might
be difficult to use for the purposes that they were originally not intended for. Most template
engines also require users to learn a template language and its constructs that are often
approaching the complexity of a simple programming language.

Blockie offers a simple approach with logicless templates primarily consisting of the so-called
*blocks* and *variables* inside them. There are no other template constructs and the logic of
filling the template with values uses just a few simple principles. If a more advanced
template-filling logic is needed, then it can be implemented directly by the user-defined
Python script.

The block diagram below illustrates the fairly standard process of generating the *content* from a
*template* using values defined in the *input data*.

.. code-block:: text

    +----------+   +------------+
    | template |   | input data |
    +----------+   +------------+
          |              |
          V              V
      +-----------------------+
      | Python filling script |
      |     using blockie     |
      +-----------------------+
                  |
                  V
        +-------------------+
        | generated content |
        +-------------------+

The *Python filling script* can in many cases be just a simple set of three template-filling
commands that are later described in the :ref:`Automatic template filling <tgt_auto_fill>` chapter:

1. Create the main *block* and load its template.
2. Fill the template *blocks* and *variables* with the loaded input data.
3. Get the generated content from the main *block*.


***************************************************************************************************
Quickstart
***************************************************************************************************

For a quick overview, jump straight to the :ref:`basic example <tgt_auto_fill_basic_example>` or
even to the more :ref:`advanced example <tgt_auto_fill_advanced_example>` that illustrates the
most important principles of Blockie.
