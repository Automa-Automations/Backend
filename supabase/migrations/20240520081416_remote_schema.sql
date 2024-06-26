
SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

CREATE EXTENSION IF NOT EXISTS "pgsodium" WITH SCHEMA "pgsodium";

COMMENT ON SCHEMA "public" IS 'standard public schema';

CREATE EXTENSION IF NOT EXISTS "pg_graphql" WITH SCHEMA "graphql";

CREATE EXTENSION IF NOT EXISTS "pg_stat_statements" WITH SCHEMA "extensions";

CREATE EXTENSION IF NOT EXISTS "pgcrypto" WITH SCHEMA "extensions";

CREATE EXTENSION IF NOT EXISTS "pgjwt" WITH SCHEMA "extensions";

CREATE EXTENSION IF NOT EXISTS "supabase_vault" WITH SCHEMA "vault";

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA "extensions";

CREATE OR REPLACE FUNCTION "public"."handle_new_user"() RETURNS "trigger"
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
begin
  insert into public.profiles (id, full_name, avatar_url)
  values (new.id, new.raw_user_meta_data->>'full_name', new.raw_user_meta_data->>'avatar_url');
  return new;
end;
$$;

ALTER FUNCTION "public"."handle_new_user"() OWNER TO "postgres";

SET default_tablespace = '';

SET default_table_access_method = "heap";

CREATE TABLE IF NOT EXISTS "public"."bot_sessions" (
    "id" bigint NOT NULL,
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "platform" "text",
    "owner_id" "uuid",
    "metadata_dict" "json"
);

ALTER TABLE "public"."bot_sessions" OWNER TO "postgres";

ALTER TABLE "public"."bot_sessions" ALTER COLUMN "id" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME "public"."bot_sessions_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE IF NOT EXISTS "public"."bots" (
    "id" bigint NOT NULL,
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "owner_id" "uuid",
    "proxy_id" bigint,
    "friendly_name" "text",
    "description" "text",
    "metadata_dict" "json",
    "bot_type" "text",
    "bot_configuration_dict" "json",
    "platform" "text",
    "session_id" bigint,
    "currently_active" boolean
);

ALTER TABLE "public"."bots" OWNER TO "postgres";

ALTER TABLE "public"."bots" ALTER COLUMN "id" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME "public"."bots_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE IF NOT EXISTS "public"."plans" (
    "id" "text" NOT NULL,
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "price" double precision,
    "base_credits" bigint DEFAULT '500'::bigint,
    "popularity_score" bigint DEFAULT '0'::bigint NOT NULL,
    "name" "text" DEFAULT 'DEMO'::"text" NOT NULL,
    "price_rep" "text" DEFAULT '$12.99'::"text" NOT NULL,
    "hex_color_int" bigint DEFAULT '0'::bigint NOT NULL,
    "cta_page" "text"[]
);

ALTER TABLE "public"."plans" OWNER TO "postgres";

COMMENT ON COLUMN "public"."plans"."popularity_score" IS 'The score we want to rank these as. The numbers indicates how they will show up in the interface)';

COMMENT ON COLUMN "public"."plans"."name" IS 'The name of the product';

CREATE TABLE IF NOT EXISTS "public"."profiles" (
    "id" "uuid" NOT NULL,
    "updated_at" timestamp with time zone,
    "username" "text",
    "full_name" "text",
    "avatar_url" "text",
    "website" "text",
    "stripe_customer_id" "text",
    "expiry_date" timestamp with time zone DEFAULT "now"(),
    "plan_type" "text",
    CONSTRAINT "username_length" CHECK (("char_length"("username") >= 3))
);

ALTER TABLE "public"."profiles" OWNER TO "postgres";

COMMENT ON COLUMN "public"."profiles"."stripe_customer_id" IS 'The stripe customer id';

CREATE TABLE IF NOT EXISTS "public"."proxies" (
    "id" bigint NOT NULL,
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "host" "text" DEFAULT '0.0.0.0'::"text",
    "port" bigint DEFAULT '8080'::bigint,
    "type_" "text" DEFAULT 'http'::"text",
    "security" "text" DEFAULT 'datacenter'::"text",
    "username" "text",
    "password" "text",
    "country" "text" DEFAULT 'us'::"text" NOT NULL
);

ALTER TABLE "public"."proxies" OWNER TO "postgres";

ALTER TABLE "public"."proxies" ALTER COLUMN "id" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME "public"."proxies_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

ALTER TABLE ONLY "public"."bot_sessions"
    ADD CONSTRAINT "bot_sessions_pkey" PRIMARY KEY ("id");

ALTER TABLE ONLY "public"."bots"
    ADD CONSTRAINT "bots_pkey" PRIMARY KEY ("id");

ALTER TABLE ONLY "public"."plans"
    ADD CONSTRAINT "plans_pkey" PRIMARY KEY ("id");

