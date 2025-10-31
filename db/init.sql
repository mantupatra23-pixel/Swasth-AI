CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  name TEXT,
  age INT,
  weight FLOAT,
  height FLOAT,
  goal TEXT,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS workout_plans (
  id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(id) ON DELETE CASCADE,
  name TEXT,
  source TEXT,
  plan_json JSONB,
  created_at TIMESTAMP DEFAULT now()
);
