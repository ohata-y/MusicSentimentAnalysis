from lyricsgenius import Genius
import pandas as pd
import os
from numpy import nan
import re
from difflib import SequenceMatcher
from multiprocessing import Pool
from typing import Pattern
from pandas import DataFrame
from time import time


genius = Genius(access_token=os.environ["GeniusAPIClientAccessToken"], 
                verbose=False, 
                remove_section_headers=True, 
                retries=2)


def parentheses_separator(s: str, include_original: bool) -> list[str]:
    """
    Separate a string by parentheses and return a list of separeted strings.\\
    If include_original is True, s itself is also included to the list.\\
    If s does not include any parenthesis, only s is returned.
    """
    left = s.find("(")
    right = s.find(")")
    if left != -1 and right != -1:
        if left == 0:
            if include_original:
                return [s, s[1:right], s[right+2:]]
            else:
                return [s[1:right], s[right+2:]]
        elif right == len(s) - 1:
            if include_original:
                return [s, s[:left-1], s[left+1:right]]
            else:
                return [s[:left-1], s[left+1:right]]
    return [s]


def is_in_list(l: list[str], x: str) -> bool:
    """
    Return True when x is in l. Otherwise, return False.
    """
    if x in l:
        return True
    else:
        return False


def lyric_modification(lyric: str, pattern: Pattern) -> str:
    """
    Replace "\\n" with "|" in a lyric.\\
    re.compile("\\n+") should be passed to pattern.
    """
    modified_lyric = pattern.sub("|", lyric)
    return modified_lyric


def artist_modification(artist: str) -> list[str]:
    """
    Return a list of modified artist names.
    """
    featuring_idx = artist.find(" featuring ")
    if featuring_idx != -1:
        artist = artist[:featuring_idx]
    
    artists_exception = ["Earth, Wind & Fire & The Emotions", 
                          "Grover Washington, Jr. & Bill Withers", 
                          "Dionne and Friends (Dionne Warwick, Gladys Knight, Elton John and Stevie Wonder)", 
                          "Delaney & Bonnie & Friends", 
                          "Nelly, Paul Wall and Ali & Gipp", 
                          "Skrillex and Diplo (Jack Ü)", 
                          "The Scotts (Travis Scott and Kid Cudi)", 
                          "Silk Sonic (Bruno Mars and Anderson .Paak)", 
                          "The Anxiety: Willow and Tyler Cole"]
    
    modified_artists_exception = [["Earth, Wind & Fire", "The Emotions"], 
                                  ["Grover Washington, Jr.", "Bill Withers"], 
                                  ["Dionne Warwick", "Gladys Knight", "Elton John", "Stevie Wonder"], 
                                  ["Delaney & Bonnie"], 
                                  ["Nelly", "Paul Wall", "Ali & Gipp"], 
                                  ["Skrillex and Diplo", "Skrillex", "Diplo"], 
                                  ["The Scotts", "Travis Scott", "Kid Cudi"], 
                                  ["Silk Sonic", "Bruno Mars"], 
                                  ["The Anxiety"]]
    
    if is_in_list(artists_exception, artist):
        result = modified_artists_exception[artists_exception.index(artist)]
    else:
        modified_artist = artist.replace(" and ", "|").replace(" & ", "|").replace(" with ", "|").replace(", ", "|")
        modified_artists = modified_artist.split(sep="|")
        result = [artist]
        for artist in modified_artists:
            result += parentheses_separator(artist, include_original=False)
        result = list(set(result))
    return result


def title_similarity_check(title1: str, title2: str) -> bool:
    """
    Return True when title1 is similar to title2. Otherwise, return False.
    """
    title1_list = parentheses_separator(title1, include_original=True)
    title2_list = parentheses_separator(title2, include_original=True)
    for t1 in title1_list:
        for t2 in title2_list:
            if SequenceMatcher(None, t1.lower(), t2.lower()).ratio() >= 0.8:
                return True
    return False


def artist_similarity_check(artist1: str, artist2: str) -> bool:
    """
    Return True when artist1 is similar to artist2. Otherwise, return False.
    """
    artist1_list = artist_modification(artist1)
    artist2_list = artist_modification(artist2)
    for a1 in artist1_list:
        for a2 in artist2_list:
            if SequenceMatcher(None, a1.lower(), a2.lower()).ratio() >= 0.8:
                return True
    return False