ALTER TABLE ONLY "public"."profiles"
    ADD CONSTRAINT "profiles_pkey" PRIMARY KEY ("id");

ALTER TABLE ONLY "public"."profiles"
    ADD CONSTRAINT "profiles_username_key" UNIQUE ("username");

ALTER TABLE ONLY "public"."proxies"
    ADD CONSTRAINT "proxies_pkey" PRIMARY KEY ("id");

ALTER TABLE ONLY "public"."bot_sessions"
    ADD CONSTRAINT "bot_sessions_owner_id_fkey" FOREIGN KEY ("owner_id") REFERENCES "public"."profiles"("id");

ALTER TABLE ONLY "public"."bots"
    ADD CONSTRAINT "bots_owner_id_fkey" FOREIGN KEY ("owner_id") REFERENCES "public"."profiles"("id");

ALTER TABLE ONLY "public"."bots"
    ADD CONSTRAINT "bots_proxy_id_fkey" FOREIGN KEY ("proxy_id") REFERENCES "public"."proxies"("id");

ALTER TABLE ONLY "public"."bots"
    ADD CONSTRAINT "bots_session_id_fkey" FOREIGN KEY ("session_id") REFERENCES "public"."bot_sessions"("id");

ALTER TABLE ONLY "public"."profiles"
    ADD CONSTRAINT "profiles_id_fkey" FOREIGN KEY ("id") REFERENCES "auth"."users"("id") ON DELETE CASCADE;

ALTER TABLE ONLY "public"."profiles"
    ADD CONSTRAINT "public_profiles_plan_type_fkey" FOREIGN KEY ("plan_type") REFERENCES "public"."plans"("id");

CREATE POLICY "Enable read access for all users" ON "public"."plans" FOR SELECT USING (true);

CREATE POLICY "Public profiles are viewable by everyone." ON "public"."profiles" FOR SELECT USING (true);

CREATE POLICY "Users can insert their own profile." ON "public"."profiles" FOR INSERT WITH CHECK ((( SELECT "auth"."uid"() AS "uid") = "id"));

CREATE POLICY "Users can update own profile." ON "public"."profiles" FOR UPDATE USING ((( SELECT "auth"."uid"() AS "uid") = "id"));

ALTER TABLE "public"."bot_sessions" ENABLE ROW LEVEL SECURITY;

ALTER TABLE "public"."bots" ENABLE ROW LEVEL SECURITY;

ALTER TABLE "public"."plans" ENABLE ROW LEVEL SECURITY;

ALTER TABLE "public"."profiles" ENABLE ROW LEVEL SECURITY;

ALTER TABLE "public"."proxies" ENABLE ROW LEVEL SECURITY;

ALTER PUBLICATION "supabase_realtime" OWNER TO "postgres";

GRANT USAGE ON SCHEMA "public" TO "postgres";
GRANT USAGE ON SCHEMA "public" TO "anon";
GRANT USAGE ON SCHEMA "public" TO "authenticated";
GRANT USAGE ON SCHEMA "public" TO "service_role";

GRANT ALL ON FUNCTION "public"."handle_new_user"() TO "anon";
GRANT ALL ON FUNCTION "public"."handle_new_user"() TO "authenticated";
GRANT ALL ON FUNCTION "public"."handle_new_user"() TO "service_role";

GRANT ALL ON TABLE "public"."bot_sessions" TO "anon";
GRANT ALL ON TABLE "public"."bot_sessions" TO "authenticated";
GRANT ALL ON TABLE "public"."bot_sessions" TO "service_role";

GRANT ALL ON SEQUENCE "public"."bot_sessions_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."bot_sessions_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."bot_sessions_id_seq" TO "service_role";

GRANT ALL ON TABLE "public"."bots" TO "anon";
GRANT ALL ON TABLE "public"."bots" TO "authenticated";
GRANT ALL ON TABLE "public"."bots" TO "service_role";

GRANT ALL ON SEQUENCE "public"."bots_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."bots_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."bots_id_seq" TO "service_role";

GRANT ALL ON TABLE "public"."plans" TO "anon";
GRANT ALL ON TABLE "public"."plans" TO "authenticated";
GRANT ALL ON TABLE "public"."plans" TO "service_role";

GRANT ALL ON TABLE "public"."profiles" TO "anon";
GRANT ALL ON TABLE "public"."profiles" TO "authenticated";
GRANT ALL ON TABLE "public"."profiles" TO "service_role";

GRANT ALL ON TABLE "public"."proxies" TO "anon";
GRANT ALL ON TABLE "public"."proxies" TO "authenticated";
GRANT ALL ON TABLE "public"."proxies" TO "service_role";

GRANT ALL ON SEQUENCE "public"."proxies_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."proxies_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."proxies_id_seq" TO "service_role";

ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES  TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES  TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES  TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES  TO "service_role";

ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS  TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS  TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS  TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS  TO "service_role";

ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES  TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES  TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES  TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES  TO "service_role";

RESET ALL;
