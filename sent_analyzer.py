import pickle
import textblob
import pandas as pd
import re 



def create_df(comments_db: dict[list]):
    #Construct a dataframe from given data
    df = pd.DataFrame(comments_db)

    #Clean data by getting rid of @'s, \n's, etc. in the comments
    for _, row in df.iterrows():
        row["Comments"] = re.sub("http\S+", "", row["Comments"])
        row["Comments"] = re.sub("@\S+", "", row["Comments"])
        row["Comments"] = re.sub("\\n+", "", row["Comments"])

    return df


def perform_analysis(df):
    #add two new columns, populate them
    df["Polarity"] = df["Comments"].map(lambda comment: textblob.TextBlob(comment).sentiment.polarity)
    df["Sentiment"] = df["Polarity"].map(lambda pol: "-" if pol < 0.1 else "+")

    #neg, pos, sentiment represented by '-', '+'


def store(df):
    '''Pickle dataframe'''
    with open("db.pickle","wb") as f:
        pickle.dump(df, f)

    print("Stored Away!")


def grab():
    '''Unpickle and return dataframe'''
    with open('db.pickle', 'rb') as f:
        df = pickle.load(f)
        return df













if __name__ == "__main__":
    from gather_comments import gather_comments
    
    test = gather_comments()

    df = create_df(test)

    perform_analysis(df)

    print(df)

    pos_comments = df[df.Sentiment == "+"]["Comments"]#.count()["Comments"]
    neg_comments = df[df.Sentiment == "-"]["Comments"]#.count()["Comments"]

    for i in neg_comments:
        print(i)

    
    print(len(neg_comments))

    store(df)







