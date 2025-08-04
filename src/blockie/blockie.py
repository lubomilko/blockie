"""
Blockie - Lightweight Python template engine.

Copyright (C) 2025 Lubomir Milko
This file is part of blockie <https://github.com/lubomilko/blockie>.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from pathlib import Path
from collections.abc import Callable
from dataclasses import dataclass
from typing import Union

__author__ = "Lubomir Milko"
__copyright__ = "Copyright (C) 2025 Lubomir Milko"
__version__ = "1.0.0"
__license__ = "GPLv3"


@dataclass
class BlockConfig:
    """The template block configuration defining the format of tags and other template parts.

    Attributes:
        tag_gen_var (Callable[[str], str]): A tag generator function for a variable tag.
            Defaults to a lamba function converting a tag name ``name`` to a variable tag string
            ``<NAME>``.
        tag_gen_blk_start (Callable[[str], str]): A tag generator function for a block start tag.
            Defaults to a lamba function converting a tag name ``name`` to a block start tag
            string ``<NAME>``.
        tag_gen_blk_end (Callable[[str], str]): A tag generator function for a block end tag.
            Defaults to a lamba function converting a tag name ``name`` to a block end tag string
            ``</NAME>``.
        tag_gen_blk_vari (Callable[[str], str]): A tag generator function for a block variation
            tag.
            Defaults to a lamba function converting a tag name ``name`` to a block variation tag
            string ``<^NAME>``.
        tag_implct_iter: The *implicit iterator* tag symbol. Defaults to ``*``.
        autotag_align: The *alignment* automatic tag symbol. Defaults to ``+``.
        autotag_vari: The *variation* automatic tag symbol. Defaults to ``.``.
        tab_size: A tabulator size in the number of space characters. Used by the *alignment*
            automatic tag when tabulators are used for the alignment. Defaults to 4.
    """
    tag_gen_var: Callable[[str], str] = lambda name: f"<{name.upper()}>"
    tag_gen_blk_start: Callable[[str], str] = lambda name: f"<{name.upper()}>"
    tag_gen_blk_end: Callable[[str], str] = lambda name: f"</{name.upper()}>"
    tag_gen_blk_vari: Callable[[str], str] = lambda name: f"<^{name.upper()}>"
    tag_implct_iter: str = "*"
    autotag_align: str = "+"
    autotag_vari: str = "."
    tab_size: int = 4


class Block:
    """Block data corresponding to a part of the template within a block start and end tags.

    Attributes:
        config (BlockConfig): A block configuration primarily defining the format of tags within
            a template.
        name (str): A block name. Usually set automatically by the :meth:`get_subblock` method.
        content (str): The generated block content, i.e., a template filled with data.
        autotags (bool): Enables the automatic tags (alignment, etc.) to be filled automatically.
    """
    def __init__(self, template: str | Path = "", name: str = "", config: BlockConfig = BlockConfig()) -> None:
        """Initializes a new block object.

        Args:
            template (str | Path): Template string or a path to a text file template.
            name (str): A block name.
            config (BlockConfig): A block configuration (template tags format, tabulator size,
                etc.)
        """
        self.config: BlockConfig = config
        self.name: str = name
        self.content: str = ""
        self.autotags: bool = True

        self.__parent: Block | None = None
        self.__children: dict[str, Block] = {}
        self.__template: str = ""
        self.__clone_flag: bool = False     # Enables autoclone when setting new variables or subblocks.
        self.__autovari_first: bool = True   # Indicates use of the first content of the "variation" autotag.

        if Path(template).is_file():
            self.load_template(template)
        else:
            self.template = str(template)

    @property
    def parent(self) -> Union["Block", None]:
        """A parent block."""
        return self.__parent

    @property
    def children(self) -> dict[str, "Block"]:
        """A list of child subblocks extracted using a :meth:`get_subblock` method."""
        return self.__children

    @property
    def template(self) -> str:
        """A block template string."""
        return self.__template

    @template.setter
    def template(self, template: str) -> None:
        self.__template = template
        self.content = template

    def load_template(self, file_path: str | Path) -> None:
        """Loads the block template from a text file."""
        with open(file_path, "r", encoding="utf-8") as file_template:
            self.template = file_template.read()
            self.name = Path(file_path).name

    def save_content(self, file_path: str | Path) -> None:
        """Saves the block content to a text file."""
        with open(file_path, "w", encoding="utf-8") as file_content:
            file_content.write(self.content)

    def fill(self, data: dict | object, clone_idx: int = 0) -> int | bool:
        """Fills the block content using the data from a dictionary or an object.

        The dictionary keys or object attribute names define the template variable or a block to
        be set. The dictionary or object attribute values are used according to the rules below:

        *   Strings, integers, floats, booleans -> Variable values.
        *   Dictionary or object -> Data to be filled into a child block in a current block.
        *   List or tuple -> Content of block clones. Each element must be a dictionary or object
            with data used a for filling one cloned instance of a block.

        Two special key/attribute-value pairs can be used in a data dictionary or object:

        *   ``fill_hndl`` - ``func(block: Block, data: dict | object, clone_subidx: int) -> None``
            function: A user-defined handler function with an access to the template block object
            and a data being filled usable for special low-level operations.

        *   ``vari_idx`` - int: A variation index to be set for a variation block type
            (see the ``vari_idx`` attribute of the :meth:``set`` method).

        Args:
            data: A dictionary or object to be used for filling a block template.
            clone_idx: An internal index of a block clone being filled.

        Returns:
            int | bool: Internally used variation index for variation blocks being filled.
        """
        if data is None or isinstance(data, (list, tuple, str, int, float, bool)):
            return 0    # Do nothing if data is not a dictionary or an object.

        # Returned variation index for a block filled with data having the special vari_idx attribute.
        ret_vari_idx = 0

        # Get the block data in form of a dictionary even if it is defined as an object.
        data_dict = data if isinstance(data, dict) else data.__dict__

        # If an external fill handle is defined within the block data, then call it first.
        fill_hndl = data_dict.get("fill_hndl")
        if fill_hndl:
            fill_hndl(self, data, clone_idx)

        # 1. Loop through list or tuple elements of block data and fill the cloned blocks.
        for (attrib, value) in data_dict.items():
            if isinstance(value, (list, tuple)):
                while True:
                    subblk = self.get_subblock(attrib)
                    if not isinstance(subblk, Block):
                        # If no block is found and value is empty, then try to clear variables.
                        if not value:
                            self.clear_variables(attrib)
                        break
                    if value:
                        for (i, elem) in enumerate(value):
                            if isinstance(elem, (list, tuple, str, int, float, bool)):
                                # If an element is not an obj / dict, then make it a dict setting an implicit variable.
                                elem = {self.config.tag_implct_iter: elem}
                            subblk.fill(elem, i)
                            subblk.clone()
                        subblk.set(count=1)
                    else:
                        subblk.clear(count=1)   # Value is an empty list, i.e., [].

        # 2. Loop through object or dict elements of block data and fill the single instance (non-cloned) blocks.
        for (attrib, value) in data_dict.items():
            if not isinstance(value, (list, tuple, str, int, float, bool)) and attrib != "fill_hndl":
                while True:
                    subblk = self.get_subblock(attrib)
                    if not isinstance(subblk, Block):
                        # If no block is found and value is empty, then try to clear the variables.
                        if not value:
                            self.clear_variables(attrib)
                        break
                    if value:
                        # Get the variation index from the internal elements if they contain a vari_idx attribute.
                        vari_idx = subblk.fill(value)
                        subblk.set(vari_idx=vari_idx, count=1)
                    else:
                        subblk.clear(count=1)   # Clear block if empty data are provided.

        # 3. Loop through simple data type items of block data and fill the template tags.
        for (attrib, value) in data_dict.items():
            if isinstance(value, (str, int, float, bool)):
                if attrib == "vari_idx":
                    # If the attribute is vari_idx, then return its value to be used as a variation idx
                    # argument of the set method setting the parent block containing this attribute.
                    ret_vari_idx = value if isinstance(value, (int, bool)) else int(value)
                else:
                    while True:
                        subblk = self.get_subblock(attrib)
                        if not isinstance(subblk, Block):
                            break
                        if isinstance(value, int):
                            subblk.set(vari_idx=value, count=1)
                        elif value:
                            subblk.set(count=1)
                        else:
                            subblk.clear(count=1)   # Value is "" or False
                    self.set_variables(autoclone=False, **{attrib: value})

        return ret_vari_idx

    def get_subblock(self, *subblock_names: str) -> Union["Block", list["Block"], None]:
        """Returns the specified child block object from the current block content. Each child
        is also automatically added into the ``children`` attribute of the current block.

        Args:
            subblock_names: The tag names of blocks to be extracted from a current block content.

        Returns:
            A :class:`Block` object or a list of blocks if multiple subblock names are specified.
            ``None`` is returned if the specified block tags are not found.
        """
        ret_blk = []
        for subblock_name in subblock_names:
            subblk = None
            # Clone block if the cloning flag is set to true to ensure that the subblock tags
            # can be found in the block content and the subblock can be extracted from them.
            self.clone(passive=True)
            if subblock_name:
                (subblk_start, subblk_end) = self.__get_block_pos(subblock_name)
                if subblk_start >= 0 and subblk_end >= 0:
                    subblk = Block(self.content[subblk_start: subblk_end], subblock_name, self.config)
                    subblk.__parent = self      # pylint: disable=protected-access, unused-private-member
                    self.__children[subblock_name] = subblk
            ret_blk.append(subblk)
        return ret_blk if len(ret_blk) > 1 else ret_blk[0]

    def set_variables(self, autoclone: bool = False, **name_value_kwargs) -> None:
        """Sets values into the specified variables within this block content.

        Args:
            autoclone: Enables automatic clone of this block after setting all variables.
            name_value_kwargs: Keyword arguments representing variable name-value pairs, e.g.,
                ``name="Thomas", surname="Anderson", age=37``. Tuples or lists can be used as
                variable values, making this block to be automatically cloned after setting each
                element value.
        """
        iter_idx = 0
        detected_iters_num = 1
        while iter_idx < detected_iters_num:
            # Clone block if the cloning flag is set to true to ensure that the variable tags can be
            # found in the block content and the variable values can be set into them.
            self.clone(passive=True)
            # Loop through variable tags and replace them with the corresponding variable values.
            for (tag, val) in [(self.config.tag_gen_var(f"{name}"), val) for (name, val) in name_value_kwargs.items()]:
                if isinstance(val, str):
                    var_value = val
                else:
                    # Check if the val is iterable and if so, then set its individual elements.
                    try:
                        _ = iter(val)
                        detected_iters_num = max(detected_iters_num, len(val))
                        if len(val) > iter_idx:
                            var_value = val[iter_idx]
                        else:
                            var_value = val[-1]
                    except TypeError:
                        var_value = val
                self.content = self.content.replace(tag, f"{var_value}")
            iter_idx += 1
            if iter_idx < detected_iters_num or autoclone:
                self.clone()

    def set(self, vari_idx: int | bool = 0, all_children: bool = False, count: int = -1) -> None:
        """Sets the content of this block into its parent block content.

        Args:
            vari_idx: An index of a variation block content (if any) to be set starting from 0.
                A negative index or boolean false causes the block to be cleared. A boolean true
                is the same as index 0.
            all_children: Enables setting of all child blocks of this block before setting it.
            count: The maximum number of blocks with the same name to be set (-1 = no limit).
        """
        # Convert potentially boolean variation index to integer.
        if isinstance(vari_idx, bool):
            vari_idx = 0 if vari_idx else -1

        # If variation index is below zero, then clear the block and exit.
        if vari_idx < 0:
            self.clear(count=count)
            return

        if all_children and self.__children:
            for child in self.__children.values():
                child.set(vari_idx, all_children=True)

        if self.parent and self.content != self.__template:
            # If content has been changed from the template, then clone the parent block if
            # its cloning flag is set to true to ensure that the subblock tags can be
            # found in the parent block content and the subblock content can be set into them.
            self.parent.clone(passive=True)
        if self.autotags:
            # Finalize the block content by setting the value of special tags.
            self.__set_autotag_vari(last=True)
            self.__autovari_first = True
            self.__set_autotag_align()
        set_num = 0
        while self.parent and (set_num < count or count < 0):
            # pylint: disable=protected-access
            # rationale: Private method __get_block_pos is called from non-self object only here and
            # it is easier and simpler to keep it that way instead of rewriting the method to be static and sending
            # parent object data into it for processing.
            (subblk_start, subblk_end) = self.parent._Block__get_block_pos(self.name, True)     # type: ignore
            if 0 <= subblk_start < subblk_end:
                blk_content = self.__get_variation(self.content, self.name, vari_idx)
                # If subblock tags are found, then set the current block content into all corresponding subblock tags
                # in the parent block content.
                self.parent.content = \
                    f"{self.parent.content[: subblk_start]}{blk_content}{self.parent.content[subblk_end:]}"
                # Increment number of blocks being set into the parent block.
                set_num += 1
            else:
                break

    def set_subblock(self, *subblocks: "Block | str") -> None:
        """Sets the content of specified child blocks into the content of the current block.

        Args:
            subblocks: The subblock object(s) or their names to be set.
        """
        for subblk in subblocks:
            if isinstance(subblk, str):
                blk_sub = self.children.get(subblk, self.get_subblock(subblk))
                if isinstance(blk_sub, Block):
                    blk_sub.set()
            else:
                subblk.set()

    def clone(self, copies: int = 1, force: bool = False, passive: bool = False, set_children: bool = False) -> None:
        """Clones the block, i.e., virtually adds another copy of a block template after the
        existing block content making the new template copy ready to be filled with other values.

        The clone is created only if blocks and variables are set after cloning. The child blocks
        are reset after cloning, unless the ``passive`` argument is set to ``True``.

        Args:
            copies: The number of template copies to be prepared. If > 1, then ``force`` and
                ``passive`` arguments are automatically ``False``.
            force: Forces the clone to be created even if no variable or block is then set.
            passive: Enables cloning only if an active (non-passive) clone has been requested
                previously and no further clone is created.
            set_children: Enables setting of all child blocks to this parent block before cloning.
        """
        if set_children:
            for child in self.__children.values():
                child.set()

        if copies > 1:
            for _ in range(copies):
                self.clone(1, False, False, False)
        else:
            # Check if cloning flag indicates that the cloning should be actually performed.
            if force or self.__clone_flag:
                if self.autotags:
                    self.__set_autotag_vari(first=self.__autovari_first)
                    self.__autovari_first = False
                    self.__set_autotag_align()
                # Perform cloning.
                self.content = f"{self.content}{self.__template}"
                self.__clone_flag = False
            if not passive:
                if not force:
                    self.__clone_flag = True
                # Reset all child blocks to make their content ready to be filled with new values.
                for child in self.__children.values():
                    child.reset(all_children=True)

    def clear_variables(self, *var_names: str) -> None:
        """Clears the specified variables from this block content. Has the same effect as setting
        the variables to an empty string.

        Args:
            var_names: Names of the variables to be cleared.
        """
        for var_name in var_names:
            self.content = self.content.replace(self.config.tag_gen_var(var_name), "")

    def clear(self, count: int = -1) -> None:
        """Clears the block from its parent block, i.e., sets the block to an empty string.

        Args:
            count: The maximum number of blocks with the same name to be cleared, -1 = all.
        """
        self.content = ""
        self.set(count=count)

    def clear_subblock(self, *subblocks: "Block | str") -> None:
        """Clears the content of specified child blocks from a current block content.

        Args:
            subblocks: Subblock object(s) or their names to be cleared.
        """
        for subblk in subblocks:
            if isinstance(subblk, str):
                blk_sub = self.children.get(subblk, self.get_subblock(subblk))
                if blk_sub:
                    blk_sub.clear()
            else:
                subblk.clear()

    def reset(self, all_children: bool = True) -> None:
        """Resets the block content to the initial template.

        Args:
            all_children: Enables a reset of all child blocks too.
        """
        self.content = self.__template
        self.__clone_flag = False
        if all_children:
            for blk_obj in self.__children.values():
                blk_obj.reset()

    def __get_block_pos(self, block_name: str, include_tags: bool = False) -> tuple[int, int]:
        """Returns the position of the specified block within the content of this block.

        Args:
            block_name: The name of the block whose position should be returned.
            include_tags: Enables the inclusion of the block tags themselves in the returned
                position.

        Returns:
            A tuple with the start and end character position of the block.
        """
        start_tag = self.config.tag_gen_blk_start(block_name)
        end_tag = self.config.tag_gen_blk_end(block_name)
        subblk_start = self.content.find(start_tag)
        if subblk_start >= 0:
            if not include_tags:
                subblk_start += len(start_tag)
                # Return "\n" char pos + 1 if "\n" is found, else return -1 + 1 = 0
                next_nl = self.content.find("\n", subblk_start) + 1
                if next_nl > 0 and not self.content[subblk_start: next_nl].strip():
                    subblk_start = next_nl
            else:
                prev_nl = self.content.rfind("\n", 0, subblk_start) + 1
                next_nl = self.content.find("\n", subblk_start)
                if next_nl > 0 and self.content[prev_nl: next_nl].strip() == start_tag:
                    subblk_start = prev_nl

        subblk_end = self.content.find(end_tag)
        if subblk_start >= 0 and subblk_end >= 0:
            if not include_tags:
                last_nl = self.content.rfind("\n", subblk_start, subblk_end) + 1
                if last_nl > 0 and not self.content[last_nl: subblk_end].strip():
                    subblk_end = last_nl
            else:
                prev_nl = self.content.rfind("\n", 0, subblk_end)
                subblk_end += len(end_tag)
                next_nl = self.content.find("\n", subblk_end) + 1
                if next_nl > 0 and self.content[prev_nl: next_nl].strip() == end_tag:
                    subblk_end = next_nl

        return (subblk_start, subblk_end)

    def __set_autotag_align(self) -> None:
        """Sets the value of the *alignment* automatic tags in this block maintaining the
        predefined right-alignment to the next character different from the repeated one.
        """
        last_pos = 0
        # Loop through all "alignment" tags in block template and replace them with the correct
        # number of repeated characters.
        while True:
            (cont_start, cont_end, new_col, repeat_char) = self.__get_autotag_align_att(self.content)
            if cont_start >= 0:
                (templ_start, templ_end, orig_col, _) = self.__get_autotag_align_att(self.__template, True, last_pos)
                orig_len = templ_end - templ_start
                # Calculate the new length of the repeated characters in the filled content, unless
                # the repeated character is a whitespace ending with newline, then just use newline.
                if self.content[cont_end] == "\n" and repeat_char.isspace():
                    new_len = 0
                else:
                    new_len = orig_len + (orig_col - new_col)
                    if repeat_char == "\t":
                        temp_len = new_len
                        new_len //= self.config.tab_size
                        if new_len * self.config.tab_size < temp_len:
                            new_len += 1
                    if new_len <= 0:
                        new_len = 1
                # Set the repeated characters into the block content instead of the "alignment" tag.
                self.content = f"{self.content[0: cont_start]}{new_len * repeat_char}{self.content[cont_end:]}"
                # Remember the last "alignment" tag position in the template, because if there are more of these
                # tags, then we need to start searching only after the previous tag position, not from the start.
                last_pos = templ_end
            else:
                break

    def __get_autotag_align_att(
            self, text: str, expand_tabs: bool = False, start_pos: int = 0) -> tuple[int, int, int, str]:
        """Returns the attributes of the first found *alignment* automatic tag.

        Args:
            text: A string in which the *alignment* automatic tag is searched.
            expand_tabs: Enables the replacement of tabulators with spaces for consistent
                character position counting.
            start_pos: The start character position for searching the *alignment* automatic tag.

        Returns:
            A tuple with the following information about the *alignment* automatic tag:
            start char position, end char position, line column index, character to be repeated.
        """
        if expand_tabs:
            text = text.expandtabs(self.config.tab_size)
        end_pos = -1
        tag_col_pos = -1
        repeat_char = ""
        charrep_tag = self.config.tag_gen_var(self.config.autotag_align)
        # Get starting position of repeated characters.
        st_pos = text.find(charrep_tag, start_pos)
        if st_pos >= 0:
            end_pos = st_pos + len(charrep_tag)
            # Get the repeated character immediately following the "alignment" tag.
            repeat_char = text[end_pos]
            while text[end_pos] == repeat_char:
                end_pos += 1
            # Get position of the last newline char before the "alignment" tag.
            line_st_pos = text.rfind("\n", 0, st_pos)
            line_st_pos = 0 if line_st_pos < 0 or line_st_pos > st_pos else line_st_pos + 1
            # Get the line column position of the "alignment" tag.
            tag_col_pos = len(text[line_st_pos: st_pos].expandtabs(self.config.tab_size))
        return (st_pos, end_pos, tag_col_pos, repeat_char)

    def __set_autotag_vari(self, first: bool = False, last: bool = False) -> None:
        """Sets the correct content variation of the *variation* automatic tags in this block
        content. The *variation* automatic tag can have two or three content variations:
        *standard / last / first*, while the last *first* variation is optional. The *first*
        (optional) variation is automatically set in the first clone of this block, the *standard*
        variation is set in all subsequent clones, except for the last one, where the *last*
        variation is set.

        Args:
            first: Enables setting of the *first* value variation of the *variation* automatic tag.
            last: Enables setting of the *last* value variation of the *variation* automatic tag.
        """
        # Loop through all *variation* autotags in a block content and replace them with either
        # the "standard", "last" or "first" value.
        while True:
            (subblk_start, subblk_end) = self.__get_block_pos(self.config.autotag_vari, True)
            if 0 <= subblk_start < subblk_end:
                (subblk_cont_start, subblk_cont_end) = self.__get_block_pos(self.config.autotag_vari)
                value_content = self.content[subblk_cont_start: subblk_cont_end]
                value_content = self.__get_variation(
                    value_content, self.config.autotag_vari, 1 if last else 2 if first else 0)
                self.content = f"{self.content[: subblk_start]}{value_content}{self.content[subblk_end:]}"
            else:
                break

    def __get_variation(self, text: str, block_name: str, vari_idx: int) -> str:
        """Finds the specified variation block and returns the content variation with the specified
        index from it.

        Args:
            text: A string where the variation block is searched.
            block_name: The variation block name being searched.
            vari_idx: The content variation index (starting from 0) to be returned. Variation 0
                is returned if the specified index is higher than the number of defined variations.

        Returns:
            A string representing the content variation corresponding to the specified variation
            index. The whole ``text`` argument is returned if the variation block is not found.
        """
        content_vari = text
        if self.config.tag_gen_blk_vari(block_name) in text:
            var_list = text.split(self.config.tag_gen_blk_vari(block_name))
            content_vari = var_list[vari_idx] if vari_idx < len(var_list) else var_list[0]
            # Remove the initial empty space up to the first newline char "\n", including the "\n" if present.
            first_nl = content_vari.find("\n") + 1
            if first_nl > 0 and content_vari[: first_nl].strip() == "":
                content_vari = content_vari[first_nl:]
            # Remove trailing empty space after the final newline char "\n", not including the final "\n" if present).
            last_nl = content_vari.rfind("\n") + 1
            if last_nl > 0 and content_vari[last_nl:].strip() == "":
                content_vari = content_vari[0: last_nl]
        return content_vari
