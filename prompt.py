#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2025-03-15 19:35:34 krylon>
#
# /data/code/python/rpg/prompt.py
# created on 15. 03. 2025
# (c) 2025 Benjamin Walkenhorst
#
# This file is part of rpg. It is distributed
# under the terms of the GNU General Public License 3. See the file
# LICENSE for details or find a copy online at
# https://www.gnu.org/licenses/gpl-3.0

"""
rpg.prompt

(c) 2025 Benjamin Walkenhorst
"""

import re
from re import Pattern
from typing import Final, Union

from prompt_toolkit import print_formatted_text as printf
from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import radiolist_dialog
from prompt_toolkit.validation import ValidationError, Validator


class MultipleChoiceDialog:
    """MultipleChoiceDialog is something we ask the player, along with a list of possible answers.

    It is also possible to mark one answer as the default. (or is it?)
    """

    __slots__ = [
        "question",
        "answers",
        "default",
    ]

    question: Final[str]
    answers: Final[list[str]]
    default: int

    def __init__(self, question: str, *answers: str, **kwargs) -> None:
        self.question = question
        self.answers = list(answers)
        if "default" in kwargs:
            if isinstance(kwargs["default"], int):
                if 0 <= kwargs["default"] < len(answers):
                    self.default = kwargs["default"]
                else:
                    raise IndexError("default answer must be a valid index into the list of answers")
            else:
                raise TypeError("default choice must an int")
        else:
            self.default = -1

    def ask(self) -> str:
        """Ask the user the question."""
        dlg = radiolist_dialog(
            title="Question",
            text=self.question,
            values=[(i, self.answers[i]) for i in range(len(self.answers))],
        )

        response = dlg.run()

        return self.answers[response]


class ChoiceValidator(Validator):
    """ChoiceValidator checks if an answer is from a list of choices (numbers)."""

    num_choices: Final[int]

    def __init__(self, num_choices) -> None:
        super().__init__()
        self.num_choices = num_choices

    def validate(self, document) -> None:
        """Attempt to validate the text."""
        txt = document.text.strip()

        if not txt:
            raise ValidationError(message="Empty input")

        if not txt.isdigit():
            _i = 0
            for _i, c in enumerate(txt):
                if not c.isdigit():
                    break
            raise ValidationError(
                message="Non-numerical character(s)",
                cursor_position=_i,
            )

        try:
            num: int = int(txt)

            if not 1 <= num <= self.num_choices:
                raise ValidationError(message=f"Input must be a number between 1 and {self.num_choices}")
        except ValueError as verr:
            # CANTHAPPEN
            raise ValidationError(message="Cannot parse input to number") from verr


predicate_pattern: Final[Pattern] = re.compile("^(y(?:es)?|no?)", re.I)


class YesOrNoValidator(Validator):
    """Validator to check if the player is responding to a yes-or-no-question correctly."""

    def validate(self, document) -> None:
        """Attempt to validate the player's input."""
        txt = document.text.strip().lower()
        if not predicate_pattern.match(txt):
            raise ValidationError(message="Yeah, no.")


class Question:
    """Question is a question with multiple allowed answers."""

    __slots__ = [
        "question",
        "answers",
        "default",
    ]

    question: Final[Union[str, HTML]]
    answers: Final[list[Union[str, HTML]]]
    default: int

    def __init__(self, question: Union[str, HTML], *answers: str, **kwargs) -> None:
        self.question = question
        self.answers = list(answers)
        if "default" in kwargs:
            if isinstance(kwargs["default"], int):
                if 0 <= kwargs["default"] < len(answers):
                    self.default = kwargs["default"]
                else:
                    raise IndexError("default answer must be a valid index into the list of answers")
            else:
                raise TypeError("default choice must an int")
        else:
            self.default = -1

    def ask(self) -> str:
        """Ask the question."""
        # printf(self.question)
        for i, a in enumerate(self.answers):
            printf(f"{i+1:2d} {a}")
        idx = int(prompt(self.question, validator=ChoiceValidator(len(self.answers))))

        match self.answers[idx-1]:
            case str(res):
                return res
            case res if isinstance(res, HTML):
                return res.value
            case _:
                raise TypeError(f"Expected a str or HTML object, not {self.answers[idx].__class__}")


# I think this could be done more elegantly and efficiently, but it should work.
def yes_or_no(question: str) -> bool:
    """Ask the player a simple yes-or-no-question"""
    res = prompt(question, validator=YesOrNoValidator())
    return res.lower()[0] == 'y'


# Local Variables: #
# python-indent: 4 #
# End: #
