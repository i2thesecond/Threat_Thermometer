from nltk.twitter import Query, Streamer, Twitter, TweetViewer, TweetWriter, credsfromfile


#inspect function twitter_samples.tokenized() the reason is because there are default 'built-in' tokenizers that would be curious to see what different rules it has over the general tokenizer in the nltk database. The reasoning is that tokenization helps training sets for labels, and the "twitter" tokenizer might be better when it comes to labelling sensibilities. 

userids = ['18535086']
oauth = credsfromfile()

client = Query(**oauth)
client.register(TweetViewer())
client.user_tweets('metasploit')
