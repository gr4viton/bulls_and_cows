#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project:    Bulls and Cows CLI game
Assignment: https://github.com/engetoacademy/pythontask
Author:     gr4viton @ gr4viton.cz
Originated: 27-02-2017
License:    GPLv3 @ http://www.gnu.org/licenses/gpl-3.0.html

Disclaimer: I apologize for the "long" code. It's mainly because of the implemented internationalization.
            I could have make it much more simple without it, but it was fun to write it.
            Surely it may be more effective to localize it more standardly with _('text-to-translate')
              and pygettext and .pot files.
            Also the game algorithm gives 1 bull and 3 cows if the target is 1234 and user guesses 1111, because I am
              sure we played it like this. However, I do understand other options are possible (1 bull and 0 cows).
"""

import os
import random
import sys

print('You are using Python version: ', sys.version_info)
if sys.version_info[0] < 3:
    print("This script is written for Python 3+ interpreter."
          "It is possible it won't run correctly on your Python version. I am sorry!" )
    raise DeprecationWarning('Programmed for Python 3+')

#TODO:
# ] check COMMENTS functions!!
# ] check PIP8
# ] user input correction
# ] check raising errors ..
# ] check names
# ] uninitialized and unused variables
# ] player chooses the number
# ] on guess == q


# It is against PEP8 to define class before the other items,
# but since using only one py file, I do not have any other choice
class DictLanguage(dict):
    """Overridden dictionary class for not defined text keys handling
    """
    def __init__(self, dict):
        self._dict = dict

    def keys(self):
        return self._dict.keys()

    def __getitem__(self, key):
        """On key absence, take value from default language dictionary,
         if not there either, raise Error
        """
        if key in self._dict.keys():
            return self._dict[key]
        else:
            if key in default_language_texts.keys():
                return default_language_texts[key]
            else:
                raise KeyError('Language texts dictionary key [' + str(key) + \
                      '] is not in selected language dictionary nor in the default one!')

##########################################
# Following texts dictionary should be in separate file, for easier game internationalization
##########################################
# Please make language_texts_dicitonary keys in snake_case and start it with one of the following prefixes:
# 't_' = normal text
# 'p_' = prompt for user input
# 'q_' = question
# 'a_' = answer from the program - response to user input
# When making formating strings
#  - let the first word after prefix in key be 'format'
# When making multiple choice string
#  - key
#   -- let the first word after prefix in be 'choice'
#  - value
#   -- let the first character be the delimiter
#   -- let the formating string be the first words after the first char
#   -- let each choice string be delimited with the chosen delimitor
##########################################
eng_texts_dict = {
't_language_name': 'English language',
'q_language_selection': 'Please select language',
'a_language_selected': 'You have selected English language.',
'q_theme':
"""Question: Which bulls and cows game theme would you like to play?
    0) Assignment identical 4 digits
    1) Chatty memefull 4 lowercase letters""",
'q_theme#': 2,
'q_graphics':\
"""Question: Which means of communication is the most visually pleasing to you?
    0) Textual only
    ×) Ascii art char graphics (not yet implemented)
    ×) Braille sub-char graphics via asciimoo's drawille (not yet implemented)""",
'q_graphics#': 1,
'p_prompt_digit': 'Please insert one digit and confirm by Enter:',
't_bac_initialized': """%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%% Bulls and Cows game initialized. %%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%""",
't_format_bac_start:1': """%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
How high are you?
Roses are red, violets are blue. I generated exactly {} lowercase letters for you.
I don't always want to play Bulls and cows game. But when I do, I play it like a boss. Deal With It! B-)""",
't_format_bac_start:0': """

Hi there!
I've generated a random {} digit number for you.
Let's play a bulls and cows game.""",
'p_format_bac_prompt_guess:0': 'Enter a {} digit number',
'p_format_bac_prompt_guess:1': 'Enter a {} lowercase letters',
't_format_bac_nums': '{} bulls, {} cows, attempt:{}/{}',
'e_format_use_exactly:0': 'You must input exactly {} digits!',
'e_format_use_exactly:1': 'You must use exactly {} lowercase letters!',
'a_users_guess': 'You have guessed:',
'a_users_input' : 'You have entered:',
'a_format_solved_attempts:0': """

Correct, you've guessed the right number in {} guesses!""",
'a_format_solved_attempts:1': """%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
You, sir, are the real MVP! Only {} guesses!""",
'a_choice_solved_great:0': """|That's {}!|amazing""",
'a_choice_solved_great:1':
"""|That's {}!|amazing|brilliant! Like a boss|beautiful|kind of you|perfect|astonishing|stunning|startling|fantastic|terrific|cool story, bro|impossibruuuu""", # noqa
'a_choice_solved_normal:0': """|That is {}.|average""",
'a_choice_solved_normal:1': """|That is {}.|average|normal skill|mediocre|swag""",
'a_choice_solved_bad:0': """|That's {}!!|not so good""",
'a_choice_solved_bad:1':
"""|That's {}!!|bad luck, Brian|literally bad|odd|sad|mad|unpleasant|saying something about your skills|Seriously?|terrible! Stahp!!""", # noqa
'a_format_max_attempts_reached:0': 'You have reached the maximum of {} guesses. Better luck next time!', # noqa
'a_format_max_attempts_reached:1': "Tell me more about how you cannot get the right answer in total {} guesses. I don't want to play with you anymore! lol.", # noqa
'q_ask_for_another_game:0' : """Do you want to play another game? I will add one character for you to guess.
Enter:
0 = end program
1 = play another game""", # noqa
    'q_ask_for_another_game:1' : """Yo Dawg, I heard you like Bulls and Cows, so I put another character in the characters to guess for you to guess!
So now you can guess which character to guess, when you guess the characters. You still wanna play another game??
Enter:
0 = exit this trash, YOLO
1 = Triggered for another of you'rES EPIC fails""", # noqa
'a_choice_unsolved:0': '|You have failed. The game will now end! {}|Pleasure playing with you.|It was a good game.',
'a_choice_unsolved:1': '|U MAD BRO?! This is GAME OVER 4 U! {}|Do you even lift?|Wubba lubba dub dub!|Facepalm.|...lol|...rofl|kek|Rickroll!|O RLY?', # noqa
'a_program_end': 'Have a great day!',
'a_program_end:1': "C U l8r. Sorry for long game. Here's a ascii potato: O"
                  }

