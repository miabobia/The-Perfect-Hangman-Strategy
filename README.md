# The Perfect Hangman Strategy

## Program to implement "The Perfect Hangman Strategy" as defined in the video ["hangman is a weird game"](https://www.youtube.com/watch?v=le5uGqHKll8) by [jan Misali](https://www.youtube.com/@HBMmaster)

## 1. consider all words that it could be, given the information you already have (how long it is, where specific letters are, and specific letters that are not in the word)
## 2. for each letter you have not guessed yet, assume that the word does not contain that letter, and determine how many of the possible words would still be on the table if that were the case
## 3. select whichever letter minimizes this number