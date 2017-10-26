--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.1
-- Dumped by pg_dump version 9.6.2

-- Started on 2017-10-27 01:16:02

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 2157 (class 0 OID 0)
-- Dependencies: 4
-- Name: SCHEMA "public"; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA "public" IS 'standard public schema';


--
-- TOC entry 1 (class 3079 OID 12387)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS "plpgsql" WITH SCHEMA "pg_catalog";


--
-- TOC entry 2158 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION "plpgsql"; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION "plpgsql" IS 'PL/pgSQL procedural language';


--
-- TOC entry 2 (class 3079 OID 104216)
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA "public";


--
-- TOC entry 2159 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


SET search_path = "public", pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 187 (class 1259 OID 104306)
-- Name: rooms; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE "rooms" (
    "id_room" integer NOT NULL,
    "name" "text"
);


ALTER TABLE "rooms" OWNER TO "postgres";

--
-- TOC entry 186 (class 1259 OID 104304)
-- Name: room_id_room_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "room_id_room_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "room_id_room_seq" OWNER TO "postgres";

--
-- TOC entry 2160 (class 0 OID 0)
-- Dependencies: 186
-- Name: room_id_room_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE "room_id_room_seq" OWNED BY "rooms"."id_room";


--
-- TOC entry 188 (class 1259 OID 104316)
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
-- TOC entry 189 (class 1259 OID 104330)
-- Name: status_sensors; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE "status_sensors" (
    "key" "uuid" DEFAULT "uuid_generate_v4"() NOT NULL,
    "sensor_id" "uuid",
    "consum_gas" "text",
    "twister_gas" "text",
    "celsium" "text",
    "twister_cold" "text",
    "twister_radiator" "text",
    "energy" "text",
    "smove" "text",
    "date" "text"
);


ALTER TABLE "status_sensors" OWNER TO "postgres";

--
-- TOC entry 2161 (class 0 OID 0)
-- Dependencies: 189
-- Name: COLUMN "status_sensors"."consum_gas"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN "status_sensors"."consum_gas" IS 'Расход газа';


--
-- TOC entry 2162 (class 0 OID 0)
-- Dependencies: 189
-- Name: COLUMN "status_sensors"."twister_gas"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN "status_sensors"."twister_gas" IS 'Крутилка газа';


--
-- TOC entry 2163 (class 0 OID 0)
-- Dependencies: 189
-- Name: COLUMN "status_sensors"."celsium"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN "status_sensors"."celsium" IS 'Температура в комнате';


--
-- TOC entry 2164 (class 0 OID 0)
-- Dependencies: 189
-- Name: COLUMN "status_sensors"."twister_cold"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN "status_sensors"."twister_cold" IS 'Крутилка кондиционера';


--
-- TOC entry 2165 (class 0 OID 0)
-- Dependencies: 189
-- Name: COLUMN "status_sensors"."twister_radiator"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN "status_sensors"."twister_radiator" IS 'Крутилка газа';


--
-- TOC entry 2166 (class 0 OID 0)
-- Dependencies: 189
-- Name: COLUMN "status_sensors"."energy"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN "status_sensors"."energy" IS 'Потребляемая энергия';


--
-- TOC entry 2023 (class 2604 OID 104309)
-- Name: rooms id_room; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY "rooms" ALTER COLUMN "id_room" SET DEFAULT "nextval"('"room_id_room_seq"'::"regclass");


--
-- TOC entry 2027 (class 2606 OID 104314)
-- Name: rooms room_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY "rooms"
    ADD CONSTRAINT "room_pkey" PRIMARY KEY ("id_room");


--
-- TOC entry 2029 (class 2606 OID 104324)
-- Name: sensors sensors_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY "sensors"
    ADD CONSTRAINT "sensors_pkey" PRIMARY KEY ("id_sensor");


--
-- TOC entry 2032 (class 2606 OID 104338)
-- Name: status_sensors status_sensors_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY "status_sensors"
    ADD CONSTRAINT "status_sensors_pkey" PRIMARY KEY ("key");


--
-- TOC entry 2030 (class 1259 OID 104344)
-- Name: status_sensors_key_uindex; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX "status_sensors_key_uindex" ON "status_sensors" USING "btree" ("key");


--
-- TOC entry 2033 (class 2606 OID 104325)
-- Name: sensors sensors_rooms_id_room_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY "sensors"
    ADD CONSTRAINT "sensors_rooms_id_room_fk" FOREIGN KEY ("room_id") REFERENCES "rooms"("id_room");


--
-- TOC entry 2034 (class 2606 OID 104339)
-- Name: status_sensors status_sensors_sensors_id_sensor_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY "status_sensors"
    ADD CONSTRAINT "status_sensors_sensors_id_sensor_fk" FOREIGN KEY ("sensor_id") REFERENCES "sensors"("id_sensor");


-- Completed on 2017-10-27 01:16:03

--
-- PostgreSQL database dump complete
--

