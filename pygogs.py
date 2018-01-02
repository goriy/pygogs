#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import requests
import json

class pygogs(object):
  __slots__ = [# private variables
               "__verbosity",
               # public variables
               "token",
               "server_url",
               "__hdrs",
               "lastcode"
               ]

  ################################################################################
  def __init__(self):
    self.__verbosity = 0
    self.server_url = ""

    os.linesep = '\n'

  ################################################################################
  def verbosity(self, verb):
    self.__verbosity = verb

  ################################################################################
  def set_token (self, new_token):
    self.token = new_token
    self.__hdrs = {'Authorization': 'token ' + new_token}

  ################################################################################
  def set_token_from_file (self, token_file):
    f = open(token_file,"r")
    new_token = f.readline().strip()
    f.close()
    self.set_token (new_token)

  ################################################################################
  def set_url (self, new_url):
    self.server_url = new_url + '/api/v1'

  ################################################################################
  def process_response(self, r, desired_code = 200):
    self.lastcode = r.status_code
    if (r.status_code == desired_code):
      if (r.headers['content-type'][:16] == 'application/json'):
        data = json.loads(r.text)
        if self.__verbosity > 0:
          print ("JSON: " + json.dumps(data))
      else:
        data = r.text
        if self.__verbosity > 0:
          print ('TEXT: ' + data)
      return data

    else:
      if self.__verbosity > 0:
        print(r)
        print(r.text)
      return False


  ################################################################################
  def list_your_organizations (self):
    url = self.server_url + '/user/orgs'
    r = requests.get(url, headers=self.__hdrs)
    return self.process_response(r)

  ################################################################################
  def list_your_repositories (self):
    url = self.server_url + '/user/repos'
    r = requests.get(url, headers=self.__hdrs)
    return self.process_response(r)

  ################################################################################
  def list_user_organizations (self, username):
    url = self.server_url + '/users/'+ username +'/orgs'
    r = requests.get(url, headers=self.__hdrs)
    return self.process_response(r)

  ################################################################################
  def list_user_repositories (self, username):
    url = self.server_url + '/users/'+ username +'/repos'
    r = requests.get(url, headers=self.__hdrs)
    return self.process_response(r)

  ################################################################################
  def get_organization (self, orgname):
    url = self.server_url + '/orgs/'+ orgname
    r = requests.get(url, headers=self.__hdrs)
    return self.process_response(r)

  ################################################################################
  def get_repository(self, owner, repo):
    url = self.server_url + '/repos/' + owner + '/' + repo
    r = requests.get(url, headers=self.__hdrs)
    return self.process_response(r)

  ################################################################################
  def create_new_organization(self, username, orgname, full_name, description, website, location):
    url = self.server_url + '/admin/users/' + username  + '/orgs'
    payload = {'UserName': orgname, 'full_name': full_name, 'description' : description, 'website': website, 'location' : location}
    r = requests.post(url, headers=self.__hdrs, data=payload)
    return self.process_response(r, 201)

  ################################################################################
  def edit_an_organization(self, orgname, full_name, description, website, location):
    url = self.server_url + '/orgs/'+ orgname
    payload = {'full_name': full_name, 'description' : description, 'website': website, 'location' : location}
    r = requests.patch(url, headers=self.__hdrs, data=payload)
    return self.process_response(r)

  ################################################################################
  def list_organization_repositories(self, orgname):
    url = self.server_url + '/orgs/'+ orgname +'/repos'
    r = requests.get(url, headers=self.__hdrs)
    return self.process_response(r)

  ################################################################################
  def search_repos (self, name, limit=100):
    url = self.server_url + '/repos/search'
    payload = {'q': name, 'limit' : limit}
    r = requests.get(url, headers=self.__hdrs, data=payload)
    return self.process_response(r)

  ################################################################################
  def create_your_repo (self, name, desc, private = False):
    url = self.server_url + '/user/repos'
    payload = {'name': name, 'description' : desc}
    if (private):
      payload['private'] = 'true'
    else:
      payload['private'] = 'false'
    r = requests.post(url, headers=self.__hdrs, data=payload)
    return self.process_response(r, 201)

  ################################################################################
  def create_organization_repo (self, org, name, desc, private = False):
    url = self.server_url + '/org/' + str(org) + '/repos'
    payload = {'name': name, 'description' : desc}
    if (private):
      payload['private'] = 'true'
    else:
      payload['private'] = 'false'
    r = requests.post(url, headers=self.__hdrs, data=payload)
    return self.process_response(r, 201)

  ################################################################################
  def delete_repository(self, owner, repo):
    url = self.server_url + '/repos/' + owner + '/' + repo
    r = requests.delete(url, headers=self.__hdrs)
    return self.process_response(r, 204)

  ################################################################################
  def create_user_repo (self, username, repos, desc, private = False):
    url = self.server_url + '/admin/users/' + username + '/repos'
    payload = {'name': name, 'description' : desc}
    if (private):
      payload['private'] = 'true'
    else:
      payload['private'] = 'false'
    r = requests.post(url, headers=self.__hdrs, data=payload)
    return self.process_response(r, 201)
