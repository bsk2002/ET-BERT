import os

def remove_dot_underscore_files(root_dir):
    """
    root_dir 내부를 재귀적으로 돌며 ._로 시작하는 파일을 삭제합니다.
    """
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.startswith("._"):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except OSError as e:
                    print(f"Error deleting {file_path}: {e}")

if __name__ == "__main__":
    # 대상 디렉토리 경로를 입력하세요.
    target_directory = "E:\\pre-data\\fine-tuning-for-tls-version\\captures\\splitcap\\"
    
    if os.path.isdir(target_directory):
        remove_dot_underscore_files(target_directory)
    else:
        print("유효한 디렉토리 경로가 아닙니다.")