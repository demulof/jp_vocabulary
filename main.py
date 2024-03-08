import tkinter as tk
from tkinter import ttk
from dict_voc import dict_50, dict_N5_voc, dict_N4_voc, dict_N3_voc, dict_N2_voc, dict_N1_voc

class TransparentWindow:
    def __init__(self, root, words, mode):
        self.root = root
        self.words = words
        self.mode = mode
        self.index = 0
        self._x = 0
        self._y = 0
        # 初始標題列隱藏狀態
        self.title_visible = True
        # 初始文字大小
        self.font_size = 10
        # 初始視窗透明度
        self.opacity = 0.3

        # 設定按鈕樣式
        style = ttk.Style()
        style.configure("TButton", relief="flat", padding=0, borderwidth=0)
        style.configure('Custom.TLabel', background='white', foreground='black')

        self.title_frame = ttk.Frame(root, style='Custom.TLabel')
        self.title_frame.pack(side=tk.TOP, fill=tk.X)

        # 單字區塊
        self.label = tk.Label(root, text=self.words[self.index], font=("Helvetica", self.font_size), bg='white')
        self.label.config(bd=0, highlightthickness=0)
        self.label.pack(expand=True, fill=tk.BOTH)

        # 切換單字鈕(下一個)
        self.prev_label = tk.Label(self.title_frame, text="<", font=("Helvetica", 14), bg='white')
        self.prev_label.pack(side=tk.LEFT, padx=10, pady=10)
        self.prev_label.bind("<Button-1>", lambda event: self.prev_word())

        # 切換單字鈕(上一個)
        self.next_label = tk.Label(self.title_frame, text=">", font=("Helvetica", 14), bg='white')
        self.next_label.pack(side=tk.RIGHT, padx=10, pady=10)
        self.next_label.bind("<Button-1>", lambda event: self.next_word())

        # 切換隱藏標題列鈕
        self.toggle_title_label = tk.Label(self.title_frame, text="^", font=("Helvetica", 14), bg='white')
        self.toggle_title_label.pack(side=tk.LEFT, padx=10, pady=10)
        self.toggle_title_label.bind("<Button-1>", lambda event: self.toggle_title())

        # 切換有無中文模式鈕
        self.toggle_mode_label = tk.Label(self.title_frame, text="#", font=("Helvetica", 14), bg='white')
        self.toggle_mode_label.pack(side=tk.RIGHT, padx=10, pady=10)
        self.toggle_mode_label.bind("<Button-1>", lambda event: self.toggle_mode())


        # 设置窗口透明
        root.attributes("-alpha", 0.1)
        # root.attributes("-transparentcolor", "white")

        # 拖動視窗事件處理
        root.bind("<Button-1>", self.start_move)
        root.bind("<B1-Motion>", self.on_move)

        # 調整視窗大小事件處理
        root.bind("<Configure>", self.on_resize)

         # 監聽視窗大小改變事件
        root.bind("<Configure>", self.on_window_resize)

        # 根據顯示模式設置初始顯示狀態
        if not self.mode:
            self.label.config(text=self.words[self.index][0])

    def prev_word(self):
        self.index = (self.index - 1) % len(self.words)
        if self.mode:
            self.label.config(text=self.words[self.index][0] + " \n " + self.words[self.index][1])
        else:
            self.label.config(text=self.words[self.index][0])

    def next_word(self):
        self.index = (self.index + 1) % len(self.words)
        if self.mode:
            self.label.config(text=self.words[self.index][0] + " \n " + self.words[self.index][1])
        else:
            self.label.config(text=self.words[self.index][0])

    def toggle_title(self):
        self.title_visible = not self.title_visible
        self.root.overrideredirect(not self.title_visible)
        if self.title_visible:
            self.root.attributes("-topmost", False)
            self.pinned = False
        else:
            self.root.attributes("-topmost", True)
            self.pinned = True

    def increase_font(self):
        self.font_size += 2
        self.label.config(font=("Helvetica", self.font_size))

    def decrease_font(self):
        if self.font_size > 2:
            self.font_size -= 2
            self.label.config(font=("Helvetica", self.font_size))
    
    def increase_opacity(self):
        self.opacity = min(self.opacity + 0.1, 1.0)
        self.set_opacity()

    def decrease_opacity(self):
        self.opacity = max(self.opacity - 0.1, 0.1)
        self.set_opacity()

    def set_opacity(self):
        self.root.attributes("-alpha", self.opacity)

    def start_move(self, event):
        self._x = event.x
        self._y = event.y

    def on_move(self, event):
        deltax = event.x - self._x
        deltay = event.y - self._y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def on_resize(self, event):
        self.root.attributes("-transparentcolor", "white")
    
    def on_window_resize(self, event):
        self.label.config(wraplength=self.root.winfo_width())

    def toggle_mode(self):
        self.mode = not self.mode
        if self.mode:
            self.label.config(text=self.words[self.index][0] + " \n " + self.words[self.index][1])
        else:
            self.label.config(text=self.words[self.index][0])

    def update_word(self):
        if self.mode:
            self.label.config(text=self.words[self.index][0] + " \n " + self.words[self.index][1])
        else:
            self.label.config(text=self.words[self.index][0])

