import customtkinter as ctk
from tkinter import messagebox, scrolledtext
import threading
from youtube_api import get_comments

# ===== 外観設定 =====
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SortYoutubeComments")
        self.geometry("700x600")

        # UIの設置
        self.setup_ui()

    # UIの関数
    def setup_ui(self):
        # IDを入力させるエントリーボックス
        self.label1 = ctk.CTkLabel(self, text='enter youtube ID')
        self.label1.pack(pady=5)
        self.entry1 = ctk.CTkEntry(self, width=300)
        self.entry1.pack(pady=5)

        # リミット数を入力させるエントリーボックス
        self.label2 = ctk.CTkLabel(self, text='enter like_limit')
        self.label2.pack(pady=5)
        self.entry2 = ctk.CTkEntry(self, width=300)
        self.entry2.pack(pady=5)

        # commandは self.button_action とする
        self.button = ctk.CTkButton(self, text='GET', command=self.button_action)
        self.button.pack(pady=10)

        # 実行結果を示す場所
        self.output = ctk.CTkTextbox(self, width=650, height=400)
        self.output.pack(pady=10, padx=10)
        self.output.configure(state='disabled') # 最初は編集不可

    # 実行ボタンを押した時のアクション関数
    def button_action(self):

        # 入力したものの取得
        video_id = self.entry1.get()
        limit_str = self.entry2.get()
        if int(limit_str) == 0:
            limit = 0
        else:
            limit = int(limit_str)
        
        # IDが入力されていなかったらエラーを表示する関数
        if not video_id:
            messagebox.showwarning('error', 'enter keyword !!!')
            return     
        
        # UIのリセット
        self.button.configure(state='disabled') # ボタンを使えなくする
        self.output.configure(state='normal')
        self.output.delete('1.0', "end") # 白紙に戻す
        self.output.insert("end", "データを取得中...（件数が多いと時間がかかります）\n")

        # サブスレッドの起動（スレッドを立てて、fetch_taskを裏で実行する)
        thread = threading.Thread(target=self.fetch_task, args=(video_id, limit))
        thread.daemon = True
        thread.start()
    
    # 裏でコメント取得
    def fetch_task(self, video_id, limit):
        try:
            # APIの進捗を受け取るコールバック関数
            def on_progress(count):
                self.after(0, lambda: self.show_msg(f'現在{count}個のコメントを取得済み\n'))

            # API呼び出し（youtube_api.py の関数）
            comments = get_comments(video_id, limit, progress_callback=on_progress)
            
            # 結果の表示
            self.after(0, lambda: self.display_result(comments))
            
        except Exception as e:
            self.after(0, lambda err=e: messagebox.showerror('Error', f'エラーが発生しました。\n{err}'))
            self.after(0, lambda: self.button.configure(state='normal'))
            self.after(0, lambda: self.output.configure(state='disabled'))
    
    # マルチスレッド時のメッセージ表示関数
    def show_msg(self, msg):
        self.output.insert("end", msg)
        self.output.see("end")

    # データを取得し終わった後に結果を画面に表示する関数
    def display_result(self, comments):
        self.output.delete('1.0', "end")
        if not comments:
            self.output.insert("end", "NOOOOOOOOOO")
        else:
            for num, c in comments:
                self.output.insert("end", "--------------------------------------------------\n")
                self.output.insert("end", f"いいね数[{num}]\n")
                self.output.insert("end", f"{c}\n")
        
        self.button.configure(state='normal')
        self.output.configure(state='disabled')


if __name__ == "__main__":
    app = App()
    app.mainloop()