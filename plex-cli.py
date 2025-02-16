#!/usr/bin/env python3
# This script uses the plexapi pip package to interact with your plex server
# via the XML API. It can be used to refresh libraries, search libraries, list
# library contents, and more! Written by John R., Feb. 2025

import os
# Uncomment for root install w/ pip deps in venv.
#try:
#    os.environ["VIRTUAL_ENV"]
#except KeyError:
#    exit(" [!] Not in virtual env!\n" +
#         "Source the venv, then re-run this script.")

import json
import sys
import configparser
import argparse
from plexapi.server import PlexServer

CONF = './plex-cli.conf'

def main():
    process_args();
    url, token = read_conf();
    plex = PlexServer(url, token)

    libraries = get_libraries(plex)

    if ARGS.debug:
        print(libraries)

    # For --info
    if ARGS.info:
        if ARGS.json:
            print("Notice: --info doesn't support json output at this time!")
        print_library_info(libraries)

    if ARGS.list:
        print_library_list(libraries)

    if ARGS.search:
        search(libraries)

    if ARGS.sessions:
        if ARGS.json:
            print("Notice: --sessions doesn't support json output at this time!")
        sessions = plex.sessions()
        print_sessions(sessions)

    if ARGS.refresh:
        refresh_libraries(libraries)


def process_args():
    """
    Processes scripts optional arguments using argparse.
    """
    # Help dict.
    help_dict = {
        "disc"     : "A simple CLI script for interacting with your plex server",
        "info"     : "Get info on libraries",
        "json"     : "Get output in json format",
        "list"     : "List contents of specified library",
        "library"  : "Library to interact with (default: All)",
        "refresh"  : "Refresh specified libraries data",
        "search"   : "Search for media matching input",
        "title"    : "Search for media by title (default search)",
        "year"     : "Search for media by year",
        "genre"    : "Search for media by genre",
        "actor"    : "Search for media by actor",
        "sessions" : "List currently playing media sessions info",
        "verbose"  : "Verbose mode - Print additional output",
        "debug"    : "Debug mode - Print additional debug output"
    }
    
    # Libraries dict.
    global LIBRARY_MAP
    LIBRARY_MAP = {
        "doc_movies"   : "Documentary Movies",
        "doc_tv_shows" : "Documentary TV",
        "movies"       : "Movies",
        "tv_shows"     : "TV Shows",
        "web_series"   : "Web Series"
    }
    
    lib_choices = list(LIBRARY_MAP.keys())
    lib_choices.insert(0, 'all')
    
    # Handle Args.
    parser = argparse.ArgumentParser(description=help_dict["disc"])
    parser.add_argument('-i', '--info', action='store_true', help=help_dict["info"])
    parser.add_argument('-j', '--json', action='store_true', help=help_dict["json"])
    parser.add_argument('-l', '--list', action='store_true', help=help_dict["list"])
    parser.add_argument('-r', '--refresh', action='store_true', help=help_dict["refresh"])
    parser.add_argument('-m', '--library', nargs='+', type=str, choices=lib_choices, default='all', help=help_dict["library"])
    parser.add_argument('-s', '--search', type=str, help=help_dict["search"])
    parser.add_argument('-t', '--title', type=str, help=help_dict["title"])
    parser.add_argument('-y', '--year', type=int, help=help_dict["year"])
    parser.add_argument('-g', '--genre', type=str, help=help_dict["genre"])
    parser.add_argument('-a', '--actor', type=str, help=help_dict["actor"])
    parser.add_argument('-p', '--sessions', action='store_true', help=help_dict["sessions"])
    parser.add_argument('-v', '--verbose', action='store_true', help=help_dict["verbose"])
    parser.add_argument('-d', '--debug', action='store_true', help=help_dict["debug"])

    global ARGS
    ARGS = parser.parse_args()

    if ARGS.search \
        and not ARGS.title \
        and not ARGS.year  \
        and not ARGS.genre \
        and not ARGS.actor:
        ARGS.title = ARGS.search

    # Search flags, any imply --search mode.
    if ARGS.title or ARGS.year or ARGS.genre or ARGS.actor:
        if not ARGS.search:
            ARGS.search = True

    if len(sys.argv) == 1:
        print('Error: No arguments supplied!')
        parser.print_help()
        exit(1)


def read_conf():
    # Import config data.
    config = configparser.ConfigParser()
    check_for_file(CONF)
    config.read(CONF)

    plex_url = config['server']['server']
    plex_token = config['server']['token']

    return plex_url, plex_token


def check_for_file(filename):
    try:
        if os.stat(filename).st_size == 0:
            print(f"Empty file: {filename}")
            exit(3)
    except OSError:
        print(f"No file: {filename}")
        exit(4)
    return


def get_libraries(plex):
    """
    Returns a list of plexapi plexapi.library.ShowSection objects based on user
    supplied --library flag.

    Args:
        plex (plexapi.server.PlexServer): Plex server object to query.
    """
    # Get all libraries.
    if 'all' in ARGS.library:
        libraries = plex.library.sections()
        return libraries

    libraries = []
    for library in ARGS.library:
        library_full_name = LIBRARY_MAP[library]
        libraries.append(plex.library.section(library_full_name))

    return libraries


