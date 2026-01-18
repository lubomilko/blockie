###################################################################################################
Introduction
###################################################################################################

`Blockie <https://github.com/lubomilko/blockie>`_ is a lightweight, universal and easy to use
Python-based template engine. It was developed as a lower-level and generic solution for the
generation of any type of text-based content including a standard text, markup language, source
code, and various data files without using complex program-like logic constructs in the templates.

Blockie uses logicless templates consisting of the so-called :ref:`variables and blocks
<tgt_tags>`. No other template elements are used, although there are some variables and
blocks with special functionalities. The logic of filling the template with values follows just
a few general principles. Typically, the filling logic can be defined just by the structure of
the input data with optional further customization implemented by the user-defined Python script.


***************************************************************************************************
Installation and quickstart
***************************************************************************************************

The Blockie package can be installed from the `Python Package Index
<https://pypi.org/project/blockie/>`__ using the `pip <https://pypi.org/project/pip/>`__ console
command: ``pip install blockie``.

The block diagram below illustrates a fairly standard process of generating a text *content*
from the *template* using values defined in the *input data*.

.. code-block:: text

    +----------+   +------------+
    | template |   | input data |
    +----------+   +------------+
          |              |
          V              V
      +-----------------------+
      | Python filling script |
      | using blockie module  |
      +-----------------------+
                  |
                  V
        +-------------------+
        | generated content |
        +-------------------+

In the simplest form, the user-defined *Python filling script* is just a set of three commands
illustrated in the example below using a more complex template to show most of the :ref:`automated
template filling <tgt_auto_fill>` concepts used by Blockie for the input data provided in form of
an appropriately structured Python dictionary or a struct-like object.

.. code-block:: python

    import blockie

    template = """
                    SHOPPING LIST
      Items                             Quantity
    --------------------------------------------
    <ITEMS>
    <FLAG>IMPORTANT! <^FLAG>MAYBE? </FLAG>
    * <@FLAG><ITEM><+>                  <QTY><UNIT> kg<^UNIT> l<^UNIT> m</UNIT>
    <ALTS><.><*>, <^.><*><^.>  - Alternatives: <*>, </.></ALTS>
    </ITEMS>
    
    Short list: <ITEMS><ITEM><FLAG>!<^FLAG>?</FLAG><.>, <^.></.></ITEMS>
    """

    data = {
        "items": [
            {"flag": 0, "item": "potatoes", "qty": "2", "unit": 0, "alts": None},
            {"flag": 0, "item": "rice", "qty": "1", "unit": 0, "alts": None},
            {"flag": None, "item": "orange juice", "qty": "1", "unit": 1,
             "alts": ["apple juice", "fruit mix juice", "cola"]},
            {"flag": None, "item": "duct tape", "qty": "50", "unit": 2, "alts": None},
            {"flag": 1, "item": "cooking magazine", "qty": None, "unit": None, "alts": None}
        ]
    }

    # User-defined template filling script:
    blk = blockie.Block(template)   # 1. Create the primary block and load its template.
    blk.fill(data)                  # 2. Fill the template blocks and variables with data values.
    print(blk.content)              # 3. Get the generated content from the primary block.

Prints the following output:

.. code-block:: text

                    SHOPPING LIST
      Items                             Quantity
    --------------------------------------------
    * IMPORTANT! potatoes               2 kg
    * IMPORTANT! rice                   1 kg
    * orange juice                      1 l
      - Alternatives: apple juice, fruit mix juice, cola
    * duct tape                         50 m
    * MAYBE? cooking magazine
    
    Short list: potatoes!, rice!, orange juice, duct tape, cooking magazine?

Any required additional template filling logic can be implemented within the Python script either
by restructuring the original input data and/or using the :ref:`low-level functions
<tgt_manual_fill>` provided by the Blockie module to precisely control the content generation.
The script can also :ref:`configure <tgt_config>` a different format of template tags.
