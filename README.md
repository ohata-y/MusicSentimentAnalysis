# Sentiment Analysis in Music

### *Note: This project was suspended .*

This is where I record codes and results of sentiment analysis in US music which I have done as a final report of Practical Data Analysis for Economics (autumn, 2023 Hitotsubashi University).

## 1. About this project

### 1.1. Motivation

You might have heard that there is a relationship between popular music and the economy. One will argue that sad songs will become popular if the economy is not doing well, while the other will assert that upbeat songs will become popular rather than sad songs because people will try to make them feel better by listening to happy songs. Both theories seem to make sense, but these are only based on individual experiences, not on empirical analysis. Therefore, to make it clear, I decided to verify these theories by using real data.

### 1.2. Analysis methods

I adopted the US Billboard Year-End Hot 100 Singles (Top Singles) and regarded songs in the charts as the US’s representative popular songs in a specific year. This is because it has been the standard music chart in the United States. However, Billboard is releasing only the most recent year’s chart, so I referred to Wikipedia’s articles. You can access all charts (1946~) from the [link table](https://en.wikipedia.org/wiki/Billboard_Hot_100#Billboard%20Year-End%20Hot%20100%20singles:~:text=Billboard%20Year%2DEnd%20Hot%20100%20singles).

#### 1.2.1. Web scraping

To acquire charts from Wikipedia's articles, I did web scraping with Python.
Before executing web scraping, I checked Wikipedia’s 
[Terms of Use](https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use), 
[robot.txt](https://en.wikipedia.org/robots.txt), 
and 
[license](https://creativecommons.org/licenses/by-sa/4.0/).

*Licensing notice*\
All contents I got from Wikipedia's articles (each articles in the 
[link table](https://en.wikipedia.org/wiki/Billboard_Hot_100#Billboard%20Year-End%20Hot%20100%20singles:~:text=Billboard%20Year%2DEnd%20Hot%20100%20singles)) 
are released under the 
[Creative Commons Attributions-ShareAlike 4.0](https://creativecommons.org/licenses/by-sa/4.0/), 
and I modified some parts of the contents in order to remove unnecessary words for searches in Genius API.

#### 1.2.2. Genius.com

I used 
[LyricsGenius](https://github.com/johnwmillr/LyricsGenius) 
to acquire lyrics from Genius, but later I found that the library uses BeutifulSoup to scrape lyrics and this activity might violate Genius’s 
[Terms of Service](https://genius.com/static/terms).

#### LyricsGenius
>Genius has legal agreements with music publishers and considers the lyrics on their website to be a legal property of Genius, and won’t allow you to re-use their lyrics without explicit licensing. They even sued Google on grounds of stolen lyrics, asking for $50 million in damages, but to no avail. So it shouldn’t come as a surprise if they don’t provide lyrics in calls to the API. So how does LyricsGenius get the lyrics?
>
>LyricsGenius uses a web-scraping library called Beautiful Soup to scrape lyrics from the song’s page on Genius. Scraping the lyrics in this way violates Genius’ terms of service. If you intend to use the lyrics for personal purposes, that shouldn’t be cause for trouble, but other than that, you should inquire what happens when you violate the terms this way. As a reminder, LyricsGenius is not responsible for your usage of the library.\
(https://lyricsgenius.readthedocs.io/en/master/how_it_works.html)

#### Genius's Terms of Service

One of the prohibited activities is
>harvesting or collecting, through use of automated scripts or otherwise, the contents of the Service or email addresses, contact information or other private information of other Users from the Service for any purpose, including without limitation for the purposes of sending unsolicited emails or other unsolicited communications to Users or reproducing the content of the Service;\
(https://genius.com/static/terms)

Therefore, I decided to suspend this project.\
Instead, I am planning to start a new project using financial data.

