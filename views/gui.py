import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from tkinter.font import Font
from PIL import Image, ImageTk
import os


class ChatbotGUI:
    def __init__(self, root, chatbot):
        self.root = root
        self.chatbot = chatbot
        self.setup_ui()
        self.setup_menu()

    def setup_ui(self):
        self.root.title("CUZ Byo Campus Chatbot")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        self.root.configure(bg='#f0f0f0')

        # Custom fonts
        self.title_font = Font(family="Helvetica", size=12, weight="bold")
        self.text_font = Font(family="Helvetica", size=10)

        # Header
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(fill='x')

        # Try to load logo image
        try:
            logo_img = Image.open('assets/logo.png').resize((60, 60))
            self.logo = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(header_frame, image=self.logo, bg='#2c3e50')
            logo_label.pack(side='left', padx=10)
        except:
            pass  # Continue without logo if image not found

        title_label = tk.Label(
            header_frame,
            text="University Assistant Chatbot",
            font=self.title_font,
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(side='left', padx=10)

        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            width=80,
            height=20,
            state='disabled',
            font=self.text_font,
            bg='white',
            padx=10,
            pady=10
        )
        self.chat_display.pack(expand=True, fill='both', padx=10, pady=10)

        # Input frame
        input_frame = tk.Frame(self.root, bg='#f0f0f0')
        input_frame.pack(fill='x', padx=10, pady=(0, 10))

        self.user_input = tk.Entry(
            input_frame,
            width=60,
            font=self.text_font,
            relief=tk.GROOVE,
            borderwidth=2
        )
        self.user_input.pack(side='left', expand=True, fill='x', padx=(0, 10))
        self.user_input.bind("<Return>", self.send_message)

        self.send_button = tk.Button(
            input_frame,
            text="Send",
            command=self.send_message,
            bg='#3498db',
            fg='white',
            activebackground='#2980b9',
            font=self.text_font,
            relief=tk.RAISED,
            borderwidth=2
        )
        self.send_button.pack(side='right')

        # Welcome message
        self.display_message("Chatbot", "Welcome to CUZ BYO Assistant! I can help with:\n\n"
                                        "1. Admissions information\n"
                                        "2. Academic programs\n"
                                        "3. Student services\n\n"
                                        "Type your question or say 'admissions', 'programs', or 'services' to focus.",
                             "system")

    def setup_menu(self):
        menubar = tk.Menu(self.root)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Clear Chat", command=self.clear_chat)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

    def send_message(self, event=None):
        user_text = self.user_input.get().strip()
        if not user_text:
            return

        self.display_message("You", user_text)
        self.user_input.delete(0, tk.END)

        # Get response from chatbot
        response = self.chatbot.respond(user_text)
        self.display_message("Chatbot", response["response"], response["category"])

    def display_message(self, sender, message, category="user"):
        self.chat_display.configure(state='normal')

        # Configure tags for different message types
        self.chat_display.tag_config('user', foreground='#2c3e50', font=self.text_font)
        self.chat_display.tag_config('system', foreground='#3498db', font=self.text_font)
        self.chat_display.tag_config('admissions', foreground='#e74c3c', font=self.text_font)
        self.chat_display.tag_config('programs', foreground='#27ae60', font=self.text_font)
        self.chat_display.tag_config('services', foreground='#9b59b6', font=self.text_font)

        # Insert message with appropriate tag
        self.chat_display.insert(tk.END, f"{sender}: ", 'user' if sender == "You" else category.lower())
        self.chat_display.insert(tk.END, f"{message}\n\n", category.lower())

        self.chat_display.configure(state='disabled')
        self.chat_display.see(tk.END)

    def clear_chat(self):
        self.chat_display.configure(state='normal')
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.configure(state='disabled')
        self.display_message("Chatbot", "Chat cleared. How can I help you today?", "system")

    def show_about(self):
        messagebox.showinfo(
            "About CUZ BYO Campus Chatbot",
            "CUZ BYO Assistant Chatbot v1.0\n\n"
            "This AI-powered chatbot provides 24/7 assistance for:\n"
            "- Admissions information\n"
            "- Academic programs\n"
            "- Student services\n\n"
            "Developed for PyCharm"
        )