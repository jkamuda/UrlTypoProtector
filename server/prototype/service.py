#!/usr/bin/env python
import web

urls = (
    '/validate/(.*)', 'validate_domain',
    '/users/(.*)', 'get_user'
)

app = web.application(urls, globals())

class validate_domain:
    def GET(self, domain):
        if domain == 'yahoo.com':
            return web.notfound("bad stuff man");
    	return 'you got it - ' + domain

class get_user:
    def GET(self, user):
        return 'you got it'

if __name__ == "__main__":
    app.run()
