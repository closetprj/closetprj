import sqlite3

#Open database
conn = sqlite3.connect('user.db')

conn.execute('''drop table if exists users;''')
conn.execute('''create table users (
  username text primary key,
  password text not null
)''')
conn.execute('''drop table if exists user_watchlists;''')
conn.execute('''create table user_watchlists(
  watchlist_id integer primary key AUTOINCREMENT,
  username text,
  email TEXT,
  gender text,
  firstName TEXT,
  lastName TEXT,
  address1 TEXT,
		postcode TEXT,
		city TEXT,
		phone TEXT,
  foreign key(username) references users(username)
)''')

conn.execute('''drop table if exists products;''')
conn.execute('''CREATE TABLE products
		(productId INTEGER PRIMARY KEY,
		name TEXT,
		price REAL,
		gender text,
		description TEXT,
		image TEXT,
		stock INTEGER,
		categoryId INTEGER,
		state text,
		FOREIGN KEY(categoryId) REFERENCES categories(categoryId)
		)''')

conn.execute('''drop table if exists categories;''')
conn.execute('''CREATE TABLE categories
		(categoryId INTEGER PRIMARY KEY,
		type TEXT,
		gender text
		)''')

conn.execute('''CREATE TABLE kart
    (watchlist_id integer,
    items_id integer PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    productId INTEGER,
    FOREIGN KEY(watchlist_id) REFERENCES user_watchlists(watchlist_id),
    FOREIGN KEY(username) REFERENCES users(username),
    FOREIGN KEY(productId) REFERENCES products(productId)
    )''')
conn.execute('''drop table if exists ordernum;''')
conn.execute('''CREATE TABLE ordernum(
    watchlist_id integer,
    order_id integer PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    status text,
    FOREIGN KEY(watchlist_id) REFERENCES user_watchlists(watchlist_id),
    FOREIGN KEY(username) REFERENCES users(username)
    )''')

conn.execute('''drop table if exists state;''')
conn.execute('''CREATE TABLE state
    (watchlist_id integer,
    username TEXT,
    order_id integer,
    productId INTEGER,
    FOREIGN KEY(watchlist_id) REFERENCES user_watchlists(watchlist_id),
    FOREIGN KEY(username) REFERENCES users(username),
    FOREIGN KEY(productId) REFERENCES products(productId),
    FOREIGN KEY(order_id) REFERENCES ordernum(order_id)
    )''')
