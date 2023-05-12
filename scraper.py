from dotenv import load_dotenv
import os
import tweepy
import requests
import pandas as pd
class Scraper():



    def __init__(self, username, count, keywords) -> None:

        load_dotenv()
        self.username = username
        self.count = count
        self.keywords = keywords


        TWITTER_API_KEY = os.getenv('API_KEY')
        TWITTER_API_SECRET = os.getenv('API_SECRET')
        TWITTER_ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
        TWITTER_ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
        BEARER_TOKEN = os.getenv('BEARER_TOKEN')

        self.client = self.get_client(TWITTER_API_KEY,
                                      TWITTER_API_SECRET,
                                      TWITTER_ACCESS_TOKEN,
                                      TWITTER_ACCESS_TOKEN_SECRET,
                                      BEARER_TOKEN)
        
        self.main()

    def get_client(self,TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN,
                    TWITTER_ACCESS_TOKEN_SECRET, BEARER_TOKEN):
        client = tweepy.Client( bearer_token=BEARER_TOKEN, 
                            consumer_key=TWITTER_API_KEY, 
                            consumer_secret=TWITTER_API_SECRET, 
                            access_token=TWITTER_ACCESS_TOKEN, 
                            access_token_secret=TWITTER_ACCESS_TOKEN_SECRET, 
                            return_type = requests.Response,
                            wait_on_rate_limit=True)
        return client

    def get_user_id(self, username):
        username = username
        user = self.client.get_user(username=username)
        user = user.json()
        id = user["data"]["id"]
        return id
    

    def get_tweets(self, user_id, count) -> list:
        #We can scrape up to 100 tweets in one request
        surplus = count % 100
        range_for = (count // 100) - 1 
        all_tweets = []

        tweets = self.client.get_users_tweets(id=user_id, max_results=surplus, tweet_fields=["created_at"])
        tweets= tweets.json()
        all_tweets = tweets['data'] 

        # İkinci ve sonraki istekler
        for i in range(range_for):
                next_token = tweets["meta"]["next_token"]
                tweets = self.client.get_users_tweets(id=user_id, max_results=100, tweet_fields=["created_at"], pagination_token=next_token)
                tweets = tweets.json()
                all_tweets.extend(tweets['data'] )
                # last_tweet_date = all_tweets[-1]["created_at"]

        return all_tweets
    

    def tweets_to_dataframe(self, tweets):
        data = []
        for tweet in  tweets:
            tweet_text_org = tweet["text"]
            tweet_id = tweet["id"]
            
            tweet_url = f"https://twitter.com/{self.username}/status/{tweet_id}"
            created_at = tweet["created_at"]
            data.append({'Tweet Text':tweet_text_org, 'Tweet URL': tweet_url, 'Created At': created_at})
        
        df =pd.DataFrame(data)
        return df
    

    def save_dataframes(self, df_all, df_filtered):
        df_all.to_excel(f'{self.username}-all.xlsx', index=False)
        df_filtered.to_excel(f'{self.username}-filtered.xlsx', index=False)

    
    def filter_dataframe(self, df, keywords):
        filtered_df = df[df['Tweet Text'].str.lower().str.contains('|'.join(keywords))]
        return filtered_df
    
    def main(self):
        user_id = self.get_user_id(self.username)
        all_tweets = self.get_tweets(user_id, self.count)
        df_all_tweets = self.tweets_to_dataframe(all_tweets)
        df_filtered = self.filter_dataframe(df = df_all_tweets, keywords = self.keywords)
        self.save_dataframes(df_all = df_all_tweets, df_filtered = df_filtered)


    


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Search and filter tweets by keywords')

    parser.add_argument('username', help='Twitter username')
    parser.add_argument('keywords', help='Keywords to search for')
    parser.add_argument('count', type=int, help='Number of tweets to retrieve')

    args = parser.parse_args()

    username = args.username
    keywords = args.keywords.split(",")
    count = args.count
    print(f"Searching for tweets from {username} containing the keywords {keywords} and retrieving {count} tweets...")

    Scraper(username, count, keywords)
