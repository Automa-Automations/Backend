alter table "public"."proxies" enable row level security;

CREATE UNIQUE INDEX bot_sessions_pkey ON public.bot_sessions USING btree (id);


CREATE UNIQUE INDEX instagram_bots_pkey ON public.bots USING btree (id);




alter table "public"."bot_sessions" add constraint "bot_sessions_pkey" PRIMARY KEY using index "bot_sessions_pkey";

alter table "public"."bots" add constraint "instagram_bots_pkey" PRIMARY KEY using index "instagram_bots_pkey";



alter table "public"."bot_sessions" add constraint "bot_sessions_owner_id_fkey" FOREIGN KEY (owner_id) REFERENCES profiles(id) not valid;

alter table "public"."bot_sessions" validate constraint "bot_sessions_owner_id_fkey";

alter table "public"."bots" add constraint "bots_session_id_fkey" FOREIGN KEY (session_id) REFERENCES bot_sessions(id) not valid;

alter table "public"."bots" validate constraint "bots_session_id_fkey";

alter table "public"."bots" add constraint "instagram_bots_owner_id_fkey" FOREIGN KEY (owner_id) REFERENCES profiles(id) not valid;

alter table "public"."bots" validate constraint "instagram_bots_owner_id_fkey";

alter table "public"."bots" add constraint "instagram_bots_proxy_id_fkey" FOREIGN KEY (proxy_id) REFERENCES proxies(id) not valid;

alter table "public"."bots" validate constraint "instagram_bots_proxy_id_fkey";


set check_function_bodies = off;

CREATE OR REPLACE FUNCTION public.handle_new_user()
 RETURNS trigger
 LANGUAGE plpgsql
 SECURITY DEFINER
AS $function$
begin
  insert into public.profiles (id, full_name, avatar_url)
  values (new.id, new.raw_user_meta_data->>'full_name', new.raw_user_meta_data->>'avatar_url');
  return new;
end;
$function$
;

grant delete on table "public"."bot_sessions" to "anon";

grant insert on table "public"."bot_sessions" to "anon";

grant references on table "public"."bot_sessions" to "anon";

grant select on table "public"."bot_sessions" to "anon";

grant trigger on table "public"."bot_sessions" to "anon";

grant truncate on table "public"."bot_sessions" to "anon";

grant update on table "public"."bot_sessions" to "anon";

grant delete on table "public"."bot_sessions" to "authenticated";

grant insert on table "public"."bot_sessions" to "authenticated";

grant references on table "public"."bot_sessions" to "authenticated";

grant select on table "public"."bot_sessions" to "authenticated";

grant trigger on table "public"."bot_sessions" to "authenticated";

grant truncate on table "public"."bot_sessions" to "authenticated";

grant update on table "public"."bot_sessions" to "authenticated";

grant delete on table "public"."bot_sessions" to "service_role";

grant insert on table "public"."bot_sessions" to "service_role";

grant references on table "public"."bot_sessions" to "service_role";

grant select on table "public"."bot_sessions" to "service_role";

grant trigger on table "public"."bot_sessions" to "service_role";

grant truncate on table "public"."bot_sessions" to "service_role";

grant update on table "public"."bot_sessions" to "service_role";

grant delete on table "public"."bots" to "anon";

grant insert on table "public"."bots" to "anon";

grant references on table "public"."bots" to "anon";

grant select on table "public"."bots" to "anon";

grant trigger on table "public"."bots" to "anon";

grant truncate on table "public"."bots" to "anon";

grant update on table "public"."bots" to "anon";

grant delete on table "public"."bots" to "authenticated";

grant insert on table "public"."bots" to "authenticated";

grant references on table "public"."bots" to "authenticated";

grant select on table "public"."bots" to "authenticated";

grant trigger on table "public"."bots" to "authenticated";

grant truncate on table "public"."bots" to "authenticated";

grant update on table "public"."bots" to "authenticated";

grant delete on table "public"."bots" to "service_role";

grant insert on table "public"."bots" to "service_role";

grant references on table "public"."bots" to "service_role";

grant select on table "public"."bots" to "service_role";

grant trigger on table "public"."bots" to "service_role";

grant truncate on table "public"."bots" to "service_role";

grant update on table "public"."bots" to "service_role";





















grant delete on table "public"."profiles" to "anon";

grant insert on table "public"."profiles" to "anon";

grant references on table "public"."profiles" to "anon";

grant select on table "public"."profiles" to "anon";

grant trigger on table "public"."profiles" to "anon";

grant truncate on table "public"."profiles" to "anon";

grant update on table "public"."profiles" to "anon";

grant delete on table "public"."profiles" to "authenticated";

grant insert on table "public"."profiles" to "authenticated";

grant references on table "public"."profiles" to "authenticated";

grant select on table "public"."profiles" to "authenticated";

grant trigger on table "public"."profiles" to "authenticated";

grant truncate on table "public"."profiles" to "authenticated";

grant update on table "public"."profiles" to "authenticated";

grant delete on table "public"."profiles" to "service_role";

grant insert on table "public"."profiles" to "service_role";

grant references on table "public"."profiles" to "service_role";

grant select on table "public"."profiles" to "service_role";

grant trigger on table "public"."profiles" to "service_role";

grant truncate on table "public"."profiles" to "service_role";

grant update on table "public"."profiles" to "service_role";

grant delete on table "public"."proxies" to "anon";

grant insert on table "public"."proxies" to "anon";

grant references on table "public"."proxies" to "anon";

grant select on table "public"."proxies" to "anon";

grant trigger on table "public"."proxies" to "anon";

grant truncate on table "public"."proxies" to "anon";

grant update on table "public"."proxies" to "anon";

grant delete on table "public"."proxies" to "authenticated";

grant insert on table "public"."proxies" to "authenticated";

grant references on table "public"."proxies" to "authenticated";

grant select on table "public"."proxies" to "authenticated";

grant trigger on table "public"."proxies" to "authenticated";

grant truncate on table "public"."proxies" to "authenticated";

grant update on table "public"."proxies" to "authenticated";

grant delete on table "public"."proxies" to "service_role";

grant insert on table "public"."proxies" to "service_role";

grant references on table "public"."proxies" to "service_role";

grant select on table "public"."proxies" to "service_role";

grant trigger on table "public"."proxies" to "service_role";

grant truncate on table "public"."proxies" to "service_role";

grant update on table "public"."proxies" to "service_role";



create policy "Public profiles are viewable by everyone."
on "public"."profiles"
as permissive
for select
to public
using (true);


create policy "Users can insert their own profile."
on "public"."profiles"
as permissive
for insert
to public
with check ((( SELECT auth.uid() AS uid) = id));


create policy "Users can update own profile."
on "public"."profiles"
as permissive
for update
to public
using ((( SELECT auth.uid() AS uid) = id));



