import os, hashlib, sys
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4

source = '/Users/XeTK/Music/'
destination = '/Users/XeTK/Desktop/'

class Artist:
	name = ""
	albums = []

class Album:
	name = ""
	songs = []

class Song:
	title = ""
	fpath = ""

class id3entry:
	artist = ""
	album = ""
	song = ""
	fpath = ""
	ftype = ""
	bitrate = None
	length = None

artist_list = []
usf = []
ef = []

def md5_Hash(filepath):
	fh = open(filepath, 'rb')
	m = hashlib.md5()
	while True:
		data = fh.read(8192)
		if not data:
			break
		m.update(data)
	return m.hexdigest()

def find_Artist(artist):
	for index in artist_list:
		if index.name == artist:
			return index
	return None

def find_Album(obj_art,album):
	for index in obj_art.albums:
		if index.name == album:
			return index
	return None

def find_Song(obj_album,song):
	for index in obj_album.songs:
		if index.title == song:
			return index
	return None

def add_Song(id3entry):

	artist = find_Artist(id3entry.artist)

	if artist == None:
		new_art = Artist()
		new_art.name = id3entry.artist
		artist_list.append(new_art)
		artist = new_art
	#	print "Adding new Artist:", new_art.name
	#else:
	#	print "Found Artist:", artist.name
	
	album = find_Album(artist,id3entry.album)

	if album == None:
		new_alb = Album()
		new_alb.name = id3entry.album
		artist.albums.append(new_alb)
		album = new_alb
	#	print "Adding new Album:", new_alb.name
	#else:
	#	print "Found Album:", album.name

	song = find_Song(album,id3entry.song)

	if song == None:
		new_song = Song()
		new_song.title = id3entry.song
		new_song.fpath = id3entry.fpath
		album.songs.append(new_song)
		song = new_song
	else:
		if not md5_Hash(song.fpath) == md5_Hash(id3entry.fpath):
			tid = info(song.fpath) 
			if tid.ftype == "FLAC":
				if id3entry.ftype == "FLAC":
					if id3entry.length > tid.length:
						song.fpath = id3entry.fpath
				else:
					print "FLAC IS BETTER THROWING AWAY OTHER FORMAT", id3entry.fpath
			elif tid.ftype == "MP3":
				if id3entry.ftype == "MP3":
					if id3entry.bitrate > tid.bitrate:
						song.fpath = id3entry.fpath
						print "Better BitRate", id3entry.fpath
					elif id3entry.bitrate == tid.bitrate:
						if id3entry.length > tid.length:
							song.fpath = id3entry.fpath
						else:
							print "Stale Mate...",song.fpath,id3entry.fpath
				elif id3entry.ftype == "FLAC":
					print "Flac is better", id3entry.fpath
					song.fpath = id3entry.fpath
				else:
					print "Throwing away less superia format",id3entry.fpath

			elif tid.ftype == "M4A":
				if id3entry.ftype == "MP3" or id3entry.ftype == "FLAC":
					print "Format  is better", id3entry.fpath
					song.fpath = id3entry.fpath
				elif id3entry.ftype == "M4A":
					if id3entry.bitrate > tid.bitrate:
						song.fprint = id3entry.fpath
						print "Better BitRate", id3.entry.fpath
					elif id3entry.bitrate == tid.bitrate:
						if id3entry.length > tid.length:
							song.fpath = id3entry.fpath
						else:
							print "Stale Mate...",song.fpath,id3entry.fpath

				else:
					print "Throwing away less superia format",id3entry.fpath

		
	return None

def mp3_info(filepath):
	newid3 = id3entry()
	tMP3 = MP3(filepath)
	newid3.artist = tMP3["TPE1"]
	newid3.album = tMP3["TALB"]
	newid3.song = tMP3["TIT2"]
	newid3.fpath = filepath
	newid3.ftype = "MP3"
	newid3.bitrate = tMP3.info.bitrate
	newid3.length = tMP3.info.length
	return newid3
	
def flac_info(filepath):
	newid3 = id3entry()
	tFLAC = FLAC(filepath)
	newid3.artist = tFLAC["artist"][0]
	newid3.album = tFLAC["album"][0]
	newid3.song = tFLAC["title"][0]
	newid3.fpath = filepath
	newid3.ftype = "FLAC"
	#newid3.bitrate = tFLAC.info.bitrate
	newid3.length = tFLAC.info.length

	return newid3

def m4a_info(filepath):
	newid3 = id3entry()
	tM4A = MP4(filepath)
	newid3.artist = tM4A["artist"][0]
	newid3.album = tM4A["album"][0]
	newid3.song = tM4A["title"][0]
	newid3.fpath = filepath
	newid3.ftype = "M4A"
	newid3.bitrate = tM4A.info.bitrate
	newid3.length = tM4A.info.length

	return newid3

def info(filepath):
	id3file = None
	if curfile.endswith('.mp3') or curfile.endswith('.MP3'):
		id3file = mp3_info(filepath)
	elif curfile.endswith('.flac') or curfile.endswith('.FLAC'):
		id3file = flac_info(filepath)
	elif curfile.endswith('.wav') or curfile.endswith('.WAV'):
		#print ".Wav found"
		usf.append(curfile)
	elif curfile.endswith('.wma') or curfile.endswith('.WMA'):
		#print ".WMA found"
		usf.append(curfile)
	elif curfile.endswith('.aac') or curfile.endswith('.AAC') or curfile.endswith('.m4p') or curfile.endswith('.M4P'):
		#print ".AAC found"
		usf.append(curfile)
	elif curfile.endswith('.m4a') or curfile.endswith('.M4A'):
		id3file = m4a_info(filepath)
	return id3file

for dirname,dirnames,filenames in os.walk(source):
	for filename in filenames:
		curfile = os.path.join(dirname, filename)
		try:
#		if 1:
			id3file = info(curfile)
		
			if not id3file == None:
				#print id3file.artist, id3file.album, id3file.song 
				add_Song(id3file)
		except:
			ef.append(curfile)
			print "Unexpected error:", sys.exc_info()[0]


