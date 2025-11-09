# Snowflake Cortex AISQL Playground
Codebase for the Snowflake Cortex AISQL Playground Streamlit app

---

## 🎯 Overview

This demo application provides interactive examples of 12 core AISQL functions with:
- **36 interactive examples** (3 per function)
- **Fictitious Tasty Bytes data** (100 rows across 7 tables)
- **Live SQL execution** with result display
- **Copy-paste ready queries** for learning
- **Complete database setup** (16 objects + sample files in 20 minutes)

### Functions Showcased

| Category | Functions |
|----------|-----------|
| **Generative AI** | AI_COMPLETE, AI_SUMMARIZE_AGG, AI_AGG |
| **Text Analysis** | AI_TRANSLATE, AI_SENTIMENT, AI_EXTRACT, AI_CLASSIFY, AI_FILTER, AI_REDACT |
| **Similarity** | AI_SIMILARITY |
| **Media** | AI_TRANSCRIBE, AI_PARSE_DOCUMENT |

---

## 📦 Database Objects Created by Setup Script

### Compute Resources
| Object Type | Name | Configuration |
|-------------|------|---------------|
| Warehouse | `AISQL_DEMO_WH` | XSMALL Gen2, auto-suspend 300s |
| Warehouse | `CORTEX_SEARCH_WH` | XSMALL, auto-suspend 60s |

### Data Organization
| Object Type | Name | Description |
|-------------|------|-------------|
| Database | `AISQL_DEMO` | Main database for all demo objects |
| Schema | `DEMO` | Schema containing all tables, stages, and views |

### Storage Stages
| Stage Name | Purpose | Encryption |
|------------|---------|------------|
| `AUDIO_STAGE` | Audio files for AI_TRANSCRIBE demos | Snowflake SSE |
| `DOCUMENT_STAGE` | PDF files for AI_PARSE_DOCUMENT demos | Snowflake SSE |
| `IMAGE_STAGE` | Image files for AI_CLASSIFY/FILTER demos | Snowflake SSE |

### Data Tables
| Table Name | Rows | Purpose |
|------------|------|---------|
| `FOOD_TRUCKS` | 10 | Food truck business information |
| `MENU_ITEMS` | 10 | Menu items with multilingual descriptions |
| `CUSTOMER_REVIEWS` | 40 | Customer reviews in English, Spanish, French |
| `SUPPORT_TICKETS` | 20 | Support tickets (NO PII) for general demos |
| `SUPPORT_TICKETS_PII` | 20 | Support tickets with embedded PII for AI_REDACT |
| `PARSE_DOC_RAW_TEXT` | 0 | Populated via app for document parsing |
| `PARSE_DOC_CHUNKED_TEXT` | 0 | Populated via app for Cortex Search |

### Analytics Views
| View Name | Description |
|-----------|-------------|
| `REVIEW_ANALYTICS` | Aggregated review statistics by food truck |
| `POPULAR_ITEMS` | Menu item popularity rankings |

**Total Objects:** 2 warehouses, 1 database, 1 schema, 3 stages, 7 tables, 2 views = **16 database objects**

---

## 🤖 AISQL Functions Demonstrated

| # | Function | Category | Use Cases |
|---|----------|----------|-----------|
| 1 | **AI_COMPLETE** | Generative AI | Content generation, Q&A, data enrichment |
| 2 | **AI_TRANSLATE** | Text Analysis | Language translation (24 languages) |
| 3 | **AI_SENTIMENT** | Text Analysis | Sentiment scoring and categorization |
| 4 | **AI_EXTRACT** | Text Analysis | Entity extraction, structured data parsing |
| 5 | **AI_CLASSIFY** | Text Analysis | Text/image categorization |
| 6 | **AI_FILTER** | Text Analysis | Boolean filtering with natural language |
| 7 | **AI_SIMILARITY** | Similarity | Semantic similarity comparison |
| 8 | **AI_REDACT** | Text Analysis | PII redaction and data anonymization |
| 9 | **AI_TRANSCRIBE** | Media | Audio/video transcription |
| 10 | **AI_PARSE_DOCUMENT** | Media | OCR and layout-aware document parsing |
| 11 | **AI_SUMMARIZE_AGG** | Generative AI | Multi-row text summarization |
| 12 | **AI_AGG** | Generative AI | Custom aggregation with prompts |

