#!/usr/bin/env python

import web
import redis
import redis_utils as r_utils

URL_CORRECTION_FORMAT = '{{"intended": "{0}"}}'

CONNECTION_POOL = redis.ConnectionPool(host='localhost', port=6379, db=0)

ENDPOINTS = (
    '/v1/domain/(.*)', 'DomainValidationService'
)

app = web.application(ENDPOINTS, globals())

class DomainValidationService():
    def GET(self, domain):
        trimmed_domain = domain.replace(".com", "")
        r_server = redis.StrictRedis(connection_pool=CONNECTION_POOL)
        intended_domain_id = r_server.hget(r_utils.get_typo_key(trimmed_domain), 'intended')
        if intended_domain_id is None:
            return ''

        intended_domain = r_server.hget(r_utils.get_domain_key(intended_domain_id), 'url')
        return URL_CORRECTION_FORMAT.format(intended_domain)

if __name__ == "__main__":
    app.run()
