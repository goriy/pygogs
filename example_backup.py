#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import pygogs

## url to use during backup (uncomment only one):
url_type = 'clone_url'
#url_type = 'html_url'
#url_type = 'ssh_url'

verbosity = 1
dry_run = False

## extra options for git
git_extra_options = ['-q']
#git_extra_options = []

# create helper class
pg = pygogs.pygogs()
# set verbosity level. 0 - quiet [default], 1 - print some information
pg.verbosity(0)
# setup access token from file
pg.set_token_from_file('example.token')
# set server url
pg.set_url('https://example.com')

repolist = pg.list_your_repositories()

if (repolist):
  for repo in repolist:

    # get repository info
    name = repo['name']
    full_name = repo['full_name']
    dirname = repo['owner']['username']
    url = repo[url_type]

    # if user/organization directory doesn't exist - create it
    if not os.path.exists(dirname):
      if verbosity > 0:
        sys.stderr.write("create dir %s\n" % (dirname))
      if not dry_run:
        os.makedirs(dirname)

    # if repository directory doesn't exist - clone it
    if not os.path.exists(full_name):
      if verbosity > 0:
        sys.stderr.write("clone %s from  %s\n" % (full_name, url))
      if not dry_run:
        subprocess.run(["git", "clone", "--mirror", url, full_name] + git_extra_options)

    else:   # if repository directory exists - fetch data into it
      if verbosity > 0:
        sys.stderr.write("fetch %s from  %s\n" % (full_name, url))
      if not dry_run:
        subprocess.run(["git", "-C", full_name, "fetch", url] + git_extra_options)
