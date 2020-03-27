# ReEcho: an echo360 lecture downloader

![sample-output](https://github.com/Dustpancake/ReEcho/blob/master/header.png)

### Features:

- Lesson selector for a given course
- Fast and high quality download
- Audio and video muxing
- Creates a `.mp4` file of your lecture

### Setting up the environment
This program requires command line `ffmpeg` and `python3.7+`. Tested on OSX and Linux. I have **strong doubts** it would work on Windows in its current form.

For installing `ffmpeg`, see [this link](https://ffmpeg.org/download.html). On OSX, you can use brew if you have it:
```
brew install ffmpeg
```
To set up the python environment, I recommend using a virtual environment:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage
To use the program, you need to provide a 'curlfile', i.e. a file containing the relevant curl command to access the home page of your lecture course.

The easiest way to obtain this is to login and visit the `home` of echo360 for your course. Open the Network tab of the developer tools, and refresh the page. The top entry should read something like 
```
Status	Method	Domain				File 		Cause
----------------------------------------------------------------------	
200		GET		echo360.org.uk 		home 		document	...
...
```
Right click on this, and under `Copy` select `Copy as cURL`. Paste this into a file, name it whatever you like, and then execute the downloader using
```
python . ./[path_to_curl_file]
```

The downloader script will use the cookie headers to automatically login as your user account, and display your courses.

## Notes
This has only been tested on the **one** course I have access to, which as of date of writing only has **one** lesson upload. I've tried my best to anticipate the generalization of the code, but there be errors since I had a very limited range of tests available. Please contact me with logs so I can patch them.

Thanks and enjoy :)