def print_library_info(libraries):
    """
    Outputs info about supplied plexapi library objects.

    Args:
        libraries (list): List of plexapi.library.ShowSection objects
    """
    print("Plex Libraries:")
    for library in libraries:
        print(f"- {library.title}")

    # Print details about each library.
    for library in libraries:
        print(f"\nLibrary: {library.title}")
        print(f" - Type: {library.type}")
        print(f" - UUID: {library.uuid}")

        if ARGS.verbose:
            print(f" - Agent: {library.agent}")
            print(f" - Scanner: {library.scanner}")
            print(f" - Location: {library.locations}")

        print(f" - Refreshing: {library.refreshing}")
        print(f" - Total Items: {library.totalSize}")    


def print_library_list(libraries):
    """
    Prints a list (in json or plain text) of all items in the supplied
    library.

    Args:
        libraries (list): List of plexapi.library.ShowSection objects
    """
    library_contents = dict()

    for library in libraries:
        if not ARGS.json:
            print(f"Library: {library.title}")

        items = library.all()
        library_items = []

        for item in items:
            item_info = dict()

            if ARGS.verbose:
                item_info['title'] = item.title
                item_info['year'] = item.year
                item_info['rating'] = item.rating
                item_info['duration'] = item.duration
                item_info['summary'] = item.summary

                if not ARGS.json:
                    print(f"Title: {item.title}")
                    print(f"Year: {item.year}")
                    print(f"Rating: {item.audienceRating}")
                    if item.duration:
                        runtime = item.duration // 60000  # Convert milliseconds to minutes
                    print(f"Runtime: {runtime} minutes")
                    print(f"Summary: {item.summary}")
                    print("-" * 40)

            else:
                item_info['title'] = item.title

                if not ARGS.json:
                    print(f" - {item.title}")

            library_items.append(item_info)

        library_contents[library.title] = library_items

        if ARGS.verbose and not ARGS.json:
            print(f"Total Items: {library.totalSize}")    

    if ARGS.json:
        libraries_json = json.dumps(library_contents)
        print(libraries_json)


def search(libraries):
    """
    Searches through supplied libraries for search string.

    Args:
        libraries (list): List of plexapi.library.ShowSection objects
    """
    search_string = ARGS.search

    for library in libraries:
        if not ARGS.json:
            print(f"Library: {library.title}")

        search_params = dict()
        if ARGS.title:
            search_params['title'] = ARGS.title
        if ARGS.year:
            search_params['year'] = ARGS.year
        if ARGS.genre:
            search_params['genre'] = ARGS.genre
        if ARGS.actor:
            search_params['actor'] = ARGS.actor

        results = library.search(**search_params)
        if results:
            print_search_results(results)
        else:
            print(f"No matching search results in {library.title}")


def print_search_results(results):
    """
    Prints results from searches.

    Args:
        results (list): List of search results.
    """
    search_result = []

    for item in results:
        result_item = dict()
        result_item['title'] = item.title

        if ARGS.verbose:
            result_item['year'] = item.year
            result_item['rating'] = item.rating
            result_item['duration'] = item.duration
            result_item['summary'] = item.summary

            if not ARGS.json:
                print(f" - Title: {item.title}")
                print(f" - Year: {item.year}")
                print(f" - Rating: {item.audienceRating}")
                if item.duration:
                    runtime = item.duration // 60000  # Convert milliseconds to minutes
                print(f" - Runtime: {runtime} minutes")
                print(f" - Summary: {item.summary}")
                print("-" * 40)

        else:
            if not ARGS.json:
                print(f" - {item.title}")

        search_result.append(result_item)

    if ARGS.json:
        results_json = json.dumps(search_result)
        print(results_json)


def print_sessions(sessions):
    """
    Prints list of currently playing plex sessions.
    """
    for session in sessions:
        print(f"User:        {session.usernames[0] if session.usernames else 'Unknown'}")
        print(f"Title:       {session.title}")

        # Check if it's a TV show (has season/episode info)
        if session.type == 'episode':
            print(f"Season:      {session.seasonNumber}")
            print(f"Episode:     {session.episodeNumber}")

        # Print directors, writers, and producers if available
        if session.directors:
            print(f"Director(s): {', '.join(director.tag for director in session.directors)}")
        if session.writers:
            print(f"Writer(s):   {', '.join(writer.tag for writer in session.writers)}")
        if session.producers:
            print(f"Producer(s): {', '.join(producer.tag for producer in session.producers)}")

        # Print summary if available
        if session.summary:
            print(f"Summary:     {session.summary}")

        if ARGS.verbose:
            # Print playback progress
            if session.viewOffset:  # viewOffset is in milliseconds
                progress_minutes = (session.viewOffset // 1000) // 60  # Convert to minutes
                total_minutes = (session.duration // 1000) // 60  # Convert to minutes
                print(f"Progress:    {progress_minutes} / {total_minutes} minutes")

            # Print media resolution
            if session.media:
                for media in session.media:
                    print(f"Resolution:  {media.videoResolution}")
                    print(f"Codec:       {media.videoCodec}")

        print("-" * 40)


def refresh_libraries(libraries):
    """
    Refreshes plex media libraries data

    Args:
        libraries (list): List of plexapi.library.ShowSection objects
    """
    for library in libraries:
        print(f"Refreshing '{library.title}' library...")
        library.refresh()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Exiting...')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

