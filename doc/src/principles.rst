###################################################################################################
Overview of principles
###################################################################################################

***************************************************************************************************
Template-based content generation
***************************************************************************************************

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

Blockie templates are logicless, so they do not contain any script-like command elements. Instead,
the logic of filling the template can be defined purely by the structure of *template* elements
and *input data*. Alternatively, the *Python filling script* can use low-level functions provided
by Blockie to precisely control the content generation.


.. _tgt_tags:

***************************************************************************************************
Template tags
***************************************************************************************************

The variable elements of the template that can be filled with specific values from the input
data are indicated by *tags*. The tag format is :ref:`configurable <tgt_config>`, and by default,
the tags have an XML-like format and their names use uppercase letters.

The template can contain two primary non-constant elements defined by their corresponding tags:

-   **Variables**: The simplest modifiable parts of the template defined by a single tag, e.g.,
    ``<NAME>``.
-   **Blocks**: Used for splitting the template into multiple hierarchical parts. A block is
    defined by the start and end tags, e.g., ``<LIST> ... </LIST>``, with a content between them
    consisting of a constant text, other child blocks and variables. The whole template is also
    considered to be a primary block despite not having any explicitly defined start and end tags.

Additionally, there are special :ref:`automatic elements <tgt_auto_elems>`, i.e., variables and
blocks, that are automatically set to appropriate values in the generated content without any
additional user-defined input data or commands.


***************************************************************************************************
Template filling
***************************************************************************************************

Blocks in the template (including the whole template) can be loaded into the :py:class:`.Block`
objects to fill the template with data, i.e., to perform operations with template blocks and
variables in order to generate an output content.

Blockie provides two ways of filling the template:

-   :ref:`Data-driven <tgt_data_fill>` approach that uses the structure and content of the
    input data to control the template filling process. This method is suitable for most use
    cases and is generally more user-friendly.
-   :ref:`Manual <tgt_man_fill>` process allowing to perform low-level operations and also
    implement custom extension-like features in form of a Python script using low-level functions
    provided by Blockie at the cost of higher complexity.
