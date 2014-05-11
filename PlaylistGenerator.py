# Spotify Poem Generator :: Max Hield 5/6/14 #
# Take user input and pull song tracks from Spotify based on song title text groupings

import spotify
import threading
logged_in_event = threading.Event()
def connection_state_listener(session):
	if session.connection.state is spotify.ConnectionState.LOGGED_IN:
		logged_in_event.set()

session = spotify.Session()
loop = spotify.EventLoop(session)
loop.start()
session.on(
	spotify.SessionEvent.CONNECTION_STATE_UPDATED,
	connection_state_listener)

session.connection.state
session.login('mhield', 'retarded33')
session.connection.state
logged_in_event.wait()
session.connection.state
session.user

print "Let's make a playlist! Enter in a text message longer than 3 words (If you're feeling uninspired right now type 'exit')."


# Loop through responses and QC
	# assumptions:
		# trim duplicate spaces
		# input shouldn't be blank
		# input shouldn't be only numbers
		# input should contain at least 3 words

while True:
	text = raw_input("Speak your mind: ")
	text = " ".join(text.lower().split())

	if text == 'exit':
		print "Bye!"
		break
	elif text == "":
		print "This is blank!"
	elif text.replace(" ", "").isdigit() == True: 
		print "%s is all numbers!" % (text)		
	elif text.count(" ") < 2:
		print "Tell me how you really feel - %s isn't really long enough, it's only %s word(s) long" % (text, text.count(" ")+ 1)
	else:
		break

# create arbitrary text groupings of user input and search Spotify for exact match - if no match, remove word from grouping and search again

def SongParser(text):
	text = text.replace(",","").replace(".","") # get rid of certain punctation to increase matching efficiency
	allwords = text.split()
	i = 0
	y = 4 # set text grouping maximum
	match = 0 # if there are multiple matching song results, only pull one
	playlist = []
	while i < len(allwords):
		tracktest = "track:"+" ".join(allwords[i:y])
		search = session.search(tracktest, track_count = 100)	
		search.load()
		if tracktest == "track:": # results are empty
			break
		for x in range(0,len(search.tracks)): # now for every song result, see if we can find a match
			if search.tracks[x].load().name.lower().replace(",","") == " ".join(allwords[i:y]) and match <> 1:
				playlist.append(str(search.tracks[x].link.uri))
				match = 1
				break
		if match == 1: # found a match, move pointer to next set
			i = y
			y += 4					
		elif match == 0 and i < y and len(allwords[i:y]) > 1: # no match with this grouping -- take out last word and try again
			y = y - 1
		elif match == 0 and len(allwords[i:y]) == 1: # no match with this grouping and no more words to cut out -- move forward a word
			i += 1
			y += 4
			playlist.append("no match for " + tracktest.replace("track:",""))
		match = 0
	return playlist

playlist = SongParser(text)

def PrintLinks(playlist):
	for x in range(0,len(playlist)):
		if "no match" in playlist[x]:
			print playlist[x]
		else:
			print "http://open.spotify.com/track/" + playlist[x].replace("spotify:track:","")

PrintLinks(playlist)


## TODO
# import grammar python package that will more accurately split out user inputs into more logical results
# make sure same song isn't chosen twice if user input has the same two groups of sayings
# remove ? / ! from spotify track result names to improve matching
# check for 200 error
# check that song results are returned or else replace with exception text
# add MORE() if song isn't found in first pull
# figure out why search in the Spotify app itself will return exact search results and PlaylistGenerator search will not