conn.execute('''insert into products values(101, 'Puffy Jacket','250','m','Pristine Condition','101.jpg','100','4','p');''')
conn.execute('''insert into products values(102, 'Ice Jacket','240','m','Pristine Condition','102.jpg','100','4','p');''')
conn.execute('''insert into products values(103, 'Lakers Sweatshirt','160','m','Pristine Condition','103.jpg','100','6','p');''')
conn.execute('''insert into products values(104, 'Ink Sweatshirt','150','m','Pristine Condition','104.jpg','100','6','p');''')
conn.execute('''insert into products values(105, 'Red Jacket','220','m','Pristine Condition','105.jpg','100','4','n');''')
conn.execute('''insert into products values(106, 'Stripe Sweatshirt','150','m','Pristine Condition','106.jpg','100','6','p');''')
conn.execute('''insert into products values(107, 'Navy Shirt','180','m','Pristine Condition','107.jpg','120','2','p');''')
conn.execute('''insert into products values(108, 'Brown Sweatshirt','330','m','Pristine Condition','108.jpg','30','6','p');''')
conn.execute('''insert into products values(109, 'Vintage Tee','80','m','Pristine Condition','109.jpg','100','1','p');''')
conn.execute('''insert into products values(110, 'Black Tee','80','m','Pristine Condition','110.jpg','100','1','p');''')
conn.execute('''insert into products values(111, 'Ash Grey Sweatshirt','260','m','Pristine Condition','111.jpg','100','6','p');''')
conn.execute('''insert into products values(112, 'Teal Tee','90','m','Pristine Condition','112.jpg','100','1','p');''')
conn.execute('''insert into products values(113, 'Royal Tee','85','m','Pristine Condition','113.jpg','100','1','p');''')
conn.execute('''insert into products values(114, 'Windproof Jacket','250','m','Pristine Condition','114.jpg','100','4','p');''')
conn.execute('''insert into products values(115, 'Black Trackpant','140','m','Pristine Condition','115.jpg','100','5','p');''')
conn.execute('''insert into products values(116, 'Chicago Tee','90','m','Pristine Condition','116.jpg','100','1','n');''')
conn.execute('''insert into products values(117, 'Sonic Tee','80','m','Pristine Condition','117.jpg','100','1','p');''')
conn.execute('''insert into products values(118, 'Purple Sweatpant','150','m','Pristine Condition','118.jpg','100','5','p');''')
conn.execute('''insert into products values(119, 'White Jumper','160','m','Pristine Condition','119.jpg','100','6','n');''')
conn.execute('''insert into products values(120, 'Wool Jacket','270','m','Pristine Condition','120.jpg','100','4','p');''')
conn.execute('''insert into products values(121, 'Leopard Shirt','180','m','Pristine Condition','121.jpg','120','2','p');''')
conn.execute('''insert into products values(122, 'Flower Shirt','180','m','Pristine Condition','122.jpg','120','2','p');''')
conn.execute('''insert into products values(123, 'Corduroy Hoodie','180','m','Pristine Condition','123.jpg','100','6','n');''')
conn.execute('''insert into products values(124, 'Grey Jumper','160','m','Pristine Condition','124.jpg','100','6','n');''')
conn.execute('''insert into products values(125, 'Goose Down Jacket','290','m','Pristine Condition','125.jpg','90','4','n');''')
conn.execute('''insert into products values(126, 'Olive Jacket','290','m','Pristine Condition','126.jpg','90','4','n');''')
conn.execute('''insert into products values(127, 'Soft Hoodie','160','m','Pristine Condition','127.jpg','100','6','n');''')
conn.execute('''insert into products values(128, 'Forest Green Jumper','320','m','Pristine Condition','128.jpg','100','6','n');''')
conn.execute('''insert into products values(129, 'White Jumper','160','m','Pristine Condition','129.jpg','100','6','n');''')
conn.execute('''insert into products values(130, 'Old Navy Tee','80','m','Pristine Condition','130.jpg','100','1','n');''')
conn.execute('''insert into products values(131, 'Red on Navy Tee','80','m','Pristine Condition','131.jpg','100','1','n');''')
conn.execute('''insert into products values(132, 'Royal Hoodie','300','m','Pristine Condition','132.jpg','100','6','n');''')
conn.execute('''insert into products values(133, 'Black Light Jacket','290','m','Pristine Condition','133.jpg','100','4','n');''')
conn.execute('''insert into products values(134, 'Mountain Jacket','320','m','Pristine Condition','134.jpg','100','4','n');''')
conn.execute('''insert into products values(135, 'Wine Jacket','250','m','Pristine Condition','135.jpg','100','4','n');''')
conn.execute('''insert into products values(136, 'Black Hoodie','350','m','Pristine Condition','136.jpg','100','6','n');''')
conn.execute('''insert into products values(137, 'Grey Embroidery Hoodie','320','m','Pristine Condition','137.jpg','100','6','n');''')
conn.execute('''insert into products values(138, 'Dots Grey Hoodie','320','m','Pristine Condition','138.jpg','100','6','n');''')
conn.execute('''insert into products values(139, 'Yellow Hoodie','320','m','Pristine Condition','139.jpg','100','6','n');''')
conn.execute('''insert into products values(140, 'Peach Hoodie','320','m','Pristine Condition','140.jpg','100','6','n');''')
conn.execute('''insert into products values(141, 'Grey Tee','80','m','Pristine Condition','141.jpg','100','1','n');''')
conn.execute('''insert into products values(142, 'Yellow on Black Tee','80','m','Pristine Condition','142.jpg','100','1','n');''')
conn.execute('''insert into products values(143, 'Black and White Tee','80','m','Pristine Condition','143.jpg','100','1','n');''')
conn.execute('''insert into products values(144, 'Yellow Tee','80','m','Pristine Condition','144.jpg','100','1','n');''')
conn.execute('''insert into products values(145, 'Grey Apple Tee','80','m','Pristine Condition','145.jpg','100','1','n');''')
conn.execute('''insert into products values(146, 'Cat WomanTee','80','m','Pristine Condition','146.jpg','100','1','n');''')
conn.execute('''insert into products values(147, 'Night Jacket','380','m','Pristine Condition','147.jpg','100','4','n');''')
conn.execute('''insert into products values(148, 'Duffle Jacket','380','m','Pristine Condition','148.jpg','100','4','n');''')
conn.execute('''insert into products values(149, 'Red and Black Tee','80','m','Pristine Condition','149.jpg','100','1','n');''')
conn.execute('''insert into products values(150, 'Black Puffy Jacket','380','m','Pristine Condition','150.jpg','100','4','n');''')
conn.execute('''insert into products values(151, 'Blue Mock Anorak','320','m','Pristine Condition','151.jpg','100','6','n');''')
conn.execute('''insert into products values(152, 'Patched Denim','180','m','Pristine Condition','152.jpg','100','5','n');''')
conn.execute('''insert into products values(153, 'Denim Jacket','290','m','Pristine Condition','153.jpg','100','4','n');''')
conn.execute('''insert into products values(154, 'Blue Denim','340','m','Pristine Condition','154.jpg','100','5','n');''')
conn.execute('''insert into products values(155, 'Stripe Jumper','320','m','Pristine Condition','155.jpg','100','6','n');''')
conn.execute('''insert into products values(156, 'Cream WorkPant','180','m','Pristine Condition','156.jpg','100','5','n');''')
conn.execute('''insert into products values(157, 'Purple Fleece','220','m','Pristine Condition','157.jpg','100','6','n');''')
conn.execute('''insert into products values(158, 'Windproof Mock','220','m','Pristine Condition','158.jpg','100','6','n');''')
conn.execute('''insert into products values(159, 'Navy Goose Jacket','290','m','Pristine Condition','159.jpg','100','4','n');''')
conn.execute('''insert into products values(160, 'Burgundy Puff Jacket','290','m','Pristine Condition','160.jpg','100','4','n');''')
conn.execute('''insert into products values(161, 'Light Jacket','290','m','Pristine Condition','161.jpg','100','4','n');''')
conn.execute('''insert into products values(162, 'Dark Blue Shirt','180','m','Pristine Condition','162.jpg','120','2','p');''')
conn.execute('''insert into products values(163, 'Wool Duffle Jacket','290','m','Pristine Condition','163.jpg','100','4','n');''')
conn.execute('''insert into products values(164, 'Navy Thick Jacket','290','m','Pristine Condition','164.jpg','100','4','n');''')
conn.execute('''insert into products values(165, 'Yellow Light Jacket','290','m','Pristine Condition','165.jpg','100','4','n');''')
conn.execute('''insert into products values(166, 'Leather Jacket','290','m','Pristine Condition','166.jpg','100','4','n');''')
conn.execute('''insert into products values(167, 'Cream Jacket','290','m','Pristine Condition','167.jpg','100','4','n');''')
conn.execute('''insert into products values(168, 'Wool Vest','290','m','Pristine Condition','168.jpg','100','4','n');''')
conn.execute('''insert into products values(169, 'Yellow Shirt','180','m','Pristine Condition','169.jpg','120','2','n');''')
conn.execute('''insert into products values(170, 'Yellow Light Jacket','290','m','Pristine Condition','170.jpg','100','4','n');''')
conn.execute('''insert into products values(171, 'Camel Shirt','180','m','Pristine Condition','171.jpg','120','2','n');''')
conn.execute('''insert into products values(172, 'Pure Yellow Crewneck','220','m','Pristine Condition','172.jpg','100','6','n');''')
conn.execute('''insert into products values(173, 'Black Fade Tee','80','m','Pristine Condition','173.jpg','100','1','n');''')
conn.execute('''insert into products values(174, 'Green Stripe Crewneck','220','m','Pristine Condition','174.jpg','100','6','n');''')
conn.execute('''insert into products values(175, 'Ice Blue Navy Jacket','230','m','Pristine Condition','175.jpg','100','4','n');''')
conn.execute('''insert into products values(176, 'Old School Coach Jacket','250','m','Pristine Condition','176.jpg','100','4','n');''')
conn.execute('''insert into products values(177, 'Red Wool Shirt','180','m','Pristine Condition','177.jpg','120','2','n');''')
conn.execute('''insert into products values(178, 'Thick Warm Jacket','200','m','Pristine Condition','178.jpg','100','4','n');''')
conn.execute('''insert into products values(179, 'Classic Red Crewneck','220','m','Pristine Condition','179.jpg','100','6','n');''')
conn.execute('''insert into products values(180, '90s Track Pant','180','m','Pristine Condition','180.jpg','100','5','n');''')
conn.execute('''insert into products values(181, 'Yellow Swoosh Crewneck','220','m','Pristine Condition','181.jpg','100','6','n');''')
conn.execute('''insert into products values(182, '90s Sports Jacket','200','m','Pristine Condition','182.jpg','100','4','n');''')
conn.execute('''insert into products values(183, 'Light Blue Shirt','160','m','Pristine Condition','183.jpg','120','2','n');''')
conn.execute('''insert into products values(184, 'Light Purple Jumper','200','m','Pristine Condition','184.jpg','100','6','n');''')
conn.execute('''insert into products values(185, 'Dark Navy Tee','80','m','Pristine Condition','185.jpg','100','1','n');''')
conn.execute('''insert into products values(186, 'Dark Yellow Shirt','180','m','Pristine Condition','186.jpg','120','2','n');''')
conn.execute('''insert into products values(187, 'Original Jumper','200','m','Pristine Condition','187.jpg','100','6','n');''')
conn.execute('''insert into products values(188, 'Sports Jumper','180','m','Pristine Condition','188.jpg','100','6','n');''')
conn.execute('''insert into products values(189, '80s Jacket','200','m','Pristine Condition','189.jpg','100','4','n');''')
conn.execute('''insert into products values(190, 'Denim Jacket','200','m','Pristine Condition','190.jpg','100','4','n');''')
conn.execute('''insert into products values(191, 'Waffle Shirt','180','m','Pristine Condition','191.jpg','120','2','n');''')
conn.execute('''insert into products values(192, '90s Training Pant','150','m','Pristine Condition','192.jpg','100','5','n');''')
conn.execute('''insert into products values(193, '90s Sports Pant','180','m','Pristine Condition','193.jpg','100','5','n');''')
conn.execute('''insert into products values(194, '90s Windproof Pant','185','m','Pristine Condition','194.jpg','100','5','n');''')
conn.execute('''insert into products values(195, 'Dark Navy Pant','180','m','Pristine Condition','195.jpg','100','5','n');''')
conn.execute('''insert into products values(196, 'Outdoor Hoodie','200','m','Pristine Condition','196.jpg','100','6','n');''')
conn.execute('''insert into products values(197, 'Vintage Denim','160','m','Pristine Condition','197.jpg','100','5','n');''')
conn.execute('''insert into products values(198, 'Classic Warmpant','130','m','Pristine Condition','198.jpg','100','5','n');''')
conn.execute('''insert into products values(199, 'Cnvas Pant','190','m','Pristine Condition','199.jpg','100','5','n');''')
conn.execute('''insert into products values(200, 'Olive Stripe Tee','80','m','Pristine Condition','200.jpg','100','1','n');''')
conn.execute('''insert into products values(201, 'Peach Tee','80','m','Pristine Condition','201.jpg','100','1','n');''')
conn.execute('''insert into products values(202, 'Navy Tee','80','m','Pristine Condition','202.jpg','100','1','n');''')
conn.execute('''insert into products values(203, 'Denim Shirt','180','m','Pristine Condition','203.jpg','120','2','n');''')
conn.execute('''insert into products values(204, 'White Shirt','180','m','Pristine Condition','204.jpg','120','2','n');''')
conn.execute('''insert into products values(205, 'Purple Silk Shirt','180','m','Pristine Condition','205.jpg','120','2','n');''')
conn.execute('''insert into products values(206, 'Corduroy Shirt','180','m','Pristine Condition','206.jpg','120','2','n');''')
conn.execute('''insert into products values(207, 'Dark Purple Shirt','180','m','Pristine Condition','207.jpg','120','2','n');''')
conn.execute('''insert into products values(208, 'Red Teddy Jumper','200','m','Pristine Condition','208.jpg','100','6','n');''')
conn.execute('''insert into products values(209, 'Leather Jacket','290','m','Pristine Condition','209.jpg','100','4','n');''')
conn.execute('''insert into products values(210, 'Black Cartoon Hoodie','210','m','Pristine Condition','210.jpg','100','6','n');''')
conn.execute('''insert into products values(211, 'Navy Cargo Pant','130','m','Pristine Condition','211.jpg','100','5','n');''')
conn.execute('''insert into products values(212, 'Half Zip Jumper','170','m','Pristine Condition','212.jpg','100','6','n');''')
conn.execute('''insert into products values(213, 'Dark Windproof Jacket','210','m','Pristine Condition','213.jpg','100','4','n');''')
conn.execute('''insert into products values(214, 'Lakers Jacket','290','m','Pristine Condition','214.jpg','100','4','n');''')
conn.execute('''insert into products values(215, 'Wool Baseball Jacket','400','m','Pristine Condition','215.jpg','100','4','n');''')
conn.execute('''insert into products values(216, 'Wool Baseball Jacket','400','m','Pristine Condition','216.jpg','100','4','n');''')
conn.commit()
conn.close()