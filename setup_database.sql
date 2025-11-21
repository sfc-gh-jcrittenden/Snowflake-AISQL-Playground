-- ============================================================================
-- Snowflake Cortex AI Functions Playground - Database Setup Script
-- ============================================================================
-- This script creates the AI_FUNCTIONS_PLAYGROUND database with all necessary tables,
-- stages, and sample data for the Tasty Bytes themed demonstration.
-- ============================================================================

-- Use SYSADMIN role (or change to a custom role of your choosing)
USE ROLE SYSADMIN;

-- Create warehouse for the demo (X-SMALL Gen2)
CREATE OR REPLACE WAREHOUSE AI_FUNCTIONS_PLAYGROUND_WH
    WAREHOUSE_SIZE = 'X-SMALL'
    WAREHOUSE_TYPE = 'STANDARD'
    AUTO_SUSPEND = 300
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE
    COMMENT = 'Warehouse for Cortex AI Functions Playground Streamlit app and query execution';

-- Create database and schema
CREATE DATABASE IF NOT EXISTS AI_FUNCTIONS_PLAYGROUND;
USE DATABASE AI_FUNCTIONS_PLAYGROUND;
USE WAREHOUSE AI_FUNCTIONS_PLAYGROUND_WH;
CREATE SCHEMA IF NOT EXISTS DEMO;
USE SCHEMA DEMO;

-- ============================================================================
-- CREATE INTERNAL STAGES FOR MEDIA FILES
-- ============================================================================

-- Stage for audio files (transcription demos)
CREATE OR REPLACE STAGE AUDIO_STAGE
    ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')
    DIRECTORY = (ENABLE = TRUE);

-- Stage for document files (parsing and extraction demos)
CREATE OR REPLACE STAGE DOCUMENT_STAGE
    ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')
    DIRECTORY = (ENABLE = TRUE);

-- Stage for supplier invoice documents (AI_EXTRACT demos)
CREATE OR REPLACE STAGE SUPPLIER_DOCUMENTS_STAGE
    ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')
    DIRECTORY = (ENABLE = TRUE);

-- Stage for image files (image analysis demos)
CREATE OR REPLACE STAGE IMAGE_STAGE
    ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')
    DIRECTORY = (ENABLE = TRUE);

-- ============================================================================
-- CREATE TABLES FOR STRUCTURED DATA
-- ============================================================================

-- Customer Reviews Table (for sentiment, summarization, translation)
CREATE OR REPLACE TABLE CUSTOMER_REVIEWS (
    review_id INT AUTOINCREMENT,
    customer_name VARCHAR(100),
    food_truck_name VARCHAR(100),
    menu_item VARCHAR(100),
    review_text TEXT,
    review_date DATE,
    rating INT,
    language VARCHAR(20),
    PRIMARY KEY (review_id)
);

-- Menu Items Table (for translation demos)
CREATE OR REPLACE TABLE MENU_ITEMS (
    menu_id INT AUTOINCREMENT,
    food_truck_name VARCHAR(100),
    item_name VARCHAR(100),
    description_english TEXT,
    description_spanish TEXT,
    description_french TEXT,
    description_german TEXT,
    description_japanese TEXT,
    price DECIMAL(10,2),
    category VARCHAR(50),
    PRIMARY KEY (menu_id)
);

-- Food Trucks Table
CREATE OR REPLACE TABLE FOOD_TRUCKS (
    truck_id INT AUTOINCREMENT,
    truck_name VARCHAR(100),
    cuisine_type VARCHAR(50),
    city VARCHAR(100),
    operating_since DATE,
    description TEXT,
    PRIMARY KEY (truck_id)
);

-- Customer Support Tickets Table (for classification, filtering - NO PII)
CREATE OR REPLACE TABLE SUPPORT_TICKETS (
    ticket_id INT AUTOINCREMENT,
    customer_name VARCHAR(100),
    food_truck_name VARCHAR(100),
    issue_description TEXT,
    created_date DATE,
    status VARCHAR(20),
    urgency VARCHAR(20),
    PRIMARY KEY (ticket_id)
);

-- Customer Support Tickets with PII Table (for AI_REDACT demos only)
CREATE OR REPLACE TABLE SUPPORT_TICKETS_PII (
    ticket_id INT AUTOINCREMENT,
    customer_name VARCHAR(100),
    food_truck_name VARCHAR(100),
    issue_description TEXT,
    created_date DATE,
    status VARCHAR(20),
    urgency VARCHAR(20),
    PRIMARY KEY (ticket_id)
);

-- Document Parsing Tables (for AI_PARSE_DOCUMENT and Cortex Search)
CREATE OR REPLACE TABLE PARSE_DOC_RAW_TEXT (
    doc_id INT AUTOINCREMENT,
    file_name VARCHAR(500),
    file_url VARCHAR(2000),
    raw_text TEXT,
    parsed_date TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
    PRIMARY KEY (doc_id)
);

CREATE OR REPLACE TABLE PARSE_DOC_CHUNKED_TEXT (
    chunk_id INT AUTOINCREMENT,
    file_name VARCHAR(500),
    file_url VARCHAR(2000),
    chunk_index INT,
    chunk_text TEXT,
    chunk_length INT,
    created_date TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
    PRIMARY KEY (chunk_id)
);

