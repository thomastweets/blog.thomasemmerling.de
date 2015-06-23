#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Thomas Emmerling'
SITENAME = u'thomastweets'
SITEURL = ''
TAGLINE = 'notes on data analysis, programming, and the rest'
LOCALE = u'en_US.utf8'

THEME = "themes/svbhack"

PATH = 'content'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

TWITTER_USERNAME = "thomastweets"
GITHUB_URL = "https://github.com/thomastweets"
USER_LOGO_URL = "https://www.gravatar.com/avatar/46624cc77f30ff81855f6fdd94fbd6f1?s=140"
DISQUS_SITENAME = "thomastweets"

SOCIAL = (('fa-twitter-square', 'http://twitter.com/thomastweets'),
          ('fa-linkedin-square', 'https://www.linkedin.com/in/thomasemmerling'),
          ('fa-github-square', 'http://github.com/thomastweets'),)

STATIC_PATHS = ['images', 'extra/CNAME']
EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'},}

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
