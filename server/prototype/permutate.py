#!/usr/bin/env python

alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'

def get_permutations(word):
  splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
  deletes = [a + b[1:] for a, b in splits if b]
  transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
  replaces = [a + c + b[1:] for a, b in splits for c in alphabet if b]
  inserts = [a + c + b for a, b in splits for c in alphabet]
  return set(deletes + transposes + replaces + inserts)

if __name__ == '__main__':
  print ', '.join(get_permutations('google'))
  print len(get_permutations('google'))
