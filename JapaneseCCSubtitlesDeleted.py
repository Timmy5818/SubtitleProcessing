# 自動刪除日文CC字幕中的括號內容，並清除空白行
import re
import os

def process_srt_file(srt_file_path):
    """處理單個 SRT 檔案，移除括號內文字並去除空行"""
    if not srt_file_path.lower().endswith(".srt"):
        print(f"❌ 錯誤: {srt_file_path} 不是 SRT 檔案，跳過處理。")
        return

    if not os.path.isfile(srt_file_path):
        print(f"❌ 錯誤: 找不到檔案 {srt_file_path}，請確認路徑是否正確。")
        return

    # 產生輸出檔案名稱
    file_dir, file_name = os.path.split(srt_file_path)
    file_base, file_ext = os.path.splitext(file_name)
    cleaned_srt_output_path = os.path.join(file_dir, f"{file_base}_Remaster{file_ext}")

    # 讀取 SRT 檔案
    with open(srt_file_path, "r", encoding="utf-8") as file:
        srt_content = file.readlines()

    cleaned_srt = []

    for line in srt_content:
        # 移除【全形】或【半形】括號及內部內容
        cleaned_line = re.sub(r"[（(].*?[）)]", "", line).strip()

        # 確保不留下空白行
        if cleaned_line:
            cleaned_srt.append(cleaned_line + "\n")

    # 輸出新的 SRT 檔案
    with open(cleaned_srt_output_path, "w", encoding="utf-8") as file:
        file.writelines(cleaned_srt)

    # 顯示成功訊息
    print(f"✅ 處理完成！輸出的 SRT 檔案: {cleaned_srt_output_path}")

def main():
    """讓使用者手動輸入單個 SRT 檔案的路徑"""
    while True:
        srt_file_path = input("請輸入 SRT 檔案的完整路徑: ").strip()

        # 確保輸入的是 .srt 檔案
        if not srt_file_path.lower().endswith(".srt"):
            print("❌ 錯誤: 只允許輸入 .srt 檔案，請重新輸入。")
            continue

        # 確保檔案存在
        if not os.path.isfile(srt_file_path):
            print("❌ 錯誤: 指定的檔案不存在，請重新輸入。")
            continue

        break  # 確保輸入合法後跳出迴圈

    # 處理單個 SRT 檔案
    process_srt_file(srt_file_path)

def batch_process():
    """讓使用者輸入資料夾，並批次處理該資料夾內的所有 SRT 檔案"""
    while True:
        folder_path = input("請輸入包含 SRT 檔案的資料夾路徑: ").strip()

        if not os.path.isdir(folder_path):
            print("❌ 錯誤: 指定的資料夾不存在，請重新輸入。")
            continue

        break  # 確保輸入合法後跳出迴圈

    # 取得資料夾內所有 .srt 檔案
    srt_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(".srt")]

    if not srt_files:
        print("⚠️ 該資料夾內沒有發現 .srt 檔案，無法進行批次處理。")
        return

    print(f"📂 發現 {len(srt_files)} 個 SRT 檔案，開始處理...\n")

    for srt_file in srt_files:
        process_srt_file(srt_file)

if __name__ == "__main__":
    # 讓使用者選擇手動輸入 或 啟動批次處理
    choice = input("請選擇模式: 1) 手動輸入 2) 批次處理(輸入資料夾路徑) (請輸入 1 或 2): ").strip()

    if choice == "1":
        main()
    elif choice == "2":
        batch_process()
    else:
        print("❌ 錯誤: 無效的選擇，請重新執行程式。")
