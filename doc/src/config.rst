.. _tgt_config:

###################################################################################################
Configuration
###################################################################################################

The format of :ref:`primary <tgt_primary_tags>` and :ref:`automatic <tgt_auto_tags>` tags in a
template, together with other settings, can be configured by the configuration object of the
:py:class:`.BlockConfig` class.

The configuration object attributes define the format of :ref:`primary tags <tgt_primary_tags>`
using functions defining how a template tag string is generated from a tag name. The most
straightforward way to define these tag generators is to use the *lamba* functions.

The configuration object contains also attributes defining the symbols used for the
:ref:`automatic tags <tgt_auto_tags>`, and a tabulator size attribute used by the *alignment
autotag* when tabulators are used for the alignment.

The following example of a block configuration object uses the *at* sign ``@`` as a primary tag
symbol:

.. code-block:: python

    config = BlockConfig(
        lambda name: f"@{name}",    # tag_gen_var
        lambda name: f"@{name}",    # tag_gen_blk_start
        lambda name: f"@!{name}",   # tag_gen_blk_end
        lambda name: f"@~{name}",   # tag_gen_blk_vari
        "*",                        # autotag_align
        "_",                        # autotag_vari
        8                           # tab_size
    )

The template tags configured by the configuration object above have the following format:

* Variable: ``@name``.
* Block start: ``@name``.
* Block end: ``@!name``.
* Block variation separator: ``@~name``.
* Alignment autotag: ``@*``.
* Variation autotag: ``@_``.

The configuration object ``config`` can then be assigned to the primary :py:class:`.Block` object
in its constructor :py:meth:`.Block.__init__` as illustrated below:

.. code-block:: python

    blk = Block(template, config=config)

Alternatively, the configuration object can be assigned directly to the :py:attr:`.Block.config`
attribute.

All child blocks of a configured block will automatically use the same configuration.
