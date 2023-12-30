import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import datetime
import webbrowser
import pyttsx3
import pywhatkit as kit
import random
import wikipediaapi
import threading
import time
import sqlite3
class CustomChatbotMobileUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Abdul's Personal AI")
        self.window.configure(bg="#f0f0f0")  # Set background color
        # Initialize SQLite database connection
        self.connection = sqlite3.connect('chatbot_database.db')
        self.cursor = self.connection.cursor()
        self.create_tables()  # Create necessary tables if they don't exist
        # Create title label
        self.title_label = tk.Label(self.window, text="Ajiz's ChatDuo Hub", font=("Helvetica", 16), bg="#2ecc71", fg="white")
        self.title_label.grid(column=0, row=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Create scrolled text widget for chat display
        self.chat_display = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, width=40, height=15, bg="#ecf0f1")  # Set chat display background color
        self.chat_display.grid(column=0, row=1, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Create entry widget for user input
        self.user_input_entry = tk.Entry(self.window, width=30)
        self.user_input_entry.grid(column=0, row=2, padx=10, pady=10, sticky="ew")

        # Create button to send user input
        self.send_button = tk.Button(self.window, text="Send", command=self.process_user_input, bg="#3498db", fg="white")
        self.send_button.grid(column=1, row=2, padx=10, pady=10, sticky="ew")
        
        
        # Set row and column weights to make the chat display expandable
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        # Initialize the text-to-speech engine
        self.engine = pyttsx3.init()
        # Initialize the chatbot attributes
        self.awaiting_topic = False  # Define and initialize the 'awaiting_topic' attribute
        # Initialize the chatbot
        self.fun_facts = self.get_random_fun_fact()
        self.thoughts = [
            # ... (remaining thoughts)
        ]

        self.USER_AGENT = 'MyInfoApp/1.0 (https://myinfoapp.com)'
         # Initialize Wikipedia API
        self.wiki_wiki = wikipediaapi.Wikipedia('en', extract_format=wikipediaapi.ExtractFormat.WIKI, headers={'User-Agent': self.USER_AGENT})
        self.initialize_chatbot()
        self.thoughts = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "In the middle of every difficulty lies opportunity. - Albert Einstein",
            "Your time is limited, don't waste it living someone else's life. - Steve Jobs",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
            "Believe you can and you're halfway there. - Theodore Roosevelt",
            "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
            "The only limit to our realization of tomorrow will be our doubts of today. - Franklin D. Roosevelt",
            "Every strike brings me closer to the next home run. - Babe Ruth",
            "The only thing we have to fear is fear itself. - Franklin D. Roosevelt",
            "Change is the law of life. And those who look only to the past or present are certain to miss the future. - John F. Kennedy",
            "The best way to predict the future is to create it. - Peter Drucker",
            "Don't cry because it's over, smile because it happened. - Dr. Seuss",
            "Success is not the key to happiness. Happiness is the key to success. If you love what you are doing, you will be successful. - Albert Schweitzer",
            "You miss 100% of the shots you don't take. - Wayne Gretzky",
            "Whether you think you can or you think you can't, you're right. - Henry Ford",
            "The greatest glory in living lies not in never falling, but in rising every time we fall. - Nelson Mandela",
            "The only thing standing between you and your goal is the story you keep telling yourself as to why you can't achieve it. - Jordan Belfort",
            "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill",
            "It is our choices, Harry, that show what we truly are, far more than our abilities. - J.K. Rowling",
            "In the end, we will remember not the words of our enemies, but the silence of our friends. - Martin Luther King Jr.",
            "The way to get started is to quit talking and begin doing. - Walt Disney",
            "Life is what happens when you're busy making other plans. - John Lennon",
            "Spread love everywhere you go. Let no one ever come to you without leaving happier. - Mother Teresa",
            "The power of imagination makes us infinite. - John Muir",
            "It's not the load that breaks you down, it's the way you carry it. - Lou Holtz",
            "Believe in yourself and all that you are. Know that there is something inside you that is greater than any obstacle. - Christian D. Larson",
            "Happiness is not by chance, but by choice. - Jim Rohn",
            "Dream big and dare to fail. - Norman Vaughan",
            "You are never too old to set another goal or to dream a new dream. - C.S. Lewis",
            # Add more thoughts as needed
        ]
        
    def create_tables(self):
        # Create a table to store conversation history if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS ConversationHistory (
                               ID INTEGER PRIMARY KEY AUTOINCREMENT,
                               UserInput TEXT,
                               BotResponse TEXT,
                               Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                             )''')
        self.connection.commit()
        
    def insert_conversation(self, user_input, bot_response):
        # Insert a new conversation into the ConversationHistory table
        self.cursor.execute("INSERT INTO ConversationHistory (UserInput, BotResponse) VALUES (?, ?)", (user_input, bot_response))
        self.connection.commit()
        
    def create_widgets(self):
        # Create the scrolled text widget for chat display
        self.chat_display = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, width=40, height=15, bg="#ecf0f1")
        self.chat_display.grid(column=0, row=1, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Create the user input entry with slightly curved borders
        self.user_input_entry = tk.Entry(self.window, width=30, relief=tk.RIDGE, bd=2, border=5)  # Use 'relief' and 'bd' options
        self.user_input_entry.grid(column=0, row=2, padx=10, pady=10, sticky="ew")

        # Create the 'Send' button
        self.send_button = tk.Button(self.window, text="Send", command=self.process_user_input, bg="#3498db", fg="white")
        self.send_button.grid(column=1, row=2, padx=10, pady=10, sticky="ew")

        # Create the 'View History' button
        self.view_history_button = tk.Button(self.window, text="View History", command=self.view_conversation_history,
                                             bg="#2ecc71", fg="white")  # Change background color here
        self.view_history_button.grid(column=0, row=3, columnspan=2, padx=10, pady=10, sticky="ew")
        
        # Set row and column weights to make the chat display expandable
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        
        # Bind the 'Return' key to the user input entry
        self.user_input_entry.bind('<Return>', self.bind_enter_key)
        
    def view_conversation_history(self):
        # Create a new window (top level window) to display conversation history
        self.history_window = tk.Toplevel(self.window)
        self.history_window.title("Conversation History")
        self.history_window.configure(bg="#f0f0f0")
        
        # Retrieve conversation history from the database
        self.cursor.execute("SELECT UserInput, BotResponse, Timestamp FROM ConversationHistory")
        history = self.cursor.fetchall()
        
        # Create scrolled text widget for displaying conversation history
        history_display = scrolledtext.ScrolledText(self.history_window, wrap=tk.WORD, width=40, height=15, bg="#ecf0f1")
        history_display.grid(column=0, row=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        # Clear the chat display
        self.chat_display.delete('1.0', tk.END)

        # Display the conversation history in the chat display widget
        for row in history:
            user_input, bot_response, timestamp = row
            history_display.insert(tk.END, f"User: {user_input}\nBot: {bot_response}\nTimestamp: {timestamp}\n\n")

            
        # Create the 'Delete History' button within the history window
        delete_history_button = tk.Button(self.history_window, text="Delete History", command=self.delete_conversation_history,
                                          bg="#e74c3c", fg="white")  # Change background color here
        delete_history_button.grid(column=0, row=1, columnspan=2, padx=10, pady=10, sticky="ew")

        # Create a 'Close' button to return to the main window
        close_button = tk.Button(self.history_window, text="Close", command=self.close_history_window)
        close_button.grid(column=0, row=2, columnspan=2, padx=10, pady=10, sticky="ew")
        
    def close_history_window(self):
        # Close the history window
        self.history_window.destroy()
        
    def delete_conversation_history(self):
        # Delete conversation history from the database
        self.cursor.execute("DELETE FROM ConversationHistory")
        self.connection.commit()
        self.chat_display.delete('1.0', tk.END)  # Clear the chat display after deletion
        # Show a message indicating successful deletion
        messagebox.showinfo("Success", "Chat History Deleted Successfully")
    
    
    
    def initialize_chatbot(self):
        greet_message = self.greet("Abdul Ajiz")
        self.speak(greet_message)  # Provide the initial greeting response in voice
        self.add_message(greet_message)  # Print the greeting message in text

    def greet(self, name):
        current_time = datetime.datetime.now()
        if current_time.hour < 12:
            greeting = f"Good morning, {name}!"
        elif 12 <= current_time.hour < 18:
            greeting = f"Good afternoon, {name}!" 
        else:
            greeting = f"Good evening, {name}!"
        return greeting

    def positive_response(self):
        responses = ["I'm doing well, thank you!", "I'm here to assist you!", "Feeling great! How can I help you?"]
        return responses

    def get_random_fun_fact(self):
        fun_facts = [
            "Did you know the shortest war in history was between Britain and Zanzibar, lasting only 38 minutes?",
            "Did you know the electric chair was invented by a dentist?",
            "Did you know that in terms of mass, the total biomass of ants on Earth is roughly equal to the total biomass of all the humans on Earth?",
            "Did you know a group of crows is called a 'murder'?",
            "Did you know bananas are berries, but strawberries aren't?",
            "Did you know the Eiffel Tower can be 15 cm taller during the summer due to the expansion of the iron from the heat?",
            "Did you know the unicorn is the national animal of Scotland?",
            "Did you know a day on Venus is longer than a year on Venus?",
            "Did you know honey never spoils; archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly good to eat?",
            "Did you know the world's oceans contain gold, but in such small amounts that it's not feasible to extract it?",
            "Did you know the longest hiccuping spree lasted 68 years?",
            "Did you know there are more possible iterations of a game of chess than there are atoms in the known universe?",
            "Did you know the 'D' in D-Day stands for 'Day.' The term is used to denote the start date of a military operation.",
            "Did you know there's enough gold in the Earth's core to coat the planet's entire surface in 1.5 feet of the precious metal?",
            "Did you know a single bolt of lightning contains enough energy to toast 100,000 slices of bread?",
            "Did you know octopuses have three hearts? Two pump blood to the gills, and one pumps it to the rest of the body.",
            "Did you know Maine is the closest U.S. state to Africa?",
            "Did you know that in Japan, letting a sumo wrestler make your baby cry is considered good luck?",
            "Did you know the oldest known sample of the smallpox virus has been found in the teeth of a 17th-century child buried in Lithuania?"
            # ... (remaining fun facts)
        ]

        # Shuffle the facts to ensure they are provided in a random order
        random.shuffle(fun_facts)
        return random.choice(fun_facts)

    def get_random_thought(self):
        if self.thoughts:
            thought = random.choice(self.thoughts)
            self.thoughts.remove(thought)
            return thought
        else:
            return "I've run out of thoughts for today."

    def perform_math_calculation(self, expression):
        try:
            result = eval(expression)
            return f"The result of {expression} is {result}"
        except Exception as e:
            return f"Sorry, I couldn't perform the calculation. Error: {e}"
    def get_wikipedia_summary(self, query, max_chars=600):
        # Get the page for the given query
        page_py = self.wiki_wiki.page(query)

        if not page_py.exists():
            return f"Sorry, I couldn't find information on '{query}'."

        # Get the full summary
        full_summary = page_py.text

        # Check if the summary exceeds the maximum characters
        if len(full_summary) > max_chars:
            # Find the last complete sentence within the character limit
            last_sentence = full_summary[:max_chars].rsplit('.', 1)[0] + '.'
            return last_sentence
        else:
            return full_summary
    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def add_message(self, message):
        self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.yview(tk.END)  # Scroll to the bottom to show the latest message

    def process_user_input(self):
        user_input = self.user_input_entry.get()
        self.add_message(f"You: {user_input}")

        # Process user input using the chatbot logic
        response = self.process_chatbot_input(user_input)
        if response == "Please provide a topic for information.":
            self.awaiting_topic = True
        self.add_message(f"Chatbot: {response}")
        self.insert_conversation(user_input, response)  # Store conversation in the database
        speak_thread = threading.Thread(target=self.delayed_speak, args=(response,))
        speak_thread.start()
        
        self.user_input_entry.delete(0, tk.END)  # Clear the user input entry
        
    def delayed_speak(self, text):
        time.sleep(0.1)  # Adjust the delay time as needed (in seconds)
        self.speak(text)
    def bind_enter_key(self, event):
        self.process_user_input()


    def process_chatbot_input(self, user_input):
        
        user_input_lower = user_input.lower()  # Convert user input to lowercase

        if any(greeting in user_input_lower for greeting in ["hello", "hi"]):
            return "Hello there! How can I help you?"
    # ... (rest of your code)

        if "hello" in user_input:
            return "Hello there! How can I help you?"
        elif any(keyword.lower() in user_input.lower() for keyword in ["calculate", "compute", "what is"]):
            parts = user_input.split(maxsplit=1)
            if len(parts) > 1:
                expression = parts[1]
                return self.perform_math_calculation(expression)
            else:
                return "Please provide a mathematical expression to calculate."
        elif "fact" in user_input_lower:
            return self.get_random_fun_fact()
        elif "thought" in user_input_lower:
            return self.get_random_thought()
        elif "open" in user_input:
            parts = user_input.split()
            if len(parts) > 1:
                website = parts[-1]
                webbrowser.open(f"https://www.{website}.com")
                return f"Opening {website} in your web browser."
            else:
                return "Please provide a website to open."
        elif "play" in user_input_lower:
            query = user_input_lower.replace("play", "").strip()
            if query:
                kit.playonyt(query)
                return f"Playing {query} on YouTube."
            else:
                return "Please provide a song or video name to play on YouTube."

        
        elif any(keyword.lower() in user_input_lower for keyword in ["exit", "goodbye", "bye"]):
            return "Goodbye! Have a great day Abdul Ajiz!."
        elif any(keyword in user_input for keyword in ["how are you", "are you there"]):
            responses = self.positive_response()
            return responses[0]  # Choose one of the positive responses
        elif "date" in user_input_lower:
            current_date = datetime.date.today().strftime("%A, %B %d, %Y")
            return f"Today is {current_date}"
        elif "time" in user_input_lower:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            return f"The current time is {current_time}"
        elif "info" in user_input_lower:
            # If "info" is detected, prompt for the topic
            return "Please provide a topic for information."
        elif self.awaiting_topic:
            # If awaiting_topic is True, treat the input as the topic
            result = self.get_wikipedia_summary(user_input)  # Pass the user input as the topic
            self.awaiting_topic = False  # Set awaiting_topic back to False
            return result
        else:
            return "I'm sorry, I didn't understand that. Can you please clarify?"





    def __del__(self): 
        # Close the database connection when the instance is destroyed
        self.connection.close()
    def run(self):
        self.create_widgets()
        self.window.mainloop()

# Create an instance of the CustomChatbotMobileUI class and run the custom UI
custom_chatbot_ui = CustomChatbotMobileUI()
custom_chatbot_ui.run()
