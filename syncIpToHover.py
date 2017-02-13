#!/usr/bin/python3.5

import requests
import re
import datetime
import os
from dotenv import load_dotenv, set_key

class HoverException(Exception):
	pass


class HoverAPI(object):
	def __init__(self, username, password):
		params = {"username": username, "password": password}
		r = requests.post("https://www.hover.com/api/login", params=params)
		if not r.ok or "hoverauth" not in r.cookies:
			raise HoverException(r)
		self.cookies = {"hoverauth": r.cookies["hoverauth"]}

	def call(self, method, resource, data=None):
		url = "https://www.hover.com/api/{0}".format(resource)
		r = requests.request(method, url, data=data, cookies=self.cookies)
		if not r.ok:
			raise HoverException(r)
		if r.content:
			body = r.json()
			if "succeeded" not in body or body["succeeded"] is not True:
				raise HoverException(body)
			return body

	def current_home(self, dom_id):
		rrs = self.call("get", "domains/dom%s/dns" % dom_id)
		for rr in rrs['domains'][0]['entries']:
			if rr['name'] == os.environ.get("HOVER_HOST") and rr['type'] == 'A':
				return rr

	def current_home_ip(self, dom_id):
		rr = self.current_home(dom_id)
		return rr['content']

	def update_home_ip(self, dom_id, new_ip):
		rr = self.current_home(dom_id)
		self.call("put", "dns/%s" % rr['id'], {"content": new_ip})

def current_ip():

	r = requests.get('http://whatismyip.org/')
	ip = re.search('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', r.text)
	if re:
		return ip.group(1)
	else:
		return null

env_file = '/etc/syncIpToHover/.env'
load_dotenv(env_file)

print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), end=" :: ")

currentIp = current_ip()
print("Current IP: %s, " % currentIp, end="")

cacheIp = os.environ.get("CURRENT_GATEWAY_IP")
print("Cache IP: %s, " % cacheIp, end="")
if currentIp != cacheIp:
	set_key(env_file, 'CURRENT_GATEWAY_IP', currentIp)
	print("Cache Updated!, ", end="")
	# Maybe update Hover
	client = HoverAPI(os.environ.get("HOVER_USERNAME"), os.environ.get("HOVER_PASSWORD"))
	hoverIp = client.current_home_ip(os.environ.get("HOVER_DOMAIN_ID"))
	print("Hover IP: %s" % hoverIp, end="")
	if currentIp != hoverIp:
		client.update_home_ip(os.environ.get("HOVER_DOMAIN_ID"), currentIp)
		print(" -->  Hover Updated", end="")
	else:
		print("Ok", end="")

print()
