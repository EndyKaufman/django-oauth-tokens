# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
from oauth_tokens.base import BaseAccessToken
import re

class VkontakteAccessToken(BaseAccessToken):

    provider = 'vkontakte'
    authenticate_url = 'https://api.vkontakte.ru/oauth/authorize'
    access_token_url = 'https://api.vkontakte.ru/oauth/access_token'
    response_decoder = None

    def parse_auth_form(self, page_content):
        '''
        Parse page with auth form and return tuple with (method, form action, form submit parameters)
        '''
        content = BeautifulSoup(page_content)

        form = content.find('form')
        if not form:
            raise Exception('There is no any form in response')

        data = {}
        for input in form.findAll('input'):
            data[input['name']] = input.get('value')

        data['email'] = self.username
        data['pass'] = self.password

        return (form.get('method').lower(), form.get('action'), data)

    def parse_permissions_form(self, page_content):
        '''
        Parse page with permissions form and return tuple with (method, form action, form submit parameters)
        '''
        matches = re.findall('function approve\(\) {\s+location.href = "([^"]+)";', page_content)
        if len(matches) != 1:
            raise Exception('Error while parsing permissions page contents')

        return ('get', matches[0], {})