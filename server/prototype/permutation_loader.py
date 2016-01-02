import redis
import json
import csv
import sys

import permutation_tools

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)

def add_permutations_for_domains(domains):
  totalDomains = len(domains)
  completed = 0
  for domain in uniqueDomains:
    add_permutations_for_domain(domain)
    completed += 1
    report_progress(completed, totalDomains)

def report_progress(completed, total):
  sys.stdout.write('\r')
  percentComplete = float(completed) / total * 100
  sys.stdout.write("[%-50s] %3.2f%%" % ('=' * int((percentComplete) / 2), percentComplete))
  sys.stdout.flush()

def add_permutations_for_domain(domain):
  r_server = redis.StrictRedis(connection_pool=pool)

  correction_info = {}
  correction_info['correction'] = domain
  correction_info_json = json.dumps(correction_info)

  domain_permutations = permutation_tools.get_permutations(domain)
  for permutation in domain_permutations:
    r_server.set(permutation, correction_info_json)

  #print 'loaded {0} permutations for {1}'.format(len(domain_permutations), domain)

def load_unique_domains_from_csv(filename):
  uniqueDomains = set()
  f = open(filename, 'rt')
  try:
    reader = csv.reader(f)
    for row in reader:
      domain = row[1].split('.')[0]
      if len(domain) < 4:
        continue
      uniqueDomains.add(domain)
  finally:
    f.close()

  return uniqueDomains

if __name__ == "__main__":
  #load_word_permutations("youtube")
  uniqueDomains = load_unique_domains_from_csv('/home/alpha/workspace/top-100.csv')
  #print len(uniqueDomains)
  add_permutations_for_domains(uniqueDomains)
