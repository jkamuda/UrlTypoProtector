#!/usr/bin/env python

import csv
from enum import *

DOMAIN_CSV_MOZ = '/home/alpha/workspace/domain_data/moz/top-500.csv'
FIXED_WHITELIST = '../../chrome-extension/resources/fixed_whitelist.txt'

DataSource = enum(MOZ='moz', QUANTCAST='quantcast')

def load_unique_domains_from_csv(filename, data_source):
  unique_domains = set()
  f = open(filename, 'rt')
  try:
    reader = csv.reader(f)
    for row in reader:
      domain = row[1].split('.')[0]
      if len(domain) < 4:
        continue
      unique_domains.add(domain)
  finally:
    f.close()
  return unique_domains

def compile_fixed_whitelist(whitelist_domains):
  with open(FIXED_WHITELIST, 'wb') as f:
    for domain in whitelist_domains:
      f.write('{},'.format(domain))

if __name__ == '__main__':
  unique_domains = load_unique_domains_from_csv(DOMAIN_CSV_MOZ, DataSource.MOZ)
  compile_fixed_whitelist(unique_domains)
