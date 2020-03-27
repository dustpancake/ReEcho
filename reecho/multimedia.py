import subprocess
import shutil
import os

class Multimedia:
	def __init__(self, session, headers, lesson):
		self._session = session
		self._headers = headers
		self._lesson = lesson

	def fetch(self, url):
		fname = os.path.join('.tmp', url.split('/')[-1])
		with self._session.get(url, stream=True) as r:
			r.raise_for_status()
			number = 0
			with open(fname, 'wb') as f:
				for chunk in r.iter_content(chunk_size=8192):
					number += 1
					print(f"\tDownloading chunk {number} ... ", end='\r')
					if chunk:
						f.write(chunk)
			print(f"\tDownloading chunk {number} ... ")
		return fname

	@staticmethod
	def _merge(audio, video, name):
		cmd = ["ffmpeg", "-i", f"{audio}", "-i", f"{video}", "-c", "copy", "-map", "0:a:0", "-map", "1:v:0", "-shortest", f"{name.replace(' ', '_').replace('/', '-')}.mp4"]
		subprocess.run(cmd, check=True)

	def _download_streams(self):
		print("Fetching audio stream:")
		audio = self.fetch(self._lesson._audio_uri)
		print("Fetching video stream:")
		video = self.fetch(self._lesson._video_uri)
		return audio, video

	@staticmethod
	def _make_env():
		try:
			os.mkdir('.tmp')
		except Exception as e:
			print("Unable to make download directory './.tmp'")
			print(e)
			exit(1)
	
	@staticmethod
	def clean():
		shutil.rmtree('.tmp')
	
	def __call__(self):
		self._make_env()
		audio, video = self._download_streams()
		self._merge(audio, video, self._lesson.name)
		self.clean()
		print("\nDownload and muxing complete.")