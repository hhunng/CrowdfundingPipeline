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

CREATE TABLE public.newsfeed (
    newsfeed_id SERIAL NOT NULL,
    author varchar(45) NOT NULL,
    headline text NOT NULL,
    summary text NOT NULL,
    media bytea NOT NULL,
    publish_date date NOT NULL,
    category text NOT NULL,
    author_id integer
);

ALTER TABLE ONLY public.newsfeed
    ADD CONSTRAINT newsfeed_pkey PRIMARY KEY (newsfeed_id);
