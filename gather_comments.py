from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

#docs: https://developers.google.com/youtube/v3/docs/commentThreads/list

#authentication stuff
flow = InstalledAppFlow.from_client_secrets_file("client_secret.json",
        scopes=["https://www.googleapis.com/auth/youtube.force-ssl"]
)

flow.run_local_server(port=8080, promt="consent", authorization_prompt_message="")
credentials = flow.credentials

youtube = build("youtube", "v3", credentials=credentials)
#FP vs OOP video ID
video_id = "08CWw_VD45w"


def post_comment(txt, parentId):
    #test post
    request = youtube.comments().insert(
        part="snippet",
        body = {
            "snippet": {
                "parentId": parentId,
                "textOriginal": txt
        }
      }
    )

    try:
        res = request.execute()
    except Exception as e:
        return e

    return res

#db is expected to be a list of json objects
def gather_comments():
    db = {"Comments":[], "IDs":[]}

    tok = ""
    while True:
        kwargs = {'part':'snippet,replies,id','videoId':video_id} if tok == "" else {'pageToken':tok,'part':'snippet,replies','videoId':video_id}

        request = youtube.commentThreads().list(**kwargs)
        res = request.execute()

        try:
            tok = res["nextPageToken"]
        except:
            break #last page was hit here?

        for item in res["items"]:
            #access the current main comment
            text = item["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
            id_ = item["id"]

            #Store in db
            db["Comments"].append(text)
            db["IDs"].append(id_)

            try:
                #access any replies to this comment
                for reply in item["replies"]["comments"]:
                    rtext = reply["snippet"]["textOriginal"]
                    rid = reply["id"]

                    #Store in db
                    db["Comments"].append(rtext)
                    db["IDs"].append(rid)
            except: 
                pass #No creplies present means keyError will occur
    
    return db



if __name__ == "__main__":
    db = gather_comments()
    print(db)

    x = db["Comments"][16]
    y = db["IDs"][16]

    # x = post_comment("_", y)
    # print(x)








