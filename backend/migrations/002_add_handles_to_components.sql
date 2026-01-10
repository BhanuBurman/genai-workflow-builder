-- Add handles column to components table
ALTER TABLE components 
ADD COLUMN handles JSON DEFAULT '[]' NOT NULL;