-- Supplier Invoice Details Table (for AI_EXTRACT demos)
CREATE OR REPLACE TABLE SUPPLIER_INVOICE_DETAILS (
    invoice_detail_id INT AUTOINCREMENT,
    file_name VARCHAR(500),
    file_url VARCHAR(2000),
    invoice_number VARCHAR(50),
    invoice_date DATE,
    supplier_name VARCHAR(200),
    supplier_address VARCHAR(500),
    supplier_phone VARCHAR(50),
    customer_name VARCHAR(200),
    customer_address VARCHAR(500),
    customer_phone VARCHAR(50),
    subtotal DECIMAL(10,2),
    tax_amount DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    payment_terms VARCHAR(100),
    item_count INT,
    extraction_date DATE,
    raw_json VARIANT,
    PRIMARY KEY (invoice_detail_id)
);

-- ============================================================================
-- INSERT SAMPLE DATA - FOOD TRUCKS
-- ============================================================================

INSERT INTO FOOD_TRUCKS (truck_name, cuisine_type, city, operating_since, description) VALUES
('Guac n Roll', 'Mexican', 'Austin', '2019-03-15', 'Authentic Mexican street tacos and fresh guacamole'),
('Freezing Point', 'Desserts', 'Boston', '2020-06-01', 'Artisanal ice cream and frozen treats'),
('Kitakata Ramen Bar', 'Japanese', 'San Francisco', '2018-11-20', 'Traditional Japanese ramen with hand-made noodles'),
('Peking Truck', 'Chinese', 'New York', '2019-08-10', 'Authentic Beijing-style cuisine and dumplings'),
('Revenge of the Curds', 'Canadian', 'Seattle', '2020-02-14', 'Gourmet poutine and Canadian comfort food'),
('Smoky BBQ', 'American BBQ', 'Denver', '2017-05-05', 'Slow-smoked meats and authentic BBQ sauces'),
('Le Coin des Crêpes', 'French', 'Portland', '2021-01-20', 'Sweet and savory French crêpes'),
('Plant Palace', 'Vegan', 'Los Angeles', '2020-09-15', 'Innovative plant-based cuisine'),
('Cheeky Greek', 'Greek', 'Chicago', '2019-04-22', 'Traditional Greek gyros and Mediterranean flavors'),
('Nani''s Kitchen', 'Indian', 'Miami', '2018-07-30', 'Authentic Indian curries and tandoori specialties');

-- ============================================================================
-- INSERT SAMPLE DATA - MENU ITEMS
-- ============================================================================

INSERT INTO MENU_ITEMS (food_truck_name, item_name, description_english, description_spanish, description_french, description_german, description_japanese, price, category) VALUES
('Guac n Roll', 'Carne Asada Taco', 'Grilled marinated steak with fresh cilantro, onions, and homemade salsa on a soft corn tortilla', 'Carne asada a la parrilla con cilantro fresco, cebolla y salsa casera en tortilla de maíz suave', 'Steak grillé mariné avec coriandre fraîche, oignons et salsa maison sur tortilla de maïs moelleuse', 'Gegrilltes mariniertes Steak mit frischem Koriander, Zwiebeln und hausgemachter Salsa auf weicher Maistortilla', 'やわらかいコーントルティーヤに新鮮なコリアンダー、玉ねぎ、自家製サルサを添えたグリルマリネステーキ', 4.50, 'Tacos'),
('Guac n Roll', 'Super Burrito', 'Large flour tortilla filled with your choice of meat, rice, beans, cheese, guacamole, and sour cream', 'Gran tortilla de harina rellena con tu elección de carne, arroz, frijoles, queso, guacamole y crema agria', 'Grande tortilla de farine garnie de votre choix de viande, riz, haricots, fromage, guacamole et crème sure', 'Große Weizentortilla gefüllt mit Fleisch nach Wahl, Reis, Bohnen, Käse, Guacamole und Sauerrahm', '大きな小麦粉トルティーヤにお好みの肉、ご飯、豆、チーズ、ワカモレ、サワークリームを詰めました', 9.99, 'Burritos'),
('Freezing Point', 'Salted Caramel Swirl', 'Rich vanilla ice cream with ribbons of salted caramel and candied pecans', 'Helado de vainilla rico con cintas de caramelo salado y nueces pecanas confitadas', 'Crème glacée vanille riche avec des rubans de caramel salé et noix de pécan confites', 'Reichhaltiges Vanilleeis mit gesalzenem Karamell und kandierten Pekannüssen', '塩キャラメルとキャンディピーカンナッツのリボンを添えた濃厚なバニラアイスクリーム', 6.50, 'Ice Cream'),
('Kitakata Ramen Bar', 'Tonkotsu Ramen', 'Rich pork bone broth with hand-pulled noodles, chashu pork, soft-boiled egg, and green onions', 'Caldo rico de hueso de cerdo con fideos hechos a mano, cerdo chashu, huevo pasado por agua y cebolletas', 'Bouillon riche d''os de porc avec nouilles faites main, porc chashu, œuf mollet et oignons verts', 'Reichhaltige Schweineknochenbrühe mit handgezogenen Nudeln, Chashu-Schweinefleisch, weichgekochtem Ei und Frühlingszwiebeln', '手打ち麺、チャーシュー、半熟卵、ねぎを添えた濃厚な豚骨スープ', 13.99, 'Ramen'),
('Peking Truck', 'Soup Dumplings', 'Delicate steamed dumplings filled with seasoned pork and savory broth', 'Delicados dumplings al vapor rellenos de cerdo sazonado y caldo sabroso', 'Délicats raviolis vapeur farcis de porc assaisonné et bouillon savoureux', 'Zarte gedämpfte Teigtaschen gefüllt mit gewürztem Schweinefleisch und herzhafter Brühe', '味付けした豚肉と旨味のあるスープを詰めた繊細な蒸し餃子', 8.50, 'Dumplings'),
('Revenge of the Curds', 'Classic Poutine', 'Crispy fries topped with cheese curds and smothered in rich gravy', 'Papas fritas crujientes cubiertas con cuajada de queso y bañadas en salsa rica', 'Frites croustillantes garnies de fromage en grains et nappées de sauce riche', 'Knusprige Pommes mit Käsebruch belegt und in reichhaltiger Soße ertränkt', 'チーズカードをトッピングし、濃厚なグレービーソースをかけたサクサクのフライドポテト', 7.99, 'Poutine'),
('Smoky BBQ', 'Pulled Pork Sandwich', 'Slow-smoked pulled pork with tangy BBQ sauce on a toasted bun', 'Cerdo desmenuzado ahumado lentamente con salsa BBQ picante en pan tostado', 'Porc effiloché fumé lentement avec sauce BBQ acidulée sur pain grillé', 'Langsam geräuchertes Pulled Pork mit würziger BBQ-Sauce auf geröstetem Brötchen', 'トーストしたバンズに濃厚なBBQソースをかけたスロースモークプルドポーク', 10.50, 'Sandwiches'),
('Le Coin des Crêpes', 'Nutella Banana Crêpe', 'Thin French crêpe filled with Nutella and fresh banana slices', 'Crêpe francés delgado relleno de Nutella y rodajas de plátano fresco', 'Crêpe française fine garnie de Nutella et tranches de banane fraîche', 'Dünner französischer Crêpe gefüllt mit Nutella und frischen Bananenscheiben', 'ヌテラと新鮮なバナナスライスを詰めた薄いフレンチクレープ', 7.50, 'Dessert'),
('Plant Palace', 'Beyond Burger', 'Plant-based burger patty with lettuce, tomato, pickles, and special sauce', 'Hamburguesa a base de plantas con lechuga, tomate, pepinillos y salsa especial', 'Galette de burger à base de plantes avec laitue, tomate, cornichons et sauce spéciale', 'Pflanzliches Burger-Patty mit Salat, Tomate, Gurken und Spezialsoße', 'レタス、トマト、ピクルス、スペシャルソースを添えた植物ベースのバーガーパティ', 11.99, 'Burgers'),
('Cheeky Greek', 'Lamb Gyro', 'Seasoned lamb with tzatziki sauce, tomatoes, and onions in warm pita bread', 'Cordero sazonado con salsa tzatziki, tomates y cebollas en pan pita caliente', 'Agneau assaisonné avec sauce tzatziki, tomates et oignons dans pain pita chaud', 'Gewürztes Lammfleisch mit Tzatziki-Sauce, Tomaten und Zwiebeln in warmem Pitabrot', '温かいピタパンにツァジキソース、トマト、玉ねぎを添えた味付けラム肉', 9.99, 'Gyros');

