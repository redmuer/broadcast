create table if not exists bill_base (
fid varchar(200) primary key not null,
fname vachar(200),
start_time time,
end_time time,
url varchar(300),
build_time time,
is_del int
);

create table if not exists bill_pull (
fid varchar(200) primary key not null,
bill_id varchar(200),
url_param varchar(200),
des varchar(200),
build_time time,
is_del int
);

create table if not exists bill_access (
fid varchar(200) primary key not null,
bill_id varchar(200),
bill_pull_id varchar(200),
visitor varchar(200),
visit_time time,
visit_long float
);

create table if not exists bill_commodity_base (
fid varchar(200) primary key not null,
bill_id varchar(200),
fname varchar(200),
url varchar(200),
total_count int,
revenue_count int,
price float
);

create table if not exists commodity_reserve (
fid varchar(200) primary key not null,
bill_commodity_id varchar(200),
bill_pull_id varchar(200),
visitor varchar(200),
reserve_time time
);



