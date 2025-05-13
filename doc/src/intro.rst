###################################################################################################
Introduction
###################################################################################################

`Blockie <https://github.com/lubomilko/blockie>`_ is an extremely lightweight and simple universal
Python-based template engine. It can generate various types of text-based content, e.g., standard
text, source code, data files or markup language files like HTML or XML.

Blockie is a minimalistic answer to the existing popular template engines that are usually bulky
and difficult to use, requiring users to learn a template language and other complex principles
and then ending up with templates looking more like a source code then a template.

Blockie uses very simple logic-less templates with no attempts to emulate a general-purpose
programming language. The template filling logic is defined by the structure of the provided
data and supplemented by the user-defined Python script using blockie to make the process of
filling the templates with data reasonably simple.

.. code-block:: text

    +----------+   +------------+
    | template |   | input data |
    +----------+   +------------+
          |               |
          V               V
      +-----------------------+
      | Python filling script |
      |     using blockie      |
      +-----------------------+
                  |
                  V
        +-------------------+
        | generated content |
        +-------------------+
