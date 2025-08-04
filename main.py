from typing import Generator

LETTERS = set('abcdefghijklmnopqrstuvwxyz')


def get_word_stream(words_path: str):
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
    word_gen: Generator[str, None, None]
) -> Generator[str, None, None]:
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

    return big_check(
        word_len=len(word),
        guess_state=guess_state,
        guessed_letters=guessed,
        word_gen=word_gen
    )


def step_two(
    guessed_letters: set,
    guess_state: tuple[chr, int],
    word_gen: Generator[str, None, None]
):
    '''
    for each letter you have not guessed yet,
    assume that the word does not contain that letter,
    and determine how many of the possible words would still 
    be on the table if that were the case
    '''
    unguessed_letters = LETTERS - guessed_letters - set(l for l, _ in guess_state)
    word_list = list(word_gen)

    unguessed_filter = {
        letter: list(filter(lambda x: letter not in x, word_list[:]))
        for letter in unguessed_letters
    }

    return min(
        unguessed_filter.items(),
        key=lambda x: len(x[1])
    )


def play(words_path: str):
    # initalize game variables
    word = 'pizza'
    guessed = set()
    guess_state = []

    HANGMAN_HEALTH = 5

    while len(guess_state) != len(word) and len(guessed) < HANGMAN_HEALTH:
        filtered_words = step_one(
            word=word,
            guessed=guessed,
            guess_state=guess_state,
            word_gen=get_word_stream(words_path)
        )

        guess, guess_len = step_two(
            guessed_letters=guessed,
            guess_state=guess_state,
            word_gen=filtered_words
        )

        if guess in word:
            # get all indexes of character in word
            guess_state += [(guess, idx) for idx, ch in enumerate(word) if ch == guess]
        else:
            guessed.add(guess)
        print(f'WORD: {word}\nGUESS: {guess}\nguess_len: {len(guess_len)}\nguess_state: {guess_state}\nguessed_letters: {guessed}\n\n')


if __name__ == "__main__":
    play('./data/words_alpha.txt')
