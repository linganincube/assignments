from models.chatbot import CUZChatbot
from views.gui import ChatbotGUI
import tkinter as tk


def main():
    # Initialize chatbot
    chatbot = CUZChatbot()

    # Create and run GUI
    root = tk.Tk()
    gui = ChatbotGUI(root, chatbot)
    root.mainloop()


if __name__ == "__main__":
    main()
