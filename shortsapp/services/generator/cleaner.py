import os

# media/temp_text 폴더 정리
def delete_temp_files():
   
    temp_dir = "media/temp_text"
    if os.path.exists(temp_dir):
        for f in os.listdir(temp_dir):
            try:
                os.remove(os.path.join(temp_dir, f))
            except Exception as e:
                print(f"⚠️ {f} 삭제 실패: {e}")