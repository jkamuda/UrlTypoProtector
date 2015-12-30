import redis
import json

import permutation_tools

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)

def load_word_permutations(word):
  r_server = redis.StrictRedis(connection_pool=pool)

  correction_info = {}
  correction_info['correction'] = word
  correction_info_json = json.dumps(correction_info)

  word_permutations = permutation_tools.get_permutations(word)
  for permutation in word_permutations:
    r_server.set(permutation, correction_info_json)

  print 'loaded {0} permutations for {1}'.format(len(word_permutations), word)

if __name__ == "__main__":
  load_word_permutations("youtube")