def search_lyrics(df: DataFrame, start: int, end: int) -> None:
    """
    Search song lyrics in Genius and output them as csv files.\\
    Output:
    1. lyrics: successfully got lyrics
    2. no_lyrics: the song does not have lyrics
    3. unreliable: the search result seems to be unreliable
    4. both_unreliable: first and second search result seem to be unreliable
    5. nan: search error
    """
    print(f"Subprocess {start}-{end} starts.")
    start_time = time()
    
    lyrics = [""] * (end - start)
    search_error = []
    unreliable_result = []
    pattern = re.compile("\n+")

    for i in range(start, end):
        year = df.iloc[i, 0]
        rank = df.iloc[i, 1]
        title = df.iloc[i, 2]
        artist = df.iloc[i, 3]
        modified_title = df.iloc[i, 4]
        modified_artist = df.iloc[i, 5]

        # When a modified_title does not contain A- and B-side titles
        if modified_title.find("|") == -1:
            try:
                song = genius.search_song(title=modified_title, artist=modified_artist, get_full_info=False)
            
            # When a search failed
            except:
                lyrics[i - start] = nan
                song_info = [year, rank, title, artist, modified_title, modified_artist]
                search_error.append(song_info)
                break

            # When the search succeeded and a song has lyrics
            if song is not None:

                # When title and artist name of the song matches those of Genius
                if title_similarity_check(modified_title, song.title) and artist_similarity_check(artist, song.artist):
                    lyrics[i - start] = lyric_modification(song.lyrics, pattern)
                
                # When the song has lyrics but title and artist name of the song does not matche those of Genius
                else:
                    lyrics[i - start] = "unreliable"
                    song_info = [year, rank, title, song.title, artist, song.artist, lyric_modification(song.lyrics, pattern)]
                    unreliable_result.append(song_info)
            
            # When the song does not have lyrics
            else:
                lyrics[i - start] = "no_lyrics"
        

        # When a modified_title contains A- and B-side titles
        else:
            titles = modified_title.split(sep="|")
            title1 = titles[0]
            title2 = titles[1]
            search_title = title1
            second_search_done_flag = False

            # First search with title1 (A-side title)
            try:
                song = genius.search_song(title=search_title, artist=modified_artist, get_full_info=False)

            # When first search failed
            except:
                search_title = title2

                # second search with title2 (B-side title)
                try:
                    song = genius.search_song(title=search_title, artist=modified_artist, get_full_info=False)

                # When both first and second searches failed
                except:
                    lyrics[i - start] = nan
                    song_info = [year, rank, title, artist, modified_title, modified_artist]
                    search_error.append(song_info)
                    break

                second_search_done_flag = True
            
            # When at least one search succeeded and a song has lyrics 
            if song is not None:

                # When title and artist name of the song matches those of Genius
                if title_similarity_check(search_title, song.title) and artist_similarity_check(artist, song.artist):
                    lyrics[i - start] = f"[{search_title}]" + lyric_modification(song.lyrics, pattern)
                
                # When the song has lyrics but title and artist name of the song does not matche those of Genius
                else:
                    
                    # When first search failed and the result of second search with title2 seems to be unreliable
                    if second_search_done_flag:
                        lyrics[i - start] = "unreliable"
                        song_info = [year, rank, title, song.title, artist, song.artist, f"[{search_title}]" + lyric_modification(song.lyrics, pattern)]
                        unreliable_result.append(song_info)
                    
                    # When the result of first search with title1 seems to be unreliable
                    else:
                        song_info1 = [year, rank, title, song.title, artist, song.artist, f"[{search_title}]" + lyric_modification(song.lyrics, pattern)]
                        search_title = title2

                        # second search with title2 (B-side title)
                        try:
                            song = genius.search_song(title=search_title, artist=modified_artist, get_full_info=False)
                        
                        # When both first and second searches failed
                        except:
                            lyrics[i - start] = nan
                            song_info = [year, rank, title, artist, modified_title, modified_artist]
                            search_error.append(song_info)
                            break

                        # When second search succeeded and the song has lyrics
                        if song is not None:

                            # When title and artist name of the song matches those of Genius
                            if title_similarity_check(search_title, song.title) and artist_similarity_check(artist, song.artist):
                                lyrics[i - start] = f"[{search_title}]" + lyric_modification(song.lyrics, pattern)

                            # When title and artist name of the song does not matche those of Genius
                            else:
                                lyrics[i - start] = "both_unreliable"
                                song_info2 = [year, rank, title, song.title, artist, song.artist, f"[{search_title}]" + lyric_modification(song.lyrics, pattern)]
                                unreliable_result.append(song_info1)
                                unreliable_result.append(song_info2)
                        
                        # When the song does not have lyrics
                        else:
                            lyrics[i - start] = "no_lyrics"
                     
            # When at least one search succeeded but the song does not have lyrics
            else:
                lyrics[i - start] = "no_lyrics"
            
    
    df_tmp1 = df.iloc[start:end,].copy()
    df_tmp1.reset_index(drop=True, inplace=True)

    df_tmp2 = pd.DataFrame(data=lyrics, columns=["lyric"])

    df_result = pd.concat([df_tmp1, df_tmp2], axis=1)
    df_result.to_csv(f"data/lyrics{start}-{end-1}.csv", index=False)

    if len(search_error) != 0:
        df_search_error = pd.DataFrame(data=search_error, columns=["year", "rank", "title", "artist", "modified_title", "modified_artist"])
        df_search_error.to_csv(f"data/search_error{start}-{end-1}.csv", index=False)

    if len(unreliable_result) != 0:
        df_unreliable_result = pd.DataFrame(data=unreliable_result, columns=["year", "rank", "title", "genius_title", "artist", "genius_artist", "lyric"])
        df_unreliable_result.to_csv(f"data/unreliable_result{start}-{end-1}.csv", index=False)
    
    total_time = time() - start_time
    print(f"Subprocess {start}-{end} ends. (Time: {total_time:.2f}s)")


def wrapper(args: list | tuple) -> None:
    """
    Wrapper function to pass several args to search_lyrics()
    """
    return search_lyrics(*args)


# 6989 entries
df_ranking = pd.read_csv("data/ranking.csv")


# multiprocessing
if __name__ == "__main__":
    start_time = time()

    data_size = len(df_ranking)
    num = data_size // 16
    rest = 6989 % 16
    idxs = [i for i in range(0, 6989, num)]
    idxs[-1] += rest
    values = [[df_ranking, idxs[i], idxs[i+1]] for i in range(len(idxs) - 1)]

    p = Pool(processes=16)
    p.map(wrapper, values)
    p.close()
    p.join()

    total_time = time() - start_time

    print(f"All processes are done. (Time: {total_time:.2f}s)")

# test
# search_lyrics(df_ranking, 400, 500)
