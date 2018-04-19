CREATE TABLE `lists` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `chat_id` int(255) NOT NULL,
  `list_name` varchar(255) NOT NULL,
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `chat_list_index` (`chat_id`,`list_name`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=big5;

CREATE TABLE `items` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `chat_id` int(255) NOT NULL,
  `list_name` varchar(255) NOT NULL,
  `item` longtext,
  `checked` int(11) DEFAULT '0',
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_items_1_idx` (`id`),
  KEY `index3` (`chat_id`,`list_name`),
  CONSTRAINT `fk_items_1` FOREIGN KEY (`chat_id`, `list_name`) REFERENCES `lists` (`chat_id`, `list_name`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=big5;
