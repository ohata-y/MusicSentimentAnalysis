# Sentiment Analysis in Music

*Note: This project is still ongoing.*\
*Note: This README is also not completed.*

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



#### Sentiment analysis by VEDER and BERT

Contents

## 2. Results

### 2.1. Scraping

[scraping_wiki.ipynb](https://github.com/ohata-y/MusicSentimentAnalysis/blob/main/scraping_wiki.ipynb)\
[robot.txt](https://en.wikipedia.org/robots.txt)

### 2.2. Getting lyrics from [Genius.com](https://genius.com/)

[getting_lyrics1.py](https://github.com/ohata-y/MusicSentimentAnalysis/blob/main/getting_lyrics1.py)\
[getting_lyrics2.ipynb](https://github.com/ohata-y/MusicSentimentAnalysis/blob/main/getting_lyrics2.ipynb)

### 2.3. Brief data description

[data_basic_info.ipynb](https://github.com/ohata-y/MusicSentimentAnalysis/blob/main/data_basic_info.ipynb)

### 2.4. Sentiment analysis (VADER)


### 2.5. Sentiment analysis (BERT)

