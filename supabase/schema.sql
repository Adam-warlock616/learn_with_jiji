-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Profiles table (linked to Supabase Auth)
CREATE TABLE IF NOT EXISTS profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Queries table
CREATE TABLE IF NOT EXISTS queries (
  id SERIAL PRIMARY KEY,
  user_id UUID REFERENCES profiles(id),
  query_text TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Resources table
CREATE TABLE IF NOT EXISTS resources (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT,
  type TEXT CHECK (type IN ('ppt', 'video')),
  file_url TEXT,
  tags TEXT[],
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert sample data
INSERT INTO resources (title, description, type, file_url, tags) VALUES
('Introduction to RAG', 'Slides on Retrieval-Augmented Generation', 'ppt', 'https://your-supabase-storage/files/rag-intro.pptx', '{"AI", "RAG", "NLP"}'),
('RAG Explained Simply', 'Video tutorial on RAG basics', 'video', 'https://your-supabase-storage/files/rag-video.mp4', '{"AI", "RAG", "tutorial"}'),
('Machine Learning Basics', 'Fundamentals of ML algorithms', 'ppt', 'https://your-supabase-storage/files/ml-basics.pptx', '{"AI", "ML", "beginner"}'),
('Neural Networks Demo', 'Visual guide to neural networks', 'video', 'https://your-supabase-storage/files/nn-demo.mp4', '{"AI", "deep-learning", "neural-networks"}');

-- Enable Row Level Security
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE queries ENABLE ROW LEVEL SECURITY;
ALTER TABLE resources ENABLE ROW LEVEL SECURITY;

-- RLS Policies
-- Profiles: users can only read their own profile
CREATE POLICY "Users can view own profile" ON profiles
  FOR SELECT USING (auth.uid() = id);

-- Queries: users can insert their own queries and read their own
CREATE POLICY "Users can insert own queries" ON queries
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view own queries" ON queries
  FOR SELECT USING (auth.uid() = user_id);

-- Resources: public read access
CREATE POLICY "Public can view resources" ON resources
  FOR SELECT USING (true);