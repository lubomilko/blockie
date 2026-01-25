# Blockie - Lightweight Python template engine

## Introduction

[Blockie](https://github.com/lubomilko/blockie) is a lightweight, fast, universal and easy to
use low-level Python-based template engine. It was developed as an expandable solution with
uncluttered templates for the generation of any type of text-based content, including a
standard text, markup language, source code, and various data files.

Blockie uses simple logicless templates consisting of two types of elements: *variables* and
*blocks*. In most cases, the logic of filling the template can be driven by the input data
structure and values. No custom script-like statements are needed. However, an additional
logic can be implemented directly in the Python script running the template filling process.

Please read the full [documentation here](https://lubomilko.github.io/blockie).


## Installation

The Blockie package can be installed from the [Python Package Index](https://pypi.org/project/blockie/)
using the [pip](https://pypi.org/project/pip/) console command:

``` console
> pip install blockie
```


## Quick start

The content generation follows the sequence below:

``` text
template + input data -> Python filling script -> generated content
```

In the simplest form, the user-defined *Python filling script* can be a set of just three commands
illustrated in the example below that shows the most important principles of the data-driven
template filling used by Blockie for the input data provided in form of an appropriately
structured Python dictionary or a struct-like object.

``` python
import blockie

template = """
                SHOPPING LIST
  Items                             Quantity
--------------------------------------------
<ITEMS>
* <ITEM><+>                         <QTY><UNIT> kg<^UNIT> l</UNIT>
</ITEMS>

Short list: <ITEMS><ITEM><.>, <^.></.></ITEMS>
"""

data = {
    "items": [
        {"item": "potatoes", "qty": 2, "unit": 0},
        {"item": "rice", "qty": 1, "unit": 0},
        {"item": "orange juice", "qty": 1, "unit": 1},
        {"item": "cooking magazine", "qty": None, "unit": None},
    ]
}

# User-defined template filling script:
blk = blockie.Block(template)   # 1. Create the primary block and load its template.
blk.fill(data)                  # 2. Fill the template blocks and variables with data values.
print(blk.content)              # 3. Get the generated content from the primary block.
```

Output:

``` text
                SHOPPING LIST
  Items                             Quantity
--------------------------------------------
* potatoes                          2 kg
* rice                              1 kg
* orange juice                      1 l
* cooking magazine

Short list: potatoes, rice, orange juice, cooking magazine
```

Any required additional template filling logic can be implemented within the Python script either
by restructuring the original input data and/or using the low-level manual filling functions
provided by the Blockie module to precisely control the content generation. The script can also
configure a different format of template tags.


## License

> Blockie - Lightweight Python template engine.
> 
> Copyright (C) 2025 Lubomir Milko
> This file is part of blockie <https://github.com/lubomilko/blockie>.
> 
> No generative artificial intelligence (AI) was used in the development process.
> 
> This program is free software: you can redistribute it and/or modify
> it under the terms of the GNU General Public License as published by
> the Free Software Foundation, either version 3 of the License, or
> (at your option) any later version.
> 
> This program is distributed in the hope that it will be useful,
> but WITHOUT ANY WARRANTY; without even the implied warranty of
> MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
> GNU General Public License for more details.
> 
> You should have received a copy of the GNU General Public License
> along with this program. If not, see <https://www.gnu.org/licenses/>.
