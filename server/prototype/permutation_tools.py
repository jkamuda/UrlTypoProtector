#!/usr/bin/env python

ALPHABET = 'abcdefghijklmnopqrstuvwxyz0123456789'

def get_permutations(word):
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
    replaces = [a + c + b[1:] for a, b in splits for c in ALPHABET if b]
    inserts = [a + c + b for a, b in splits for c in ALPHABET]
    return set(deletes + transposes + replaces + inserts)

def test_runner():
    word_permutations = get_permutations('google')
    print ', '.join(word_permutations)
    print len(word_permutations)

if __name__ == '__main__':
    test_runner()
