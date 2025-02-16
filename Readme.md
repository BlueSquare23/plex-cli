<h1 align="center">Unofficial Plex Server CLI Script</h1>

<h3 align="center"> 🎥  A simple CLI interface for interacting with your Plex server! 🎬 </h3>

</p>

<p align="center">
  <a href="./license.txt">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg">
  </a>
  <a href="https://github.com/BlueSquare23/plex-cli/stargazers">
    <img src="https://img.shields.io/github/stars/BlueSquare23/plex-cli">
  </a>
  <a href="https://github.com/BlueSquare23/plex-cli/network">
    <img src="https://img.shields.io/github/forks/BlueSquare23/plex-cli">
  </a>
</p>

![-----------------------------------------------------](https://johnlradford.io/static/img/bar.gif)

## :dizzy: Overview

The `plex-cli.py` is a python wrapper script for interacting with your Plex
Server's API via the CLI. It uses the
[plexapi](https://github.com/pkkid/python-plexapi) pip module to get info about
libraries, search libraries, list current library contents, refresh library
data, and more! 

![-----------------------------------------------------](https://johnlradford.io/static/img/bar.gif)

## :point_down: Install & Setup

First clone this repo:

```
git clone https://github.com/BlueSquare23/plex-cli.git
```

Then install the pip requirements:

```
pip install -r requirements.txt
```

Finally setup your `plex-cli.conf` file:

* Example:

```
[server]
server = YOUR_PLEX_SERVER_URL
token = YOUR_TOKEN_HERE
```

:round_pushpin: <span style="color: orange;">Note:</span> You may need to edit
the hardcoded `CONF` var path in the actual `plex-cli.py` if you plan on moving
these files elsewhere on your system.

![-----------------------------------------------------](https://johnlradford.io/static/img/bar.gif)

## :grey_question: Usage

```
usage: plex-cli.py [-h] [-i] [-j] [-l] [-r] [-m {all,doc_movies,doc_tv_shows,movies,tv_shows,web_series} [{all,doc_movies,doc_tv_shows,movies,tv_shows,web_series} ...]] [-s SEARCH] [-t TITLE] [-y YEAR]
                   [-g GENRE] [-a ACTOR] [-p] [-v] [-d]

A simple CLI script for interacting with your plex server

options:
  -h, --help            show this help message and exit
  -i, --info            Get info on libraries
  -j, --json            Get output in json format
  -l, --list            List contents of specified library
  -r, --refresh         Refresh specified libraries data
  -m {all,doc_movies,doc_tv_shows,movies,tv_shows,web_series} [{all,doc_movies,doc_tv_shows,movies,tv_shows,web_series} ...], --library {all,doc_movies,doc_tv_shows,movies,tv_shows,web_series} [{all,doc_movies,doc_tv_shows,movies,tv_shows,web_series} ...]
                        Library to interact with (default: All)
  -s SEARCH, --search SEARCH
                        Search for media matching input
  -t TITLE, --title TITLE
                        Search for media by title (default search)
  -y YEAR, --year YEAR  Search for media by year
  -g GENRE, --genre GENRE
                        Search for media by genre
  -a ACTOR, --actor ACTOR
                        Search for media by actor
  -p, --sessions        List currently playing media sessions info
  -v, --verbose         Verbose mode - Print additional output
  -d, --debug           Debug mode - Print additional debug output
```

![-----------------------------------------------------](https://johnlradford.io/static/img/bar.gif)

## :beginner: Examples

* **List Libraries Info**

```
plex-cli.py --info
```

* **Refresh Documentary TV Shows Library**

```
plex-cli.py --refresh --library doc_tv_shows
```

* **List Current Sessions**

```
plex-cli.py --sessions --verbose
```

* **List All Movies Verbose**

```
plex-cli.py --list --library movies -v
```

* **List All TV Show w/ JSON Output**

```
plex-cli.py --list --library tv_shows -v --json
```

* **Search for Movie by Actor and Year**

```
plex-cli.py --year 1970 --actor "Charlton Heston" --library movies -v
```

![-----------------------------------------------------](https://johnlradford.io/static/img/bar.gif)

## :closed_lock_with_key: Additional Auth Scripts

If you'd like to ensure that the plex api auth key in your `plex-cli.conf`
stays up to date you can use the scripts linked below. Not written by me, but
they should do the needful. Just be aware he calls the conf `plex_config.ini`,
but yeah same file as what I call `plex-cli.conf`.

[Plex Auth Token Rotate Scripts](https://gitlab.com/media-scripts/apps/-/tree/master/plex/p3)

Maybe some day I'll rip those off tweak em a bit and include them in this repo.

![-----------------------------------------------------](https://johnlradford.io/static/img/bar.gif)

## :free: License MIT

[MIT License Text](license.txt)

![-----------------------------------------------------](https://johnlradford.io/static/img/bar.gif)

## :writing_hand: Author

[John L. Radford](https://johnlradford.io/)

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/bluesquare23)
