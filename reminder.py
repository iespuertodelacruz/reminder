"""
Reminder lets you change the badge on the header of website.

Usage:
	reminder.py set <url> 
	reminder.py remove
"""
from docopt import docopt
import config
import glob
import os
import datetime


def set_badge(url):
	filename = "badge_" + datetime.datetime.now().strftime("%s") + ".png"
	path = os.path.join(config.BADGES_PATH, filename)
	os.system("curl --silent -o {} {}".format(path, url))
	os.system("mogrify -resize x300 {}".format(path))
	os.system('sed -i -E "s/badge_[0-9]+\.png/{}/" {}'.format(filename, config.HEADER_PATH))


def clean_badges():
	path = os.path.join(config.BADGES_PATH, "badge*")
	for f in glob.glob(path):
		os.remove(f)


def remove_badges():
	clean_badges()
	set_badge(config.TRANSPARENT_BADGE_URL)


if __name__ == "__main__":
    arguments = docopt(__doc__)
    if arguments["set"]:
        set_badge(arguments["<url>"])
    elif arguments["remove"]:
        remove_badges()
