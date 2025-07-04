from googleapiclient.discovery import build


# 유투브 영상에 댓글을 작성합니다.
# Args:
#   youtube: Google API 클라이언트 객체
#   video_id: 댓글을 작성할 유투브 영상의 ID
#   comment_text: 작성할 댓글 내용
# Returns:
#   dict: 댓글 API 응답 결과
def post_youtube_comment(youtube, video_id, comment_text):
    try:
        request = youtube.commentThreads().insert(
            part="snippet",
            body={
                "snippet": {
                    "videoId": video_id,
                    "topLevelComment": {"snippet": {"textOriginal": comment_text}},
                }
            },
        )
        response = request.execute()
        print("✅ 유투브 댓글 작성 성공:", response)
        return response
    except Exception as e:
        print("❌ 유투브 댓글 작성 실패:", e)
        return None