-- ============================================================================
-- INSERT SAMPLE DATA - CUSTOMER REVIEWS
-- ============================================================================

INSERT INTO CUSTOMER_REVIEWS (customer_name, food_truck_name, menu_item, review_text, review_date, rating, language) VALUES
('Sarah Johnson', 'Guac n Roll', 'Carne Asada Taco', 'The carne asada tacos were absolutely incredible! The meat was perfectly seasoned and grilled to perfection. The homemade salsa had just the right amount of kick. Best tacos I have ever had in Austin. Will definitely be coming back!', '2024-10-15', 5, 'English'),
('Michael Chen', 'Kitakata Ramen Bar', 'Tonkotsu Ramen', 'This is as close to authentic Japanese ramen as you can get in San Francisco. The broth was rich and creamy, the noodles had perfect texture, and the chashu pork melted in my mouth. Only complaint is the long wait time, but it was worth it!', '2024-10-20', 4, 'English'),
('Emily Rodriguez', 'Freezing Point', 'Salted Caramel Swirl', 'Good ice cream but a bit overpriced for the portion size. The salted caramel flavor was delicious though. I wish they offered larger sizes.', '2024-10-18', 3, 'English'),
('David Williams', 'Smoky BBQ', 'Pulled Pork Sandwich', 'Disappointed with my order today. The pulled pork was dry and the BBQ sauce could not save it. The service was also quite slow. I have had better experiences here before, so maybe it was just an off day.', '2024-10-22', 2, 'English'),
('Jessica Martinez', 'Le Coin des Crêpes', 'Nutella Banana Crêpe', 'Absolutely divine! The crêpe was thin and delicate, just like in France. The Nutella was generous and the bananas were fresh. Perfect for dessert or a sweet breakfast. Highly recommend!', '2024-10-25', 5, 'English'),
('James Taylor', 'Plant Palace', 'Beyond Burger', 'As a vegetarian, I am always looking for good plant-based options. This burger exceeded my expectations! It tasted amazing and I could not even tell it was not real meat. Great job!', '2024-10-19', 5, 'English'),
('Lisa Anderson', 'Revenge of the Curds', 'Classic Poutine', 'The fries were crispy and the cheese curds were fresh, but the gravy was way too salty for my taste. Also, the portion was smaller than expected. Decent but not great.', '2024-10-21', 3, 'English'),
('Robert Brown', 'Peking Truck', 'Soup Dumplings', 'These soup dumplings are the real deal! The broth inside was flavorful and hot, the wrapper was delicate. You can tell these are made fresh. Best Chinese food truck in NYC by far.', '2024-10-23', 5, 'English'),
('Maria Garcia', 'Cheeky Greek', 'Lamb Gyro', 'El gyro de cordero estaba delicioso. La carne estaba bien condimentada y la salsa tzatziki era fresca y cremosa. Definitivamente volveré por más.', '2024-10-24', 4, 'Spanish'),
('Thomas White', 'Kitakata Ramen Bar', 'Tonkotsu Ramen', 'Terrible experience. Found a hair in my ramen and when I told the staff, they were very dismissive. Will never go back.', '2024-10-26', 1, 'English'),
('Amanda Lee', 'Guac n Roll', 'Super Burrito', 'This burrito is HUGE and so filling! Everything inside was fresh and flavorful. The guacamole is clearly made fresh. Great value for the price. My new favorite lunch spot!', '2024-10-27', 5, 'English'),
('Christopher Davis', 'Smoky BBQ', 'Pulled Pork Sandwich', 'The BBQ here never disappoints. The meat is always tender and smoky, and the sauce is tangy and sweet. The coleslaw on the side is also excellent. A must-try!', '2024-10-28', 5, 'English'),
('Jennifer Wilson', 'Freezing Point', 'Salted Caramel Swirl', 'This ice cream is amazing! Creamy, rich, and the salted caramel ribbons are perfect. The candied pecans add a nice crunch. Worth every penny.', '2024-10-29', 5, 'English'),
('Daniel Moore', 'Plant Palace', 'Beyond Burger', 'Not bad, but I have had better plant-based burgers. The patty was a bit dry and lacked seasoning. The toppings were fresh though.', '2024-10-30', 3, 'English'),
('Michelle Taylor', 'Le Coin des Crêpes', 'Nutella Banana Crêpe', 'Way too sweet for me. I could barely finish it. If you have a major sweet tooth you might like it, but it was overwhelming for me.', '2024-11-01', 2, 'English'),
('Kevin Martinez', 'Cheeky Greek', 'Lamb Gyro', 'Solid gyro! The lamb was tender and well-seasoned. The pita was warm and soft. Only wish they gave more tzatziki sauce. Overall a great meal.', '2024-11-02', 4, 'English'),
('Laura Anderson', 'Peking Truck', 'Soup Dumplings', 'Be careful when eating these - the soup inside is super hot! But they are absolutely delicious. The pork filling is seasoned perfectly. Love this truck!', '2024-11-03', 5, 'English'),
('Steven Jackson', 'Revenge of the Curds', 'Classic Poutine', 'Ce poutine est authentique et délicieux. Les frites sont croustillantes et la sauce est parfaite. Je recommande vivement!', '2024-11-04', 5, 'French'),
('Karen Thomas', 'Kitakata Ramen Bar', 'Tonkotsu Ramen', 'Good ramen but nothing special. The broth was tasty but the noodles were a bit overcooked. Service was friendly though.', '2024-11-05', 3, 'English'),
('Patricia White', 'Guac n Roll', 'Carne Asada Taco', 'These tacos remind me of my childhood in Mexico. Authentic and delicious. The salsa verde is particularly good. Gracias!', '2024-11-06', 5, 'English'),
('Brandon Cooper', 'Smoky BBQ', 'Pulled Pork Sandwich', 'The BBQ sauce on this sandwich is perfection! Sweet, smoky, and just the right amount of tang. The meat literally melts in your mouth. Best BBQ in Denver!', '2024-11-07', 5, 'English'),
('Rachel Green', 'Freezing Point', 'Salted Caramel Swirl', 'I come here every week! The ice cream is always fresh and the flavors change seasonally. The staff remembers my usual order which makes me feel special.', '2024-11-08', 5, 'English'),
('Tyler Johnson', 'Nani''s Kitchen', 'Chicken Tikka Masala', 'Absolutely authentic Indian cuisine. The spices are balanced perfectly and the naan bread is made fresh. Reminds me of my trip to Mumbai!', '2024-11-09', 5, 'English'),
('Samantha Blake', 'Le Coin des Crêpes', 'Nutella Banana Crêpe', 'C''est magnifique! Les crêpes sont légères et délicieuses. Je me sens comme si j''étais à Paris!', '2024-11-10', 5, 'French'),
('Marcus Williams', 'Peking Truck', 'Soup Dumplings', 'These xiaolongbao are as good as what I had in Shanghai. The wrapper is thin, the broth is flavorful, and they are made fresh to order. Worth the wait!', '2024-11-11', 5, 'English'),
('Ashley Martinez', 'Plant Palace', 'Beyond Burger', 'As a lifelong vegetarian, I am so happy to have quality plant-based options like this. The burger is juicy and flavorful. My meat-eating friends could not tell the difference!', '2024-11-12', 5, 'English'),
('Eric Thompson', 'Revenge of the Curds', 'Classic Poutine', 'This poutine takes me back to my college days in Montreal. The cheese curds squeak just right and the gravy is rich without being too heavy. Authentic Canadian comfort food!', '2024-11-13', 5, 'English'),
('Nicole Rodriguez', 'Cheeky Greek', 'Lamb Gyro', 'The lamb is seasoned beautifully and the vegetables are always fresh. The tzatziki sauce is homemade and you can taste the difference. Highly recommend!', '2024-11-14', 4, 'English'),
('Justin Lee', 'Kitakata Ramen Bar', 'Tonkotsu Ramen', 'Finally found authentic tonkotsu in SF! The broth is rich and creamy, clearly simmered for hours. The chashu pork is tender and the egg is perfect. This is the real deal!', '2024-11-15', 5, 'English'),
('Melissa Brown', 'Guac n Roll', 'Super Burrito', 'This burrito is massive! Packed with perfectly seasoned carne asada, fresh guac, and all the fixings. One burrito is easily two meals. Great value!', '2024-11-16', 5, 'English'),
('Derek Wilson', 'Smoky BBQ', 'Pulled Pork Sandwich', 'Good BBQ but I have had better. The meat was a bit dry today and could use more sauce. Maybe just an off day? Will give it another try.', '2024-11-17', 3, 'English'),
('Christina Davis', 'Freezing Point', 'Salted Caramel Swirl', 'Overpriced for the portion size. The ice cream itself is good but $8 for a small scoop is too much. I will stick to other places.', '2024-11-18', 2, 'English'),
('Andrew Miller', 'Plant Palace', 'Beyond Burger', 'Not impressed. The patty fell apart and the bun was soggy. I love plant-based food but this needs improvement.', '2024-11-19', 2, 'English'),
('Victoria Garcia', 'Cheeky Greek', 'Lamb Gyro', 'Muy delicioso! La carne de cordero está perfectamente sazonada. Las porciones son generosas y el precio es justo. Volveré pronto!', '2024-11-20', 5, 'Spanish'),
('Ryan Martinez', 'Peking Truck', 'Soup Dumplings', 'These dumplings are incredible! Be warned - they are addictive. I ordered 8 and wished I had gotten more. The ginger dipping sauce is the perfect complement.', '2024-11-21', 5, 'English'),
('Angela White', 'Kitakata Ramen Bar', 'Tonkotsu Ramen', 'The ramen was okay but the wait time was over 45 minutes. For a food truck, that is way too long. The taste was good but not worth the wait.', '2024-11-22', 3, 'English'),
('Brian Taylor', 'Revenge of the Curds', 'Classic Poutine', 'As a Canadian living in Seattle, I can confirm this is authentic poutine! The gravy recipe must be from Quebec. So happy to find this gem!', '2024-11-23', 5, 'English'),
('Monica Harris', 'Le Coin des Crêpes', 'Nutella Banana Crêpe', 'The crêpe was delicious but there was not enough Nutella. For the price, I expected more filling. Still tasty though!', '2024-11-24', 3, 'English'),
('Kevin Anderson', 'Nani''s Kitchen', 'Chicken Tikka Masala', 'Best Indian food I have had from a food truck! The curry is rich and creamy, the chicken is tender, and the spice level is perfect. Will be back weekly!', '2024-11-25', 5, 'English'),
('Gregory Peterson', 'Smoky BBQ', 'Pulled Pork Sandwich', 'Outstanding BBQ! The pulled pork is incredibly tender and smoky. The BBQ sauce has the perfect balance of sweet and tangy. The portion size is generous and the service was quick. This is now my go-to spot for authentic BBQ!', '2024-11-26', 5, 'English');

