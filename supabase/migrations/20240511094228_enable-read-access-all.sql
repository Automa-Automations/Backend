create policy "Enable read access for all users"
on "public"."plans"
as permissive
for select
to public
using (true);