all_texts = [eng_texts_dict]
default_language_texts = eng_texts_dict
texts = DictLanguage({})

THEME_ASSIGNMENT_IDENTICAL = 0
THEME_CHATTY = 1

# if you want to have the same target sequence every time (0000 and ab)
DEBUGGING = True


def prompt_language_selection(select=None):
    """Asks user for language selection,
    assigns selected language texts dicst to global dictionary texts
    returns lang_num from all_texts list
    """
    global texts

    if select is not None:
        lang_num = select
        texts = DictLanguage(all_texts[lang_num])
        return select

    lang_count = len(all_texts)
    print(sep='/', *[lang['q_language_selection'] for lang in all_texts])
    [print(number, ':', lang['t_language_name']) for number, lang in enumerate(all_texts)]

    lang_num = prompt_number(None, lang_count, 'a_language_selected')

    texts = DictLanguage(all_texts[lang_num])
    return lang_num


def prompt_number(q_text_key, incremented_max_digit, a_text_valid_key=None):
    """Prompts the user for integer with inserted q_text_key text
    If not in desired range, the user is prompted again repeatedly
    returns user-inserted value
    """
    if q_text_key is not None:
        print(texts[q_text_key])

    def print_range():
        print('0 <= #', incremented_max_digit, sep=' < ')
    valid_input = False
    value = None
    while not valid_input:
        value = input('# = ')
        if value.isdigit():
            value = int(value)
            if 0 <= value < incremented_max_digit:
                if a_text_valid_key is not None:
                    print(texts[a_text_valid_key])
                valid_input = True
            else:
                print_range()
        else:
            print_range()
    return value


def cls():
    """Clears the console screen.
    Might not be functional in all types of terminal.
    Functional, tested: Windows 7 commandline
    Does not work in: Pycharm console
    """
    os.system('cls' if os.name=='nt' else 'clear')


