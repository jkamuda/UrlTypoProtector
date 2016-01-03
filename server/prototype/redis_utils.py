#!/usr/bin/env python

DOMAIN_ID_KEY = 'next_domain_id'
DOMAIN_KEY_FORMAT = 'domain:{0}'
DOMAIN_NAME_KEY_FORMAT = 'domain.name:{0}'
TYPO_KEY_FORMAT = 'typo:{0}'

def get_typo_key(typo):
    return TYPO_KEY_FORMAT.format(typo)

def get_domain_key(domain_id):
    return DOMAIN_KEY_FORMAT.format(domain_id)
