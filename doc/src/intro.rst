###################################################################################################
Introduction
###################################################################################################

`Blockie <https://github.com/lubomilko/blockie>`_ is an extremely lightweight and simple universal
Python-based template engine. It can generate various types of text-based content, e.g., standard
text, source code, data files or markup language content like HTML, XML or markdown.

Blockie is a minimalistic answer to the existing popular template engines that are usually bulky
and difficult to use, requiring users to learn a template language and other complex principles,
with templates often approaching the form of a source code. Many template-based projects do not
need such complexity, and Blockie offers a much simpler approach with only a few simple but
extremely multipurpose principles and clean, logicless templates. If a more advanced
template-filling logic is needed, then it is expected to be defined directly within the
user-defined Python script, which avoids the need for a custom template language.

.. note::
    The reasoning behind using a standard Python script to control certain parts of the template
    filling is that the input data in many cases need some additional processing anyway, so
    the commands that other template engines define through custom logic constructs within a
    template itself, can just as well be located directly within the script that loads the
    template, provides the input data, and potentially performs additional processing, etc.

The block diagram below illustrates the fairly standard process of generating the content from a
template using values defined in the input data:

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


***************************************************************************************************
Quickstart
***************************************************************************************************

For a quick overview, jump straight to the :ref:`basic example <tgt_auto_fill_basic_example>` or
even to the more :ref:`advanced example <tgt_auto_fill_advanced_example>` that illustrates the
most important principles of Blockie.
