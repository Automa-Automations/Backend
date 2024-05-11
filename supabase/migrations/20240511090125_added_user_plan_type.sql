alter table "public"."profiles" add column "plan_type" text;

alter table "public"."profiles" add constraint "public_profiles_plan_type_fkey" FOREIGN KEY (plan_type) REFERENCES plans(id) not valid;

alter table "public"."profiles" validate constraint "public_profiles_plan_type_fkey";


