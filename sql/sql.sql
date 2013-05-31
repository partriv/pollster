BEGIN;
CREATE TABLE `pollster_tag` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(30) NOT NULL UNIQUE,
    `date_created` datetime NOT NULL,
    `poll_count` integer NOT NULL
)
;
CREATE TABLE `pollster_poll` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `question` varchar(75) NOT NULL,
    `description` varchar(400) NOT NULL,
    `date_created` datetime NOT NULL,
    `date_modified` datetime NOT NULL,
    `active` bool NOT NULL,
    `user_id` integer NOT NULL,
    `url` varchar(75) NOT NULL,
    `link` varchar(250) NOT NULL,
    `total_votes` integer NOT NULL,
    `total_comments` integer NOT NULL,
    `allow_user_answers` bool NOT NULL,
    `video_link` varchar(800) NOT NULL,
    `inappropriate` bool NOT NULL
)
;
ALTER TABLE `pollster_poll` ADD CONSTRAINT user_id_refs_id_1891ee08 FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
CREATE TABLE `pollster_poll_tags` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `poll_id` integer NOT NULL,
    `tag_id` integer NOT NULL
)
;
ALTER TABLE `pollster_poll_tags` ADD CONSTRAINT poll_id_refs_id_4fdf0e5e FOREIGN KEY (`poll_id`) REFERENCES `pollster_poll` (`id`);
ALTER TABLE `pollster_poll_tags` ADD CONSTRAINT tag_id_refs_id_32507e4 FOREIGN KEY (`tag_id`) REFERENCES `pollster_tag` (`id`);
CREATE TABLE `pollster_pollfile` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `poll_id` integer NOT NULL,
    `file` varchar(100) NOT NULL,
    `main_file` varchar(100) NOT NULL
)
;
ALTER TABLE `pollster_pollfile` ADD CONSTRAINT poll_id_refs_id_4f686b91 FOREIGN KEY (`poll_id`) REFERENCES `pollster_poll` (`id`);
CREATE TABLE `pollster_pollanswer` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `poll_id` integer NOT NULL,
    `answer` varchar(70) NOT NULL,
    `user_id` integer NOT NULL
)
;
ALTER TABLE `pollster_pollanswer` ADD CONSTRAINT poll_id_refs_id_46e8fdcb FOREIGN KEY (`poll_id`) REFERENCES `pollster_poll` (`id`);
ALTER TABLE `pollster_pollanswer` ADD CONSTRAINT user_id_refs_id_61e9a330 FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
CREATE TABLE `pollster_pollvote` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `poll_id` integer NOT NULL,
    `date_created` datetime NOT NULL,
    `poll_answer_id` integer NOT NULL,
    `user_id` integer NOT NULL
)
;
ALTER TABLE `pollster_pollvote` ADD CONSTRAINT poll_id_refs_id_13971cf1 FOREIGN KEY (`poll_id`) REFERENCES `pollster_poll` (`id`);
ALTER TABLE `pollster_pollvote` ADD CONSTRAINT poll_answer_id_refs_id_2a68e6a9 FOREIGN KEY (`poll_answer_id`) REFERENCES `pollster_pollanswer` (`id`);
ALTER TABLE `pollster_pollvote` ADD CONSTRAINT user_id_refs_id_2d2b7c14 FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
CREATE TABLE `pollster_pollstermessage` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `date_created` datetime NOT NULL,
    `to_user_id` integer NOT NULL,
    `from_user_id` integer NOT NULL,
    `subject` varchar(100) NULL,
    `body` varchar(1500) NOT NULL,
    `read` bool NOT NULL
)
;
ALTER TABLE `pollster_pollstermessage` ADD CONSTRAINT to_user_id_refs_id_7b468f56 FOREIGN KEY (`to_user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `pollster_pollstermessage` ADD CONSTRAINT from_user_id_refs_id_7b468f56 FOREIGN KEY (`from_user_id`) REFERENCES `auth_user` (`id`);
CREATE TABLE `pollster_userdata` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL UNIQUE,
    `profile_pic` varchar(255) NULL,
    `default_chart_type` varchar(60) NOT NULL
)
;
ALTER TABLE `pollster_userdata` ADD CONSTRAINT user_id_refs_id_679a4266 FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
CREATE TABLE `pollster_userdata_polls_watched` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `userdata_id` integer NOT NULL,
    `poll_id` integer NOT NULL
)
;
ALTER TABLE `pollster_userdata_polls_watched` ADD CONSTRAINT userdata_id_refs_id_71e15a21 FOREIGN KEY (`userdata_id`) REFERENCES `pollster_userdata` (`id`);
ALTER TABLE `pollster_userdata_polls_watched` ADD CONSTRAINT poll_id_refs_id_fe2f159 FOREIGN KEY (`poll_id`) REFERENCES `pollster_poll` (`id`);
CREATE TABLE `pollster_userprofile` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL UNIQUE,
    `sex` bool NULL,
    `birthday` date NULL,
    `country` integer NULL,
    `city` varchar(64) NULL,
    `state` varchar(2) NULL,
    `zip_code` varchar(32) NULL,
    `phone` varchar(20) NULL,
    `income` smallint NULL,
    `ethnicity` smallint NULL,
    `sexual_orientation` smallint NULL,
    `relationship_status` smallint NULL,
    `about` longtext NULL,
    `political_id` integer NULL,
    `religious_id` integer NULL,
    `education_id` integer NULL,
    `work_id` integer NULL
)
;
ALTER TABLE `pollster_userprofile` ADD CONSTRAINT user_id_refs_id_61b371e2 FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `pollster_userprofile` ADD CONSTRAINT political_id_refs_id_f9146cd FOREIGN KEY (`political_id`) REFERENCES `pollster_tag` (`id`);
ALTER TABLE `pollster_userprofile` ADD CONSTRAINT religious_id_refs_id_f9146cd FOREIGN KEY (`religious_id`) REFERENCES `pollster_tag` (`id`);
ALTER TABLE `pollster_userprofile` ADD CONSTRAINT education_id_refs_id_f9146cd FOREIGN KEY (`education_id`) REFERENCES `pollster_tag` (`id`);
ALTER TABLE `pollster_userprofile` ADD CONSTRAINT work_id_refs_id_f9146cd FOREIGN KEY (`work_id`) REFERENCES `pollster_tag` (`id`);
CREATE TABLE `pollster_screenname` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `screen_name` varchar(64) NOT NULL,
    `service` smallint NOT NULL,
    `user_profile_id` integer NOT NULL
)
;
ALTER TABLE `pollster_screenname` ADD CONSTRAINT user_profile_id_refs_id_21d49293 FOREIGN KEY (`user_profile_id`) REFERENCES `pollster_userprofile` (`id`);
CREATE TABLE `pollster_poll_tags` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `poll_id` integer NOT NULL,
    `tag_id` integer NOT NULL,
    UNIQUE (`poll_id`, `tag_id`)
)
;
ALTER TABLE `pollster_poll_tags` ADD CONSTRAINT poll_id_refs_id_4fdf0e5e FOREIGN KEY (`poll_id`) REFERENCES `pollster_poll` (`id`);
ALTER TABLE `pollster_poll_tags` ADD CONSTRAINT tag_id_refs_id_32507e4 FOREIGN KEY (`tag_id`) REFERENCES `pollster_tag` (`id`);
CREATE TABLE `pollster_userdata_polls_watched` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `userdata_id` integer NOT NULL,
    `poll_id` integer NOT NULL,
    UNIQUE (`userdata_id`, `poll_id`)
)
;
ALTER TABLE `pollster_userdata_polls_watched` ADD CONSTRAINT userdata_id_refs_id_71e15a21 FOREIGN KEY (`userdata_id`) REFERENCES `pollster_userdata` (`id`);
ALTER TABLE `pollster_userdata_polls_watched` ADD CONSTRAINT poll_id_refs_id_fe2f159 FOREIGN KEY (`poll_id`) REFERENCES `pollster_poll` (`id`);
CREATE TABLE `pollster_userdata_messages` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `userdata_id` integer NOT NULL,
    `pollstermessage_id` integer NOT NULL,
    UNIQUE (`userdata_id`, `pollstermessage_id`)
)
;
ALTER TABLE `pollster_userdata_messages` ADD CONSTRAINT userdata_id_refs_id_6bad3853 FOREIGN KEY (`userdata_id`) REFERENCES `pollster_userdata` (`id`);
ALTER TABLE `pollster_userdata_messages` ADD CONSTRAINT pollstermessage_id_refs_id_34012743 FOREIGN KEY (`pollstermessage_id`) REFERENCES `pollster_pollstermessage` (`id`);
CREATE TABLE `pollster_userdata_friends` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `userdata_id` integer NOT NULL,
    `user_id` integer NOT NULL,
    UNIQUE (`userdata_id`, `user_id`)
)
;
ALTER TABLE `pollster_userdata_friends` ADD CONSTRAINT userdata_id_refs_id_219a4bb9 FOREIGN KEY (`userdata_id`) REFERENCES `pollster_userdata` (`id`);
ALTER TABLE `pollster_userdata_friends` ADD CONSTRAINT user_id_refs_id_71ef9544 FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
CREATE TABLE `pollster_userprofile_interests` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `userprofile_id` integer NOT NULL,
    `tag_id` integer NOT NULL,
    UNIQUE (`userprofile_id`, `tag_id`)
)
;
ALTER TABLE `pollster_userprofile_interests` ADD CONSTRAINT userprofile_id_refs_id_5509da37 FOREIGN KEY (`userprofile_id`) REFERENCES `pollster_userprofile` (`id`);
ALTER TABLE `pollster_userprofile_interests` ADD CONSTRAINT tag_id_refs_id_3de8d38b FOREIGN KEY (`tag_id`) REFERENCES `pollster_tag` (`id`);
CREATE TABLE `pollster_userprofile_music` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `userprofile_id` integer NOT NULL,
    `tag_id` integer NOT NULL,
    UNIQUE (`userprofile_id`, `tag_id`)
)
;
ALTER TABLE `pollster_userprofile_music` ADD CONSTRAINT userprofile_id_refs_id_78211d57 FOREIGN KEY (`userprofile_id`) REFERENCES `pollster_userprofile` (`id`);
ALTER TABLE `pollster_userprofile_music` ADD CONSTRAINT tag_id_refs_id_39e2a6b FOREIGN KEY (`tag_id`) REFERENCES `pollster_tag` (`id`);
CREATE TABLE `pollster_userprofile_tv` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `userprofile_id` integer NOT NULL,
    `tag_id` integer NOT NULL,
    UNIQUE (`userprofile_id`, `tag_id`)
)
;
ALTER TABLE `pollster_userprofile_tv` ADD CONSTRAINT userprofile_id_refs_id_227d5cfb FOREIGN KEY (`userprofile_id`) REFERENCES `pollster_userprofile` (`id`);
ALTER TABLE `pollster_userprofile_tv` ADD CONSTRAINT tag_id_refs_id_2afc2d9 FOREIGN KEY (`tag_id`) REFERENCES `pollster_tag` (`id`);
CREATE TABLE `pollster_userprofile_books` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `userprofile_id` integer NOT NULL,
    `tag_id` integer NOT NULL,
    UNIQUE (`userprofile_id`, `tag_id`)
)
;
ALTER TABLE `pollster_userprofile_books` ADD CONSTRAINT userprofile_id_refs_id_6c902aa FOREIGN KEY (`userprofile_id`) REFERENCES `pollster_userprofile` (`id`);
ALTER TABLE `pollster_userprofile_books` ADD CONSTRAINT tag_id_refs_id_7f59a9c2 FOREIGN KEY (`tag_id`) REFERENCES `pollster_tag` (`id`);
CREATE TABLE `pollster_userprofile_movies` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `userprofile_id` integer NOT NULL,
    `tag_id` integer NOT NULL,
    UNIQUE (`userprofile_id`, `tag_id`)
)
;
ALTER TABLE `pollster_userprofile_movies` ADD CONSTRAINT userprofile_id_refs_id_865925c FOREIGN KEY (`userprofile_id`) REFERENCES `pollster_userprofile` (`id`);
ALTER TABLE `pollster_userprofile_movies` ADD CONSTRAINT tag_id_refs_id_461d5530 FOREIGN KEY (`tag_id`) REFERENCES `pollster_tag` (`id`);
COMMIT;
