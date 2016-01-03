#!/usr/bin/env python

import csv
import re

DOMAIN_CSV_MOZ = '/home/alpha/workspace/domain_data/moz/top-500.csv'
DOMAIN_TXT_QUANTCAST = '/home/alpha/workspace/domain_data/quantcast/Quantcast-Top-Million.txt'
DOMAIN_CSV_QUANTCAST = '/home/alpha/workspace/domain_data/quantcast/Quantcast-Top-Million.csv'
FIXED_WHITELIST = '../../chrome-extension/resources/fixed_whitelist.txt'

def load_from_csv(filename, whitelist_domains, limit):
  f = open(filename, 'rt')
  try:
    reader = csv.reader(f)
    domain_cnt = 0
    for row in reader:
      domain = row[1].split('.')[0]
      if len(domain) < 4:
        continue
      whitelist_domains.add(domain)
      domain_cnt += 1
      if domain_cnt > limit:
        break
  finally:
    f.close()
  return whitelist_domains

def to_csv(filename):
  sites = []
  f = open(filename, 'rt')
  cnt = 0
  try:
    for line in f.readlines():
      cnt += 1
      if '#' in line or 'Hidden profile' in line:
        continue
      split = re.split(r'\t+', line)
      rank = split[0]
      domain = split[1].replace('\r\n', '')
      sites.append('{0},"{1}"'.format(rank, domain))
  finally:
    f.close()

  with open(DOMAIN_CSV_QUANTCAST, 'wb') as f:
    for site in sites:
      f.write(site + '\n')

def compile_fixed_whitelist(whitelist_domains):
  with open(FIXED_WHITELIST, 'wb') as f:
    for domain in whitelist_domains:
      f.write('{},'.format(domain))

if __name__ == '__main__':
  #to_csv(DOMAIN_TXT_QUANTCAST)
  unique_domains = set()
  unique_domains = load_from_csv(DOMAIN_CSV_MOZ, unique_domains, 600)
  unique_domains = load_from_csv(DOMAIN_CSV_QUANTCAST, unique_domains, 1000)
  compile_fixed_whitelist(unique_domains)
