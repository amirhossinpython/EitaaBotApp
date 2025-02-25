import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import filedialog
from eitaa_bot import EitaaBot
import requests
import random
import shutil

def get_response_from_api(user_input):
    url = "https://api.api-code.ir/gpt-4/"
    payload = {"text": user_input}

    try:
        response = requests.get(url, params=payload, timeout=10)
        response.raise_for_status()

        data = response.json()
        if "result" in data:
            return data["result"]
        else:
            return "Error: Invalid response format from API."

    except requests.exceptions.Timeout:
        return "Error: The request timed out. Please try again later."
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except requests.exceptions.RequestException as req_err:
        return f"Request error occurred: {req_err}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def generate_image(prompt, file_name="downloaded_image.jpg"):
    try:
        response = requests.get(f"http://api-free.ir/api/img.php?text={prompt}&v=3.5")
        response.raise_for_status()
        data = response.json()
        result = data.get("result", [])
        if result:
            random_link = random.choice(result)
            img_response = requests.get(random_link, stream=True)
            img_response.raise_for_status()
            with open(file_name, "wb") as out_file:
                shutil.copyfileobj(img_response.raw, out_file)
            return file_name
    except Exception:
        return None

class EitaaBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Eitaa Bot")
        self.root.geometry("500x400")
        self.root.configure(bg='#f0f0f0')

        # درخواست توکن از کاربر
        self.token = None
        self.chat_id = None
        self.show_token_input()

    def show_token_input(self):
        self.token_window = tk.Toplevel(self.root)
        self.token_window.title("ورود توکن")
        self.token_window.geometry("400x200")
        self.token_window.configure(bg='#f0f0f0')

        self.token_label = tk.Label(self.token_window, text="لطفاً توکن ربات Eitaa را وارد کنید:", font=('Arial', 12), bg='#f0f0f0')
        self.token_label.pack(pady=10)

        self.token_entry = tk.Entry(self.token_window, font=('Arial', 12), width=30)
        self.token_entry.pack(pady=10)

        self.chat_id_label = tk.Label(self.token_window, text="لطفاً شناسه چت (Chat ID) را وارد کنید:", font=('Arial', 12), bg='#f0f0f0')
        self.chat_id_label.pack(pady=10)

        self.chat_id_entry = tk.Entry(self.token_window, font=('Arial', 12), width=30)
        self.chat_id_entry.pack(pady=10)

        self.submit_button = tk.Button(self.token_window, text="تأیید", font=('Arial', 12), command=self.set_token, bg='#4CAF50', fg='white')
        self.submit_button.pack(pady=10)

    def set_token(self):
        self.token = self.token_entry.get()
        self.chat_id = self.chat_id_entry.get()

        if not self.token or not self.chat_id:
            messagebox.showerror("خطا", "لطفاً توکن و شناسه چت را وارد کنید.")
            return

        self.token_window.destroy()
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="چه خدمتی می‌خواهید؟", font=('Arial', 14), bg='#f0f0f0')
        self.label.pack(pady=10)

        self.service_combobox = ttk.Combobox(self.root, values=["چت", "ساخت تصویر", "خروج"], font=('Arial', 12), state="readonly")
        self.service_combobox.pack(pady=10)
        self.service_combobox.current(0)

        self.next_button = tk.Button(self.root, text="ادامه", font=('Arial', 12), command=self.next_step, bg='#4CAF50', fg='white')
        self.next_button.pack(pady=10)

    def next_step(self):
        choice = self.service_combobox.get()

        if choice == "چت":
            self.chat_window()
        elif choice == "ساخت تصویر":
            self.image_window()
        elif choice == "خروج":
            self.root.quit()

    def chat_window(self):
        self.chat_window = tk.Toplevel(self.root)
        self.chat_window.title("چت")
        self.chat_window.geometry("400x300")
        self.chat_window.configure(bg='#f0f0f0')

        self.chat_label = tk.Label(self.chat_window, text="لطفاً پیام خود را وارد کنید:", font=('Arial', 12), bg='#f0f0f0')
        self.chat_label.pack(pady=10)

        self.chat_entry = tk.Entry(self.chat_window, font=('Arial', 12), width=30)
        self.chat_entry.pack(pady=10)

        self.send_button = tk.Button(self.chat_window, text="ارسال", font=('Arial', 12), command=self.send_message, bg='#4CAF50', fg='white')
        self.send_button.pack(pady=10)

        self.response_label = tk.Label(self.chat_window, text="", font=('Arial', 12), bg='#f0f0f0')
        self.response_label.pack(pady=10)

    def send_message(self):
        text = self.chat_entry.get()
        ai_response = get_response_from_api(text)
        bot = EitaaBot(token=self.token)
        response = bot.send_message(chat_id=self.chat_id, message=f"پاسخ سوال شما:\n{ai_response}\nمتن سوال:\n{text}")
        self.response_label.config(text=f"پاسخ: {ai_response}")

    def image_window(self):
        self.image_window = tk.Toplevel(self.root)
        self.image_window.title("ساخت تصویر")
        self.image_window.geometry("400x300")
        self.image_window.configure(bg='#f0f0f0')

        self.image_label = tk.Label(self.image_window, text="لطفاً متن تصویر را وارد کنید:", font=('Arial', 12), bg='#f0f0f0')
        self.image_label.pack(pady=10)

        self.image_entry = tk.Entry(self.image_window, font=('Arial', 12), width=30)
        self.image_entry.pack(pady=10)

        self.generate_button = tk.Button(self.image_window, text="ساخت تصویر", font=('Arial', 12), command=self.create_image, bg='#008CBA', fg='white')
        self.generate_button.pack(pady=10)

        self.image_display_label = tk.Label(self.image_window, text="", font=('Arial', 12), bg='#f0f0f0')
        self.image_display_label.pack(pady=10)

    def create_image(self):
        prompt = self.image_entry.get()
        image_file = generate_image(prompt, "downloaded_image.jpg")
        if image_file:
            self.image_display_label.config(text="تصویر با موفقیت ساخته شد.")
            bot = EitaaBot(token=self.token)
            response = bot.send_file(chat_id=self.chat_id, file_path=image_file, caption="عکس شما")
            messagebox.showinfo("موفقیت", "تصویر با موفقیت ارسال شد.")
        else:
            messagebox.showerror("خطا", "خطا در ساخت تصویر. لطفاً دوباره تلاش کنید.")

if __name__ == "__main__":
    root = tk.Tk()
    app = EitaaBotApp(root)
    root.mainloop()
