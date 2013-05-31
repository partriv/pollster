-- THIS IS A TEMP FILE TO BE USED FOR SHIT TO APPLY FROM PATCH TO PATCH --

INSERT INTO pollster_pollwatch (poll_id, user_id, date_created)
select pw.poll_id, ud.user_id, '2009-05-17 00:00:00'
from pollster_userdata_polls_watched pw, pollster_userdata ud
where pw.userdata_id = ud.id


DROP TABLE IF EXISTS `pollster`.`pollster_userdata_polls_watched`;
CREATE TABLE  `pollster`.`pollster_userdata_polls_watched` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userdata_id` int(11) NOT NULL,
  `pollwatch_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `userdata_id` (`userdata_id`,`pollwatch_id`),
  KEY `pollwatch_id_refs_id_fe2f159` (`pollwatch_id`)
) ENGINE=MyISAM AUTO_INCREMENT=27 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;



insert into  pollster_userdata_polls_watched(userdata_id, pollwatch_id)
select ud.id, pw.id
from pollster_pollwatch pw, pollster_userdata ud
where pw.user_id = ud.user_id