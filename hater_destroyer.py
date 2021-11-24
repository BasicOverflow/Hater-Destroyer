from gather_comments import post_comment, gather_comments
from sent_analyzer import create_df, perform_analysis, store
import random



def unleash_beast(df):
    '''Actually posts replies to the foolish comments'''

    epic_comebacks = ["shut up", "shutup youre mouth", "literaly shutup", "shutupe now", "you shut up", "i dont like that shutup", "i dont like that so shutiup",
        "youre mom so fat peter grifen fart", "it is foolish to test me", "you fool"]

    for _, row in df.iterrows(): 
        if row["Sentiment"] == "-": #if comment is negative
            #post epic reply
            post_comment(random.choice(epic_comebacks), row["IDs"])   
    


def main():
    #grab comments and any other relevant information
    data = gather_comments()

    #insert into pandas df
    df = create_df(data)

    # perform sentiment analysis on comments, and add results to df
    perform_analysis(df)

    # store into file for future reference
    store(df) #grab function is available in sent_analyzer.py to unpickle the df

    # reply to negative comments
    unleash_beast(df)



if __name__ == "__main__":
    main()