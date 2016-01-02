#!/usr/bin/env python

import web
import redis
import redis_utils as r_utils

URL_CORRECTION_FORMAT = '{{"correction": "{0}"}}'

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)

urls = (
  '/domain/(.*)', 'validate_domain'
)

app = web.application(urls, globals())

class validate_domain:
  def GET(self, domain):
    trimmedDomain = domain.replace(".com", "")
    r_server = redis.StrictRedis(connection_pool=pool)
    intended_domain_id = r_server.hget(r_utils.get_typo_key(trimmedDomain), 'intended')
    if intended_domain_id is None:
      return ''

    intended_domain = r_server.hget(r_utils.get_domain_key(intended_domain_id), 'url')
    return URL_CORRECTION_FORMAT.format(intended_domain)

if __name__ == "__main__":
  app.run()
