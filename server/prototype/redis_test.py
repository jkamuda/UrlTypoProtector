import redis
import json

import permutate

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)

def fill(word):
  r_server = redis.StrictRedis(connection_pool=pool)
  correction = {}
  correction['correction'] = word
  correctionJson = json.dumps(correction)

  for permutation in permutate.get_permutations(word):
    print permutation
    r_server.set(permutation, correctionJson)

if __name__ == "__main__":
  fill("youtube")
