.. _tgt_config:

###################################################################################################
Template format configuration
###################################################################################################

The format of :ref:`primary <tgt_primary_tags>` and :ref:`automatic <tgt_auto_tags>` secondary
tags in a template, together with other settings, can be configured by the configuration object of
the :py:class:`.BlockConfig` class.

The configuration object attributes define the format of :ref:`primary tags <tgt_primary_tags>`
using functions defining how a template tag string is generated from a tag name. The most
straightforward way to define these tag generators is to use the *lamba* functions.

The configuration object also contains the attributes defining the symbols used for the
:ref:`automatic tags <tgt_auto_tags>`, and a tabulator size attribute used by the *alignment
autotag* when tabulators are used for the alignment.

The created :py:class:`.BlockConfig` object can be either assigned directly to the
:py:attr:`.Block.config` attribute or it can be provided to the :py:class:`.Block` object
constructor :py:meth:`.Block.__init__`. All child blocks of a configured block will automatically
use the same configuration.


Example
===================================================================================================

The following example equivalent to the :ref:`advanced example <tgt_auto_fill_advanced_example>`
shown before, uses a block configuration object with an *at* sign ``@`` used as a primary tag
symbol:

.. code-block:: python

    template = """
                                SHOPPING LIST
      Items                                                         Quantity
    ------------------------------------------------------------------------
    @items
    * @flagIMPORTANT! @~flagMAYBE? @!flag@item@*                    @qty@unit kg@~unit l@!unit
    @!items


    Short list: @items@item@_, @~_@!_@!items
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

    config = blockie.BlockConfig(
        lambda name: f"@{name}",    # tag_gen_var
        lambda name: f"@{name}",    # tag_gen_blk_start
        lambda name: f"@!{name}",   # tag_gen_blk_end
        lambda name: f"@~{name}",   # tag_gen_blk_vari
        "*",                        # autotag_align
        "_",                        # autotag_vari
        8                           # tab_size
    )

    blk = blockie.Block(template, config=config)
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
