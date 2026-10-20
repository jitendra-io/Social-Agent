-- =====================================================================
-- AUTONOMOUS AI DIGITAL AGENCY & OPERATIONS OS
-- Database Initialization Script (MySQL 8.0 / InnoDB)
-- =====================================================================

CREATE DATABASE IF NOT EXISTS agency_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE agency_db;

-- ---------------------------------------------------------------------
-- 1. Table: posts
-- Tracks social media generation, approvals, distribution, and analytics
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    platform VARCHAR(50) NOT NULL DEFAULT 'all', -- 'youtube_shorts', 'instagram_reels', 'twitter', 'all'
    topic VARCHAR(255) NOT NULL,
    hook TEXT,
    caption TEXT NOT NULL,
    media_path TEXT,                             -- Path inside shared_media volume
    media_url TEXT,                              -- External or preview URL
    status VARCHAR(50) NOT NULL DEFAULT 'draft', -- 'draft', 'pending_approval', 'approved', 'scheduled', 'publishing', 'published', 'failed', 'rejected'
    scheduled_at DATETIME NULL,
    published_at DATETIME NULL,
    post_external_ids JSON NULL,                 -- e.g. {"youtube": "abc123xyz", "instagram": "1789...", "twitter": "1678..."}
    analytics_data JSON NULL,                    -- e.g. {"views": 15400, "retention_pct": 72.5, "shares": 340, "likes": 1200}
    generation_metadata JSON NULL,               -- voice model, prompt seeds, duration
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_posts_status (status),
    INDEX idx_posts_scheduled_at (scheduled_at),
    INDEX idx_posts_created_at (created_at DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------------------------------------------------------------------
-- 2. Table: leads
-- Stores qualified inbound clients acquired through WhatsApp Cloud API
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS leads (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source VARCHAR(50) NOT NULL DEFAULT 'whatsapp',
    business_name VARCHAR(255) NULL,
    phone VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) NULL,
    industry_niche VARCHAR(150) NULL,
    requirements JSON NULL,                      -- Brand colors, target pages, features, tagline
    site_status VARCHAR(50) NOT NULL DEFAULT 'collecting', -- 'collecting', 'ready_for_build', 'building', 'deployed', 'failed'
    site_url TEXT NULL,                          -- Live production URL (Render, Vercel)
    repo_url TEXT NULL,                          -- GitHub repository URL
    build_log TEXT NULL,                         -- Execution output from Dev Bridge
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_leads_phone (phone),
    INDEX idx_leads_site_status (site_status),
    INDEX idx_leads_created_at (created_at DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------------------------------------------------------------------
-- 3. Table: conversations
-- Persistent conversational memory for Telegram Executive & WhatsApp Agents
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS conversations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(100) UNIQUE NOT NULL,    -- e.g. 'tg_123456789' or 'wa_14155552671'
    user_id VARCHAR(100) NOT NULL,
    platform VARCHAR(50) NOT NULL,              -- 'telegram', 'whatsapp'
    context_history JSON NULL,                  -- Array of {"role": "user"|"assistant", "content": "...", "timestamp": "..."}
    last_state VARCHAR(100) DEFAULT 'idle',     -- 'idle', 'awaiting_caption_edit', 'collecting_brand_name', etc.
    metadata JSON NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_conversations_session_id (session_id),
    INDEX idx_conversations_platform_user (platform, user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------------------------------------------------------------------
-- 4. Table: executive_memory
-- Long-term persistent memory for Executive Director directives, preferences, and rules
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS executive_memory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    memory_type VARCHAR(50) NOT NULL DEFAULT 'directive', -- 'directive', 'preference', 'fact', 'conversation', 'rule'
    category VARCHAR(50) NOT NULL DEFAULT 'general',       -- 'media', 'branding', 'clients', 'strategy'
    context_key VARCHAR(150) NULL,
    content TEXT NOT NULL,
    source VARCHAR(50) DEFAULT 'telegram',
    importance_score INT DEFAULT 5,                       -- 1 to 10
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_memory_type (memory_type),
    INDEX idx_memory_category (category),
    FULLTEXT idx_memory_search (content)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------------------------------------------------------------------
-- 5. Default Baseline Seed Data (Verification Sanity Check)
-- ---------------------------------------------------------------------
INSERT IGNORE INTO posts (id, platform, topic, hook, caption, status, scheduled_at, analytics_data)
VALUES (
    1,
    'all',
    'AI Operations Introduction',
    'How autonomous AI systems will replace $5,000/mo SaaS subscriptions in 2026',
    'Full automated system demonstration #ai #automation #tech #future #business',
    'draft',
    DATE_ADD(NOW(), INTERVAL 1 HOUR),
    JSON_OBJECT('sample', true)
);
