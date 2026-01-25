.. _tgt_config:

###################################################################################################
Configuration and examples
###################################################################################################

***************************************************************************************************
Tags configuration
***************************************************************************************************

The format of :ref:`tags <tgt_tags>` in a template, together with other settings, can be
configured by the configuration object of the :py:class:`.BlockConfig` class.

The configuration object attributes define the format of :ref:`primary tags <tgt_tags>`
using functions defining how a template tag string is generated from a tag name. The most
straightforward way to define these tag generators is to use the *lamba* functions.

The tabulator size attribute is used by the :ref:`alignment autotag <tgt_auto_align_var>` when
tabulators are used for the alignment.

The created :py:class:`.BlockConfig` object can be either assigned directly to the
:py:attr:`.Block.config` attribute or it can be assigned in the :py:class:`.Block` object
constructor :py:meth:`.Block.__init__`. All child blocks of a configured block will automatically
use the same configuration.


.. _tgt_examples:

***************************************************************************************************
Examples
***************************************************************************************************

The *samples/demo_advanced.py* file, provides various examples that should serve as an additional
source of information and inspiration for further experimentation.

The most important demo functions are:

-   **General examples**

    -   ``demo_shoplist_advanced``: A shopping list generated using most of the :ref:`data-driven
        filling <tgt_data_fill>` features.
    -   ``demo_shoplist_advanced_custom_cfg``: A shopping list generated from a template using
        custom :ref:`tag format configuration <tgt_config>`.

.. _tgt_extensions:

-   **Custom feature extensions** implemented using the :ref:`fill handler <tgt_fill_hndl>` with
    :ref:`manual filling methods <tgt_man_fill>`

    -   ``demo_macros_1`` and ``demo_macros_2``: *Template macros*, i.e., template blocks
        referenced in multiple places in the template and filled with different data.
    -   ``demo_extensions_1`` and ``demo_extensions_2``: *Template extensions*, i.e., modification
        of existing template blocks using other custom extension blocks.
