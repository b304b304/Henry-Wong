create database productInfo;
use productInfo;
SET SQL_SAFE_UPDATES = 0;

create table ProductTypeInfo
(
Product_Type_ID int NOT NULL auto_increment,
Product_Type varchar(50) unique,
UpdateTime varchar(50),
User varchar(50),
primary key(Product_Type_ID)
)engine=InnoDB default charset=utf8 auto_increment=1;

create table BrandInfo
(
Brand_ID int NOT NULL auto_increment,
Brand_Name varchar(50) unique,
UpdateTime varchar(50),
User varchar(50),
primary key(Brand_ID)
)engine=InnoDB default charset=utf8 auto_increment=1;

create table DataSourceInfo
(
DataSource_ID int NOT NULL auto_increment,
DataSource_CNname varchar(50) unique,
URL varchar(50),
UpdateTime varchar(50),
User varchar(128),
primary key(DataSource_ID)
)engine=InnoDB default charset=utf8 auto_increment=1;

create table RootURLInfo
(
RootURL_ID int NOT NULL auto_increment,
Brand_ID int,
Product_Type_ID int,
DataSource_ID int,
Root_URL varchar(128),
UpdateTime varchar(50),
User varchar(50),
primary key (RootURL_ID),
foreign key (Brand_ID) references BrandInfo(Brand_ID),
foreign key (Product_Type_ID) references ProductTypeInfo(Product_Type_ID),
foreign key (DataSource_ID) references DataSourceInfo(DataSource_ID)
)engine=InnoDB default charset=utf8 auto_increment=1;

DROP TABLE ProductTypeInfo;
DROP TABLE BrandInfo;
DROP TABLE DataSourceInfo;
DROP TABLE RootURLInfo;

SET SQL_SAFE_UPDATES = 1;
