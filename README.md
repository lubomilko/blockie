# Blockie template engine

[Blockie](https://github.com/lubomilko/blockie) is an extremely lightweight and simple universal
Python-based template engine. It can generate various types of text-based content, e.g., standard
text, source code, data files or markup language files like HTML or XML.

Blockie is a minimalistic answer to the existing popular template engines that are usually bulky
and difficult to use, requiring users to learn a template language and other complex principles
and then ending up with templates looking more like a source code then a template.

Blockie uses very simple logic-less templates with no attempts to emulate a general-purpose
programming language. The template filling logic is defined by the structure of the provided
data and supplemented by the user-defined Python script using blockie to make the process of
filling the templates with data reasonably simple.


# Quick start

The following Python script serves as a small illustration of all basic principles. The template
is loaded from the `template` string and filled using the `data` dictionary. Then the generated
content is printed at the end.

``` python
  from blockie import Block


  template = """
                              SHOPPING LIST
    Items                                                         Quantity
  ------------------------------------------------------------------------
  <ITEMS>
  * <FLAG>IMPORTANT! <^FLAG>MAYBE? </FLAG><ITEM><+>               <QTY><UNIT> kg<^UNIT> l</UNIT>
  </ITEMS>


  Short list: <ITEMS><ITEM><.>, <^.></.></ITEMS>
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

  blk = Block(template)
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
* rice                                                          1 kg
* orange juice                                                  1 l
* MAYBE? cooking magazine


Short list: apples, potatoes, rice, orange juice, cooking magazine
```


Please read a more detailed [documentation here](https://lubomilko.github.io/blockie).
