import twitter

# initialize api instance
twitter_api = twitter.Api(consumer_key='YOUR_CONSUMER_KEY',
                        consumer_secret='YOUR_CONSUMER_SECRET',
                        access_token_key='YOUR_ACCESS_TOKEN_KEY',
                        access_token_secret='YOUR_ACCESS_TOKEN_SECRET')

# test authentication
print(twitter_api.VerifyCredentials())

