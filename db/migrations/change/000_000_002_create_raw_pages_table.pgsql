
create table vorp.raw_pages(
  id serial primary key,

  url varchar unique,
  season varchar,
  raw_html text,
  type varchar,

  created_at timestamp default current_timestamp,
  updated_at timestamp default current_timestamp,
  deleted_at timestamp
);

create unique index raw_pages_url_idx on vorp.raw_pages (url);
create index raw_pages_type_idx on vorp.raw_pages (type);
create index raw_pages_season_idx on vorp.raw_pages (season);

create trigger set_raw_pages_updated_at
  before update on vorp.raw_pages
  for each row
  execute procedure trigger_set_updated_at();
