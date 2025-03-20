#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2025-03-20 19:41:25 krylon>
#
# /data/code/python/rpg/dialog.py
# created on 15. 03. 2025
# (c) 2025 Benjamin Walkenhorst
#
# This file is part of rpg. It is distributed
# under the terms of the GNU General Public License 3. See the file
# LICENSE for details or find a copy online at
# https://www.gnu.org/licenses/gpl-3.0

"""
rpg.dialog

(c) 2025 Benjamin Walkenhorst

In this file, we attempt to model dialogue between the player and various beings they encounter.
"""

import re
from collections.abc import Sequence
from dataclasses import dataclass, field
from re import Pattern
from typing import Final, Union

from prompt_toolkit import print_formatted_text as printf
from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import radiolist_dialog
from prompt_toolkit.validation import ValidationError, Validator

from rpg.data import Flag


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


# I think this could be done more elegantly and efficiently, but it should work.
def yes_or_no(question: str) -> bool:
    """Ask the player a simple yes-or-no-question"""
    res = prompt(question, validator=YesOrNoValidator())
    return res.lower()[0] == 'y'


@dataclass(slots=True)
class Question:
    """A question we ask the user."""

    question: Union[str, HTML]
    choices: list[str]
    validator: ChoiceValidator

    def __init__(self, question: Union[str, HTML], *choices: str) -> None:
        self.question = question
        self.choices = list(choices)
        self.validator = ChoiceValidator(len(choices))

    def ask(self) -> Union[str, HTML]:
        """As the user the question."""
        for i, a in enumerate(self.choices):
            printf(f"{i+1:2d} {a}")

        idx: int = int(prompt(self.question, validator=self.validator))
        return self.choices[idx-1]


def ask_multiple_choice(question: str, *choices: str) -> str:
    """Ask the user a multiple choice question."""
    q: Question = Question(question, *choices)
    reply = q.ask()
    match reply:
        case str(x):
            return x
        case _ if isinstance(reply, HTML):
            return str(reply)
        case _:
            raise ValueError(f"(Invalid reply: {reply}")


@dataclass(slots=True)
class Choice:
    """Choice is one possible choice the player can make in a dialogue"""

    key: int
    leads_to: int
    text: Union[str, HTML]
    taken: bool
    ends_dialog: bool
    conditions: set[int] = field(default_factory=set)
    consequences: set[int] = field(default_factory=set)

    def __init__(self, k: int, n: int, t: str, cond: set[int], cons: set[int], **kwargs) -> None:  # pylint: disable-msg=R0917
        self.key = k
        self.leads_to = n
        self.text = t
        self.conditions = cond
        self.consequences = cons
        self.taken = False
        if "ends_dialog" in kwargs:
            self.ends_dialog = bool(kwargs["ends_dialog"])
        else:
            self.ends_dialog = False

    def is_available(self, state: dict[int, Flag]) -> bool:
        """Return true, if the Choice is available under the given state of the World."""
        if self.taken:
            return False

        for c in self.conditions:
            if c not in state:
                return False
        return True


@dataclass(slots=True)
class Panel:
    """Panel is one node in the dialogue tree"""

    key: int
    speech: Union[str, HTML]
    choices: list[Choice]

    def __init__(self, k: int, s: Union[str, HTML], *responses: Choice) -> None:
        self.key = k
        self.speech = s
        self.choices = list(responses)

    def ask(self, state: dict[int, Flag]) -> Choice:
        """Ask the question."""
        available = [c for c in self.choices if c.is_available(state)]

        if len(available) == 0:
            raise RuntimeError("No Choices are available.")

        for i, a in enumerate(available):
            printf(f"{i+1:2d} {a.text}")

        idx = int(prompt(self.speech, validator=ChoiceValidator(len(available))))
        taken = available[idx]
        taken.taken = True
        return taken


@dataclass(slots=True, kw_only=True)
class DialogTree:
    """DialogTree is a set of Panels, plus a starting Panel."""

    panels: dict[int, Panel]
    begin: int
    preconditions: Sequence[int]
    finished: bool = False

    def __getitem__(self, key: int) -> Panel:
        return self.panels[key]


# Local Variables: #
# python-indent: 4 #
# End: #
