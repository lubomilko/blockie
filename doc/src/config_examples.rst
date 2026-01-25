.. _tgt_config:

###################################################################################################
Configuration and examples
###################################################################################################

***************************************************************************************************
Tags configuration
***************************************************************************************************

The format of :ref:`tags <tgt_tags>` in a template, together with other settings, can be
configured by the :py:class:`.BlockConfig` configuration object.

The configuration object attributes define the format of :ref:`template tags <tgt_tags>`
using functions defining how a template tag string is generated from a tag name. The most
straightforward way to define these tag generators is to use the *lamba* functions.

The tabulator size attribute is used by the :ref:`alignment autotag <tgt_auto_align_var>` when
tabulators are used for the alignment.

The block configuration can be modified by the :py:attr:`.Block.config` attribute. Alternatively,
a :py:class:`.BlockConfig` object can be created and set as an attribute to the :py:class:`.Block`
object constructor or assigned to the :py:attr:`.Block.config` attribute.

All child :py:class:`.Block` objects use the same configuration as their parent block.

A simple demo function using the custom tag format configuration can be found in the
:ref:`examples <tgt_examples>` listed in the following section.


.. _tgt_examples:

***************************************************************************************************
Examples
***************************************************************************************************

The *demo_advanced.py* file in the *samples* directory provides various examples that should serve
as an additional source of information and inspiration for further experimentation.

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
