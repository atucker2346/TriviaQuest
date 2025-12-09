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
    
    # History (40 questions)
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
    {
        "category": "History",
        "question": "Which ancient empire built the mountain city of Machu Picchu?",
        "choices": ["Aztec Empire", "Inca Empire", "Mayan Empire", "Roman Empire"],
        "correct": "Inca Empire"
    },
    {
        "category": "History",
        "question": "In which century was Japan's samurai class officially abolished by the Meiji government?",
        "choices": ["16th century", "17th century", "18th century", "19th century"],
        "correct": "19th century"
    },
    {
        "category": "History",
        "question": "Which Egyptian queen famously aligned herself with both Julius Caesar and Mark Antony?",
        "choices": ["Nefertiti", "Cleopatra VII", "Hatshepsut", "Akhenaten"],
        "correct": "Cleopatra VII"
    },
    {
        "category": "History",
        "question": "Which Roman city was frozen in time by the eruption of Mount Vesuvius in 79 AD?",
        "choices": ["Athens", "Carthage", "Pompeii", "Alexandria"],
        "correct": "Pompeii"
    },
    {
        "category": "History",
        "question": "Which West African emperor is said to have given away so much gold on his pilgrimage to Mecca that he caused inflation?",
        "choices": ["Sundiata Keita", "Mansa Musa", "Shaka Zulu", "Haile Selassie"],
        "correct": "Mansa Musa"
    },
    {
        "category": "History",
        "question": "What 13th-century document forced King John of England to accept that even a king must follow the law?",
        "choices": ["Bill of Rights", "Domesday Book", "Magna Carta", "Petition of Right"],
        "correct": "Magna Carta"
    },
    {
        "category": "History",
        "question": "Which famously 'unsinkable' ocean liner sank on its first voyage in 1912?",
        "choices": ["Lusitania", "Titanic", "Olympic", "Britannic"],
        "correct": "Titanic"
    },
    {
        "category": "History",
        "question": "Which Roman emperor is legendarily blamed for 'fiddling while Rome burned'?",
        "choices": ["Augustus", "Nero", "Caligula", "Tiberius"],
        "correct": "Nero"
    },
    {
        "category": "History",
        "question": "Which ancient Mesoamerican civilization first turned cacao beans into a chocolate drink for rituals?",
        "choices": ["Aztecs", "Olmecs", "Mayans", "Toltecs"],
        "correct": "Mayans"
    },
    {
        "category": "History",
        "question": "Which massive stone monument in England has puzzled historians with its unknown original purpose?",
        "choices": ["Hadrian's Wall", "Stonehenge", "Carnac Stones", "Avebury Circle"],
        "correct": "Stonehenge"
    },
    {
        "category": "History",
        "question": "Which French king, obsessed with grandeur, was nicknamed the 'Sun King'?",
        "choices": ["Louis XIII", "Louis XIV", "Louis XV", "Louis XVI"],
        "correct": "Louis XIV"
    },
    {
        "category": "History",
        "question": "Which Mongol conqueror stitched together the largest land empire in history?",
        "choices": ["Kublai Khan", "Genghis Khan", "Tamerlane", "Attila"],
        "correct": "Genghis Khan"
    },
    {
        "category": "History",
        "question": "Which ancient library became a symbol of lost knowledge after being destroyed multiple times?",
        "choices": ["Library of Pergamon", "Library of Alexandria", "Nalanda University", "Celsus Library"],
        "correct": "Library of Alexandria"
    },
    {
        "category": "History",
        "question": "Who was the first human to orbit Earth in a spacecraft?",
        "choices": ["Alan Shepard", "Yuri Gagarin", "John Glenn", "Valentina Tereshkova"],
        "correct": "Yuri Gagarin"
    },
    {
        "category": "History",
        "question": "Which early 20th-century pandemic killed more people than World War I?",
        "choices": ["Asian Flu", "Spanish Flu", "Hong Kong Flu", "Black Death"],
        "correct": "Spanish Flu"
    },
    {
        "category": "History",
        "question": "Which civil rights icon refused to give up her bus seat in Montgomery, Alabama, in 1955?",
        "choices": ["Rosa Parks", "Ella Baker", "Coretta Scott King", "Fannie Lou Hamer"],
        "correct": "Rosa Parks"
    },
    {
        "category": "History",
        "question": "Which Indian leader led the 1930 Salt March to protest a British tax?",
        "choices": ["Jawaharlal Nehru", "Mahatma Gandhi", "Subhas Chandra Bose", "B. R. Ambedkar"],
        "correct": "Mahatma Gandhi"
    },
    {
        "category": "History",
        "question": "Which Caribbean nation became the first Black republic after a successful slave revolt in 1804?",
        "choices": ["Jamaica", "Haiti", "Barbados", "Trinidad and Tobago"],
        "correct": "Haiti"
    },
    {
        "category": "History",
        "question": "Which ancient Greek city-state was famous for training boys to be full-time soldiers from childhood?",
        "choices": ["Athens", "Corinth", "Sparta", "Thebes"],
        "correct": "Sparta"
    },
    {
        "category": "History",
        "question": "Which huge fortification was built over centuries to defend China from northern invaders?",
        "choices": ["Hadrian's Wall", "Great Wall of China", "Berlin Wall", "Wall of Babylon"],
        "correct": "Great Wall of China"
    },
    {
        "category": "History",
        "question": "Which 1815 battle finally ended Napoleon Bonaparte's comeback attempt?",
        "choices": ["Battle of Trafalgar", "Battle of Leipzig", "Battle of Waterloo", "Battle of Austerlitz"],
        "correct": "Battle of Waterloo"
    },
    {
        "category": "History",
        "question": "Which country's 1789 revolution turned King Louis XVI's monarchy into a cautionary tale?",
        "choices": ["Spain", "France", "Russia", "Prussia"],
        "correct": "France"
    },
    {
        "category": "History",
        "question": "Which famous U.S. landmark was a giant green gift from France, completed in 1886?",
        "choices": ["Mount Rushmore", "Statue of Liberty", "Golden Gate Bridge", "Lincoln Memorial"],
        "correct": "Statue of Liberty"
    },
    {
        "category": "History",
        "question": "Which astronaut left the first human footprints on the Moon in 1969?",
        "choices": ["Buzz Aldrin", "Yuri Gagarin", "Neil Armstrong", "Michael Collins"],
        "correct": "Neil Armstrong"
    },
    {
        "category": "History",
        "question": "Which country launched the first artificial satellite, Sputnik 1, in 1957?",
        "choices": ["United States", "Soviet Union", "China", "United Kingdom"],
        "correct": "Soviet Union"
    },
    {
        "category": "History",
        "question": "Which empire's soldiers in the American Revolution were nicknamed 'Redcoats' for their uniforms?",
        "choices": ["French Empire", "Spanish Empire", "British Empire", "Dutch Republic"],
        "correct": "British Empire"
    },
    {
        "category": "History",
        "question": "Which African country defeated Italy at the Battle of Adwa in 1896 and avoided colonization?",
        "choices": ["Nigeria", "Ethiopia", "Kenya", "Ghana"],
        "correct": "Ethiopia"
    },
    {
        "category": "History",
        "question": "Which legendary English outlaw is said to have robbed the rich to help the poor in Sherwood Forest?",
        "choices": ["King Arthur", "Robin Hood", "Guy Fawkes", "William Wallace"],
        "correct": "Robin Hood"
    },
    {
        "category": "History",
        "question": "Which Chicago crime boss turned Prohibition-era bootlegging into a criminal empire in the 1920s?",
        "choices": ["Bugsy Siegel", "John Dillinger", "Al Capone", "Lucky Luciano"],
        "correct": "Al Capone"
    },
    {
        "category": "History",
        "question": "Which decade is famously known as the 'Roaring Twenties' for its jazz, flappers, and speakeasies?",
        "choices": ["1900s", "1910s", "1920s", "1930s"],
        "correct": "1920s"
    },
    {
        "category": "History",
        "question": "Which ancient civilization carved giant stone heads on Easter Island?",
        "choices": ["Inca", "Rapa Nui", "Maya", "Polynesians"],
        "correct": "Rapa Nui"
    },
    {
        "category": "History",
        "question": "Which medieval leader united the Franks and was crowned the first Holy Roman Emperor?",
        "choices": ["Charlemagne", "Clovis I", "Frederick II", "William the Conqueror"],
        "correct": "Charlemagne"
    },
    {
        "category": "History",
        "question": "Which empire constructed the world's first known postal system?",
        "choices": ["Roman Empire", "Persian Empire", "Ottoman Empire", "Byzantine Empire"],
        "correct": "Persian Empire"
    },
    {
        "category": "History",
        "question": "Which Chinese dynasty built most of the Grand Canal connecting northern and southern China?",
        "choices": ["Tang Dynasty", "Song Dynasty", "Sui Dynasty", "Han Dynasty"],
        "correct": "Sui Dynasty"
    },
    {
        "category": "History",
        "question": "Which war was sparked by the assassination of Archduke Franz Ferdinand?",
        "choices": ["World War II", "Crimean War", "World War I", "Franco-Prussian War"],
        "correct": "World War I"
    },
    {
        "category": "History",
        "question": "Which famous female pharaoh wore a false beard to legitimize her rule?",
        "choices": ["Cleopatra VII", "Hatshepsut", "Nefertiti", "Sobekneferu"],
        "correct": "Hatshepsut"
    },
    {
        "category": "History",
        "question": "Which explorer completed the first recorded circumnavigation of the globe?",
        "choices": ["Christopher Columbus", "Ferdinand Magellan", "Marco Polo", "James Cook"],
        "correct": "Ferdinand Magellan"
    },
    {
        "category": "History",
        "question": "Which ancient city was home to the legendary Hanging Gardens?",
        "choices": ["Babylon", "Nineveh", "Ur", "Jericho"],
        "correct": "Babylon"
    },
    {
        "category": "History",
        "question": "Which North American civilization built the cliff dwellings at Mesa Verde?",
        "choices": ["Ancestral Puebloans", "Iroquois", "Cherokee", "Aztecs"],
        "correct": "Ancestral Puebloans"
    },
    {
        "category": "History",
        "question": "Which medieval conflict was fought between the houses of Lancaster and York?",
        "choices": ["Hundred Years' War", "War of the Roses", "Crusades", "Norman Conquest"],
        "correct": "War of the Roses"
    },
    {
        "category": "History",
        "question": "Which African kingdom was known for its powerful female warriors, the Agojie?",
        "choices": ["Axum", "Mali Empire", "Dahomey Kingdom", "Zimbabwe Kingdom"],
        "correct": "Dahomey Kingdom"
    },
    {
        "category": "History",
        "question": "Which leader introduced the policy of Perestroika in the late Soviet Union?",
        "choices": ["Joseph Stalin", "Leonid Brezhnev", "Mikhail Gorbachev", "Nikita Khrushchev"],
        "correct": "Mikhail Gorbachev"
    },
    {
        "category": "History",
        "question": "Which Italian city-state was ruled by the powerful Medici family during the Renaissance?",
        "choices": ["Rome", "Venice", "Florence", "Naples"],
        "correct": "Florence"
    },
    {
        "category": "History",
        "question": "Which American abolitionist led hundreds of enslaved people to freedom via the Underground Railroad?",
        "choices": ["Frederick Douglass", "Harriet Tubman", "Sojourner Truth", "Nat Turner"],
        "correct": "Harriet Tubman"
    },
    {
        "category": "History",
        "question": "Which battle marked the start of the American Revolutionary War?",
        "choices": ["Lexington and Concord", "Bunker Hill", "Yorktown", "Trenton"],
        "correct": "Lexington and Concord"
    },
    {
        "category": "History",
        "question": "Which Chinese admiral commanded massive treasure fleets during the Ming Dynasty?",
        "choices": ["Sun Tzu", "Qin Shi Huang", "Zheng He", "Kublai Khan"],
        "correct": "Zheng He"
    },
    {
        "category": "History",
        "question": "Which European event wiped out nearly one-third of the population in the 14th century?",
        "choices": ["Great Famine", "Black Death", "Hundred Years' War", "Little Ice Age"],
        "correct": "Black Death"
    },
    {
        "category": "History",
        "question": "Which ancient African kingdom built the Great Zimbabwe stone structures?",
        "choices": ["Benin Kingdom", "Nubia", "Zimbabwe Kingdom", "Mali Empire"],
        "correct": "Zimbabwe Kingdom"
    },
    {
        "category": "History",
        "question": "Which empire used quipus—knotted strings—to record information?",
        "choices": ["Inca Empire", "Maya Empire", "Olmec Empire", "Aztec Empire"],
        "correct": "Inca Empire"
    },
    {
        "category": "History",
        "question": "Which famous Viking is credited with reaching North America around 1000 AD?",
        "choices": ["Erik the Red", "Harald Bluetooth", "Ragnar Lothbrok", "Leif Erikson"],
        "correct": "Leif Erikson"
    },
    {
        "category": "History",
        "question": "Which ancient civilization built the city of Petra, carved directly into red sandstone cliffs?",
        "choices": ["Assyrians", "Nabataeans", "Phoenicians", "Persians"],
        "correct": "Nabataeans"
    },
    {
        "category": "History",
        "question": "Which European explorer claimed Canada for France in the 16th century?",
        "choices": ["Henry Hudson", "Samuel de Champlain", "Jacques Cartier", "John Cabot"],
        "correct": "Jacques Cartier"
    },
    {
        "category": "History",
        "question": "Which early civilization developed cuneiform, one of the world's first writing systems?",
        "choices": ["Babylonians", "Sumerians", "Hittites", "Phoenicians"],
        "correct": "Sumerians"
    },
    {
        "category": "History",
        "question": "Which English queen's 45-year reign oversaw the defeat of the Spanish Armada?",
        "choices": ["Elizabeth I", "Mary I", "Anne", "Victoria"],
        "correct": "Elizabeth I"
    },
    {
        "category": "History",
        "question": "Which empire used elite soldiers known as Janissaries?",
        "choices": ["Ottoman Empire", "Mughal Empire", "Persian Empire", "Byzantine Empire"],
        "correct": "Ottoman Empire"
    },
    {
        "category": "History",
        "question": "Which ancient city was famous for its Cyclopean walls, supposedly built by giants?",
        "choices": ["Memphis", "Knossos", "Mycenae", "Troy"],
        "correct": "Mycenae"
    },
    {
        "category": "History",
        "question": "Which Native American leader united tribes in resistance during Tecumseh's War?",
        "choices": ["Crazy Horse", "Sitting Bull", "Tecumseh", "Geronimo"],
        "correct": "Tecumseh"
    },
    {
        "category": "History",
        "question": "Which Asian kingdom built Angkor Wat, the largest religious monument in the world?",
        "choices": ["Khmer Empire", "Ayutthaya Kingdom", "Champa Kingdom", "Srivijaya Empire"],
        "correct": "Khmer Empire"
    },
    {
        "category": "History",
        "question": "Which Renaissance artist painted the ceiling of the Sistine Chapel?",
        "choices": ["Raphael", "Michelangelo", "Leonardo da Vinci", "Donatello"],
        "correct": "Michelangelo"
    },
    {
        "category": "History",
        "question": "Which South American revolutionary helped liberate multiple countries from Spanish rule?",
        "choices": ["Pancho Villa", "Che Guevara", "Simón Bolívar", "José Martí"],
        "correct": "Simón Bolívar"
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
