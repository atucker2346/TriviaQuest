import sqlite3
import json

conn = sqlite3.connect("questions.db")
cursor = conn.cursor()

# Categories
categories = [
    "General Knowledge",
    "Science",
    "History",
    "Pop Culture",
    "Sports"
]

# Insert categories
for name in categories:
    cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (name,))

# Fetch category IDs
cursor.execute("SELECT id, name FROM categories")
category_map = {name: cid for cid, name in cursor.fetchall()}

# Sample questions - 10 per category
sample_questions = [
    # General Knowledge (10 questions)
    {
        "category": "General Knowledge",
        "question": "What is the capital of France?",
        "choices": ["Paris", "Rome", "Berlin", "Madrid"],
        "correct": "Paris"
    },
    {
        "category": "General Knowledge",
        "question": "What is the largest ocean on Earth?",
        "choices": ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
        "correct": "Pacific Ocean"
    },
    {
        "category": "General Knowledge",
        "question": "How many continents are there?",
        "choices": ["5", "6", "7", "8"],
        "correct": "7"
    },
    {
        "category": "General Knowledge",
        "question": "What is the smallest country in the world?",
        "choices": ["Monaco", "Vatican City", "San Marino", "Liechtenstein"],
        "correct": "Vatican City"
    },
    {
        "category": "General Knowledge",
        "question": "What is the longest river in the world?",
        "choices": ["Amazon", "Nile", "Mississippi", "Yangtze"],
        "correct": "Nile"
    },
    {
        "category": "General Knowledge",
        "question": "What is the chemical symbol for gold?",
        "choices": ["Go", "Gd", "Au", "Ag"],
        "correct": "Au"
    },
    {
        "category": "General Knowledge",
        "question": "How many sides does a hexagon have?",
        "choices": ["4", "5", "6", "7"],
        "correct": "6"
    },
    {
        "category": "General Knowledge",
        "question": "What is the hardest natural substance on Earth?",
        "choices": ["Gold", "Iron", "Diamond", "Platinum"],
        "correct": "Diamond"
    },
    {
        "category": "General Knowledge",
        "question": "What is the largest mammal in the world?",
        "choices": ["African Elephant", "Blue Whale", "Giraffe", "Hippopotamus"],
        "correct": "Blue Whale"
    },
    {
        "category": "General Knowledge",
        "question": "What is the currency of Japan?",
        "choices": ["Yuan", "Won", "Yen", "Ringgit"],
        "correct": "Yen"
    },
    
    # Science (10 questions)
    {
        "category": "Science",
        "question": "What planet is known as the Red Planet?",
        "choices": ["Venus", "Mars", "Jupiter", "Saturn"],
        "correct": "Mars"
    },
    {
        "category": "Science",
        "question": "What is the chemical symbol for water?",
        "choices": ["H2O", "CO2", "O2", "NaCl"],
        "correct": "H2O"
    },
    {
        "category": "Science",
        "question": "What is the speed of light in a vacuum?",
        "choices": ["300,000 km/s", "150,000 km/s", "450,000 km/s", "600,000 km/s"],
        "correct": "300,000 km/s"
    },
    {
        "category": "Science",
        "question": "What is the smallest unit of matter?",
        "choices": ["Molecule", "Atom", "Electron", "Proton"],
        "correct": "Atom"
    },
    {
        "category": "Science",
        "question": "What gas do plants absorb from the atmosphere?",
        "choices": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"],
        "correct": "Carbon Dioxide"
    },
    {
        "category": "Science",
        "question": "What is the closest star to Earth?",
        "choices": ["Alpha Centauri", "Sirius", "The Sun", "Betelgeuse"],
        "correct": "The Sun"
    },
    {
        "category": "Science",
        "question": "What is the freezing point of water in Celsius?",
        "choices": ["-10°C", "0°C", "10°C", "32°C"],
        "correct": "0°C"
    },
    {
        "category": "Science",
        "question": "How many bones are in the adult human body?",
        "choices": ["196", "206", "216", "226"],
        "correct": "206"
    },
    {
        "category": "Science",
        "question": "What is the most abundant gas in Earth's atmosphere?",
        "choices": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Argon"],
        "correct": "Nitrogen"
    },
    {
        "category": "Science",
        "question": "What type of animal is a dolphin?",
        "choices": ["Fish", "Amphibian", "Mammal", "Reptile"],
        "correct": "Mammal"
    },
    
    # History (10 questions)
    {
        "category": "History",
        "question": "Who was the first President of the United States?",
        "choices": ["George Washington", "John Adams", "Thomas Jefferson", "James Monroe"],
        "correct": "George Washington"
    },
    {
        "category": "History",
        "question": "In which year did World War II end?",
        "choices": ["1943", "1944", "1945", "1946"],
        "correct": "1945"
    },
    {
        "category": "History",
        "question": "Who painted the Mona Lisa?",
        "choices": ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Michelangelo"],
        "correct": "Leonardo da Vinci"
    },
    {
        "category": "History",
        "question": "What was the name of the ship that brought the Pilgrims to America in 1620?",
        "choices": ["Santa Maria", "Mayflower", "Titanic", "Endeavour"],
        "correct": "Mayflower"
    },
    {
        "category": "History",
        "question": "Which ancient wonder of the world was located in Alexandria, Egypt?",
        "choices": ["Great Pyramid", "Hanging Gardens", "Colossus of Rhodes", "Lighthouse of Alexandria"],
        "correct": "Lighthouse of Alexandria"
    },
    {
        "category": "History",
        "question": "Who was the first woman to win a Nobel Prize?",
        "choices": ["Marie Curie", "Rosalind Franklin", "Jane Goodall", "Dorothy Hodgkin"],
        "correct": "Marie Curie"
    },
    {
        "category": "History",
        "question": "In which year did the Berlin Wall fall?",
        "choices": ["1987", "1988", "1989", "1990"],
        "correct": "1989"
    },
    {
        "category": "History",
        "question": "Who was known as the 'Iron Lady'?",
        "choices": ["Angela Merkel", "Margaret Thatcher", "Indira Gandhi", "Golda Meir"],
        "correct": "Margaret Thatcher"
    },
    {
        "category": "History",
        "question": "Which empire was ruled by Julius Caesar?",
        "choices": ["Greek Empire", "Roman Empire", "Byzantine Empire", "Ottoman Empire"],
        "correct": "Roman Empire"
    },
    {
        "category": "History",
        "question": "What was the name of the first satellite launched into space?",
        "choices": ["Apollo 1", "Sputnik 1", "Explorer 1", "Vanguard 1"],
        "correct": "Sputnik 1"
    },
    
    # Pop Culture (10 questions)
    {
        "category": "Pop Culture",
        "question": "Which singer is known as the 'Queen of Pop'?",
        "choices": ["Beyoncé", "Madonna", "Lady Gaga", "Ariana Grande"],
        "correct": "Madonna"
    },
    {
        "category": "Pop Culture",
        "question": "What is the highest-grossing film of all time?",
        "choices": ["Avatar", "Avengers: Endgame", "Titanic", "Star Wars: The Force Awakens"],
        "correct": "Avatar"
    },
    {
        "category": "Pop Culture",
        "question": "Which streaming service created the show 'Stranger Things'?",
        "choices": ["Hulu", "Netflix", "Amazon Prime", "Disney+"],
        "correct": "Netflix"
    },
    {
        "category": "Pop Culture",
        "question": "Who played Jack in the movie 'Titanic'?",
        "choices": ["Brad Pitt", "Leonardo DiCaprio", "Matt Damon", "Tom Cruise"],
        "correct": "Leonardo DiCaprio"
    },
    {
        "category": "Pop Culture",
        "question": "What is the name of Taylor Swift's 2014 album?",
        "choices": ["Red", "1989", "Reputation", "Lover"],
        "correct": "1989"
    },
    {
        "category": "Pop Culture",
        "question": "Which TV show features the character Walter White?",
        "choices": ["The Sopranos", "Breaking Bad", "Game of Thrones", "The Wire"],
        "correct": "Breaking Bad"
    },
    {
        "category": "Pop Culture",
        "question": "What is the name of the wizarding school in Harry Potter?",
        "choices": ["Hogwarts", "Beauxbatons", "Durmstrang", "Ilvermorny"],
        "correct": "Hogwarts"
    },
    {
        "category": "Pop Culture",
        "question": "Which band released the album 'Abbey Road'?",
        "choices": ["The Rolling Stones", "The Beatles", "Led Zeppelin", "Pink Floyd"],
        "correct": "The Beatles"
    },
    {
        "category": "Pop Culture",
        "question": "What is the name of the main character in 'The Hunger Games'?",
        "choices": ["Katniss Everdeen", "Hermione Granger", "Bella Swan", "Tris Prior"],
        "correct": "Katniss Everdeen"
    },
    {
        "category": "Pop Culture",
        "question": "Which social media platform was originally called 'TheFacebook'?",
        "choices": ["Twitter", "Instagram", "Facebook", "LinkedIn"],
        "correct": "Facebook"
    },
    
    # Sports (10 questions)
    {
        "category": "Sports",
        "question": "How many players are on a standard soccer team on the field?",
        "choices": ["9", "10", "11", "12"],
        "correct": "11"
    },
    {
        "category": "Sports",
        "question": "In which sport would you perform a slam dunk?",
        "choices": ["Volleyball", "Basketball", "Tennis", "Soccer"],
        "correct": "Basketball"
    },
    {
        "category": "Sports",
        "question": "How many rings are in the Olympic symbol?",
        "choices": ["4", "5", "6", "7"],
        "correct": "5"
    },
    {
        "category": "Sports",
        "question": "What is the maximum number of players on a basketball court at one time?",
        "choices": ["8", "10", "12", "14"],
        "correct": "10"
    },
    {
        "category": "Sports",
        "question": "In tennis, what is a score of zero called?",
        "choices": ["Nil", "Zero", "Love", "Nothing"],
        "correct": "Love"
    },
    {
        "category": "Sports",
        "question": "How many holes are in a standard round of golf?",
        "choices": ["16", "17", "18", "19"],
        "correct": "18"
    },
    {
        "category": "Sports",
        "question": "Which country won the FIFA World Cup in 2018?",
        "choices": ["Brazil", "Germany", "France", "Argentina"],
        "correct": "France"
    },
    {
        "category": "Sports",
        "question": "What is the distance of a marathon?",
        "choices": ["24.2 miles", "25.2 miles", "26.2 miles", "27.2 miles"],
        "correct": "26.2 miles"
    },
    {
        "category": "Sports",
        "question": "In baseball, how many strikes result in an out?",
        "choices": ["2", "3", "4", "5"],
        "correct": "3"
    },
    {
        "category": "Sports",
        "question": "Which sport is played at Wimbledon?",
        "choices": ["Golf", "Tennis", "Cricket", "Rugby"],
        "correct": "Tennis"
    }
]

# Clear existing questions (optional - comment out if you want to keep existing questions)
cursor.execute("DELETE FROM questions")

# Insert sample questions
for q in sample_questions:
    cursor.execute("""
        INSERT INTO questions (category_id, question, choices, correct_answer)
        VALUES (?, ?, ?, ?)
    """, (
        category_map[q["category"]],
        q["question"],
        json.dumps(q["choices"]),   # store as JSON string
        q["correct"]
    ))

conn.commit()
conn.close()

print("Sample questions added!")
