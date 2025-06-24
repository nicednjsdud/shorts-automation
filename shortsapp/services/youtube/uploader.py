from googleapiclient.http import MediaFileUpload
from .auth import get_authenticated_service

# YouTube에 동영상을 업로드하는 함수
def upload_video(file_path, title, description= "", tags=None, category_id="22", privacy_status="unlisted"):
    youtube = get_authenticated_service()

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags if tags else [],
            "categoryId": category_id
        },
        "status": {
            "privacyStatus": privacy_status,
            "selfDeclaredMadeForKids": False
        }
    }

    # 동영상 파일을 업로드합니다.
    media = MediaFileUpload(file_path, mimetype="video/mp4", resumable=True)
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )
    response = request.execute()
    print("✅ 업로드 완료! Video ID:", response["id"])

    return response['id']