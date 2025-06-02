# Schema Overview

### `01_create_locations.sql`

Defines a normalized list of geographic locations to avoid repetition in related tables (e.g. users, events). Includes a unique name and optional identifier code.

---

### `02_create_devices.sql`

Stores normalized device types (e.g. 'Mobile', 'Desktop') to enforce clean categorical data and enable future extensibility.

---

### `03_create_interests.sql`

Lists all user/campaign interests as normalized entities. Prevents inconsistent text and supports many-to-many mapping.

---

### `04_create_ad_slot_sizes.sql`

Stores ad slot sizes like '300x250' as normalized values to reduce redundancy and allow consistent querying.

---

### `05_create_genders.sql`

Uses an ENUM-based controlled set of gender values for data integrity and future flexibility. Normalized via ID instead of inline strings.

---

### `06_create_advertisers.sql`

Defines advertisers as independent entities to eliminate duplication and establish FK relationships in campaigns and events.

---

### `07_create_users.sql`

Represents platform users with normalized references to gender and location. Includes business and audit fields.

---

### `08_create_user_interests.sql`

A bridge table linking users to interests (many-to-many). Enforces uniqueness to prevent duplicate tag assignments.

---

### `09_create_campaigns.sql`

Captures campaigns with references to advertisers and ad slot sizes. Designed to support performance metrics like budget tracking and targeting.

---

### `10_create_campaign_targets.sql`

A bridge table for associating campaigns with its targets (many-to-many), supporting advanced targeting logic and filtering.

---

### `11_create_ad_events.sql`

Tracks individual ad impressions and clicks with full normalization across users, campaigns, locations, devices, and slots. Omits redundant `advertiser_id` in favor of FK traversal via `campaign`.

---

### `12_create_indexes.sql`

Creates indexes on frequently joined and filtered columns to for query performance. Includes indexes on foreign keys, timestamps, and click flags across `users`, `campaigns`, `ad_events`, and bridge tables. Designed to support fast lookups, analytics, and join-heavy queries.

---

### `13_seed_genders.sql`

Seeds the `genders` table with a predefined list of values (`Male`, `Female`). This ensures referential integrity for the `users` table and enforces a controlled vocabulary for gender.

---

### `14_seed_devices.sql`

Populates the `devices` table with common device types (`Mobile`, `Desktop`, `Tablet`, etc.) used in ad events. Enables fast foreign key lookups and consistent device tracking.

---

### `15_seed_ad_slot_sizes.sql`

Preloads the `ad_slot_sizes` table with standard IAB ad dimensions. This supports campaign targeting and ad event matching without relying on dynamic insertion.

---

### `16_create_seed_status.sql`

Creates a utility table for tracking the execution of Python-based seed scripts.  
Each script inserts a record into this table after successful execution, enabling idempotent data seeding and safe reruns during development. Used by the `run_seeders.py` orchestration logic.
