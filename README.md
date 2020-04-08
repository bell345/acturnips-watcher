acturnips-watcher
===

A small script that polls /r/acturnips/new for posts advertising islands selling turnips above a certain price, and opens the first post which matches in a web browser.

## Installation + Usage

You need Python 3.5+ and the `praw` package using `pip`:

    python3 -m pip install praw

Create an app in your [app_preferences](reddit app preferences) with the following details:

- Name: acturnips-watcher
- Type: script
- Description: Watches /r/acturnips/new for new turnips posts
- About URL: https://github.com/bell345/acturnips-watcher
- Redirect URI: https://example.com/n/a

You will get a client ID, which is under the words "personal use script", and a client secret, which has the label "secret". Put these two parameters in the `praw.ini` in place of the placeholders.

To run the script, run the `watcher.py` file as a module:

    python3 -m watcher [options] <price>

## Command-line Options

- `price`: This is your minimum price in bells to search for. Posts below this price are ignored.

- `-c`, `--continuous`: Keep looking for posts, even after one has been found.

- `-d <DELAY>`, `--delay=DELAY`: Wait for `DELAY` seconds in between polls of the subreddit. Due to API limitations, this cannot be set below 1.

- `-n`, `--no-browser`: Do not open any links in a web browser.