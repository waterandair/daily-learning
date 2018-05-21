CREATE TABLE `userinfo` (
  `uid` INT(10) NOT NULL AUTO_INCREMENT ,
  `username` VARCHAR(64) null default null ,
  `department` varchar (64) null default null ,
  `created` date null default null ,
  primary key (`uid`)
);

create table `userdetail` (
  `uid` int (10) not null default 0,
  `intro` TEXT null,
  `pfrofile` TEXT null ,
  primary key (`uid`)
);

