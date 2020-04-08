acturnips-watcher
===

A small script that polls /r/acturnips/new for posts advertising islands selling turnips above a certain price, and opens the first post which matches in a web browser.

## Wait, what is this??

In the hot video game [Animal Crossing: New Horizons][acnh], you are a participant in the "Deserted Island Getaway Package" and get to live on a deserted island with a tanuki named Tom Nook and his nephews Timmy and Tommy. Timmy and Tommy set up a shop where you can buy things with a currency called "Bells" and you can also sell stuff to them in exchange for Bells.

One of the more interesting things you can sell them are turnips. Turnips can only be bought on Saturday mornings for a fixed price, and then can be sold on another day of the week for a varying price. This sell price can vary in many different ways, and some lucky people have even seen cases where they can sell in excess of 6 times their buy price! Both the sell price and buy price are different on the islands of different players.

In the subreddit [/r/acturnips][acturnips], there are people allowing other players to visit their islands to buy or sell turnips at good prices and make a massive profit. However, as this is a hot video game, the queues fill up very fast and the process of visiting another island is terribly slow. This script waits for new posts, extracts the price they are advertising, and selectively opens the posts right away if they are above a prospective price. This lets you get into one of the first couple of groups and save a lot of waiting!

## Installation + Usage

You need Python 3.5+ and the `praw` package using `pip`:

    python3 -m pip install praw

Create an app in your [reddit app preferences][app_prefs] with the following details:

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

## Limitations

Currently, this script only allows watching for prices above a certain amount. It does not care if it is a buy or sell price. This means you can't use it to buy turnips below a certain price... yet.

Also, I wrote this script in about an hour, so posters will likely get around it to make sure players who don't use scripts like me can get in.

[acnh]: https://www.animal-crossing.com/new-horizons/
[acturnips]: https://www.reddit.com/r/acturnips/
[app_prefs]: https://www.reddit.com/prefs/apps/