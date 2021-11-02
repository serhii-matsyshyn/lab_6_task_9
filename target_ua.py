"""
Game 'Target UA'

Description of the game:
The user receives randomly generated letters
of the Ukrainian alphabet
(5 letters, similar to the English version,
all letters are unique).
After that, he randomly receives a part of speech
("noun", "verb", "adjective", "adverb").
He must come up with at most words, up to and including 5 letters,
that belong to this part of speech
and begin with one of the generated letters.
"""

from typing import List
from typing import Tuple
from typing import Any
import random
import string


def generate_grid() -> List[str]:
    """ Generates a playing grid,
    similar to the English version of the game,
    but uses lowercase letters of the Ukrainian alphabet.

    :return: A list of generated letters (5 unique letters)
    :rtype: List[str]
    """
    alphabet = list('абвгґдеєжзиіїйклмнопрстуфхцчшщьюя')
    random.shuffle(alphabet)
    game_grid = alphabet[:5]

    return game_grid


def get_words(filename: str, letters: list) -> list:
    """ Reads the dictionary file and
    returns the list of tuples: the word as part of the language.
    Parts of speech to be considered: "noun", "verb", "adjective", "adverb".

    :param filename: Filename of dictionary
    :type filename: str
    :param letters: 1 letter of the words that should be found
    :type letters: list, str
    :return: the list of tuples: the word as part of the language
    :rtype: list

    >>> print(get_words("base.lst", ['я'])[:10])
    [('ябеда', 'noun'), ('яв', 'noun'), ('ява', 'noun'), \
('явити', 'verb'), ('явище', 'noun'), ('явір', 'noun'), \
('явка', 'noun'), ('явний', 'adjective'), ('яга', 'noun'), \
('ягель', 'noun')]
    """

    language_parts = {"/n": "noun",
                      "/v": "verb",
                      "noun": "noun",
                      "adj": "adjective",
                      "adv": "adverb",
                      "n": "noun",
                      "v": "verb",
                      }
    bad_types = ['intj', 'noninfl']
    all_words = []
    with open(filename, encoding='utf8') as file:
        for line in file.readlines():
            word, *word_property = (line.rstrip().lower().split(' '))

            if (len(word) <= 5) and (len(word) > 0) and (word[0] in letters):
                word_property = " ".join(i for i in word_property if i)
                if not any(bad_part in word_property for bad_part in bad_types):
                    for part in language_parts.keys():
                        if part in word_property:
                            word_property = language_parts[part]
                            break

                    all_words.append((word, word_property))

    return all_words


def check_user_words(user_words: List[str],
                     language_part: str,
                     letters: List[str],
                     dict_of_words: List[tuple]) -> tuple:
    """ checks the words entered by the user
    (it is given a user_words - a list of words),
    using a list of letters from which to start words (list of letters),
    and checks which of the words entered by the user belong
    to the transmitted part of speech (language_part tape).
    Dict_of_words - list of word pairs -
    part of speech generated by the get_words function.
    The function returns a list of correct
    user words and a list of words that the user missed

    :param user_words: A list of words
    :type user_words: List[str]
    :param language_part: Part of language
    :type language_part: str
    :param letters: A list of letters from which to start words
    :type letters: List[str]
    :param dict_of_words: List of word pairs
    :type dict_of_words:
    :return: A list of correct user words and
    a list of words that the user missed
    :rtype: Tuple[List[str]]

    >>> print(check_user_words(['брати', 'мити', '', 'писати', 'тест', '123'],\
"verb", ['р', 'х', 'б', 'ц', 'м'], get_words("base.lst", ['р', 'х', 'б', 'ц', 'м'])))
    (['брати', 'мити'], ['бгати', 'бити', 'бігти', 'брити', 'буяти', \
'мати', 'маяти', 'мерти', 'мести', 'мжити', 'мліти', 'мріти', 'мчати',\
 "м'яти", 'раяти', 'рвати', 'ревти', 'ректи', 'ржати', 'рити', 'роїти', 'рости', 'хляти'])
    """
    correct_words = []

    dict_of_words_dict = dict(dict_of_words)

    for word in user_words:
        if dict_of_words_dict.get(word) == language_part:
            correct_words.append(word)

    more_words = [word for word in dict_of_words_dict.keys()
                  if ((word not in correct_words) and
                      (word[0] in letters) and
                      (dict_of_words_dict[word] == language_part))]

    return correct_words, more_words


def get_user_words() -> List[str]:
    """ Gets words from user input and returns a list with these words.
    Usage: enter a word or press ctrl+d to finish.

    :return: list with words
    :rtype: List[str]
    """
    words_input = input("Enter the words (lowercase, in Ukrainian) separated by space: ")
    return list(set(words_input.split()))


def main():
    """
    Main function of the game
    """
    print("A game that will help students learn Ukrainian \
words that belong to different parts of speech")

    game_grid = generate_grid()
    print("The game grid:", ' '.join(game_grid))

    language_parts = ["noun", "verb", "adjective", "adverb"]
    language_part = random.choice(language_parts)
    print("Language part:", language_part)

    all_words_from_dictionary = get_words("base.lst", game_grid)
    user_words = get_user_words()

    correct_words, more_words = check_user_words(user_words,
                                                 language_part,
                                                 game_grid,
                                                 all_words_from_dictionary)
    print("Correct words:")
    for word in correct_words:
        print(word)

    print("More words:", )
    for word in more_words:
        print(word)


if __name__ == '__main__':
    main()
