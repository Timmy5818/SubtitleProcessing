# 清除簡體中文+日文字幕中的簡體中文字幕保留日文字幕(有很多問題，測試中)
import re

# 讀取 SRT 檔案
srt_file_path = r"E:\影片\Dragon Ball\Films\【DRAGON BALL THE MOVIES】【03】ドラゴンボール 摩訶不思議大冒険 (Dragon Ball Mystical Adventure)\日本語 (Japanese).srt"

with open(srt_file_path, "r", encoding="utf-8") as file:
    srt_lines = file.readlines()

cleaned_srt = []
index = 1
buffer = []
timestamp = None

for line in srt_lines:
    stripped_line = line.strip()

    if stripped_line.isdigit():  # 字幕索引號
        if buffer and timestamp:
            cleaned_text = "\n".join(buffer).strip()
            if cleaned_text:  # 確保內容不是空的
                cleaned_srt.append(f"{index}\n{timestamp}\n{cleaned_text}\n")
                index += 1
        buffer = []
        timestamp = None

    elif "-->" in stripped_line:  # 時間戳
        timestamp = stripped_line

    else:
        # 檢查是否包含日文字符
        contains_japanese = re.search(r"[\u3040-\u30FF\u31F0-\u31FF]", stripped_line) is not None
        contains_chinese = re.search(r"[\u4e00-\u9FFF]", stripped_line) is not None

        if contains_japanese:
            # 如果該行是雙語字幕，刪除其中的中文部分
            if contains_chinese:
                stripped_line = re.sub(r"[\u4e00-\u9FFF]", "", stripped_line)  # 刪除中文
            buffer.append(stripped_line.strip())  # 保留日文部分

# 處理最後一個字幕區塊
if buffer and timestamp:
    cleaned_text = "\n".join(buffer).strip()
    if cleaned_text:
        cleaned_srt.append(f"{index}\n{timestamp}\n{cleaned_text}\n")

# 輸出新的 SRT 檔案
cleaned_srt_output_path = r"E:\影片\Dragon Ball\Films\【DRAGON BALL THE MOVIES】【03】ドラゴンボール 摩訶不思議大冒険 (Dragon Ball Mystical Adventure)\cleaned_japanese_only.srt"
with open(cleaned_srt_output_path, "w", encoding="utf-8") as file:
    file.writelines(cleaned_srt)

# 顯示成功訊息
print(f"✅ 處理完成！輸出的 SRT 檔案: {cleaned_srt_output_path}")