-- ============================================================================
-- INSERT SAMPLE DATA - SUPPORT TICKETS (NO PII)
-- ============================================================================

INSERT INTO SUPPORT_TICKETS (customer_name, food_truck_name, issue_description, created_date, status, urgency) VALUES
('Sarah Johnson', 'Smoky BBQ', 'I ordered the pulled pork sandwich yesterday but received the wrong item. The order was supposed to be for delivery but arrived incorrect. I need this resolved as soon as possible.', '2024-10-15', 'Open', 'High'),
('Michael Chen', 'Guac n Roll', 'I was charged twice for my order on Saturday. Please process a refund for the duplicate charge. This appears to be a system error.', '2024-10-16', 'In Progress', 'High'),
('Emily Rodriguez', 'Freezing Point', 'My ice cream order arrived completely melted. I would like either a refund or replacement. Very disappointing experience.', '2024-10-17', 'Open', 'Medium'),
('David Williams', 'Le Coin des Crêpes', 'Just wanted to compliment your amazing crêpes! The quality and service were outstanding. Keep up the great work!', '2024-10-18', 'Closed', 'Low'),
('Jessica Martinez', 'Plant Palace', 'I have a severe nut allergy and need to verify if your Beyond Burger contains any tree nuts before ordering. This is urgent for health reasons.', '2024-10-19', 'Open', 'High'),
('James Taylor', 'Peking Truck', 'Your soup dumplings were incredible! I would love to book your truck for a corporate event. Please send me information about catering services.', '2024-10-20', 'In Progress', 'Medium'),
('Lisa Anderson', 'Kitakata Ramen Bar', 'I found a hair in my ramen last week. This is unacceptable and I expect a full refund. Very unhappy with this experience.', '2024-10-21', 'Open', 'High'),
('Robert Brown', 'Cheeky Greek', 'I am inquiring about franchise opportunities for your food truck brand. Please send me information about requirements and investment details.', '2024-10-22', 'In Progress', 'Low'),
('Maria Garcia', 'Revenge of the Curds', 'Your poutine is amazing! I want to order catering for my birthday party next month. Please send pricing information for large groups.', '2024-10-23', 'Closed', 'Medium'),
('Thomas White', 'Nani''s Kitchen', 'The chicken tikka masala arrived cold when delivered. For the price point, this is not acceptable. I would like a refund.', '2024-10-24', 'In Progress', 'High'),
('Amanda Lee', 'Freezing Point', 'I wanted to report excellent service from your staff yesterday! They went above and beyond to help. Keep up the amazing work!', '2024-10-25', 'Closed', 'Low'),
('Christopher Davis', 'Guac n Roll', 'The burrito had no guacamole despite me paying extra for it. I was charged full price. This needs to be corrected.', '2024-10-26', 'Open', 'Medium'),
('Jennifer Wilson', 'Smoky BBQ', 'Your pulled pork sandwich made my day! The flavors were incredible. Would love to get the recipe if possible. Thank you for amazing food!', '2024-10-27', 'Closed', 'Low'),
('Daniel Moore', 'Kitakata Ramen Bar', 'Your ramen gave me food poisoning. My attorney will be contacting you. This is a serious health and safety issue.', '2024-10-28', 'Open', 'High'),
('Michelle Taylor', 'Le Coin des Crêpes', 'I am requesting catering information for a large event. Need pricing for approximately two hundred people. Please respond with availability.', '2024-10-29', 'In Progress', 'Medium'),
('Kevin Martinez', 'Cheeky Greek', 'The lamb gyro was undercooked and I got sick after eating it. I need a full refund immediately.', '2024-10-30', 'Open', 'High'),
('Laura Anderson', 'Plant Palace', 'I am inquiring about job opportunities with your food truck. I have five years of food service experience and am very interested in joining your team.', '2024-10-31', 'In Progress', 'Low'),
('Steven Jackson', 'Peking Truck', 'Your soup dumplings are the best! My doctor recommended your food for my diet. Thank you for providing healthy and delicious options.', '2024-11-01', 'Closed', 'Low'),
('Karen Thomas', 'Revenge of the Curds', 'I need a tax receipt for a business expense. My recent order needs to be properly documented for accounting purposes.', '2024-11-02', 'Open', 'Low'),
('Patricia White', 'Nani''s Kitchen', 'I recently joined your loyalty program and love your food! Looking forward to earning rewards. Keep making delicious Indian cuisine!', '2024-11-03', 'Closed', 'Low');

