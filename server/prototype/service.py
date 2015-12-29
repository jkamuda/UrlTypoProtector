#!/usr/bin/env python
import web
import redis

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)

urls = (
  '/validate/(.*)', 'validate_domain',
  '/users/(.*)', 'get_user'
)

app = web.application(urls, globals())

class validate_domain:
  def GET(self, domain):
    trimmedDomain = domain.replace(".com", "")
    print trimmedDomain
    r_server = redis.StrictRedis(connection_pool=pool)
    correction = r_server.get(trimmedDomain)
    print correction
    if correction:
      return correction
    else:
      return ''

class get_user:
  def GET(self, user):
    return 'you got it'

if __name__ == "__main__":
  app.run()