class BACgame:
    """ Main class for Bulls and Cows game
    Handles user input and game mechanics
    """
    def __init__(self, theme_num, graphics_num):
        """
        theme_num = Textual in-game communication may differ if user selected different themes
        graphics_num = Graphical in-game communication may differ if user selected different graphics
        """
        self.theme = theme_num
        self.graphics = graphics_num
        self.theme_str = str(theme_num)
        self.theme_suffix = ':' + self.theme_str
        self.graphics_str = str(graphics_num)


        self.char_range = [chr(i) for i in range(ord('a'), ord('z')+1)]

        self.attempt = 0
        themed_rules = {THEME_ASSIGNMENT_IDENTICAL: (4, 10, 3, 6),
                        THEME_CHATTY: (2, 42, 15, 25)
                        }
        self.guess_char_count, self.max_attempts , self.attempts_great, self.attempts_normal = \
            themed_rules[theme_num]

        print(texts['t_bac_initialized'])

    def themed(self, texts_key_base):
        """Returns themed key from texts dictionary= text_key_base + theme_sufix
        """
        return texts_key_base + self.theme_suffix

    def themed_text(self, texts_key_base):
        """Returns the themed version of key text from global texts dictionary (theme suffix)
         or default one if themed does not exist
        """
        key = self.themed(texts_key_base)
        if key not in texts.keys():
            key = texts_key_base
        return texts[key]

    def print(self, *args, sep=' '):
        """Prints text global texts dictionary according to given key
        Prints the themed version of key text from texts dictionary (theme suffix)
         or default one if themed does not exist
        """
        args = list(args)
        texts_key_base = args.pop(0)
        print(self.themed_text(texts_key_base), *args, sep=sep)

    def print_choice(self, texts_key_base):
        """Prints text global texts dictionary according to given key
        Chooses randomly one of the choices strings into the formating string
        and then prints the formating string formated by the chosen choice string
        """
        whole_choice_str = self.themed_text(texts_key_base)
        delimiter = whole_choice_str[0]
        _, format_str, *choice_strs = whole_choice_str.split(delimiter)

        if type(choice_strs) == list:
            choice_str = choice_strs[random.randint(0, len(choice_strs)-1)]
        else:
            choice_str = choice_strs

        print(format_str.format(choice_str))

    def print_formated(self, text_key_base, *format_list):
        """Prints formated text global texts dictionary according to given key
        """
        print(self.themed_text(text_key_base).format(*format_list))

    @staticmethod
    def _get_input():
        return input('>>> ')

    def prompt_guess_str(self):
        """Prompts the user for guess input
        If he refuses to
        """
        valid_input = False
        guess = def_guess = '-'
        while not valid_input:
            if self.theme == THEME_ASSIGNMENT_IDENTICAL:
                valid_input = str.isdigit(guess) and len(guess) == self.guess_char_count
            elif self.theme == THEME_CHATTY:
                valid_input = str.islower(guess) and len(guess) == self.guess_char_count

            if not valid_input:
                if guess != def_guess:
                    self.print_formated('e_format_use_exactly', self.guess_char_count)
                guess = self._get_input()
        self.attempt += 1
        return guess

    def ask_for_another(self):
        """Asks user for another game
        returns False on 'y'
        returns True on 'n'
        """
        self.print('q_ask_for_another_game')
        self.guess_char_count += 1
        return prompt_number(None, 2)

    def generate_target(self):
        """Generates the target sequence for the user to guess
        """
        if theme_num == THEME_ASSIGNMENT_IDENTICAL:
            target_num = random.randint(0, 10 ^ self.guess_char_count-1)
            if DEBUGGING:
                target_num = '0' * self.guess_char_count
            target_str = str(target_num).zfill(self.guess_char_count)
        elif theme_num == THEME_CHATTY:
            target_str = [random.choice(self.char_range) for i in range(self.guess_char_count)]
            if DEBUGGING:
                target_str = 'ab'+'b'*(self.guess_char_count-2)

        self.target = [ord(num) for num in list(target_str)]

    def let_user_guess(self):
        """Loop for user to guess the target sequence
        after every guess the number of bulls and cows is displayed
        number of attempts is stored in self.attempts
        if the max_attempts is reached the loop is terminated
        self.solved carries the information about the guessing successfulness
        """
        self.solved = False
        while not self.solved:
            self.print_formated('p_format_bac_prompt_guess', self.guess_char_count)
            guess_str = self.prompt_guess_str()
            guess = [ord(num) for num in list(guess_str)]

            # the main algorithm for bulls and cows game

            bulls_list = [int(guess_num == target_num)
                          for guess_num, target_num in zip(guess, self.target) ]
            cows_list = [1 for guess_num, bull in zip(guess, bulls_list)
                         if guess_num in self.target and bull == 0]

            if DEBUGGING:
                print('target_ascii', self.target, 'guess_ascii', guess)
            self.print_formated('t_format_bac_nums', sum(bulls_list), sum(cows_list), self.attempt, self.max_attempts)
            self.solved = sum(bulls_list) == self.guess_char_count

            if self.attempt >= self.max_attempts and not self.solved:
                self.print_formated('a_format_max_attempts_reached', self.max_attempts)
                break

    def print_end_game_str(self):
        """Prints end game texts dependent on solved and attempts variables
        """
        if self.solved:
            self.print_formated('a_format_solved_attempts', self.attempt)
            if self.attempt < self.attempts_great:
                self.print_choice('a_choice_solved_great')
            elif self.attempt < self.attempts_normal:
                self.print_choice('a_choice_solved_normal')
            else:
                self.print_choice('a_choice_solved_bad')
            return True
        else:
            self.print_choice('a_choice_unsolved')
            return False

    def start_one_game(self):
        """Starts one game of Bulls and cows
        returns True after succesfull guess in less then max_attempts attempts otherwise returns False
        """
        cls()
        self.print_formated('t_format_bac_start', self.guess_char_count)

        self.generate_target()
        self.let_user_guess()
        self.print_end_game_str()
        return self.solved

    def start_game_loop(self):
        """Starts a loop of individual games
        If the game is successfully concluded user prompted if s/he wants to play another game
        """
        another_game = True
        while another_game:
            successfull = self.start_one_game()
            if successfull:
                another_game = self.ask_for_another()
            else:
                another_game = False
        self.print('a_program_end')


if __name__ == '__main__':
    if not DEBUGGING:
        prompt_language_selection()
        theme_num = prompt_number('q_theme', texts['q_theme#'])
        graphics_num = prompt_number('q_graphics', texts['q_graphics#'])
    else:
        prompt_language_selection(0)
        theme_num = graphics_num = 1

    bac = BACgame(theme_num, graphics_num)
    bac.start_game_loop()