-- ============================================================================
-- INSERT SAMPLE DATA - SUPPORT TICKETS WITH PII (FOR AI_REDACT ONLY)
-- ============================================================================

INSERT INTO SUPPORT_TICKETS_PII (customer_name, food_truck_name, issue_description, created_date, status, urgency) VALUES
('Sarah Johnson', 'Smoky BBQ', 'Hi, I am Sarah Johnson (SSN: 123-45-6789, DOB: 03/15/1985, Female) and I ordered the pulled pork sandwich yesterday but it was completely wrong. You can reach me at sarah.j@email.com or call 555-123-4567. I need this resolved ASAP. My order was supposed to be delivered to 742 Evergreen Terrace, Austin, TX 78701. My credit card 4532-1234-5678-9012 was charged.', '2024-10-15', 'Open', 'High'),
('Michael Chen', 'Guac n Roll', 'This is Michael Chen, DOB 03/15/1985, Male, DL# D1234567, SSN 234-56-7890. I visited your truck on Saturday and was charged twice on my card ending in 4532. Please refund to michael.chen@gmail.com or call me at 555-234-5678. My billing address is 1428 Elm Street, Apt 5B, Portland, OR 97209.', '2024-10-16', 'In Progress', 'High'),
('Emily Rodriguez', 'Freezing Point', 'I am writing about my recent order. My name is Emily Rodriguez (Female, Age 32, SSN: 345-67-8901), email emily.rodriguez@yahoo.com, phone 555-345-6789. I live at 3845 Oak Avenue, Miami, FL 33101. The ice cream I received was melted. My payment card 5412-7534-8901-2345 needs to be refunded.', '2024-10-17', 'Open', 'Medium'),
('David Williams', 'Le Coin des Crêpes', 'Just wanted to compliment your amazing crêpes! I am David Williams (Male, DOB: 07/22/1990, DL# D7654321) and you can reach me at 555-456-7890 or david.w@outlook.com if you ever need a testimonial. I live nearby at 956 Pine Street, Portland, OR 97209. Keep up the great work!', '2024-10-18', 'Closed', 'Low'),
('Jessica Martinez', 'Plant Palace', 'Hi, this is Jessica Martinez (Female, Age 29, SSN: 456-78-9012, DOB: 08/30/1995) calling from 555-567-8901. I have a severe nut allergy and need to know if your Beyond Burger contains any tree nuts. My email is jessica.m@email.com. I am located at 2134 Maple Drive, Los Angeles, CA 90028. Please respond urgently.', '2024-10-19', 'Open', 'High'),
('James Taylor', 'Peking Truck', 'Hello, James Taylor here (Male, Passport P12345678, SSN: 567-89-0123). I visited your truck yesterday and the soup dumplings were incredible! I would love to book you for a corporate event. Please contact me at james.taylor@company.com or 555-678-9012. Our office is at 675 Birch Lane, New York, NY 10001.', '2024-10-20', 'In Progress', 'Medium'),
('Lisa Anderson', 'Kitakata Ramen Bar', 'This is Lisa Anderson, Female, born 11/30/1988, SSN: 678-90-1234. I ordered ramen last week and found a hair in it. This is unacceptable. My contact info: lisa.a@email.net or 555-789-0123. I live at 1523 Cedar Court, San Francisco, CA 94102. DL# D8765432. I expect a full refund.', '2024-10-21', 'Open', 'High'),
('Robert Brown', 'Cheeky Greek', 'Robert Brown here, Male, Age 42, SSN on file is 789-01-2345, DL# D2468135. I am inquiring about franchise opportunities. Please send information to robert.brown@business.com or call 555-890-1234. My current address is 789 Willow Way, Denver, CO 80201. Credit card 6011-2345-6789-0123.', '2024-10-22', 'In Progress', 'Low'),
('Maria Garcia', 'Revenge of the Curds', 'Maria Garcia (Female, DOB 09/25/1985, SSN: 890-12-3456) calling from 555-901-2345. Your poutine is amazing! I want to order catering for my birthday party on 09/25. Email me at maria.garcia@party.com with pricing. Event location: 445 Sunset Boulevard, Seattle, WA 98101. IP address 192.168.1.105.', '2024-10-23', 'Closed', 'Medium'),
('Thomas White', 'Nani''s Kitchen', 'This is Thomas White, Male, Age 38, SSN: 901-23-4567, Passport P87654321. I have been trying to reach someone about my order. My phone is 555-012-3456 and email is thomas.white@email.com. I am located at 234 River Road, Miami, FL 33101. The chicken tikka masala was cold when delivered. Card 3782-8224-6310-005. Need refund.', '2024-10-24', 'In Progress', 'High'),
('Amanda Lee', 'Freezing Point', 'Amanda Lee here, Female, born 12/08/1992, SSN: 012-34-5678, DL# D1357924. I wanted to report excellent service from your staff yesterday! You can reach me at amanda.lee@health.org or 555-123-4560. I live at 1867 Mountain View, Boston, MA 02101. Keep up the amazing work!', '2024-10-25', 'Closed', 'Low'),
('Christopher Davis', 'Guac n Roll', 'Christopher Davis (Male, Age 44, DOB 04/12/1980, SSN: 123-45-6780) writing to complain about service. My phone: 555-234-5670, email: c.davis@email.com. The burrito had no guacamole despite me paying extra. My card ending in 6789 was charged full price. Address: 678 Valley Street, Phoenix, AZ 85001. DL# D9876543.', '2024-10-26', 'Open', 'Medium'),
('Jennifer Wilson', 'Smoky BBQ', 'Hi, Jennifer Wilson here (Female, DOB 06/14/1990, SSN: 234-56-7891, Passport P23456789). Your pulled pork sandwich made my day! Can I get the recipe? Contact me at j.wilson@foodie.com or 555-345-6781. I am at 891 School Lane, Austin, TX 78701. Thanks for amazing food!', '2024-10-27', 'Closed', 'Low'),
('Daniel Moore', 'Kitakata Ramen Bar', 'Daniel Moore (Male, Age 47, SSN: 567-89-0123, DL# D5432167) filing complaint. Your ramen gave me food poisoning. Attorney will contact you. My info: 555-456-7892, moore.legal@lawfirm.com. Address: 1122 Justice Drive, Dallas, TX 75201. Credit card 4111-1111-1111-1111. This is serious.', '2024-10-28', 'Open', 'High'),
('Michelle Taylor', 'Le Coin des Crêpes', 'Michelle Taylor (Female, DOB 08/30/1985, SSN: 678-90-1235, Passport P12345678) requesting catering info. My drivers license is D3698521 if you need ID for the venue. Contact: michelle.t@events.com or 555-567-8903. Event venue: 445 Airport Road, Portland, OR 97209. Credit card 5555-4444-3333-2222. Need pricing for 200 people.', '2024-10-29', 'In Progress', 'Medium'),
('Kevin Martinez', 'Cheeky Greek', 'Kevin Martinez here (Male, born 10/15/1991, SSN: 789-01-2346, Age 33, DL# D7531598). The lamb gyro was undercooked and I got sick. My credit card 3782-8224-6310-005 was charged. Email: kevin.m@email.com, phone: 555-678-9014. Home: 2233 Rental Avenue, Chicago, IL 60601. Passport P98765432. Need full refund.', '2024-10-30', 'Open', 'High'),
('Laura Anderson', 'Plant Palace', 'Laura Anderson (Female, DOB 01/25/1995, Age 29, SSN: 890-12-3457) inquiring about job opportunities. Resume attached. Contact: laura.anderson@jobseeker.com or 555-789-0125. Currently at 556 Career Path, Houston, TX 77001. I have 5 years food service experience. DL# D1928374. Very interested!', '2024-10-31', 'In Progress', 'Low'),
('Steven Jackson', 'Peking Truck', 'Steven Jackson (Male, DOB 07/04/1970, Age 54, SSN: 901-23-4568) with feedback. Your soup dumplings are the best! My doctor at 555-890-1236 recommended your food for my diet. Email: steven.j@health.net. Address: 778 Wellness Street, Minneapolis, MN 55401. Passport P11223344.', '2024-11-01', 'Closed', 'Low'),
('Karen Thomas', 'Revenge of the Curds', 'Karen Thomas (Female, DOB 12/18/1983, Age 40, SSN: 012-34-5679, DL# D4826159) requesting tax receipt for business expense. Business address: 334 Revenue Road, Sacramento, CA 95814. Email to karen.thomas@business.com. Phone: 555-901-2347. Order was $156.80 on card 4532-8765-4321-9876.', '2024-11-02', 'Open', 'Low'),
('Patricia White', 'Nani''s Kitchen', 'Patricia White here (Female, DOB 05/22/1989, Age 35, SSN: 123-45-6791, Passport P55667788). I joined your loyalty program. Card 4111-1111-1111-1111 on file. Ship rewards to 667 Member Lane, Miami, FL 33101. Contact: patricia.white@email.org or 555-012-3458. DL# D9517530. Member ID: CLB-99887. Love your food!', '2024-11-03', 'Closed', 'Low');

