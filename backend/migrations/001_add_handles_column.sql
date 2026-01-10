-- Migration: Add handles column to workflow_node_configs table
-- This stores the handle/port configuration for each node

ALTER TABLE workflow_node_configs 
ADD COLUMN handles JSON DEFAULT '[]' NOT NULL;

-- If using PostgreSQL, you may want to use jsonb instead:
-- ALTER TABLE workflow_node_configs 
-- ADD COLUMN handles JSONB DEFAULT '[]'::jsonb NOT NULL;