def main():
    words = [(f"{i+1}. {word[0]}", word[1]) for i, word in enumerate(dict_50.items())]

    root = tk.Tk()
    root.title(" ")
    root.geometry("400x200")
    root.wm_attributes('-transparentcolor', 'white')

    app1 = TransparentWindow(root, words, mode=True)

    # 第二個視窗，控制視窗
    control_window = tk.Toplevel(root)
    control_window.title("control_window")
    control_window.geometry("400x200")

    # 标签文本
    dictionary_label = tk.Label(control_window, text="單元：")
    dictionary_label.grid(row=0, column=0, padx=10, pady=10)

    word_label = tk.Label(control_window, text="單字：")
    word_label.grid(row=1, column=0, padx=10, pady=10)

    button_label = tk.Label(control_window, text="字體：")
    button_label.grid(row=2, column=0, padx=10, pady=10)

    alpha_label = tk.Label(control_window, text="透明：")
    alpha_label.grid(row=3, column=0, padx=10, pady=10)

    # 切換字典下拉選單
    dictionary_combobox = ttk.Combobox(control_window, values=["50音", "N5", "N4", "N3", "N2", "N1"]) # 修改為你的字典名稱
    dictionary_combobox.current(0)  # 預設選擇第一個字典
    dictionary_combobox.grid(row=0, column=1, padx=10, pady=10)

    # 切換單字下拉選單
    word_combobox = ttk.Combobox(control_window, values=[word[0] for word in words]) # 使用字典中的所有字作為選項
    word_combobox.grid(row=1, column=1, padx=10, pady=10)

    decrease_font_button = ttk.Button(control_window, text="-", command=app1.decrease_font, style="TButton")
    decrease_font_button.grid(row=2, column=1, padx=10, pady=10)

    increase_font_button = ttk.Button(control_window, text="+", command=app1.increase_font, style="TButton")
    increase_font_button.grid(row=2, column=2, padx=10, pady=10)

    decrease_alpha_button = ttk.Button(control_window, text="-", command=app1.decrease_opacity, style="TButton")
    decrease_alpha_button.grid(row=3, column=1, padx=10, pady=10)

    increase_alpha_button = ttk.Button(control_window, text="+", command=app1.increase_opacity, style="TButton")
    increase_alpha_button.grid(row=3, column=2, padx=10, pady=10)

    # 設定當第一個下拉式選單改變時，觸發切換字典的函數
    dictionary_combobox.bind("<<ComboboxSelected>>", lambda event: change_dictionary(event, words, app1, word_combobox))

    # 設定當第二個下拉式選單改變時，觸發切換字的函數
    word_combobox.bind("<<ComboboxSelected>>", lambda event: change_word(event, app1))

    root.mainloop()

def change_dictionary(event, words, app, word_combobox):
    selected_dictionary = event.widget.get()
    if selected_dictionary == "50音":
        words = [(f"{i+1}. {word[0]}", word[1]) for i, word in enumerate(dict_50.items())]
    elif selected_dictionary == "N5":
        words = [(f"{i+1}. {word[0]}", word[1]) for i, word in enumerate(dict_N5_voc.items())]
    elif selected_dictionary == "N4":
        words = [(f"{i+1}. {word[0]}", word[1]) for i, word in enumerate(dict_N4_voc.items())]
    elif selected_dictionary == "N3":
        words = [(f"{i+1}. {word[0]}", word[1]) for i, word in enumerate(dict_N3_voc.items())]
    elif selected_dictionary == "N2":
        words = [(f"{i+1}. {word[0]}", word[1]) for i, word in enumerate(dict_N2_voc.items())]
    elif selected_dictionary == "N1":
        words = [(f"{i+1}. {word[0]}", word[1]) for i, word in enumerate(dict_N1_voc.items())]
    app.words = words
    app.index = 0
    app.update_word()
    # 更新第二個下拉式選單中的選項
    word_combobox['values'] = [word[0] for word in app.words]

def change_word(event, app):
    selected_word = event.widget.get()
    # 根據選擇的字重新設定索引
    for i, (word, _) in enumerate(app.words):
        if word == selected_word:
            app.index = i
            app.update_word()
            break

if __name__ == "__main__":
    main()