**At least 3 examples per function = 36 interactive demos**

---

## 📋 Prerequisites

- **Snowflake Account** with Cortex AI enabled
- **Role Privileges**:
  - CREATE DATABASE, CREATE SCHEMA
  - CREATE TABLE, CREATE STAGE, CREATE VIEW  
  - CREATE STREAMLIT
  - SNOWFLAKE.CORTEX_USER database role
- **Warehouse**: XSMALL Gen2

---

## 🚀 Quick Start (15 minutes or less)

### Step 1: Create Database (5 min)

```sql
-- Execute entire setup_database.sql file in Snowflake worksheet
-- This creates AISQL_DEMO database with sample data
```

**Verify:**
```sql
USE DATABASE AISQL_DEMO;
USE SCHEMA DEMO;
SHOW TABLES;  -- Should show 7 tables
```

Expected Tables:
- FOOD_TRUCKS (10 rows)
- MENU_ITEMS (10 rows)
- CUSTOMER_REVIEWS (40 rows)
- SUPPORT_TICKETS (20 rows - NO PII, for general use)
- SUPPORT_TICKETS_PII (20 rows - with PII for AI_REDACT demos only)
- PARSE_DOC_RAW_TEXT (0 rows - populated via app)
- PARSE_DOC_CHUNKED_TEXT (0 rows - populated via app)

### Step 2: Deploy Streamlit App (5 min)

**Option A: Snowflake UI (Recommended)**

1. Navigate to **Projects** → **Streamlit**
2. Click **+ Streamlit App**
3. Settings:
   - Name: `AISQL_Demo_App`
   - Location: `AISQL_DEMO.DEMO`
   - Warehouse: AISQL_DEMO_WH (xsmall Gen2)
4. Delete default code
5. Copy/paste entire `app.py` content
6. Click **Run**


### Step 3: Upload Sample Files to Stages (3 min)

Upload the provided sample files to their corresponding stages for the AI demos to work properly.

#### File-to-Stage Mapping

| Folder in `sample_files/` | Files | Target Stage | Used By |
|---------------------------|-------|--------------|---------|
| `audio/` | 10 .wav files | `AUDIO_STAGE` | AI_TRANSCRIBE examples |
| `documents/` | 2 .pdf files | `DOCUMENT_STAGE` | AI_PARSE_DOCUMENT examples |
| `images/` | 10 .jpg files | `IMAGE_STAGE` | AI_CLASSIFY, AI_FILTER, AI_SIMILARITY examples |

#### Upload via Snowsight UI (Recommended)

1. In Snowsight, navigate to **Data** → **Databases** → **AISQL_DEMO** → **DEMO**
2. Click on **Stages** and select the target stage (e.g., `AUDIO_STAGE`)
3. Click the **+ Files** button in the top right corner
4. In the upload dialog:
   - Select or drag-and-drop files from the corresponding folder
   - Verify the schema shows `AISQL_DEMO.DEMO`
   - Verify the stage name is correct
   - Leave the path field empty (optional)
   - Click **Upload**

5. Repeat for each stage:
   - Upload `audio/*.wav` files to `AUDIO_STAGE`
   - Upload `documents/*.pdf` files to `DOCUMENT_STAGE`
   - Upload `images/*.jpg` files to `IMAGE_STAGE`
6. Enable Directory table to view the file contents in UI

**Verify uploads via SQL (optional):**
```sql
LIST @AISQL_DEMO.DEMO.AUDIO_STAGE;      -- Should show 10 .wav files
LIST @AISQL_DEMO.DEMO.DOCUMENT_STAGE;   -- Should show 2 .pdf files
LIST @AISQL_DEMO.DEMO.IMAGE_STAGE;      -- Should show 10 .jpg files
```

