import sys
import os
import difflib

# CHANGE YOUR MUSIC FOLDER AT FIRST LINE
# I set up an alias to make it even faster : 
# alias dl="ipython /path/to/python.py"
# 
# Use with :
# dl Artist / Title
# It sorts songs in folders in the music folder specified
#
# If the first result was not satisfying, you can try 
# dl *N Artist / Title
# N being the number of the Youtube result you want to try. Most of the time, the default (1) will be alright.

music_folder = "/home/dardelet/Music/"
music_command = "kde-open"
answers = ["", "y", "n", "yes", "no"]

def similar(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()

def cancel_last(filelist):
    ans = "empty"
    file_to_rm = filelist[-1]
    while ans.lower() not in answers:
        ans = raw_input("Confirm suppression of file {0} ? (Y/n)".format(file_to_rm.replace("\ ", " ")))
    if ans == "" or "y" in ans:
        print "Removing {0}".format(file_to_rm.replace("\ ", " "))
        os.system("rm "+file_to_rm)
        while file_to_rm[-1] != "/":
            file_to_rm = file_to_rm[:-1]
        if len(os.listdir(file_to_rm.replace("\ ", " "))) == 0:
            print "Removing empty directory {0}.".format(file_to_rm.replace("\ ", " "))
            os.rmdir(file_to_rm.replace("\ ", " "))
        print ""
        return filelist[:-1]
    else:
        print ""
        return filelist

def open_function(last_files):
    print last_files
    if len(last_files) == 0 :
        print "No file to open !"
        print ""
    else:
        os.system(music_command+" "+last_files[-1])
        print "Opening last downloaded song : {0}".format(last_files[-1].replace("\ ", " "))


last_files = []

while True:
    artist = ""
    title=""
    search = False
    cancel = False
    
    n_query = 1
    open_command = False

    raw = raw_input("New query : ")

    if "cancel" == raw.lower() or "revert" == raw.lower():
        if len(last_files) == 0 :
            print "No file to delete !"
            print ""
        else:
            last_files = cancel_last(last_files)
        cancel = True
    elif "open" == raw.split(" ")[0].strip():
        open_command = True
        raw = raw.split("open")[1].strip()
    if "," in raw.lower():
        args = raw.split(",")
        for arg in args:
            if "=" in arg:
                if "result" in arg.strip().split("=")[0]:
                    n_query = int(arg.strip().split("=")[1].strip())
                else:
                    print "Wrong parameter detected for argument {0}. Ignoring.".format(args.index(arg))
            else:
                if artist == "":
                    artist = arg.strip()
                else:
                    title = arg.strip()
        search = True      

        print ""
        print "Looking for " + artist + " singing "+ title +", result {0}.".format(n_query)
        print ""
        
        initial_string = "youtube-dl  --extract-audio --audio-format mp3 -o \""+music_folder+".tmp.mp3\" \"gvsearch{0}:".format(n_query)
        initial_string+=" "+artist
        initial_string+=" "+title
        
    else:
        print "No artist specified, looking for title only and placing it in \"Others\" folder"
        print "Looking for " + title +", result {0}.".format(n_query)
        title = raw
        artist = "Others"
        initial_string = "youtube-dl  --extract-audio --audio-format mp3 -o \""+music_folder+".tmp.mp3\" \"gvsearch{0}:".format(n_query)
        initial_string+=" "+title
    
        search = True      
    if search and not cancel:
        final_string = initial_string + "\""
        print "Final query string :"
        print final_string
        
        os.system(final_string)
        print ""
        print "Downloaded and put as hidden .tmp file"
        print ""
        
        folders = os.listdir(music_folder)
        folder = difflib.get_close_matches(artist, folders)
        
        
        if len(folder)==0:
            print "Artist related folder doesn't exist. Creating folder "+artist
            os.mkdir(music_folder+artist)
            print "Moving songfile to "+music_folder+artist
            os.system("mv "+music_folder+".tmp.mp3 "+music_folder+artist.replace(" ", "\ ")+"/"+title.replace(" ", "\ ")+".mp3")
            last_files += [music_folder+artist.replace(" ", "\ ")+"/"+title.replace(" ", "\ ")+".mp3"]
        else:
            print "Similarity found :"
            p = similar(folder[0], artist)
            print folder[0]
            print "compared to :"
            print artist
            if p<0.85:
                print "Artist related folder doesn't seem to exist ({0} related). Creating folder ".format(p)+artist
                os.mkdir(music_folder+artist)
                print "Moving songfile to "+music_folder+artist
                os.system("mv "+music_folder+".tmp.mp3 "+music_folder+artist.replace(" ", "\ ")+"/"+title.replace(" ", "\ ")+".mp3")
                last_files += [music_folder+artist.replace(" ", "\ ")+"/"+title.replace(" ", "\ ")+".mp3"]
            else:
                print "Artist related folder found ({0} related)".format(p)
                print "Moving songfile to "+music_folder+folder[0]
                os.system("mv "+music_folder+".tmp.mp3 "+music_folder+folder[0].replace(" ", "\ ")+"/"+title.replace(" ", "\ ")+".mp3")
                last_files += [music_folder+folder[0].replace(" ", "\ ")+"/"+title.replace(" ", "\ ")+".mp3"]
    if open_command:
        open_function(last_files)
