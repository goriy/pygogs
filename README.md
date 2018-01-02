# pygogs

## Description

Simple Python helper class to work with [Gogs API](https://github.com/gogits/go-gogs-client/wiki).

It doesn't provide full API support at the moment.

## How does it work

*pygogs* uses *requests* python package as a backend to sending API to Gogs server.

### Authorization on Gogs server

Authorization on Gogs server is done by means of *Access Token*.

So, first of all, you need to create *Access Token* on your Gogs server.

This token could be used as a string directly in your script or it could be read
from separate file.
Usage of separate file with token is more preferrable for several reasons:

* your script could be in repository (even in public one) without revealing authorization info
* separate file with token could have different (i.e. more restricted) premissions
* file with token could be ignored by version control systems (.gitignore, .hgignore, ...)

*pygogs* sends Access Token as a header.

Server response is data in *json* format, so it loaded by means of python's json.loads()

### In your script

Simple script example:

```python
    import pygogs

    # create helper class
    pg = pygogs()

    # set verbosity level. 0 - quiet, 1 - print some information
    pg.verbosity(1)

    # setup access token from file
    pg.set_token_from_file ('example.token')
    # alternatively access token could be setup directly as string
    # pg.set_token ('1234567890abcdef...')

    # set server url
    pg.set_url ('https://example.com')

    # create private repository for current user
    result = pg.create_your_repo ('project1', 'Super project for current user', True)

    # check http answer code
    if (pg.lastcode == 404):
      print ('not found')
    else:
      # print id from server response
      print (result['id'])

    # create public organization repository
    result = pg.create_organization_repo ('OCPCorp', 'project2', 'Mega Ultra Super project', False)
```
