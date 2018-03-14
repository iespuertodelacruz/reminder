"""
Reminder lets you change the badge on the header of website.

Usage:
	reminder.py set <url> [--target=<url>] [--size=<px>] [--left=<px>] [--top=<px>] [--verbose]
	reminder.py remove

Options:
    --target=<url>    Target URL of the badget.
    --size=<px>       Height size of the badget [default: 300].
    --left=<px>       Relative left position of the badget [default: 150].
    --top=<px>        Relative top position of the badget [default: 0].
	--verbose         Verbose mode.
"""
from docopt import docopt
import config
import glob
import os
import datetime


def set_badge(url, target, size, left, top, verbose=False):
	filename = "badge_" + datetime.datetime.now().strftime("%s") + ".png"
	path = os.path.join(config.BADGES_PATH, filename)
	os.system("curl --silent -o {} {}".format(path, url))
	os.system("mogrify -resize x{} {}".format(size, path))
	os.system('sed -i -E "s/badge_[0-9]+\.png/{}/" {}'.format(filename, config.HEADER_PATH))
	if target is None:
		target = ""
	else:
		target = target.replace("/", "\/")
	os.system("""sed -i -E 's/id="badge_target" href="\S*">/id="badge_target" href="{}">/' {}""".format(target, config.HEADER_PATH))
	os.system('sed -i -E "s/left: -?[0-9]+px; \/\*badge_left/left: {}px; \/\*badge_left/" {}'.format(left, config.HEADER_PATH))
	os.system('sed -i -E "s/top: -?[0-9]+px; \/\*badge_top/top: {}px; \/\*badge_top/" {}'.format(top, config.HEADER_PATH))
	if verbose:
		print("\nURL: {}".format(url))
		print("Target: {}".format(target))
		print("Size: {}px".format(size))
		print("Left: {}px".format(left))
		print("Top: {}px".format(top))


def clean_badges():
	path = os.path.join(config.BADGES_PATH, "badge*")
	for f in glob.glob(path):
		os.remove(f)


def remove_badges():
	clean_badges()
	set_badge(config.TRANSPARENT_BADGE_URL, None, 1, 0, 0)


if __name__ == "__main__":
	arguments = docopt(__doc__)
	if arguments["set"]:
		set_badge(
			arguments["<url>"],
			arguments["--target"],
			arguments["--size"],
			arguments["--left"],
			arguments["--top"],
			arguments["--verbose"]
		)
	elif arguments["remove"]:
		remove_badges()
