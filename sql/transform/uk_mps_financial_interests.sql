-- SQL transformation for UK MPs' financial interests data
-- This script processes raw data from the register of interests
-- and loads it into the core database tables

-- Parameters provided by Airflow:
-- {{ params.ds }} - execution date in YYYY-MM-DD format

-- Step 1: Create staging table for persons
CREATE TABLE IF NOT EXISTS stg_uk_mp_persons (
    full_name TEXT NOT NULL,
    type TEXT NOT NULL,
    title TEXT,
    first_name TEXT,
    last_name TEXT,
    middle_names TEXT,
    constituency TEXT,
    party TEXT,
    parliament_id TEXT,
    is_current_mp BOOLEAN,
    biography TEXT,
    photo_url TEXT,
    source_url TEXT,
    scrape_date TIMESTAMP,
    batch_date DATE
);

-- Step 2: Create staging table for financial interests
CREATE TABLE IF NOT EXISTS stg_uk_mp_financial_interests (
    person_name TEXT NOT NULL,
    company_name TEXT,
    type TEXT NOT NULL,
    description TEXT,
    amount NUMERIC,
    yearly_value NUMERIC,
    currency TEXT,
    registered_date DATE,
    start_date DATE,
    end_date DATE,
    source_document TEXT,
    source_url TEXT,
    scrape_date TIMESTAMP,
    batch_date DATE
);

-- Step 3: Truncate staging tables for this batch
TRUNCATE TABLE stg_uk_mp_persons;
TRUNCATE TABLE stg_uk_mp_financial_interests;

-- Step 4: Load data from S3 into staging tables
-- Note: In a real implementation, this would use a COPY command or similar
-- specific to the database being used (e.g., PostgreSQL, Redshift, Snowflake)
-- For this example, we're assuming some mechanism to load data exists

-- The following is PostgreSQL-specific COPY syntax
-- COPY stg_uk_mp_persons (full_name, type, title, ...) 
-- FROM PROGRAM 's3cmd get s3://inequality-data/raw/uk_mps/register_of_interests_{{ params.ds }}.json - | jq -c "select(.full_name != null)"'
-- CSV DELIMITER ',' QUOTE '"';

-- Step 5: Insert new persons into the core person table
INSERT INTO person (
    full_name, 
    type, 
    title, 
    first_name, 
    last_name, 
    middle_names,
    constituency, 
    party, 
    parliament_id, 
    is_current_mp,
    biography,
    photo_url
)
SELECT 
    stg.full_name,
    (CASE 
        WHEN stg.type = 'politician' THEN 'politician'::person_type 
        WHEN stg.type = 'billionaire' THEN 'billionaire'::person_type
        ELSE 'other'::person_type
     END),
    stg.title,
    stg.first_name,
    stg.last_name,
    stg.middle_names,
    stg.constituency,
    stg.party,
    stg.parliament_id,
    stg.is_current_mp,
    stg.biography,
    stg.photo_url
FROM stg_uk_mp_persons stg
LEFT JOIN person p ON p.parliament_id = stg.parliament_id
WHERE p.id IS NULL  -- Only insert new persons
  AND stg.batch_date = '{{ params.ds }}'::DATE;

-- Step 6: Update existing persons with new information
UPDATE person p
SET 
    full_name = stg.full_name,
    title = COALESCE(stg.title, p.title),
    constituency = COALESCE(stg.constituency, p.constituency),
    party = COALESCE(stg.party, p.party),
    is_current_mp = COALESCE(stg.is_current_mp, p.is_current_mp),
    biography = COALESCE(stg.biography, p.biography),
    photo_url = COALESCE(stg.photo_url, p.photo_url),
    updated_at = NOW()
FROM stg_uk_mp_persons stg
WHERE p.parliament_id = stg.parliament_id
  AND stg.batch_date = '{{ params.ds }}'::DATE;

-- Step 7: Insert new financial interests
INSERT INTO financial_interest (
    person_id,
    company_id,
    type,
    description,
    amount,
    yearly_value,
    currency,
    registered_date,
    start_date,
    end_date,
    source_document,
    source_url
)
SELECT 
    p.id,
    c.id,
    (CASE 
        WHEN stg.type = 'employment' THEN 'employment'::interest_type
        WHEN stg.type = 'directorship' THEN 'directorship'::interest_type
        WHEN stg.type = 'shareholding' THEN 'shareholding'::interest_type
        WHEN stg.type = 'donation' THEN 'donation'::interest_type
        WHEN stg.type = 'gift' THEN 'gift'::interest_type
        WHEN stg.type = 'property' THEN 'property'::interest_type
        ELSE 'miscellaneous'::interest_type
     END),
    stg.description,
    stg.amount,
    stg.yearly_value,
    COALESCE(stg.currency, 'GBP'),
    stg.registered_date,
    stg.start_date,
    stg.end_date,
    stg.source_document,
    stg.source_url
FROM stg_uk_mp_financial_interests stg
JOIN person p ON p.full_name = stg.person_name
LEFT JOIN company c ON c.name = stg.company_name
LEFT JOIN financial_interest fi 
    ON fi.person_id = p.id 
    AND fi.description = stg.description
    AND fi.registered_date = stg.registered_date
WHERE fi.id IS NULL  -- Only insert new interests
  AND stg.batch_date = '{{ params.ds }}'::DATE;

-- Step 8: Cleanup staging tables (optional)
-- TRUNCATE TABLE stg_uk_mp_persons;
-- TRUNCATE TABLE stg_uk_mp_financial_interests; 