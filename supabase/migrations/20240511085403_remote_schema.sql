alter table "public"."plans" add column "name" text not null default 'DEMO'::text;

alter table "public"."plans" add column "popularity_score" bigint not null default '0'::bigint;

alter table "public"."profiles" alter column "expiry_date" drop not null;


