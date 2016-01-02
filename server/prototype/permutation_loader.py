#!/usr/bin/env pythons

import redis
import json
import csv
import sys

import permutation_tools

DOMAIN_CSV = '/home/alpha/workspace/top-100.csv'

DOMAIN_ID_KEY = 'next_domain_id'
DOMAIN_KEY_FORMAT = 'domain:{0}'
DOMAIN_NAME_KEY_FORMAT = 'domain.name:{0}'
TYPO_KEY_FORMAT = 'typo:{0}'

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)

def load_typos():
  uniqueDomains = load_unique_domains_from_csv(DOMAIN_CSV)
  print 'flushing database...'
  flush_db()
  add_permutations_for_domains(uniqueDomains)

def add_permutations_for_domains(domains):
  totalDomains = len(domains)
  completed = 0
  for domain in domains:
    add_permutations_for_domain(domain)
    completed += 1
    report_progress(completed, totalDomains)

def report_progress(completed, total):
  sys.stdout.write('\r')
  percentComplete = float(completed) / total * 100
  sys.stdout.write("[%-50s] %3.2f%%" % ('=' * int((percentComplete) / 2), percentComplete))
  sys.stdout.flush()

def add_permutations_for_domain(domain):
  r_server = get_redis_connection()

  domain_id = add_domain(r_server, domain)

  domain_typo_permutations = permutation_tools.get_permutations(domain)
  for typo in domain_typo_permutations:
    r_server.hset(TYPO_KEY_FORMAT.format(typo), 'intended', domain_id)

  #print 'loaded {0} permutations for {1}'.format(len(domain_permutations), domain)

def add_domain(r_server, domain):
  domain_id = r_server.incr(DOMAIN_ID_KEY)
  r_server.hset(DOMAIN_KEY_FORMAT.format(domain_id), 'url', domain)
  r_server.hset(DOMAIN_NAME_KEY_FORMAT.format(domain), 'id', domain_id)
  return domain_id

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

def flush_db():
  get_redis_connection().flushdb()

def get_redis_connection():
  return redis.StrictRedis(connection_pool=pool)

if __name__ == "__main__":
  load_typos()