-- ============================================================================
-- CREATE VIEWS FOR ANALYTICS
-- ============================================================================

-- View for review analytics
CREATE OR REPLACE VIEW REVIEW_ANALYTICS AS
SELECT 
    food_truck_name,
    AVG(rating) as avg_rating,
    COUNT(*) as total_reviews,
    SUM(CASE WHEN rating >= 4 THEN 1 ELSE 0 END) as positive_reviews,
    SUM(CASE WHEN rating <= 2 THEN 1 ELSE 0 END) as negative_reviews
FROM CUSTOMER_REVIEWS
GROUP BY food_truck_name;

-- View for menu item popularity
CREATE OR REPLACE VIEW POPULAR_ITEMS AS
SELECT 
    menu_item,
    food_truck_name,
    COUNT(*) as order_count,
    AVG(rating) as avg_rating
FROM CUSTOMER_REVIEWS
GROUP BY menu_item, food_truck_name
ORDER BY order_count DESC;

-- ============================================================================
-- GRANT PRIVILEGES (adjust as needed for your environment)
-- ============================================================================

-- Grant usage on database and schema
GRANT USAGE ON DATABASE AI_FUNCTIONS_PLAYGROUND TO ROLE SYSADMIN;
GRANT USAGE ON SCHEMA AI_FUNCTIONS_PLAYGROUND.DEMO TO ROLE SYSADMIN;

