# pygogs

## Description

Simple Python helper class to work with [Gogs API](https://github.com/gogits/go-gogs-client/wiki).

It doesn't provide full API support at the moment.

## How does it work

*pygogs* uses *requests* python package as a backend for sending data to Gogs server.

### Authorization on Gogs server

Authorization on Gogs server is done by means of *Access Token*.

So, first of all, you need to create *Access Token* on your Gogs server.

This token could be used as a string directly in your script or it could be read
from separate file.
Usage of separate file with token is more preferrable for several reasons:

* your script could be in repository (even in public one) without revealing authorization info
* separate file with token could have different (i.e. more restricted) file permissions
* file with token could be ignored by version control systems (.gitignore, .hgignore, ...)

*pygogs* sends Access Token as a http(s) header.

Server response is data in *json* format, so it's loaded by means of python's json.loads()

### Implemented

Those API functions are implemented:

- [ ] Administration Organizations - [doc](https://github.com/gogits/go-gogs-client/wiki/Administration-Organizations#create-team-of-an-organization)
    - [x] create_new_organization
    - [x] create_your_organization
    - [ ] create_team_of_organization
    - [ ] add_team_membership
    - [ ] remove_team_membership
    - [ ] add_or_update_team_repository
    - [ ] remove_team_repository
- [x] Administration Repositories - [doc](https://github.com/gogits/go-gogs-client/wiki/Administration-Repositories)
    - [x] create_user_repo
- [ ] Administration Users - [doc](https://github.com/gogits/go-gogs-client/wiki/Administration-Users)
    - [ ] create_user
    - [ ] edit_user
    - [ ] delete_user
    - [ ] create_user
    - [ ] create_a_public_key_for_user
- [ ] Issues - [doc](https://github.com/gogits/go-gogs-client/wiki/Issues)
- [ ] Issues Comments - [doc](https://github.com/gogits/go-gogs-client/wiki/Issues-Comments)
- [ ] Issues Labels - [doc](https://github.com/gogits/go-gogs-client/wiki/Issues-Labels)
- [ ] Issues Milestones - [doc](https://github.com/gogits/go-gogs-client/wiki/Issues-Milestones)
- [ ] Miscellaneous - [doc](https://github.com/gogits/go-gogs-client/wiki/Miscellaneous)
- [x] Organizations - [doc](https://github.com/gogits/go-gogs-client/wiki/Organizations)
    - [x] list_your_organizations
    - [x] list_user_organizations
    - [x] get_organization
    - [x] edit_an_organization
- [ ] Organizations Members - [doc](https://github.com/gogits/go-gogs-client/wiki/Organizations-Members)
    - [ ] add_or_update_organization_membership
- [ ] Organizations Teams - [doc](https://github.com/gogits/go-gogs-client/wiki/Organizations-Teams)
    - [ ] list_teams_of_an_organization
- [ ] Repositories - [doc](https://github.com/gogits/go-gogs-client/wiki/Repositories)
    - [x] search_repos
    - [x] list_your_repositories
    - [x] list_user_repositories
    - [x] list_organization_repositories
    - [x] create_your_repo
    - [x] create_organization_repo
    - [ ] migrate
    - [x] get_repository
    - [x] delete_repository
    - [x] list_branches
    - [x] get_branch
    - [ ] mirror_sync
- [ ] Repositories Collaborators - [doc](https://github.com/gogits/go-gogs-client/wiki/Repositories-Collaborators)
    - [ ] add_user_as_a_collaborator
- [ ] Repositories Contents - [doc](https://github.com/gogits/go-gogs-client/wiki/Repositories-Contents)
    - [ ] download_raw_content
    - [ ] download_archive
- [ ] Repositories Deploy Keys - [doc](https://github.com/gogits/go-gogs-client/wiki/Repositories-Deploy-Keys)
- [ ] Repositories Webhooks - [doc](https://github.com/gogits/go-gogs-client/wiki/Repositories-Webhooks)
- [ ] Users - [doc](https://github.com/gogits/go-gogs-client/wiki/Users)
- [ ] Users Emails - [doc](https://github.com/gogits/go-gogs-client/wiki/Users-Emails)
- [ ] Users Followers - [doc](https://github.com/gogits/go-gogs-client/wiki/Users-Followers)
- [ ] Users Public Keys - [doc](https://github.com/gogits/go-gogs-client/wiki/Users-Public-Keys)


### Example 1

Simple script example:

```python
    import pygogs

    # create helper class
    pg = pygogs.pygogs()

    # set verbosity level. 0 - quiet, 1 - print some information
    pg.verbosity(0)

    # setup access token from file
    pg.set_token_from_file ('example.token')
    # alternatively access token could be setup directly as string
    # pg.set_token ('1234567890abcdef...')

    # set server url
    pg.set_url ('https://example.com')

    # print some basic information about all user's repositories
    repolist = pg.list_your_repositories()
    if (repolist):
      for repo in repolist:
        print ('%s [id = %d]' % (repo['full_name'], repo['id']))

    # create private repository for current user
    result = pg.create_your_repo (name='project1', description='Super project for current user', private=True)

    # check http answer code
    if (pg.lastcode == 404):
      print ('not found')
    else:
      # print id from server response
      print (result['id'])

    # create public organization repository
    result = pg.create_organization_repo (organization='OCPCorp', name='project2', description='Mega Ultra Super project')
```

### Example 2

File [*example_backup.py*](example_backup.py) is a bit more useful example script.
It does backup of all your repositories from server to current directory.
It's does something like incremental backups (by means of git) and could be run even from *crontab*.
