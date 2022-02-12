# Problem Set 4 - RSS Feed Filter


import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


# -----------------------------------------------------------------------

# ======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
# ======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
        #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
        #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret


# ======================
# Data structure design
# ======================

# Problem 1

class NewsStory():
    def __init__(self, guid, title, description, link, pubdate):

        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate


# ======================
# Triggers
# ======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError


# PHRASE TRIGGERS

# Problem 2

class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower()

    def get_phrase(self):
        return self.phrase

    def is_phrase_in(self,text):
        bool_val = False
        final_story = ""
        temp_story = text.lower()

        for punctuation in string.punctuation:
            temp_story = temp_story.replace(punctuation , " ")

        temp_story = temp_story.split(" ")
        while "" in temp_story:
            temp_story.remove("")

        index_word =[]
        checklist = self.get_phrase().split(" ")
        for x,check_word in enumerate(checklist):


            if check_word  in temp_story:
                index_word.append(temp_story.index(check_word))
                if len(index_word) == 1:
                    bool_val = True
                elif index_word[x-1] + 1 == index_word[x]:

                    bool_val = True

                else:
                    bool_val = False
                    break

            else:
                bool_val = False
                break

        return bool_val



# Problem 3
class TitleTrigger(PhraseTrigger,):
    def __init__(self, phrase,):
        self.phrase = phrase.lower()




    def evaluate(self, story):
        title_pass = False

        if self.is_phrase_in(story.get_title()) == True:
            title_pass = True
        else:
            title_pass = False



        return title_pass


# Problem 4
class DescriptionTrigger(PhraseTrigger,):
    def __init__(self, phrase,):
        self.phrase = phrase.lower()




    def evaluate(self, story):
        title_pass = False

        if self.is_phrase_in(story.get_description()) == True:
            title_pass = True
        else:
            title_pass = False



        return title_pass


# TIME TRIGGERS

# Problem 5
class TimeTrigger(Trigger):
    def __init__(self, stringtime):
        time_real = datetime.strptime(stringtime, '%d %b %Y %H:%M:%S')
        time_real = time_real.replace(tzinfo=pytz.timezone("EST"))
        self.time = time_real

class BeforeTrigger(TimeTrigger):
    def __init__(self, stringtime):
        time_real = datetime.strptime(stringtime, '%d %b %Y %H:%M:%S')
        time_real = time_real.replace(tzinfo=pytz.timezone("EST"))
        self.time = time_real
        info = self.time.tzinfo
        a='a'

    def get_time(self):
        return self.time

    def evaluate(self, story):
        if story.get_pubdate().tzinfo == None:
            story.get_pubdate = story.get_pubdate().replace(tzinfo = pytz.timezone("EST"))
        time_pass = False

        try:
            if self.time > story.get_pubdate():
                time_pass = True
            return time_pass
        except:
            if self.time > story.get_pubdate:
                time_pass = True
            return time_pass



class AfterTrigger(TimeTrigger):
    def __init__(self, stringtime):
        time_real = datetime.strptime(stringtime , '%d %b %Y %H:%M:%S')
        time_real=time_real.replace(tzinfo=pytz.timezone("EST"))
        self.time = time_real

    def get_time(self):
        return self.time

    def evaluate(self, story):
        try:
            if story.get_pubdate().tzinfo == None:
                story.get_pubdate = story.get_pubdate().replace(tzinfo=pytz.timezone("EST"))
        except:
            if story.get_pubdate.tzinfo == None:
                story.get_pubdate = story.get_pubdate().replace(tzinfo=pytz.timezone("EST"))
        time_pass = False
        try:
            if self.time < story.get_pubdate():
                time_pass = True
        except:
            if self.time < story.get_pubdate:
                time_pass = True

        return time_pass


# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):
    def __init__(self,trigger):
        self.trigger = trigger



    def evaluate(self, story):

        if self.trigger.evaluate(story) == False:
            not_pass = True
        if self.trigger.evaluate(story) == True:
            not_pass = False

        return not_pass



# Problem 8
class AndTrigger(Trigger):
    def __init__(self,trigger1,trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2



    def evaluate(self, story):
        not_pass = False

        if self.trigger1.evaluate(story) == True and self.trigger2.evaluate(story) == True:
            not_pass = True


        return not_pass

# Problem 9
class OrTrigger(Trigger):
    def __init__(self,trigger1,trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2



    def evaluate(self, story):
        not_pass = True

        if self.trigger1.evaluate(story) == False and self.trigger2.evaluate(story) == False:
            not_pass = False


        return not_pass


# ======================
# Filtering
# ======================

# Problem 10

def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    new_story = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story) == True:
                new_story.append(story)
    stories = new_story.copy()

    return stories


# ======================
# User-Specified Triggers
# ======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers


    trigger_names = {}

    for  trigger_info in lines:

        trigger_info = trigger_info.split(",")

        if trigger_info[0] == "ADD":
            for x in range(len(trigger_info) - 1):
                trigger_names[trigger_info[x+1]] = None

    for  trigger_info in lines:

        trigger_info = trigger_info.split(",")

        if trigger_info[1] == "DESCRIPTION":
            trigger_names[trigger_info[0]] = DescriptionTrigger(trigger_info[2])

        elif trigger_info[1] == "TITLE":
            trigger_names[trigger_info[0]] = TitleTrigger(trigger_info[2])

        elif trigger_info[1] == "AFTER":
            trigger_names[trigger_info[0]] = AfterTrigger(trigger_info[2])

        elif trigger_info[1] == "BEFORE":
            trigger_names[trigger_info[0]] = BeforeTrigger(trigger_info[2])

        elif trigger_info[1] == "NOT":
            trigger_names[trigger_info[0]] = NotTrigger(trigger_info[2])

        elif trigger_info[1] == "AND":
            trigger_names[trigger_info[0]] = AndTrigger(trigger_info[2], trigger_info[3])

        elif trigger_info[1] == "OR":
            trigger_names[trigger_info[0]] = OrTrigger(trigger_info[2], trigger_info[3])


    return trigger_names
    print(lines)  # for now, print it so you see what it contains!


SLEEPTIME = 120  # seconds -- how often we poll


def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("bitcoin")
        t2 = DescriptionTrigger("tax")
        t3 = DescriptionTrigger("Budget")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line
        #triggerlist = read_trigger_config('triggers.txt')

        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT, fill=Y)

        t = "Google Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica", 14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []

        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title() + "\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:
            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed


            #stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)

            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