-- Create warehouse for Cortex Search (if not exists)
CREATE WAREHOUSE IF NOT EXISTS CORTEX_SEARCH_WH
    WAREHOUSE_SIZE = 'XSMALL'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE;

-- Grant privileges on all tables
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA AI_FUNCTIONS_PLAYGROUND.DEMO TO ROLE SYSADMIN;

-- Grant privileges on stages
GRANT READ, WRITE ON STAGE AI_FUNCTIONS_PLAYGROUND.DEMO.AUDIO_STAGE TO ROLE SYSADMIN;
GRANT READ, WRITE ON STAGE AI_FUNCTIONS_PLAYGROUND.DEMO.DOCUMENT_STAGE TO ROLE SYSADMIN;
GRANT READ, WRITE ON STAGE AI_FUNCTIONS_PLAYGROUND.DEMO.SUPPLIER_DOCUMENTS_STAGE TO ROLE SYSADMIN;
GRANT READ, WRITE ON STAGE AI_FUNCTIONS_PLAYGROUND.DEMO.IMAGE_STAGE TO ROLE SYSADMIN;

-- Grant privileges on views
GRANT SELECT ON ALL VIEWS IN SCHEMA AI_FUNCTIONS_PLAYGROUND.DEMO TO ROLE SYSADMIN;

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

