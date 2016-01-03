#!/usr/bin/env python

import csv
import sys
import redis

import permutation_tools
import redis_utils as r_utils

#DOMAIN_CSV = '/home/alpha/workspace/domain_data/top-100.csv'
DOMAIN_CSV = '/home/alpha/workspace/domain_data/moz/top-500.csv'

CONNECTION_POOL = redis.ConnectionPool(host='localhost', port=6379, db=0)

def load_typos():
    flush_db()
    add_permutations_for_domains(load_unique_domains_from_csv(DOMAIN_CSV))

def add_permutations_for_domains(domains):
    total_domains = len(domains)
    completed = 0
    for domain in domains:
        add_permutations_for_domain(domain)
        completed += 1
        report_progress(completed, total_domains)

def report_progress(completed, total):
    sys.stdout.write('\r')
    percent__complete = float(completed) / total * 100
    sys.stdout.write("[%-50s] %3.2f%%" % ('=' * int((percent__complete) / 2), percent__complete))
    sys.stdout.flush()

def add_permutations_for_domain(domain):
    r_server = get_redis_connection()

    domain_id = add_domain(r_server, domain)

    domain_typo_permutations = permutation_tools.get_permutations(domain)
    for typo in domain_typo_permutations:
        typo_key = r_utils.get_typo_key(typo)
        identify_conflict(r_server, domain, typo)
        if typo == domain:
            continue
        r_server.hset(typo_key, 'intended', domain_id)

    #print 'loaded {0} permutations for {1}'.format(len(domain_permutations), domain)

def add_domain(r_server, domain):
    domain_id = r_server.incr(r_utils.DOMAIN_ID_KEY)
    r_server.hset(r_utils.get_domain_key(domain_id), 'url', domain)
    r_server.hset(r_utils.DOMAIN_NAME_KEY_FORMAT.format(domain), 'id', domain_id)
    return domain_id

def identify_conflict(r_server, domain, typo):
    typo_key = r_utils.get_typo_key(typo)
    if r_server.exists(typo_key):
        domain_id = r_server.hget(typo_key, 'intended')
        intended_domain = r_server.hget(r_utils.get_domain_key(domain_id), 'url')
        print 'conflict for ' + domain + ' on ' + typo + ' (' + intended_domain + ')'

def load_unique_domains_from_csv(filename):
    unique_domains = set()
    f_csv = open(filename, 'rt')
    try:
        reader = csv.reader(f_csv)
        for row in reader:
            domain = row[1].split('.')[0]
            if len(domain) < 4:
                continue
            unique_domains.add(domain)
    finally:
        f_csv.close()

    return unique_domains

def flush_db():
    get_redis_connection().flushdb()

def get_redis_connection():
    return redis.StrictRedis(connection_pool=CONNECTION_POOL)

if __name__ == "__main__":
    load_typos()
    #domains = load_unique_domains_from_csv('/home/alpha/workspace/domain_data/moz/top-500.csv')
    #print domains
