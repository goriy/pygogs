import os
import requests
import json


class pygogs(object):
    __slots__ = [  # private variables
                 "__verbosity",
                 "__hdrs",
                 # public variables
                 "token",
                 "server_url",
                 "lastcode"
                 ]

    ###########################################################################
    def __init__(self):
        self.__verbosity = 0
        self.server_url = ''
        self.token = ''
        self.__hdrs = {'Authorization': 'token 123'}
        os.linesep = '\n'

    ###########################################################################
    def verbosity(self, verb):
        self.__verbosity = verb

    ###########################################################################
    def set_token(self, new_token):
        self.token = new_token
        self.__hdrs = {'Authorization': 'token ' + new_token,
                       'content-type': 'application/json; charset=UTF-8'}

    ###########################################################################
    def set_token_from_file(self, token_file):
        f = open(token_file, "r")
        new_token = f.readline().strip()
        f.close()
        self.set_token(new_token)

    ###########################################################################
    def set_url(self, new_url):
        self.server_url = new_url + '/api/v1'

    ###########################################################################
    def __process_response(self, r, desired_code=200):
        self.lastcode = r.status_code
        if (r.status_code == desired_code):
            if ('content-type' in r.headers and
                    r.headers['content-type'].startswith('application/json')):

                data = r.json()
                if self.__verbosity > 0:
                    print("JSON: " + json.dumps(data))
            else:
                data = r.text.strip()
                if self.__verbosity > 0 and data != '':
                    print('TEXT: ' + data)
            return data

        else:
            if self.__verbosity > 0:
                print(r)
                data = r.text.strip()
                if data != '':
                    print(data)
            return False

    ###########################################################################
    def list_your_organizations(self):
        url = self.server_url + '/user/orgs'
        r = requests.get(url, headers=self.__hdrs)
        return self.__process_response(r)

    ###########################################################################
    def list_your_repositories(self):
        url = self.server_url + '/user/repos'
        r = requests.get(url, headers=self.__hdrs)
        return self.__process_response(r)

    ###########################################################################
    def list_user_organizations(self, username):
        url = self.server_url + '/users/' + username + '/orgs'
        r = requests.get(url, headers=self.__hdrs)
        return self.__process_response(r)

    ###########################################################################
    def list_user_repositories(self, username):
        url = self.server_url + '/users/' + username + '/repos'
        r = requests.get(url, headers=self.__hdrs)
        return self.__process_response(r)

    ###########################################################################
    def get_organization(self, orgname):
        url = self.server_url + '/orgs/' + orgname
        r = requests.get(url, headers=self.__hdrs)
        return self.__process_response(r)

    ###########################################################################
    def get_repository(self, owner, repo):
        url = self.server_url + '/repos/' + owner + '/' + repo
        r = requests.get(url, headers=self.__hdrs)
        return self.__process_response(r)

    ###########################################################################
    def list_organization_repositories(self, orgname):
        url = self.server_url + '/orgs/' + orgname + '/repos'
        r = requests.get(url, headers=self.__hdrs)
        return self.__process_response(r)

    ###########################################################################
    def search_repos(self, name, limit=100):
        url = self.server_url + '/repos/search'
        payload = {'q': name, 'limit': limit}
        r = requests.get(url, headers=self.__hdrs, data=json.dumps(payload))
        return self.__process_response(r)

    ###########################################################################
    def list_branches(self, owner, repo):
        url = self.server_url + '/repos/' + owner + '/' + repo + '/branches'
        r = requests.get(url, headers=self.__hdrs)
        return self.__process_response(r)

    ###########################################################################
    def get_branch(self, owner, repo, branch):
        url = self.server_url + '/repos/' + owner + '/' + repo + '/branches/' + branch
        r = requests.get(url, headers=self.__hdrs)
        return self.__process_response(r)

    ###########################################################################
    def __construct_repo_payload(self, name, description, private, auto_init,
                                 gitignores, license, readme):

        basic_data = {'name': name,
                      'description': description,
                      'private': private}

        advanced_data = {'auto_init': True,
                         'gitignores': gitignores,
                         'license': license,
                         'readme': readme}

        if (auto_init):
            payload = {**basic_data, **advanced_data}
        else:
            payload = basic_data

        return payload

    ###########################################################################
    def __create_repo(self, url, name, description, private, auto_init,
                      gitignores, license, readme):

        payload = self.__construct_repo_payload(name, description, private,
                                                auto_init, gitignores, license,
                                                readme)
        r = requests.post(url, headers=self.__hdrs, data=json.dumps(payload))
        return self.__process_response(r, 201)

    ###########################################################################
    def create_your_repo(self, name, description='',
                         private=False, auto_init=False,
                         gitignores='', license='', readme='Default'):
        url = self.server_url + '/user/repos'
        return self.__create_repo(url, name, description, private, auto_init, gitignores, license, readme)

    ###########################################################################
    def create_organization_repo(self, organization, name, description='',
                                 private=False, auto_init=False,
                                 gitignores='', license='', readme='Default'):

        url = self.server_url + '/org/' + str(organization) + '/repos'
        return self.__create_repo(url, name, description, private, auto_init, gitignores, license, readme)

    ###########################################################################
    def create_user_repo(self, username, name, description='',
                         private=False, auto_init=False,
                         gitignores='', license='', readme='Default'):

        url = self.server_url + '/admin/users/' + username + '/repos'
        return self.__create_repo(url, name, description, private, auto_init, gitignores, license, readme)

    ###########################################################################
    def delete_repository(self, owner, repo):
        url = self.server_url + '/repos/' + owner + '/' + repo
        r = requests.delete(url, headers=self.__hdrs)
        return self.__process_response(r, 204)

    ###########################################################################
    def create_new_organization(self, username, orgname, full_name='', description='', website='', location=''):
        url = self.server_url + '/admin/users/' + username + '/orgs'
        payload = {'username': orgname, 'full_name': full_name, 'description': description, 'website': website, 'location': location}
        r = requests.post(url, headers=self.__hdrs, data=json.dumps(payload))
        return self.__process_response(r, 201)

    ###########################################################################
    def create_your_organization(self, orgname, full_name='', description='', website='', location=''):
        url = self.server_url + '/user/orgs'
        payload = {'username': orgname, 'full_name': full_name, 'description': description, 'website': website, 'location': location}
        r = requests.post(url, headers=self.__hdrs, data=json.dumps(payload))
        return self.__process_response(r, 201)

    ###########################################################################
    def edit_an_organization(self, orgname, full_name, description, website, location):
        url = self.server_url + '/orgs/' + orgname
        payload = {'full_name': full_name, 'description': description, 'website': website, 'location': location}
        r = requests.patch(url, headers=self.__hdrs, data=json.dumps(payload))
        return self.__process_response(r)
