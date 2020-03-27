from reecho import Multimedia
from reecho import HomeParse
import requests
import argparse
import json

#Multimedia._merge('.tmp/s0q0.m4s', '.tmp/s1q1.m4s', "SPCE0005 20/03/2020")

#exit(0)

parser = argparse.ArgumentParser(description='Download lecture streams from echo360. Only tested on UCL Moodle so far.')
parser.add_argument('curl_file', type=str, nargs=1, help="Curl requests from the echo360 home.")

args = parser.parse_args()
file = args.curl_file[0]

try:
	Multimedia.clean()
except FileNotFoundError:
	pass

class ExtendAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        items = getattr(namespace, self.dest) or []
        items.extend(values)
        setattr(namespace, self.dest, items)

# read in curl contents
with open(file, 'r') as f:
    contents = f.read().split("\n")[0]

contents = contents.split('-H')
home_url = contents[0].split(' ')[1].replace('\'', '')
print(f"Using HOME url: '{home_url}'")

headers = ""
for i in contents[1:]:
    i = i.replace('--compressed', '')
    i = i.replace('\'', '"').replace(': ', '":"')
    headers += i.strip() + ", "
headers = headers.strip()[:-1]
headers = json.loads("{" + headers + "}")

for k in headers:
    print(f"HEADER loaded: {k}")

# setup requests sesssion
session = requests.Session()
adapter = requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=10, max_retries=10)
session.mount('https://', adapter)
session.mount('http://', adapter)

hp = HomeParse(session, home_url, headers)
hp.full_parse()
hp.select_lesson()
hp.download()