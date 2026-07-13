-- Vagas.me Database Schema for Supabase

-- 1. Table for Job Openings (vagas)
CREATE TABLE public.vagas (
    id TEXT PRIMARY KEY,
    empresa TEXT NOT NULL,
    ramo TEXT NOT NULL,
    vagas TEXT[] NOT NULL,
    beneficios TEXT,
    salarios TEXT,
    turnos TEXT,
    endereco TEXT,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    imagem TEXT,
    patrocinado BOOLEAN DEFAULT FALSE,
    estrela BOOLEAN DEFAULT FALSE,
    descricao TEXT,
    contato TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Enable Row Level Security (RLS) for vagas
ALTER TABLE public.vagas ENABLE ROW LEVEL SECURITY;

-- Allow public read access to vagas
CREATE POLICY "Allow public read access to vagas" ON public.vagas
    FOR SELECT USING (true);

-- Allow authenticated recruiters to insert/update vagas
CREATE POLICY "Allow authenticated insert to vagas" ON public.vagas
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY "Allow authenticated update to vagas" ON public.vagas
    FOR UPDATE USING (auth.role() = 'authenticated');


-- 2. Table for Candidates (candidatos)
CREATE TABLE public.candidatos (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    address TEXT,
    linkedin TEXT,
    objective TEXT,
    skills TEXT[] DEFAULT '{}'::TEXT[],
    experiences JSONB DEFAULT '[]'::JSONB,
    education JSONB DEFAULT '[]'::JSONB,
    photo TEXT,
    courses JSONB DEFAULT '[]'::JSONB,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Enable RLS for candidatos
ALTER TABLE public.candidatos ENABLE ROW LEVEL SECURITY;

-- Allow users to manage their own candidate profile
CREATE POLICY "Allow users to read own profile" ON public.candidatos
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Allow users to insert own profile" ON public.candidatos
    FOR INSERT WITH CHECK (auth.uid() = id);

CREATE POLICY "Allow users to update own profile" ON public.candidatos
    FOR UPDATE USING (auth.uid() = id);

-- Allow recruiters to read candidates who applied to their jobs
CREATE POLICY "Allow recruiters to read applicant profiles" ON public.candidatos
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM public.candidaturas c
            WHERE c.candidate_id = candidatos.id::TEXT
        )
    );


-- 3. Table for Job Applications (candidaturas)
CREATE TABLE public.candidaturas (
    id TEXT PRIMARY KEY,
    candidate_id TEXT NOT NULL,
    job_id TEXT NOT NULL,
    stage TEXT DEFAULT 'applied' NOT NULL, -- applied, triagem, entrevista, proposta, rejeitado
    match_score INTEGER DEFAULT 75 NOT NULL,
    date_applied TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Enable RLS for candidaturas
ALTER TABLE public.candidaturas ENABLE ROW LEVEL SECURITY;

-- Allow candidates to read and create their own applications
CREATE POLICY "Allow candidates to manage own applications" ON public.candidaturas
    FOR SELECT USING (auth.uid()::TEXT = candidate_id);

CREATE POLICY "Allow candidates to insert own applications" ON public.candidaturas
    FOR INSERT WITH CHECK (auth.uid()::TEXT = candidate_id);

-- Allow recruiters to read and update applications for any job
CREATE POLICY "Allow recruiters to read applications" ON public.candidaturas
    FOR SELECT USING (true); -- Simplified for MVP, can be restricted by role later

CREATE POLICY "Allow recruiters to update applications" ON public.candidaturas
    FOR UPDATE USING (true);
