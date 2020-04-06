import json
from reecho import Multimedia

class Lesson:
	def __init__(self, lesson):
		ldata = lesson['lesson']
		mediadata = lesson['medias'][0]

		self.name = ldata['displayName']
		self._id = ldata['id']
		self._inst_id = ldata['institutionId']
		self._medi_id = mediadata['id']
		self._available_for_download = mediadata['isAvailable'] 

		# cover image gives it all away
		# otherwise would be 0000.inst_id/medi_id/1/[...].m4s
		stemurl = "/".join(mediadata['coverImage'].split('/')[:-1]).replace('thumbnails', 'content')

		self._audio_uri = stemurl + "/s0q0.m4s"
		self._video_uri = stemurl + "/s1q1.m4s"

class HomeParse():
	def __init__(self, session, url, headers={}):
		self._session = session
		self._session.headers.update(headers)
		self._url = url
		self._headers=headers
		self._lessons = []
		self._choice = None

	def full_parse(self):
		content = self._get_syllabus()
		content = json.loads(content.text)
		self._make_lessons(content['data'])

	def select_lesson(self):
		print("\nAVAILABLE LESSONS: ")
		counter = 0
		for l in self._lessons:
			print(f"\t[{counter}] - '{l.name}'")
			counter += 1

		print(f"\nSelect a lesson [0-{counter - 1}]:")
		for i in range(10):
			try:
				inp = input()
				if inp == 'q':
					print("Quitting...")
				else:
					inp = int(inp)
					if inp >= counter:
						raise
			except:
				print("Bad input, try again.")
			else:
				break
		try:
			inp = int(inp)
		except:
			exit(1)
		else:
			self._choice = inp

	def download(self):
		Multimedia(self._session, self._headers, self._lessons[self._choice])()

	def _make_lessons(self, content):
		lessons = []
		for l in content:
			lessons.append(Lesson(l['lesson']))
		self._lessons = lessons

	def _get_syllabus(self):
		syllabus = self._url.replace('home', 'syllabus')
		return self._fetch(syllabus)

	def _fetch(self, url):
		return self._session.get(url)	