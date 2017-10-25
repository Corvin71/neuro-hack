--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.9
-- Dumped by pg_dump version 9.6.2

-- Started on 2017-10-25 23:13:30

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 2187 (class 0 OID 0)
-- Dependencies: 7
-- Name: SCHEMA "public"; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA "public" IS 'standard public schema';


--
-- TOC entry 1 (class 3079 OID 12393)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS "plpgsql" WITH SCHEMA "pg_catalog";


--
-- TOC entry 2189 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION "plpgsql"; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION "plpgsql" IS 'PL/pgSQL procedural language';


--
-- TOC entry 2 (class 3079 OID 86234)
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA "public";


--
-- TOC entry 2190 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


SET search_path = "public", pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 183 (class 1259 OID 86225)
-- Name: rooms; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE "rooms" (
    "id_room" integer NOT NULL,
    "name" "text"
);


ALTER TABLE "rooms" OWNER TO "postgres";

--
-- TOC entry 182 (class 1259 OID 86223)
-- Name: rooms_id_room_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "rooms_id_room_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "rooms_id_room_seq" OWNER TO "postgres";

--
-- TOC entry 2191 (class 0 OID 0)
-- Dependencies: 182
-- Name: rooms_id_room_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE "rooms_id_room_seq" OWNED BY "rooms"."id_room";


--
-- TOC entry 184 (class 1259 OID 86245)
-- Name: sensors; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE "sensors" (
    "id_sensor" "uuid" DEFAULT "uuid_generate_v4"() NOT NULL,
    "ip" "text",
    "name" "text",
    "room_id" integer
);


ALTER TABLE "sensors" OWNER TO "postgres";

--
-- TOC entry 187 (class 1259 OID 86287)
-- Name: status_boiler; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE "status_boiler" (
    "key" "uuid" DEFAULT "uuid_generate_v4"() NOT NULL,
    "sensor_id" "uuid" NOT NULL,
    "consumgas" "text",
    "consumelectric" "text",
    "date" "text"
);


ALTER TABLE "status_boiler" OWNER TO "postgres";

--
-- TOC entry 2192 (class 0 OID 0)
-- Dependencies: 187
-- Name: TABLE "status_boiler"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE "status_boiler" IS 'Статистика бойлера';


--
-- TOC entry 2193 (class 0 OID 0)
-- Dependencies: 187
-- Name: COLUMN "status_boiler"."consumgas"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN "status_boiler"."consumgas" IS 'расход воды';


--
-- TOC entry 2194 (class 0 OID 0)
-- Dependencies: 187
-- Name: COLUMN "status_boiler"."consumelectric"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN "status_boiler"."consumelectric" IS 'Расход электричества';


--
-- TOC entry 186 (class 1259 OID 86273)
-- Name: status_sensors; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE "status_sensors" (
    "key" "uuid" DEFAULT "uuid_generate_v4"() NOT NULL,
    "sensor" "uuid",
    "statec" "text",
    "date" "text"
);


ALTER TABLE "status_sensors" OWNER TO "postgres";

--
-- TOC entry 2195 (class 0 OID 0)
-- Dependencies: 186
-- Name: TABLE "status_sensors"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE "status_sensors" IS 'Состояние датчиков (задвижки и прочее)';


--
-- TOC entry 2196 (class 0 OID 0)
-- Dependencies: 186
-- Name: COLUMN "status_sensors"."statec"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN "status_sensors"."statec" IS 'Для плавающих значений';


--
-- TOC entry 185 (class 1259 OID 86259)
-- Name: weather; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE "weather" (
    "key" "uuid" DEFAULT "uuid_generate_v4"() NOT NULL,
    "sensor_id" "uuid" NOT NULL,
    "celsium" "text",
    "date" "text"
);


ALTER TABLE "weather" OWNER TO "postgres";

--
-- TOC entry 2049 (class 2604 OID 86228)
-- Name: rooms id_room; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY "rooms" ALTER COLUMN "id_room" SET DEFAULT "nextval"('"rooms_id_room_seq"'::"regclass");


--
-- TOC entry 2055 (class 2606 OID 86233)
-- Name: rooms rooms_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY "rooms"
    ADD CONSTRAINT "rooms_pkey" PRIMARY KEY ("id_room");


--
-- TOC entry 2057 (class 2606 OID 86253)
-- Name: sensors sensors_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY "sensors"
    ADD CONSTRAINT "sensors_pkey" PRIMARY KEY ("id_sensor");


--
-- TOC entry 2063 (class 2606 OID 86295)
-- Name: status_boiler status_boiler_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY "status_boiler"
    ADD CONSTRAINT "status_boiler_pkey" PRIMARY KEY ("key");


--
-- TOC entry 2061 (class 2606 OID 86281)
-- Name: status_sensors status_sensors_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY "status_sensors"
    ADD CONSTRAINT "status_sensors_pkey" PRIMARY KEY ("key");


--
-- TOC entry 2059 (class 2606 OID 86267)
-- Name: weather weather_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY "weather"
    ADD CONSTRAINT "weather_pkey" PRIMARY KEY ("key");


--
-- TOC entry 2064 (class 2606 OID 86254)
-- Name: sensors sensors_rooms_id_room_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY "sensors"
    ADD CONSTRAINT "sensors_rooms_id_room_fk" FOREIGN KEY ("room_id") REFERENCES "rooms"("id_room");


--
-- TOC entry 2067 (class 2606 OID 86296)
-- Name: status_boiler status_boiler_sensors_id_sensor_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY "status_boiler"
    ADD CONSTRAINT "status_boiler_sensors_id_sensor_fk" FOREIGN KEY ("sensor_id") REFERENCES "sensors"("id_sensor");


--
-- TOC entry 2066 (class 2606 OID 86282)
-- Name: status_sensors status_sensors_sensors_id_sensor_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY "status_sensors"
    ADD CONSTRAINT "status_sensors_sensors_id_sensor_fk" FOREIGN KEY ("sensor") REFERENCES "sensors"("id_sensor");


--
-- TOC entry 2065 (class 2606 OID 86268)
-- Name: weather weather_sensors_id_sensor_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY "weather"
    ADD CONSTRAINT "weather_sensors_id_sensor_fk" FOREIGN KEY ("sensor_id") REFERENCES "sensors"("id_sensor");


--
-- TOC entry 2188 (class 0 OID 0)
-- Dependencies: 7
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA "public" FROM PUBLIC;
REVOKE ALL ON SCHEMA "public" FROM "postgres";
GRANT ALL ON SCHEMA "public" TO "postgres";
GRANT ALL ON SCHEMA "public" TO PUBLIC;


-- Completed on 2017-10-25 23:13:31

--
-- PostgreSQL database dump complete
--

