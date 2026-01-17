###################################################################################################
Introduction
###################################################################################################

`Blockie <https://github.com/lubomilko/blockie>`_ is a lightweight, universal and easy to use
Python-based template engine. It was developed as a lower-level and generic solution for the
generation of any type of text-based content including a standard text, markup language, source
code, and various data files.

Blockie uses logicless templates consisting of the so-called :ref:`variables and blocks
<tgt_primary_tags>`. There are no other template constructs and the logic of filling the template
with values follows just a few generic principles. Typically, the filling logic is defined by
the structure of input data. Additional customization can be implemented by the user-defined
Python script that can also use low-level functions provided by the Blockie module.


***************************************************************************************************
Installation and quickstart
***************************************************************************************************

The Blockie package can be installed from the `Python Package Index
<https://pypi.org/project/blockie/>`__ using the `pip <https://pypi.org/project/pip/>`__ console
command:

.. code-block:: console

    > pip install blockie

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
      |     using blockie     |
      +-----------------------+
                  |
                  V
        +-------------------+
        | generated content |
        +-------------------+

In the simplest form, the user-defined *Python filling script* is just a set of three commands
illustrated in the example below showing most of the :ref:`automated template filling 
<tgt_auto_fill>` concepts used by Blockie for the input data provided in form of an appropriately
structured Python dictionary or a struct-like object (note that the format of template tags is
:ref:`configurable <tgt_config>`).

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
