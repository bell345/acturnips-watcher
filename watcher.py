import re
import logging
import argparse
import webbrowser
from datetime import datetime
from typing import Optional, List
from time import sleep
from collections import OrderedDict

try:
    import winsound
except ImportError:
    winsound = None

import praw
from praw.models import Subreddit, Submission

logging.basicConfig(
    style='{', format='{asctime} {message}',
    datefmt='%H:%M:%S',
    level=logging.INFO)
logger = logging.getLogger(__name__)

APP_NAME = "acturnips-watcher"
APP_VERSION = "0.3.0"
APP_AUTHOR = "Thomas Bell"

SUBREDDIT = "acturnips"
URL_REGEX = re.compile(r'((https?://)?[a-z][a-z0-9]+\.[a-z][a-z0-9]+/[^ ]+)')

LOADING_PARTS = [
    'Now loading' + 
    '.'*i + ' '*(10-i) for i in range(10)]
_loading_index = 0
def now_loading():
    global _loading_index
    print(LOADING_PARTS[_loading_index], end='\r')
    _loading_index += 1
    if _loading_index >= len(LOADING_PARTS):
        _loading_index = 0

def find_integer(title: str) -> Optional[int]:
    """Returns first (positive) integer in `title`.

    Aside from digits 0-9, can also translate words into digits
    and compose them into integers.

    :return: First integer found. If no integer found, returns None.
    """
    REPLACEMENTS = OrderedDict({
        " and ": " ",
        "and": "",
        "-": " ",
        ",": "",
        "oh": 0,
        "tee": 0,
        "one hundred": 100,
        "one": 1,
        "ten": 10,
        "two hundred": 200,
        "two": 2,
        "twenty": 20,
        "three hundred": 300,
        "three": 3,
        "thirty": 30,
        "four hundred": 400,
        "four": 4,
        "forty": 40,
        "five hundred": 500,
        "five": 5,
        "fifty": 50,
        "six hundred": 600,
        "six": 6,
        "sixty": 60,
        "seven": 7,
        "seventy": 70,
        "eight": 8,
        "eighty": 80,
        "nine": 9,
        "ninety": 90,
        "zero": 0,
        "hundred": 100
    })

    title = title.lower()
    for word, repl in REPLACEMENTS.items():
        title = title.replace(word, str(repl))
    
    together = title.replace(' ', '')

    match = re.search(r'([0-9]+)', together)
    if match is not None:
        return int(match.group(1))
    else:
        return None


def find_links(text: str) -> List[str]:
    """Returns all URLs embedded in the given `text`."""
    links = []

    match = URL_REGEX.search(text.lower())
    while match:
        url = match.group(1)
        if 'http' not in url:
            url = f'http://{url}'
        links.append(url)
        match = URL_REGEX.search(text.lower(), match.end)
    
    return links


def watch_new(subreddit: Subreddit, price: int, delay=2.0) -> Submission:
    """Watches `subreddit` for prices at least `price` and returns the next uploaded post.

    First, makes a note of the newest posts on the subreddit. Then, polling in
    intervals of `delay`, will find new posts that weren't there on the first
    pass, and returns the first one that has an integer not less than `price`.

    This may run forever if no results appear, so be careful.

    :param subreddit: A Subreddit instance returned by praw.Reddit.subreddit.
    :param price: A positive integer used as a lower-bound filter.
    :param delay: Number of seconds in between polls. Defaults to 2.0.
    :return: Returns first submission with an integer not less than the
        given `price`.
    """

    old_posts = [p.id for p in subreddit.new(limit=10)]
    logger.debug(f'Made a record of {", ".join(old_posts)}')

    last_time = datetime.now()
    while True:
        for post in subreddit.new(limit=5):
            if post.id not in old_posts:
                n = find_integer(post.title)
                logger.info(f'[{post.id}, {n}] {post.title}')
                if n and n >= price:
                    return post

                old_posts.append(post.id)

        now_loading()

        passed = (datetime.now() - last_time).total_seconds()
        if passed < delay:
            sleep(delay - passed)
        last_time = datetime.now()


def main():
    parser = argparse.ArgumentParser(prog=APP_NAME,
        description="Watches the acturnips subreddit for new posts.")
    parser.add_argument('-v', '--verbose', action='store_true',
        help="Displays more log information.")
    
    parser.add_argument('price', type=int,
        help="Minimum sell price in bells to look out for.")
    parser.add_argument('-c', '--continuous', action='store_true',
        help="If supplied, will keep looking for new posts even after one is found.")
    parser.add_argument('-d', '--delay', type=float, default=2.0,
        help="Delay in seconds between each poll. Cannot be set to less than 1.")
    parser.add_argument('-n', '--no-browser', action='store_true',
        help="If supplied, won't open any links in browser.")
    
    args = parser.parse_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    if args.delay < 1.0:
        raise ValueError(f'Delay is set too low ({args.delay}); must not be less than 1')

    reddit = praw.Reddit(
        APP_NAME,
        user_agent=f'script:{APP_NAME}:{APP_VERSION} (by /u/isurvived12)'
    )

    subreddit = reddit.subreddit(SUBREDDIT)
    while True:
        post = watch_new(subreddit, args.price, args.delay)
        links = find_links(post.selftext)

        if winsound:
            winsound.MessageBeep(winsound.MB_ICONHAND)

        logger.info(f'Found post: {post}')
        logger.info(post.selftext)
        logger.info('')

        logger.info(f'Post URL: {post.url}')
        if not args.no_browser:
            webbrowser.open_new_tab(post.url)

        logger.info(f'Links: {len(links)}')
        for link in links:
            logger.info(link)
            if not args.no_browser:
                webbrowser.open_new_tab(link)

        logger.info('')

        if not args.continuous:
            break


if __name__ == "__main__":
    main()
