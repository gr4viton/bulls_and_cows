import os
import random
# if import

#TODO:
# ] check COMMENTS!!
# ] check PIP8
# ] check raising errors ..
# ] check names
# ] uninitialized and unused variables
# ] player chooses the number
# ] calculator?

# it is against PEP8 to define class before the other items,
# but since using only one py file, I do not have any other choice
class DictLanguage(dict):
    """Overridden dictionary class for not defined text keys handling"""
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

## Please make language_texts_dicitonary keys in snake_case and start it with one of the following prefixes:
# 't_' = normal text
# 'p_' = prompt for user input
# 'q_' = question
# 'a_' = answer from the program - response to user input

eng_texts_dict = {
't_language_name': 'English language',
'q_language_selection': 'Please select language',
'a_language_selected': 'You have selected English language.',
'q_theme':
"""Question: Which bulls and cows game theme would you like to play?
    0) Assignment identical
    1) Minimalist
    2) Chatty
    3) Graphical""",
'q_theme#': 3,
'q_graphics':\
"""Question: Which means of communication is the most visually pleasing to you?
    0) Textual only
    1) Ascii art char graphics
    2) Braille sub-char graphics
    3) pygame opengl
    4) Blender script""",
'q_graphics#': 5,
'p_prompt_digit': 'Please insert one digit and confirm by Enter:',
't_bac_initialized': """%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%% Bulls and Cows game initialized. %%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%""",
't_bac_start:0': """Hi there!
I've generated a random 4 digit number for you.
Let's play a bulls and cows game.""",
'p_bac_prompt_number:0': 'Enter a number',
't_bac_format_bac_nums': '{} bulls, {} cows',
'e_use_only:0': 'You must input only 4 digits!',
'e_use_only': 'You must use only allowed characters!',
'a_users_guess': 'You have guessed:',
'a_users_input' : 'You have entered:',
                  }

all_texts = [eng_texts_dict]
default_language_texts = eng_texts_dict
texts = DictLanguage({})


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
    """Clears the console screen"""
    os.system('cls' if os.name=='nt' else 'clear')



class BACgame():
    """
    as
    """
    def __init__(self, theme_num, graphics_num):
        """
        """
        self.theme = theme_num
        self.graphics = graphics_num
        self.theme_str = str(theme_num)
        self.theme_suffix = ':' + self.theme_str
        self.graphics_str = str(graphics_num)

        self.guess_char_count = 4
        self.range_of_chars = ['0', '9']

        print(texts['t_bac_initialized'])

    def themed(self, texts_key_base):
        """Returns themed key from texts dictionary= text_key_base + theme_sufix"""
        return texts_key_base + self.theme_suffix

    def themed_text(self, texts_key_base):
        """Returns key text from texts dictionary
        Returns the themed version of key text from texts dictionary (theme suffix)
         or default one if themed does not exist
        """
        key = self.themed(texts_key_base)
        if key not in texts.keys():
            key = texts_key_base
        return texts[key]

    def print(self, *args, sep=' '):
        """Prints key text from texts dictionary
        Prints the themed version of key text from texts dictionary (theme suffix)
         or default one if themed does not exist
        """
        args = list(args)
        texts_key_base = args.pop(0)
        print(self.themed_text(texts_key_base), *args, sep=sep)

    def get_input(self):
        """
        """
        #return input('>>>')[0:-1]
        return input('>>> ')

    def prompt_number_str(self):
        """

        """
        # only get the right chars
        # only selected number of chars - others cannot be inputed
        valid_input = False
        guess = def_guess = '-'
        while not valid_input:
            valid_input = str.isdigit(guess) and len(guess) == self.guess_char_count
            if not valid_input:
                if guess != def_guess:
                    self.print('e_use_only')
                guess = self.get_input()
            else:
                ##self.print('a_users_input', guess, '', sep='"')
                pass

        return guess

    def start_one_game(self):
        """
        """
        cls()
        self.print('t_bac_start')

        self.target_num = random.randint(0,9999)
        self.target_num = 2011
        target_str = str(self.target_num).zfill(4)

        target = [int(num) for num in list(target_str)]
        #random.choice(self.char_range(self.range_of_chars))
        print(target, self.target_num)

        cows = bulls = 0
        while not( bulls == 4 and cows == 4):
            self.print('p_bac_prompt_number')
            guess_str = self.prompt_number_str()

            guess = [int(num) for num in list(guess_str)]

            # the main algorithm for bulls and cows game
            zip_guess_target = zip(guess, target)
            bulls = [int(guess_num == target_num) for guess_num, target_num in zip_guess_target ]
            print(bulls)
            #[print(guess_num, target_num) for guess_num, target_num in zip_guess_target]
            print('hey')
            #[print(type(guess_num), type(target_num)) for guess_num, target_num in zip_guess_target]
            print('sdas')
            #bulls = sum([1 for guess_num, target_num in zip_guess_target if guess_num == target_num])
            #bulls = sum([guess_num == target_num for guess_num, target_num in zip_guess_target ])

            cows = [1 for guess_num, bull in zip(guess, bulls) if guess_num in target and bull == 0]

            print(target, guess)
            print(self.themed_text('t_bac_format_bac_nums').format(sum(bulls), sum(cows)))

        print('you are right!')




if __name__ == '__main__':
    prompt_language_selection(0)
#    theme_num = prompt_number('q_theme', texts['q_theme#'])
#    graphics_num = prompt_number('q_graphics', texts['q_graphics#'])
    theme_num = graphics_num = 0
    bac = BACgame(theme_num, graphics_num)
    bac.start_one_game()