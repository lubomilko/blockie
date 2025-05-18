# Blockie template engine

[Blockie](https://github.com/lubomilko/blockie) is an extremely lightweight and simple universal
Python-based template engine. It can generate various types of text-based content, e.g., standard
text, source code, data files or markup language content like HTML, XML or markdown.

Blockie is aimed to be used in template-based projects that do not need templates containing
complex custom commands or programming language parsers. Instead, Blockie uses only a few simple
but extremely multipurpose principles and clean, logicless templates. If a more advanced
template-filling logic is needed, then it is expected to be defined directly within the
user-defined Python script, which avoids the need for a custom template language.

The block diagram below illustrates the fairly standard process of generating the content from a
template using values defined in the input data:

``` text
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
``` 

Please read the full [documentation here](https://lubomilko.github.io/blockie).


# Quick start

The following Python script serves as a simple illustration of all basic principles. The template
is loaded from the `template` string and filled using the `data` dictionary with the `FLAG`
variable in the template defined by the script since the Blockie templates are logicless. At the
end the generated content is printed out.

``` python
    import blockie


    template = """
                                SHOPPING LIST
      Items                                                         Quantity
    ------------------------------------------------------------------------
    <ITEMS>
    * <FLAG>IMPORTANT! <^FLAG>MAYBE? </FLAG><ITEM><+>               <QTY><UNIT> kg<^UNIT> l</UNIT>
    </ITEMS>


    Short list: <ITEMS><ITEM><.>, <^.></.></ITEMS>
    """

    important_items = ("potatoes", "rice")
    maybe_items = ("cooking magazine",)

    data = {
        "items": [
            {"item": "apples", "qty": "1", "unit": 0},
            {"item": "potatoes", "qty": "2", "unit": 0},
            {"item": "rice", "qty": "1", "unit": 0},
            {"item": "orange juice", "qty": "1", "unit": 1},
            {"item": "cooking magazine", "qty": None, "unit": None}
        ]
    }

    for item in data["items"]:
        item["flag"] = 0 if item["item"] in important_items else 1 if item["item"] in maybe_items else None

    blk = blockie.Block(template)
    blk.fill(data)
    print(blk.content)
```

Prints the following generated content:

``` text
                            SHOPPING LIST
  Items                                                         Quantity
------------------------------------------------------------------------
* apples                                                        1 kg
* IMPORTANT! potatoes                                           2 kg
* IMPORTANT! rice                                               1 kg
* orange juice                                                  1 l
* MAYBE? cooking magazine                                       


Short list: apples, potatoes, rice, orange juice, cooking magazine
```
