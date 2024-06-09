CREATE TABLE public.donation (
    donation_id SERIAL NOT NULL,
    campaign_id integer NOT NULL,
    donator_id integer NOT NULL,
    donation_amount decimal NOT NULL,
    donation_date date NOT NULL,
    message_leaving text NOT NULL
);

ALTER TABLE public.donation OWNER TO postgres;

ALTER TABLE ONLY public.donation
    ADD CONSTRAINT donation_pkey PRIMARY KEY (donation_id);