import argparse
import snscrape.modules.twitter as sntwitter
import pandas as pd
import numpy as np
import re

parser = argparse.ArgumentParser()
parser.add_argument("-topic", dest="topic", required=True)
parser.add_argument("-limit", dest="limit", default=1500)
args = parser.parse_args()

query = f'"{args.topic}" lang:id' #this is the keyword
limit = args.limit #total tweet we wanna crawl
tweets = []
try:
    print('Start crawling')
    for tweet in sntwitter.TwitterSearchScraper(query=query).get_items():
        if len(tweets) == limit:
            break
        else:
            if tweet.inReplyToUser is not None:
                tweet_type = 'reply'
                tweet_reply = re.findall(r'[/]\w+', str(tweet.inReplyToUser))[-1].replace('/','')
            elif tweet.quotedTweet is not None:
                tweet_type = 'retweet'
                tweet_reply = None
            else:
                tweet_type = 'original'
                tweet_reply = None
            tweets.append([tweet.conversationId,
                           tweet.coordinates,
                           tweet.date,
                           tweet.hashtags,
                           tweet.id,
                           tweet.inReplyToTweetId,
                           tweet.inReplyToUser,
                           tweet_reply,
                           tweet.lang,
                           tweet.likeCount,
                           tweet.media,
                           tweet.mentionedUsers,
                           tweet.outlinks,
                           tweet.place,
                           tweet.quoteCount,
                           tweet.quotedTweet,
                           tweet.renderedContent,
                           tweet_type,
                           tweet.replyCount,
                           tweet.retweetCount,
                           tweet.retweetedTweet,
                           tweet.sourceLabel,
                           tweet.url,
                           tweet.user,
                           tweet.user.username])
    df = pd.DataFrame(tweets, columns=(['conversationId',
                                        'coordinates',
                                        'date',
                                        'hashtags',
                                        'id',
                                        'inReplyToTweetId',
                                        'inReplyToUser_url',
                                        'inReplyToUser',
                                        'lang',
                                        'likeCount',
                                        'media',
                                        'mentionedUsers',
                                        'outlinks',
                                        'place',
                                        'quoteCount',
                                        'quotedTweet',
                                        'description',
                                        'tweet_type',
                                        'replyCount',
                                        'retweetCount',
                                        'retweetedTweet',
                                        'source',
                                        'tweet_url',
                                        'user_url',
                                        'username']))
    df.to_csv('./sna.csv', index=False)
except Exception as e:
    print(e)
    
print('Finished')
print('-----')