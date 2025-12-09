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

# Sample questions - 40 per category
sample_questions = [
    # General Knowledge (40 questions)
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
    {
        "category": "General Knowledge",
        "question": "What mythical creature is said to guard a pot of gold at the end of a rainbow?",
        "choices": ["Fairy", "Leprechaun", "Gnome", "Elf"],
        "correct": "Leprechaun"
    },
    {
        "category": "General Knowledge",
        "question": "Which month has an extra day during a leap year?",
        "choices": ["January", "February", "March", "April"],
        "correct": "February"
    },
    {
        "category": "General Knowledge",
        "question": "Which animal is known as the 'King of the Jungle'?",
        "choices": ["Tiger", "Bear", "Lion", "Leopard"],
        "correct": "Lion"
    },
    {
        "category": "General Knowledge",
        "question": "Which continent is home to the Amazon Rainforest?",
        "choices": ["Africa", "South America", "Asia", "Australia"],
        "correct": "South America"
    },
    {
        "category": "General Knowledge",
        "question": "What is the name of the fairy in Peter Pan?",
        "choices": ["Tinker Bell", "Fawn", "Iridessa", "Silvermist"],
        "correct": "Tinker Bell"
    },
    {
        "category": "General Knowledge",
        "question": "Which bird is known for being able to mimic human speech?",
        "choices": ["Crow", "Parrot", "Sparrow", "Owl"],
        "correct": "Parrot"
    },
    {
        "category": "General Knowledge",
        "question": "Which country is famous for inventing pizza?",
        "choices": ["France", "Italy", "Greece", "Spain"],
        "correct": "Italy"
    },
    {
        "category": "General Knowledge",
        "question": "What is the tallest animal in the world?",
        "choices": ["Elephant", "Giraffe", "Horse", "Camel"],
        "correct": "Giraffe"
    },
    {
        "category": "General Knowledge",
        "question": "What natural disaster is measured using the Richter scale?",
        "choices": ["Hurricanes", "Earthquakes", "Tornadoes", "Floods"],
        "correct": "Earthquakes"
    },
    {
        "category": "General Knowledge",
        "question": "Which fruit is known as the 'king of fruits' in many Asian countries?",
        "choices": ["Mango", "Pineapple", "Durian", "Papaya"],
        "correct": "Durian"
    },
    {
        "category": "General Knowledge",
        "question": "Which everyday tool did the ancient Egyptians invent?",
        "choices": ["Hammer", "Toothpaste", "Pencil", "Screwdriver"],
        "correct": "Toothpaste"
    },
    {
        "category": "General Knowledge",
        "question": "What is the most widely spoken language in the world?",
        "choices": ["English", "Spanish", "Mandarin Chinese", "Hindi"],
        "correct": "Mandarin Chinese"
    },
    {
        "category": "General Knowledge",
        "question": "What geometric shape is a STOP sign?",
        "choices": ["Hexagon", "Octagon", "Pentagon", "Heptagon"],
        "correct": "Octagon"
    },
    {
        "category": "General Knowledge",
        "question": "Which animal sleeps up to 22 hours a day?",
        "choices": ["Koala", "Sloth", "Cat", "Bat"],
        "correct": "Koala"
    },
    {
        "category": "General Knowledge",
        "question": "Which organ helps humans breathe?",
        "choices": ["Heart", "Liver", "Lungs", "Kidneys"],
        "correct": "Lungs"
    },
    {
        "category": "General Knowledge",
        "question": "What is the primary ingredient in guacamole?",
        "choices": ["Avocado", "Cucumber", "Lettuce", "Peas"],
        "correct": "Avocado"
    },
    {
        "category": "General Knowledge",
        "question": "Which continent has the most countries?",
        "choices": ["Asia", "Africa", "Europe", "South America"],
        "correct": "Africa"
    },
    {
        "category": "General Knowledge",
        "question": "What is a baby kangaroo called?",
        "choices": ["Cub", "Joey", "Fawn", "Calf"],
        "correct": "Joey"
    },
    {
        "category": "General Knowledge",
        "question": "Which famous scientist developed the theory of relativity?",
        "choices": ["Isaac Newton", "Albert Einstein", "Nikola Tesla", "Marie Curie"],
        "correct": "Albert Einstein"
    },
    {
        "category": "General Knowledge",
        "question": "What is the fastest land animal?",
        "choices": ["Cheetah", "Lion", "Horse", "Falcon"],
        "correct": "Cheetah"
    },
    {
        "category": "General Knowledge",
        "question": "Which musical instrument has black and white keys?",
        "choices": ["Guitar", "Piano", "Violin", "Flute"],
        "correct": "Piano"
    },
    {
        "category": "General Knowledge",
        "question": "What is the boiling point of water in Celsius?",
        "choices": ["50°C", "75°C", "90°C", "100°C"],
        "correct": "100°C"
    },
    {
        "category": "General Knowledge",
        "question": "Which animal can rotate its head nearly 270 degrees?",
        "choices": ["Eagle", "Owl", "Hawk", "Falcon"],
        "correct": "Owl"
    },
    {
        "category": "General Knowledge",
        "question": "How many colors are there in a traditional rainbow?",
        "choices": ["5", "6", "7", "8"],
        "correct": "7"
    },
    {
        "category": "General Knowledge",
        "question": "Which country is known for giving the world sushi?",
        "choices": ["China", "Japan", "Thailand", "South Korea"],
        "correct": "Japan"
    },
    {
        "category": "General Knowledge",
        "question": "What do you call a group of lions?",
        "choices": ["Pack", "Pride", "Herd", "Flock"],
        "correct": "Pride"
    },
    {
        "category": "General Knowledge",
        "question": "Which organ pumps blood throughout the body?",
        "choices": ["Liver", "Heart", "Brain", "Kidneys"],
        "correct": "Heart"
    },
    {
        "category": "General Knowledge",
        "question": "Which instrument is used to measure temperature?",
        "choices": ["Thermometer", "Barometer", "Hygrometer", "Speedometer"],
        "correct": "Thermometer"
    },
    {
        "category": "General Knowledge",
        "question": "Which planet has a giant red storm known as the Great Red Spot?",
        "choices": ["Mars", "Jupiter", "Saturn", "Uranus"],
        "correct": "Jupiter"
    },
    {
        "category": "General Knowledge",
        "question": "Which creature is known for changing its color to camouflage?",
        "choices": ["Frog", "Lizard", "Chameleon", "Snake"],
        "correct": "Chameleon"
    },
    
    # Science (40 questions)
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
    {
        "category": "Science",
        "question": "What force keeps planets in orbit around the Sun?",
        "choices": ["Magnetism", "Gravity", "Friction", "Electricity"],
        "correct": "Gravity"
    },
    {
        "category": "Science",
        "question": "What is the powerhouse of the cell?",
        "choices": ["Ribosome", "Nucleus", "Mitochondria", "Golgi Apparatus"],
        "correct": "Mitochondria"
    },
    {
        "category": "Science",
        "question": "What part of the human eye controls how much light enters?",
        "choices": ["Cornea", "Iris", "Retina", "Lens"],
        "correct": "Iris"
    },
    {
        "category": "Science",
        "question": "What do bees collect from flowers to make honey?",
        "choices": ["Water", "Nectar", "Pollen", "Sap"],
        "correct": "Nectar"
    },
    {
        "category": "Science",
        "question": "What is the largest organ in the human body?",
        "choices": ["Heart", "Liver", "Skin", "Lungs"],
        "correct": "Skin"
    },
    {
        "category": "Science",
        "question": "What kind of energy is stored in food?",
        "choices": ["Thermal energy", "Kinetic energy", "Chemical energy", "Solar energy"],
        "correct": "Chemical energy"
    },
    {
        "category": "Science",
        "question": "Which planet has the most moons?",
        "choices": ["Mars", "Jupiter", "Neptune", "Saturn"],
        "correct": "Saturn"
    },
    {
        "category": "Science",
        "question": "What is the process by which plants release oxygen?",
        "choices": ["Transpiration", "Photosynthesis", "Respiration", "Fermentation"],
        "correct": "Photosynthesis"
    },
    {
        "category": "Science",
        "question": "Which scientist proposed the three laws of motion?",
        "choices": ["Albert Einstein", "Isaac Newton", "Nikola Tesla", "Galileo Galilei"],
        "correct": "Isaac Newton"
    },
    {
        "category": "Science",
        "question": "What is the most common element in the universe?",
        "choices": ["Oxygen", "Hydrogen", "Helium", "Carbon"],
        "correct": "Hydrogen"
    },
    {
        "category": "Science",
        "question": "What device is used to measure earthquakes?",
        "choices": ["Barometer", "Seismograph", "Thermometer", "Hygrometer"],
        "correct": "Seismograph"
    },
    {
        "category": "Science",
        "question": "What type of cloud is associated with thunderstorms?",
        "choices": ["Cirrus", "Stratus", "Cumulonimbus", "Altostratus"],
        "correct": "Cumulonimbus"
    },
    {
        "category": "Science",
        "question": "Which vitamin do humans produce when exposed to sunlight?",
        "choices": ["Vitamin A", "Vitamin C", "Vitamin D", "Vitamin B12"],
        "correct": "Vitamin D"
    },
    {
        "category": "Science",
        "question": "How many chromosomes do humans typically have?",
        "choices": ["42", "44", "46", "48"],
        "correct": "46"
    },
    {
        "category": "Science",
        "question": "What gas do humans exhale?",
        "choices": ["Oxygen", "Carbon Dioxide", "Helium", "Nitrogen"],
        "correct": "Carbon Dioxide"
    },
    {
        "category": "Science",
        "question": "What part of the brain controls balance and coordination?",
        "choices": ["Cerebrum", "Cerebellum", "Brainstem", "Hypothalamus"],
        "correct": "Cerebellum"
    },
    {
        "category": "Science",
        "question": "Which metal is liquid at room temperature besides mercury?",
        "choices": ["Sodium", "Gallium", "Aluminum", "Copper"],
        "correct": "Gallium"
    },
    {
        "category": "Science",
        "question": "What kind of waves are used in microwave ovens?",
        "choices": ["Radio waves", "X-rays", "Gamma rays", "Ultraviolet waves"],
        "correct": "Radio waves"
    },
    {
        "category": "Science",
        "question": "What is the term for animals that eat only plants?",
        "choices": ["Carnivores", "Herbivores", "Omnivores", "Detritivores"],
        "correct": "Herbivores"
    },
    {
        "category": "Science",
        "question": "What part of Earth lies beneath the crust?",
        "choices": ["Core", "Mantle", "Lithosphere", "Asthenosphere"],
        "correct": "Mantle"
    },
    {
        "category": "Science",
        "question": "What is the name for molten rock beneath Earth’s surface?",
        "choices": ["Lava", "Magma", "Basalt", "Obsidian"],
        "correct": "Magma"
    },
    {
        "category": "Science",
        "question": "Which blood type is considered the universal donor?",
        "choices": ["A", "AB", "O-", "O+"],
        "correct": "O-"
    },
    {
        "category": "Science",
        "question": "Which gas makes up most of the Sun?",
        "choices": ["Hydrogen", "Nitrogen", "Carbon", "Helium"],
        "correct": "Hydrogen"
    },
    {
        "category": "Science",
        "question": "What do you call a scientist who studies rocks?",
        "choices": ["Biologist", "Chemist", "Geologist", "Meteorologist"],
        "correct": "Geologist"
    },
    {
        "category": "Science",
        "question": "How long does Earth take to orbit the Sun?",
        "choices": ["24 hours", "30 days", "365 days", "730 days"],
        "correct": "365 days"
    },
    {
        "category": "Science",
        "question": "What is the primary gas in Earth’s ozone layer?",
        "choices": ["Ozone", "Oxygen", "Carbon Dioxide", "Hydrogen"],
        "correct": "Ozone"
    },
    {
        "category": "Science",
        "question": "Which organ pumps blood throughout the human body?",
        "choices": ["Liver", "Lungs", "Heart", "Kidneys"],
        "correct": "Heart"
    },
    {
        "category": "Science",
        "question": "What phenomenon causes the sky to appear blue?",
        "choices": ["Reflection", "Refraction", "Rayleigh Scattering", "Absorption"],
        "correct": "Rayleigh Scattering"
    },
    {
        "category": "Science",
        "question": "What type of animal lays eggs but is not a bird?",
        "choices": ["Whale", "Kangaroo", "Platypus", "Bat"],
        "correct": "Platypus"
    },
    {
        "category": "Science",
        "question": "What instrument is used to view very small objects like cells?",
        "choices": ["Telescope", "Periscope", "Microscope", "Endoscope"],
        "correct": "Microscope"
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
    {
        "category": "Pop Culture",
        "question": "Which artist created the viral hit 'Blinding Lights'?",
        "choices": ["The Weeknd", "Drake", "Post Malone", "Justin Bieber"],
        "correct": "The Weeknd"
    },
    {
        "category": "Pop Culture",
        "question": "Which animated series features the characters Finn and Jake?",
        "choices": ["Adventure Time", "Steven Universe", "Regular Show", "Gravity Falls"],
        "correct": "Adventure Time"
    },
    {
        "category": "Pop Culture",
        "question": "Who hosted the TV show 'The Oprah Winfrey Show'?",
        "choices": ["Ellen DeGeneres", "Oprah Winfrey", "Wendy Williams", "Tyra Banks"],
        "correct": "Oprah Winfrey"
    },
    {
        "category": "Pop Culture",
        "question": "Which musician is known for the album 'Thriller'?",
        "choices": ["Prince", "Michael Jackson", "James Brown", "Stevie Wonder"],
        "correct": "Michael Jackson"
    },
    {
        "category": "Pop Culture",
        "question": "Which video game franchise features the character Master Chief?",
        "choices": ["Halo", "Destiny", "Mass Effect", "Call of Duty"],
        "correct": "Halo"
    },
    {
        "category": "Pop Culture",
        "question": "What is the name of Beyoncé's fanbase?",
        "choices": ["Swifties", "Barbz", "Beehive", "Navy"],
        "correct": "Beehive"
    },
    {
        "category": "Pop Culture",
        "question": "Who voices Donkey in the 'Shrek' movie franchise?",
        "choices": ["Eddie Murphy", "Kevin Hart", "Chris Rock", "Will Smith"],
        "correct": "Eddie Murphy"
    },
    {
        "category": "Pop Culture",
        "question": "Which Netflix series made the red jumpsuit and Salvador Dali mask iconic?",
        "choices": ["Money Heist", "Dark", "Narcos", "Elite"],
        "correct": "Money Heist"
    },
    {
        "category": "Pop Culture",
        "question": "Who created the Marvel character Black Panther?",
        "choices": ["Stan Lee & Jack Kirby", "Steve Ditko", "Frank Miller", "Todd McFarlane"],
        "correct": "Stan Lee & Jack Kirby"
    },
    {
        "category": "Pop Culture",
        "question": "Which singer released the hit song 'Bad Romance'?",
        "choices": ["Lady Gaga", "Rihanna", "Adele", "Katy Perry"],
        "correct": "Lady Gaga"
    },
    {
        "category": "Pop Culture",
        "question": "Which long-running cartoon features a baby named Stewie?",
        "choices": ["The Simpsons", "Family Guy", "American Dad", "Bob's Burgers"],
        "correct": "Family Guy"
    },
    {
        "category": "Pop Culture",
        "question": "Which rapper is known for the album 'To Pimp a Butterfly'?",
        "choices": ["Kendrick Lamar", "J. Cole", "Kanye West", "Lil Wayne"],
        "correct": "Kendrick Lamar"
    },
    {
        "category": "Pop Culture",
        "question": "Which fantasy series features dragons and the Iron Throne?",
        "choices": ["The Witcher", "Game of Thrones", "Shadow and Bone", "The Wheel of Time"],
        "correct": "Game of Thrones"
    },
    {
        "category": "Pop Culture",
        "question": "What popular app became famous for short dance and lip-sync videos?",
        "choices": ["Snapchat", "Vine", "TikTok", "Triller"],
        "correct": "TikTok"
    },
    {
        "category": "Pop Culture",
        "question": "Which 2000s TV show centered around a teenage detective named Veronica?",
        "choices": ["Buffy the Vampire Slayer", "Veronica Mars", "Pretty Little Liars", "Charmed"],
        "correct": "Veronica Mars"
    },
    {
        "category": "Pop Culture",
        "question": "Which boy band performed the hit 'I Want It That Way'?",
        "choices": ["NSYNC", "Backstreet Boys", "One Direction", "98 Degrees"],
        "correct": "Backstreet Boys"
    },
    {
        "category": "Pop Culture",
        "question": "Which actress starred as Miranda Priestly in 'The Devil Wears Prada'?",
        "choices": ["Julia Roberts", "Meryl Streep", "Anne Hathaway", "Sandra Bullock"],
        "correct": "Meryl Streep"
    },
    {
        "category": "Pop Culture",
        "question": "Which video game series includes locations like Vice City and Los Santos?",
        "choices": ["Saints Row", "Grand Theft Auto", "Cyberpunk", "Watch Dogs"],
        "correct": "Grand Theft Auto"
    },
    {
        "category": "Pop Culture",
        "question": "Which K-pop group released the hit song 'Dynamite'?",
        "choices": ["BLACKPINK", "EXO", "BTS", "TWICE"],
        "correct": "BTS"
    },
    {
        "category": "Pop Culture",
        "question": "Who is the creator of the animated series 'Rick and Morty'?",
        "choices": ["Justin Roiland & Dan Harmon", "Matt Groening", "Mike Judge", "Seth MacFarlane"],
        "correct": "Justin Roiland & Dan Harmon"
    },
    {
        "category": "Pop Culture",
        "question": "Which singer became famous from the Disney show 'Hannah Montana'?",
        "choices": ["Selena Gomez", "Miley Cyrus", "Demi Lovato", "Ariana Grande"],
        "correct": "Miley Cyrus"
    },
    {
        "category": "Pop Culture",
        "question": "What movie features the character Jack Sparrow?",
        "choices": ["Pirates of the Caribbean", "Hook", "Treasure Island", "Swiss Family Robinson"],
        "correct": "Pirates of the Caribbean"
    },
    {
        "category": "Pop Culture",
        "question": "Which social media platform uses a ghost as its logo?",
        "choices": ["Instagram", "Snapchat", "Telegram", "Discord"],
        "correct": "Snapchat"
    },
    {
        "category": "Pop Culture",
        "question": "Which musical features the songs 'My Shot' and 'The Room Where It Happens'?",
        "choices": ["Hamilton", "Les Misérables", "Wicked", "Rent"],
        "correct": "Hamilton"
    },
    {
        "category": "Pop Culture",
        "question": "Who played the character Black Widow in the Marvel Cinematic Universe?",
        "choices": ["Scarlett Johansson", "Brie Larson", "Elizabeth Olsen", "Natalie Portman"],
        "correct": "Scarlett Johansson"
    },
    {
        "category": "Pop Culture",
        "question": "Which Pixar movie features the characters Joy, Sadness, and Anger?",
        "choices": ["Up", "Inside Out", "Monsters Inc.", "Soul"],
        "correct": "Inside Out"
    },
    {
        "category": "Pop Culture",
        "question": "What singer released the hit album 'Lemonade' in 2016?",
        "choices": ["Rihanna", "Nicki Minaj", "Beyoncé", "SZA"],
        "correct": "Beyoncé"
    },
    {
        "category": "Pop Culture",
        "question": "Which show features the quote 'How you doin?'",
        "choices": ["Friends", "Seinfeld", "The Office", "New Girl"],
        "correct": "Friends"
    },
    {
        "category": "Pop Culture",
        "question": "Which animated movie features a talking snowman named Olaf?",
        "choices": ["Frozen", "Shrek", "Moana", "Tangled"],
        "correct": "Frozen"
    },
    {
        "category": "Pop Culture",
        "question": "Which rapper famously said 'It's lit!' in many of his songs?",
        "choices": ["Kanye West", "Travis Scott", "Playboi Carti", "Future"],
        "correct": "Travis Scott"
    },

    # Sports (40 questions)
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
    },
    {
        "category": "Sports",
        "question": "Which athlete is known as 'The Fastest Man Alive'?",
        "choices": ["Tyson Gay", "Usain Bolt", "Yohan Blake", "Asafa Powell"],
        "correct": "Usain Bolt"
    },
    {
        "category": "Sports",
        "question": "Which American football team has won the most Super Bowls?",
        "choices": ["Pittsburgh Steelers", "Dallas Cowboys", "New England Patriots", "San Francisco 49ers"],
        "correct": "New England Patriots"
    },
    {
        "category": "Sports",
        "question": "In what sport would you execute a 'hat trick'?",
        "choices": ["Basketball", "Soccer", "Tennis", "Baseball"],
        "correct": "Soccer"
    },
    {
        "category": "Sports",
        "question": "Which NBA player is known as 'King James'?",
        "choices": ["Kobe Bryant", "Michael Jordan", "LeBron James", "Kevin Durant"],
        "correct": "LeBron James"
    },
    {
        "category": "Sports",
        "question": "Which sport uses the terms 'spare' and 'strike'?",
        "choices": ["Darts", "Bowling", "Cricket", "Baseball"],
        "correct": "Bowling"
    },
    {
        "category": "Sports",
        "question": "Which boxer was nicknamed 'The Greatest'?",
        "choices": ["Mike Tyson", "Muhammad Ali", "Floyd Mayweather", "Joe Frazier"],
        "correct": "Muhammad Ali"
    },
    {
        "category": "Sports",
        "question": "Which sport features a pommel horse?",
        "choices": ["Gymnastics", "Equestrian", "Track and Field", "Powerlifting"],
        "correct": "Gymnastics"
    },
    {
        "category": "Sports",
        "question": "Which country hosted the 2016 Summer Olympics?",
        "choices": ["China", "Brazil", "United Kingdom", "Japan"],
        "correct": "Brazil"
    },
    {
        "category": "Sports",
        "question": "Which famous golfer is known for wearing a red shirt on Sundays?",
        "choices": ["Tiger Woods", "Phil Mickelson", "Rory McIlroy", "Jordan Spieth"],
        "correct": "Tiger Woods"
    },
    {
        "category": "Sports",
        "question": "In what sport do athletes compete in the '100-meter butterfly'?",
        "choices": ["Track and Field", "Swimming", "Cycling", "Rowing"],
        "correct": "Swimming"
    },
    {
        "category": "Sports",
        "question": "Which country invented the sport of rugby?",
        "choices": ["Australia", "Wales", "New Zealand", "England"],
        "correct": "England"
    },
    {
        "category": "Sports",
        "question": "What is the maximum score in a single frame of bowling?",
        "choices": ["20", "30", "40", "50"],
        "correct": "30"
    },
    {
        "category": "Sports",
        "question": "Which female tennis player has won the most Grand Slam titles?",
        "choices": ["Serena Williams", "Martina Navratilova", "Steffi Graf", "Margaret Court"],
        "correct": "Margaret Court"
    },
    {
        "category": "Sports",
        "question": "Which NBA team did Michael Jordan play for the longest?",
        "choices": ["Washington Wizards", "Los Angeles Lakers", "Chicago Bulls", "New York Knicks"],
        "correct": "Chicago Bulls"
    },
    {
        "category": "Sports",
        "question": "Which sport includes terms like 'icing' and 'power play'?",
        "choices": ["Soccer", "Ice Hockey", "Volleyball", "Rugby"],
        "correct": "Ice Hockey"
    },
    {
        "category": "Sports",
        "question": "What piece of equipment is essential for fencing?",
        "choices": ["Bow", "Foil", "Paddle", "Racket"],
        "correct": "Foil"
    },
    {
        "category": "Sports",
        "question": "Which country has won the most FIFA Women's World Cups?",
        "choices": ["Germany", "United States", "Brazil", "Japan"],
        "correct": "United States"
    },
    {
        "category": "Sports",
        "question": "What is the term for a baseball player hitting a home run with the bases loaded?",
        "choices": ["Triple Play", "Grand Slam", "Power Hit", "Four-Run Shot"],
        "correct": "Grand Slam"
    },
    {
        "category": "Sports",
        "question": "Which legendary swimmer earned 23 Olympic gold medals?",
        "choices": ["Ryan Lochte", "Ian Thorpe", "Michael Phelps", "Caeleb Dressel"],
        "correct": "Michael Phelps"
    },
    {
        "category": "Sports",
        "question": "Which sport requires a balance beam?",
        "choices": ["Figure Skating", "Gymnastics", "Diving", "Wrestling"],
        "correct": "Gymnastics"
    },
    {
        "category": "Sports",
        "question": "Which soccer player is known as 'CR7'?",
        "choices": ["Cristiano Ronaldo", "Kylian Mbappé", "Lionel Messi", "Neymar"],
        "correct": "Cristiano Ronaldo"
    },
    {
        "category": "Sports",
        "question": "Which sport uses a 'shuttlecock'?",
        "choices": ["Tennis", "Badminton", "Pickleball", "Squash"],
        "correct": "Badminton"
    },
    {
        "category": "Sports",
        "question": "Which country is famous for dominating sumo wrestling?",
        "choices": ["China", "Japan", "South Korea", "Mongolia"],
        "correct": "Japan"
    },
    {
        "category": "Sports",
        "question": "What is the highest score possible in a single turn of darts (using 3 darts)?",
        "choices": ["120", "150", "180", "200"],
        "correct": "180"
    },
    {
        "category": "Sports",
        "question": "Which sport features events like uneven bars and vault?",
        "choices": ["Track and Field", "Gymnastics", "Swimming", "Cycling"],
        "correct": "Gymnastics"
    },
    {
        "category": "Sports",
        "question": "Which NFL quarterback is known as 'The GOAT'?",
        "choices": ["Peyton Manning", "Tom Brady", "Aaron Rodgers", "Joe Montana"],
        "correct": "Tom Brady"
    },
    {
        "category": "Sports",
        "question": "Which sport involves a device called a 'putter'?",
        "choices": ["Baseball", "Golf", "Cricket", "Hockey"],
        "correct": "Golf"
    },
    {
        "category": "Sports",
        "question": "Which country has won the most Olympic gold medals overall?",
        "choices": ["China", "Russia", "Germany", "United States"],
        "correct": "United States"
    },
    {
        "category": "Sports",
        "question": "Which sport uses a rectangular ring and three-minute rounds?",
        "choices": ["MMA", "Karate", "Boxing", "Kickboxing"],
        "correct": "Boxing"
    },
    {
        "category": "Sports",
        "question": "What is the name of the annual championship series in Major League Baseball?",
        "choices": ["World Series", "Super Cup", "MLB Finals", "Grand Classic"],
        "correct": "World Series"
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
