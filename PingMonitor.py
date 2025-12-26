import os
import time
import threading
from datetime import datetime
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog

# 設定預設的ping間隔時間（秒）
DEFAULT_PING_INTERVAL = 1
pinging = False

def ping(ip):
    response = os.system(f"ping -n 1 {ip}")
    return response == 0

def log_status(ip, status):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status_message = f"{current_time}: {ip} - {'Connected' if status else 'Disconnected'}\n"
    text_area.insert(tk.END, status_message)
    text_area.see(tk.END)

def ping_host():
    global pinging
    ip = ip_entry.get()
    interval = int(interval_entry.get())
    pinging = True
    while pinging:
        is_connected = ping(ip)
        log_status(ip, is_connected)
        time.sleep(interval)

def start_ping():
    threading.Thread(target=ping_host, daemon=True).start()

def stop_ping():
    global pinging
    pinging = False

def export_log():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                               filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        try:
            with open(file_path, 'w', encoding='utf-8') as log_file:
                log_file.write(text_area.get(1.0, tk.END))
            messagebox.showinfo("成功", "日誌已成功匯出到 " + file_path)
        except Exception as e:
            messagebox.showerror("錯誤", f"匯出日誌時發生錯誤: {e}")

# 創建主窗口
root = tk.Tk()
root.title("Ping網路監控 Monitor")

# IP輸入框
tk.Label(root, text="輸入IP Address:").pack(pady=5)
ip_entry = tk.Entry(root)
ip_entry.pack(pady=5)

# Ping間隔時間輸入框
tk.Label(root, text="設定Ping 間隔時間(秒):").pack(pady=5)
interval_entry = tk.Entry(root)
interval_entry.insert(0, str(DEFAULT_PING_INTERVAL))
interval_entry.pack(pady=5)

# 按鈕框架
button_frame = tk.Frame(root)
button_frame.pack(pady=5)

# 開始按鈕
start_button = tk.Button(button_frame, text="開始Start", command=start_ping)
start_button.pack(side=tk.LEFT, padx=5)

# 停止按鈕
stop_button = tk.Button(button_frame, text="暫停Stop", command=stop_ping)
stop_button.pack(side=tk.LEFT, padx=5)

# 匯出日誌按鈕
export_button = tk.Button(button_frame, text="匯出Export Log", command=export_log)
export_button.pack(side=tk.RIGHT, padx=5)

# 日誌顯示區域
text_area = scrolledtext.ScrolledText(root, width=50, height=20)
text_area.pack(pady=5)

# 啟動主循環
root.mainloop()