📖 **Full Upload Documentation:** [Staging Files using Snowsight](https://docs.snowflake.com/en/user-guide/data-load-local-file-system-stage-ui)

### Step 4: Grant Access (2 min)

```sql
-- Replace YOUR_ROLE with actual role name
GRANT USAGE ON DATABASE AISQL_DEMO TO ROLE YOUR_ROLE;
GRANT USAGE ON SCHEMA AISQL_DEMO.DEMO TO ROLE YOUR_ROLE;
GRANT SELECT ON ALL TABLES IN SCHEMA AISQL_DEMO.DEMO TO ROLE YOUR_ROLE;
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE YOUR_ROLE;
GRANT USAGE ON STREAMLIT AISQL_DEMO.DEMO.AISQL_DEMO_APP TO ROLE YOUR_ROLE;
```

### Step 5: Launch & Test

1. Open Streamlit app URL
2. Navigate functions via sidebar
3. Try interactive examples
4. View SQL queries for learning

---

## 🎨 Features

### Modern UI
- **Snowflake Branding**: Official colors (#29B5E8) and logo
- **Wide Layout**: 1600px max width for less scrolling
- **Gradient Buttons**: Smooth hover effects
- **Responsive Cards**: Hover animations and shadows

### Data Quality
- **Fictitious Examples**: 100 rows of Tasty Bytes themed data
- **10 Food Trucks**: Guac n Roll, Kitakata Ramen, Freezing Point, etc.
- **Multilingual Content**: Menu descriptions in 5 languages
- **Diverse Reviews**: 40 reviews with ratings from 1-5 stars
- **Support Tickets**: 20 clean tickets + 20 PII-embedded tickets
- **Realistic Scenarios**: Payment issues, complaints, compliments, inquiries

### Educational
- **SQL Displayed**: Every query shown for learning
- **Cost Transparency**: Pricing on each function page
- **Best Practices**: Proper function usage demonstrated
- **Error Handling**: SQL escaping for apostrophes

---

## 🐛 Troubleshooting

### "Function AI_XXX does not exist"
**Solution:** Grant CORTEX_USER role:
```sql
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE YOUR_ROLE;
```

### "Insufficient privileges"
**Solution:** Grant all required permissions (see Step 3 above)

### "Stage does not exist"
**Solution:** Re-run `setup_database.sql`


### Streamlit Won't Load
**Check:**
- Warehouse is running
- App has AISQL_DEMO database access
- No syntax errors in app.py

---

## 📖 Additional Resources

- **AISQL Docs**: https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql
- **Streamlit Docs**: https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit
- **Tasty Bytes**: https://www.snowflake.com/en/developers/guides/tasty-bytes-introduction/
- **Pricing**: https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf

---

## 🔐 Security & Governance

- ✅ **Data Never Leaves Snowflake**: All AI processing in your account
- ✅ **RBAC Compliant**: Respects Snowflake role-based access control
- ✅ **Audit Trail**: Query history tracked in Snowflake
- ✅ **No External APIs**: Fully managed Snowflake service

---

## 📝 Files in This Project

| File | Purpose | Details |
|------|---------|---------|
| `app.py` | Main Streamlit application | 3,000+ lines, 12 functions, 36 examples |
| `setup_database.sql` | Database setup script | Creates 16 objects with 100 rows of data |
| `sample_files/` | Unstructured data files | 10 audio, 10 images, 2 PDFs for stages |
| `README.md` | Complete documentation | Setup, troubleshooting, customization |


---

## 🚀 Customization

### Change Branding
Edit `app.py` lines 29-33:
```python
SNOWFLAKE_BLUE = "#29B5E8"  # Change to your brand color
```

### Add Your Data
1. Modify `setup_database.sql` with your schema
2. Update table references in `app.py`
3. Adjust SQL queries for your use cases

### Add More Examples
In `app.py`, find the function page (e.g., `page_ai_translate()`) and add:
```python
show_example_card("New Example Title", "Description", 4)
# Add your SQL query and result display
```

---

## ✅ Success Criteria

Your deployment is successful when:

- ✅ Database has 16 objects created (2 warehouses, 3 stages, 7 tables, 2 views)
- ✅ Tables contain 100 rows of sample data (80 in core tables + 20 PII tickets)
- ✅ Streamlit app loads without errors
- ✅ All 12 function pages accessible via sidebar
- ✅ SQL queries execute and return results
- ✅ Sample files uploaded to 3 internal stages

---

## 🆘 Support

**For Snowflake Cortex AISQL questions:**
- Check [official documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql)
- Contact your Snowflake account team or Snowflake Support

**For this demo application:**
- Review code comments in `app.py`
- Check troubleshooting section above
- Consult `Cursor_Instructions.md` for build context

---

## 📄 License

This demo application is provided as-is for educational and demonstration purposes.

---

**Built with ❄️ Snowflake + Cursor | Powered by Cortex AI**

**Version 1.0** | Last Updated: November 7, 2025
