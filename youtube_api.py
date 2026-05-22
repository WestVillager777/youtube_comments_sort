from pathlib import Path
from dotenv import load_dotenv
from googleapiclient.discovery import build
import os

env_path = Path(__file__).parent.parent / ".env"
# 1. .envの内容を読み込む
load_dotenv(dotenv_path=env_path)
# 2. os.getenv("変数名") で値を取り出す
api_key = os.getenv("YOUTUBE_API_KEY")

def get_comments(id, limit, progress_callback=None):
    #動画IDからデータ取得パターン
    video_id = id          
    YOUTUBE_API_KEY = api_key

    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    comments = []
    page_token = None
    fetched_count = 0

    while True:
        response = youtube.commentThreads().list(
            videoId=video_id,
            part='snippet',
            maxResults=100,
            textFormat='plainText',
            order="relevance",
            pageToken=page_token
        ).execute()
        
        items = response.get('items', [])
        for comment in items:
            text = comment['snippet']['topLevelComment']['snippet']['textDisplay']
            like = int(comment['snippet']['topLevelComment']['snippet']['likeCount'])

            if like >= limit:
                comments.append([like, text])
        
        fetched_count += len(items)
        
        # UIに進捗を伝えるためのコールバック
        if progress_callback:
            progress_callback(fetched_count)

        # 次のページがない場合はループを抜ける
        page_token = response.get("nextPageToken")
        if not page_token:
            break

    # いいね数で降順ソート
    comments.sort(reverse=True)
    return comments
