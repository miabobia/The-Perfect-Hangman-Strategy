'''
consider all words that it could be, given the information you already have
(how long it is, where specific letters are, 
and specific letters that are not in the word)
'''


from typing import Generator


def word_stream(words_path: str):
    with open(words_path, 'r') as f:
        for word in [w.strip() for w in f.readlines()]:
            yield word


def big_check(
    word_len: int,
    guess_state: list[tuple[chr, int]],
    guessed_letters: set[str],
    word_gen: Generator[str, None, None]
) -> Generator[str, None, None]:
    for word in word_gen:
        valid_word = True
        if len(word) != word_len:
            continue
        if len(guessed_letters.intersection(set(word))) > 0:
            # print(f'intersection fail -> {word} : {guessed_letters}')
            continue
        for c, idx in guess_state:
            if word[idx] != c:
                valid_word = False
                break

        if valid_word:
            yield word


def step_one(
    word: str,
    guessed: set,
    guess_state: list[tuple[chr, int]],
    words_path: str
):
    '''
    first pass of possible words to guess using step one of "The Perfect Hangman Strategy":
    ```
    consider all words that it could be, given the information you already have
    (how long it is,
    where specific letters are,
    and specific letters that are not in the word)
    ```
    Params:
    word        -> word user is attempting to guess
    guessed     -> letters that have been guessed incorrectly by the user
    guess_state -> character, index pairs of correctly guessed letters
    words_path  -> path to word dictionary
    '''

    word = 'pizza'
    guessed = set('eom')
    guess_state = [('p', 0)]

    word_gen = big_check(
        word_len=len(word),
        guess_state=guess_state,
        guessed_letters=guessed,
        word_gen=word_stream(words_path)
    )

    for word in word_gen:
        print(word)





if __name__ == "__main__":
    step_one('', '', '', './data/words_alpha.txt')