-- Verify food trucks
SELECT COUNT(*) as food_truck_count FROM FOOD_TRUCKS;

-- Verify menu items
SELECT COUNT(*) as menu_item_count FROM MENU_ITEMS;

-- Verify customer reviews
SELECT COUNT(*) as review_count FROM CUSTOMER_REVIEWS;

-- Verify support tickets
SELECT COUNT(*) as ticket_count FROM SUPPORT_TICKETS;
SELECT COUNT(*) as ticket_pii_count FROM SUPPORT_TICKETS_PII;

-- Verify document parsing tables
SELECT COUNT(*) as raw_docs_count FROM PARSE_DOC_RAW_TEXT;
SELECT COUNT(*) as chunked_docs_count FROM PARSE_DOC_CHUNKED_TEXT;

-- Verify supplier invoice details table
SELECT COUNT(*) as invoice_count FROM SUPPLIER_INVOICE_DETAILS;

-- List all stages
SHOW STAGES;

-- ============================================================================
-- SAMPLE FILE INSTRUCTIONS
-- ============================================================================

-- After running this script, you will need to manually upload sample files:
-- 
-- Option 1: Using Snowsight UI (Manual Upload)
-- Navigate to Data > Databases > AI_FUNCTIONS_PLAYGROUND > DEMO > Stages
-- Select the appropriate stage and click "+ Files" to upload files
-- Documentation: https://docs.snowflake.com/en/user-guide/data-load-local-file-system-stage-ui
--
-- Option 2: Using Snowflake CLI (PUT command)
-- 1. AUDIO FILES (for AI_TRANSCRIBE examples):
--    PUT file:///path/to/audio.wav @AUDIO_STAGE AUTO_COMPRESS=FALSE;
--
-- 2. DOCUMENT FILES (for AI_PARSE_DOCUMENT examples):
--    PUT file:///path/to/document.pdf @DOCUMENT_STAGE AUTO_COMPRESS=FALSE;
--
-- 3. SUPPLIER INVOICE FILES (for AI_EXTRACT examples):
--    PUT file://supplier_invoice_*.pdf @SUPPLIER_DOCUMENTS_STAGE AUTO_COMPRESS=FALSE;
--
-- 4. IMAGE FILES (for AI_CLASSIFY and AI_COMPLETE image examples):
--    PUT file:///path/to/image.jpg @IMAGE_STAGE AUTO_COMPRESS=FALSE;

-- ============================================================================
-- END OF SETUP SCRIPT
-- ============================================================================

SELECT 'Database setup completed successfully!' as status;

