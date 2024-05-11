alter table "public"."plans" alter column "price" drop default;

alter table "public"."plans" alter column "price" set data type double precision using "price"::double precision;


