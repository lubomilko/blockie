###################################################################################################
Automatic template elements
###################################################################################################

The template can contain special so-called *automatic* variables and blocks, meaning that they are
filled automatically without any values specified in the input data.


.. _tgt_auto_align_var:

***************************************************************************************************
Automatic left-alignment variable
***************************************************************************************************

A left-alignment automatic variable has a ``<+>`` tag and can be used to maintain the
left-alignment of a text within the template having :ref:`variables <tgt_variables>` filled with
values of different character lengths.

Blockie automatically scans the first character located right after this tag and counts the number
of consecutive occurrences of this character until a different character is found. Then it
maintains the column position of the different character regardless of the content generated
on the line before this character.

.. code-block:: python

    template = """
    Name        Surname     Role
    ----------------------------
    <CHARACTERS>
    <NAME><+>   <SNAME><+>  <ROLE>
    </CHARACTERS>"""

    blk = blockie.Block(template)
    blk.fill({"characters": [
        {"name": "Dave", "sname": "Bowman", "role": "astronaut 1"},
        {"name": "Frank", "sname": "Poole", "role": "astronaut 2"},
        {"name": "Heywood", "sname": "Floyd", "role": "chairman of the US National Council of Astronautics"},
        {"name": "HAL", "sname": "9000", "role": "broken computer that can kill, but can't lie"}]})
    print(blk.content)

Output:

.. code-block:: text

    Name        Surname     Role
    ----------------------------
    Dave        Bowman      astronaut 1
    Frank       Poole       astronaut 2
    Heywood     Floyd       chairman of the US National Council of Astronautics
    HAL         9000        broken computer that can kill, but can't lie

.. code-block:: python

    template = """
    Name            Phone number
    ----------------------------
    <PEOPLE>
    <NAME><+>.......<PHONE>
    </PEOPLE>"""

    blk = blockie.Block(template)
    blk.fill({"people": [
        {"name": "Dave", "phone": "0940 123 456"},
        {"name": "Frank", "phone": "0933 987 654"},
        {"name": "Heywood", "phone": "0911 111 111"}]})
    print(blk.content)

Output:

.. code-block:: text

    Name            Phone number
    ----------------------------
    Dave............0940 123 456
    Frank...........0933 987 654
    Heywood.........0911 111 111


.. _tgt_auto_block_var:

***************************************************************************************************
Automatic block variable
***************************************************************************************************

A :ref:`block <tgt_blocks>` content can be :ref:`set <tgt_set_blk_cont>` into a different location
than its original location, or into multiple different locations within the template using a
special tag having a ``<@BLOCK_NAME>`` format. This so-called *block variable* acts as a target
for a block content, while the original block is :ref:`cleared <tgt_clear_blk>`.

The block variable can be useful for repeating the referenced content multiple times or for
maintaining the :ref:`left-alignment <tgt_auto_align_var>` as illustrated in the example below.

.. code-block:: python

    template = """
    <LIST>
    <IDX>a)<^IDX>b)<^IDX>c)<^IDX>d)<^IDX>e)<^IDX>f)</IDX>
    <@IDX> <ITEM><+>        <QTY>
    </LIST>
    """

    blk = blockie.Block(template)
    blk.fill({"list": [
        {"idx": 0, "item": "first", "qty": 1},
        {"idx": 1, "item": "second", "qty": 2},
        {"idx": 2, "item": "third", "qty": 3}]})
    print(blk.content)

Output:

.. code-block:: text

    a) first                1
    b) second               2
    c) third                3

.. note::
    The block variable tag(s) must be located within the parent block of a referenced block.


.. _tgt_auto_vari_block:

***************************************************************************************************
Automatic variation block
***************************************************************************************************

With :ref:`cloned block contents <tgt_blk_cont_clone>` it is often useful to have some part of the
block content to be different in the first and/or the last clone. An *automatic variation block*
can be used to define such part of the content using a special ``<.>`` block tag having either two
or three :ref:`content variations <tgt_set_blk_cont_vari>`:

- ``<.>standard content<^.>last content</.>``
- ``<.>standard content<^.>last content<^.>first content</.>``

Where the ``standard content`` is used in the second and second to last clones of a parent block,
the ``last content`` is used in the last clone, and the ``first content`` is used in the first
parent block content.

.. code-block:: python

    blk = blockie.Block("Characters: <CHARACTERS><NAME> <SURNAME><.>, <^.></.></CHARACTERS>.")
    blk.fill({"characters": [
        {"name": "Dave", "surname": "Bowman"},
        {"name": "Frank", "surname": "Poole"},
        {"name": "Heywood", "surname": "Floyd"},
        {"name": "HAL", "surname": "9000"}]})
    print(blk.content)

Output:

.. code-block:: text

    Characters: Dave Bowman, Frank Poole, Heywood Floyd, HAL 9000.

.. code-block:: python

    template = """
    <CHARACTERS>
    <.>
    | <NAME><+>     <SURNAME><+> |
    <^.>
    | <NAME><+>     <SURNAME><+> |
    +----------------------------+
    <^.>
    +----------------------------+
    | <NAME><+>     <SURNAME><+> |
    </.>
    </CHARACTERS>"""

    blk = blockie.Block(template)
    blk.fill({"characters": [
        {"name": "Dave", "surname": "Bowman"},
        {"name": "Frank", "surname": "Poole"},
        {"name": "Heywood", "surname": "Floyd"},
        {"name": "HAL", "surname": "9000"}]})
    print(blk.content)

Output:

.. code-block:: text

    +----------------------------+
    | Dave          Bowman       |
    | Frank         Poole        |
    | Heywood       Floyd        |
    | HAL           9000         |
    +----------------------------+
