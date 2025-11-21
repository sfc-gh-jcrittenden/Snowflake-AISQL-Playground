# =============================================================================
# Snowflake AI Functions in Action - Comprehensive Demo Application
# =============================================================================
# A Streamlit in Snowflake application showcasing all Cortex AI Functions
# with Tasty Bytes themed examples
# =============================================================================

import streamlit as st
from snowflake.snowpark.context import get_active_session
import json
import pypdfium2 as pdfium

# Configure page - MUST be first Streamlit command
st.set_page_config(
    page_title="Snowflake Cortex AI Functions Playground",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Snowflake session
session = get_active_session()

# =============================================================================
# CONFIGURATION & STYLING
# =============================================================================

# Snowflake Brand Colors
SNOWFLAKE_BLUE = "#29B5E8"
SNOWFLAKE_DARK_BLUE = "#111827" 
SNOWFLAKE_AQUA = "#00D4FF"
SNOWFLAKE_WHITE = "#FFFFFF"
SNOWFLAKE_LIGHT_GRAY = "#E8EEF2"

# Global AI_COMPLETE Models List (alphabetically ordered)
# Curated list of latest and most capable models
AI_COMPLETE_MODELS = [
    "claude-4-sonnet",
    "claude-haiku-4-5",
    "claude-sonnet-4-5",
    "llama4-maverick",
    "llama4-scout",
    "mistral-large2",
    "openai-gpt-5",
    "openai-gpt-5-mini"
]

# Custom CSS for Snowflake branding
st.markdown(f"""
<style>
    /* Main app styling */
    .stApp {{
        background-color: {SNOWFLAKE_WHITE};
    }}
    
    /* Main content area - let wide layout handle width */
    .main .block-container {{
        padding-left: 2rem;
        padding-right: 2rem;
        padding-top: 1rem;
    }}
    
    /* Header styling */
    .main-header {{
        background: linear-gradient(135deg, {SNOWFLAKE_BLUE} 0%, {SNOWFLAKE_AQUA} 100%);
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 30px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }}
    
    /* Card styling for examples */
    .demo-card {{
        background: linear-gradient(to right, #F8FAFC 0%, #FFFFFF 100%);
        border-left: 5px solid {SNOWFLAKE_BLUE};
        padding: 24px;
        border-radius: 12px;
        margin: 20px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }}
    
    .demo-card:hover {{
        box-shadow: 0 4px 12px rgba(41, 181, 232, 0.15);
        transform: translateY(-2px);
    }}
    
    /* Button styling */
    .stButton>button {{
        background: linear-gradient(135deg, {SNOWFLAKE_BLUE} 0%, {SNOWFLAKE_AQUA} 100%);
        color: white;
        border-radius: 8px;
        border: none;
        padding: 12px 28px;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(41, 181, 232, 0.3);
    }}
    
    .stButton>button:hover {{
        background: linear-gradient(135deg, {SNOWFLAKE_AQUA} 0%, {SNOWFLAKE_BLUE} 100%);
        box-shadow: 0 4px 8px rgba(41, 181, 232, 0.4);
        transform: translateY(-1px);
    }}
    
    /* Sidebar styling - Modern light gray */
    [data-testid="stSidebar"] {{
        background-color: {SNOWFLAKE_LIGHT_GRAY};
        border-right: 1px solid #D1D9E0;
    }}
    
    [data-testid="stSidebar"] > div:first-child {{
        background-color: {SNOWFLAKE_LIGHT_GRAY};
    }}
    
    /* Sidebar text colors */
    [data-testid="stSidebar"] * {{
        color: #1E293B !important;
    }}
    
    /* Sidebar radio buttons */
    [data-testid="stSidebar"] .stRadio > label {{
        background-color: white;
        padding: 10px 12px;
        border-radius: 8px;
        margin: 4px 0;
        transition: all 0.2s ease;
        border: 1px solid #D1D9E0;
        font-size: 14px;
    }}
    
    [data-testid="stSidebar"] .stRadio > label:hover {{
        background-color: #F0F7FA;
        border-color: {SNOWFLAKE_BLUE};
    }}
    
    /* Selected radio button */
    [data-testid="stSidebar"] .stRadio > label[data-baseweb="radio"] > div:first-child {{
        background-color: {SNOWFLAKE_BLUE};
    }}
    
    /* Sidebar logo container */
    .sidebar-logo {{
        text-align: center;
        padding: 20px 10px;
        margin-bottom: 10px;
        background: white;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }}
    
    /* Code block styling */
    .stCodeBlock {{
        background-color: #1E293B;
        border-left: 4px solid {SNOWFLAKE_BLUE};
        border-radius: 8px;
    }}
    
    /* Metric styling */
    [data-testid="stMetricValue"] {{
        font-size: 28px;
        color: {SNOWFLAKE_BLUE};
        font-weight: 700;
    }}
    
    /* Expander styling */
    .streamlit-expanderHeader {{
        background-color: #F8FAFC;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
    }}
    
    .streamlit-expanderHeader:hover {{
        background-color: #F0F7FA;
        border-color: {SNOWFLAKE_BLUE};
    }}
</style>
""", unsafe_allow_html=True)

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def escape_sql_string(text):
    """Escape apostrophes in text for SQL queries"""
    if text is None:
        return ""
    return str(text).replace("'", "''")

def show_header():
    """Display the app header"""
    st.markdown('<div class="main-header"><h1>❄️ Snowflake Cortex AI Functions Playground ❄️</h1><p>Powered by Cortex AI - Explore Every Function</p></div>', unsafe_allow_html=True)

def execute_query(query):
    """Execute a Snowflake query and return results"""
    try:
        result = session.sql(query).collect()
        return result, None
    except Exception as e:
        return None, str(e)

def show_example_card(title, description, example_num):
    """Display a styled example card"""
    st.markdown(f"""
    <div class="demo-card">
        <h4>📌 Example {example_num}: {title}</h4>
        <p>{description}</p>
    </div>
    """, unsafe_allow_html=True)

def show_multimodal_support(text=True, images=False, documents=False, audio=False):
    """Display multi-modal capability indicators as inline badges"""
    capabilities = []
    if text:
        capabilities.append("📝 Text")
    if images:
        capabilities.append("🖼️ Images")
    if documents:
        capabilities.append("📄 Documents")
    if audio:
        capabilities.append("🎵 Audio")
    
    caps_str = " · ".join(capabilities)
    return f"""<span style='background: linear-gradient(135deg, #E8F4F8 0%, #D6EEF7 100%); 
                           padding: 6px 14px; 
                           border-radius: 6px; 
                           font-size: 13px;
                           font-weight: 500;
                           color: #1E293B;
                           border: 1px solid #B8DCEA;'>
        🎯 {caps_str}
    </span>"""

def display_pdf_page():
    """Display the current PDF page as an image"""
    pdf = st.session_state['pdf_doc']
    page_index = st.session_state['pdf_page']
    
    # Render the page to an image
    page = pdf[page_index]
    pil_image = page.render(scale=2).to_pil()
    
    # Display the image
    st.image(pil_image, use_container_width=True)

# =============================================================================
# PAGE NAVIGATION
# =============================================================================

# Sidebar with logo
st.sidebar.markdown("""
<div class="sidebar-logo">
    <img src="https://www.snowflake.com/wp-content/themes/snowflake/assets/img/brand-guidelines/logo-sno-blue-example.svg" width="140"/>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

# Define all pages
pages = {
    "🏠 Home": "home",
    "🤖 AI_COMPLETE": "ai_complete",
    "🌍 AI_TRANSLATE": "ai_translate",
    "😊 AI_SENTIMENT": "ai_sentiment",
    "🔍 AI_EXTRACT": "ai_extract",
    "🏷️ AI_CLASSIFY": "ai_classify",
    "🎯 AI_FILTER": "ai_filter",
    "🔗 AI_SIMILARITY": "ai_similarity",
    "🔒 AI_REDACT": "ai_redact",
    "🎙️ AI_TRANSCRIBE": "ai_transcribe",
    "📄 AI_PARSE_DOCUMENT": "ai_parse_document",
    "📝 AI_SUMMARIZE_AGG": "ai_summarize_agg",
    "📊 AI_AGG": "ai_agg"
}

# Page selection
selected_page = st.sidebar.radio("**Select a Function:**", list(pages.keys()), label_visibility="visible")
current_page = pages[selected_page]

# Sidebar info
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='background: white; padding: 16px; border-radius: 8px; border-left: 4px solid #29B5E8;'>
    <h4 style='color: #1E293B; margin-top: 0;'>🍔 About Tasty Bytes</h4>
    <p style='color: #475569; font-size: 14px; margin-bottom: 0;'>
        A fictitious food truck company serving delicious street food across major cities. 
        This demo uses Tasty Bytes data to showcase AI Functions capabilities.
    </p>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# PAGE: HOME
# =============================================================================

def page_home():
    show_header()
    
    st.markdown("""
    ## Welcome to the Cortex AI Functions Interactive Demo!
    
    This application demonstrates **12 core Snowflake Cortex AI Functions** using real-world scenarios 
    from the Tasty Bytes food truck business.
    
    ### What are Cortex AI Functions?
    
    Use Cortex AI Functions in Snowflake to run unstructured analytics on text, images, audio files, and more, with industry-leading LLMs 
    from OpenAI, Anthropic, Meta, Mistral AI, and DeepSeek. 
    
    All models are fully hosted in Snowflake, ensuring **performance**, **scalability**, and **governance** 
    while keeping your data secure and in place.
    """)
    
    st.success("👈 **Select a function from the sidebar to explore interactive examples!**")
    
    # Model availability disclaimer
    st.info("""
    ⚠️ **Model Availability Note:** Not all AI models are available by default in every Snowflake region. 
    Some models may require enabling **cross-region inference** to access models hosted in different regions. 
    
    📖 Learn more: [Cross-Region Inference Documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cross-region-inference#label-use-cross-region-inference)
    """)
    
    # Pricing disclaimer
    st.warning("""
    💰 **Pricing Information:** Credit costs displayed throughout this app are for reference purposes only. 
    Always consult the official **[Snowflake Credit Consumption Table (Table 6a)](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf)** 
    for the most current and accurate pricing information.
    """)
    
    # Function overview with documentation links
    st.markdown("### 📚 Available Cortex AI Functions")
    
    st.markdown("""
    **[AI_COMPLETE](https://docs.snowflake.com/en/sql-reference/functions/ai_complete)**  
    Generates a completion for a given text string or image using a selected LLM. Use this function for most generative AI tasks.
    
    **[AI_TRANSLATE](https://docs.snowflake.com/en/sql-reference/functions/ai_translate)**  
    Translates text between supported languages.
    
    **[AI_SENTIMENT](https://docs.snowflake.com/en/sql-reference/functions/ai_sentiment)**  
    Extracts sentiment from text.
    
    **[AI_EXTRACT](https://docs.snowflake.com/en/sql-reference/functions/ai_extract)**  
    Extracts information from an input string or file, for example, text, images, and documents. Supports multiple languages.
    
    **[AI_CLASSIFY](https://docs.snowflake.com/en/sql-reference/functions/ai_classify)**  
    Classifies text or images into user-defined categories.
    
    **[AI_FILTER](https://docs.snowflake.com/en/sql-reference/functions/ai_filter)**  
    Returns True or False for a given text or image input, allowing you to filter results in SELECT, WHERE, or JOIN ... ON clauses.
    
    **[AI_SIMILARITY](https://docs.snowflake.com/en/sql-reference/functions/ai_similarity)**  
    Calculates the embedding similarity between two inputs.
    
    **[AI_REDACT](https://docs.snowflake.com/en/sql-reference/functions/ai_redact)**  
    Redacts personally identifiable information (PII) from text.
    
    **[AI_TRANSCRIBE](https://docs.snowflake.com/en/sql-reference/functions/ai_transcribe)**  
    Transcribes audio and video files stored in a stage, extracting text, timestamps, and speaker information.
    
    **[AI_PARSE_DOCUMENT](https://docs.snowflake.com/en/sql-reference/functions/ai_parse_document)**  
    Extracts text (using OCR mode) or text with layout information (using LAYOUT mode) from documents in an internal or external stage.
    
    **[AI_SUMMARIZE_AGG](https://docs.snowflake.com/en/sql-reference/functions/ai_summarize_agg)**  
    Aggregates a text column and returns a summary across multiple rows. This function isn't subject to context window limitations.
    
    **[AI_AGG](https://docs.snowflake.com/en/sql-reference/functions/ai_agg)**  
    Aggregates a text column and returns insights across multiple rows based on a user-defined prompt. This function isn't subject to context window limitations.
    """)
    
    st.markdown("---")
    
    # Quick stats
    st.markdown("### 📊 Demo Database Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        result, _ = execute_query("SELECT COUNT(*) as cnt FROM AI_FUNCTIONS_PLAYGROUND.DEMO.FOOD_TRUCKS")
        if result:
            st.metric("Food Trucks", result[0]['CNT'])
    
    with col2:
        result, _ = execute_query("SELECT COUNT(*) as cnt FROM AI_FUNCTIONS_PLAYGROUND.DEMO.CUSTOMER_REVIEWS")
        if result:
            st.metric("Customer Reviews", result[0]['CNT'])
    
    with col3:
        result, _ = execute_query("SELECT COUNT(*) as cnt FROM AI_FUNCTIONS_PLAYGROUND.DEMO.MENU_ITEMS")
        if result:
            st.metric("Menu Items", result[0]['CNT'])
    
    with col4:
        result, _ = execute_query("SELECT COUNT(*) as cnt FROM AI_FUNCTIONS_PLAYGROUND.DEMO.SUPPORT_TICKETS")
        if result:
            st.metric("Support Tickets", result[0]['CNT'])

# =============================================================================
# PAGE: AI_COMPLETE
# =============================================================================

def page_ai_complete():
    show_header()
    
    st.title("🤖 AI_COMPLETE")
    
    # Multi-modal support and documentation links inline
    multimodal_badge = show_multimodal_support(text=True, images=False, documents=False, audio=False)
    st.markdown(f"""
    **AI_COMPLETE** generates intelligent completions using state-of-the-art LLMs like Claude, GPT, and Llama. 
    Use it for content generation, question answering, data enrichment, and creative tasks.
    
    {multimodal_badge} &nbsp;&nbsp; 📖 [View Documentation](https://docs.snowflake.com/en/sql-reference/functions/ai_complete)
    
    **💰 Cost (per 1M tokens):** Varies by model - Input / Output
    - **Claude-4.5-Sonnet**: 1.65 / 8.25 credits (Latest, Best Quality)
    - **OpenAI GPT-5**: 0.69 / 5.50 credits (Latest GPT)
    - **Llama4-Maverick**: 0.12 / 0.49 credits (Cost-Effective)
    - **Claude-3.5-Sonnet**: 1.50 / 7.50 credits
    
    [View full pricing](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf)
    """, unsafe_allow_html=True)
    
    # Model availability disclaimer
    st.info("""
    ⚠️ **Model Availability Note:** Not all AI models are available by default in every Snowflake region. 
    Some models may require enabling **cross-region inference** to access models hosted in different regions. 
    
    📖 Learn more: [Cross-Region Inference Documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cross-region-inference#label-use-cross-region-inference)
    """)
    
    # Example 1: Menu Description Generation
    show_example_card(
        "Generate Creative Menu Descriptions",
        "Use AI_COMPLETE to create appealing menu item descriptions for marketing",
        1
    )
    
    col1, col2 = st.columns([3, 1])
    with col1:
        menu_item = st.selectbox("Select a menu item:", 
                                 ["Carne Asada Taco", "Tonkotsu Ramen", "Lamb Gyro", "Classic Poutine"])
    with col2:
        model_ex1 = st.selectbox("Model:", AI_COMPLETE_MODELS, key="model_ex1")
    
    if st.button("Generate Description", key="gen_desc"):
        with st.spinner("Generating..."):
            escaped_item = escape_sql_string(menu_item)
            query = f"""
            SELECT AI_COMPLETE(
                '{model_ex1}',
                'Write a mouth-watering, creative menu description for a {escaped_item}. 
                Keep it under 50 words and make it appealing to food lovers.',
                {{'temperature': 0.7}}
            ) as description
            """
            result, error = execute_query(query)
            if result:
                st.success("**Generated Description:**")
                st.markdown(result[0]['DESCRIPTION'])
                st.code(query, language="sql")
    
    st.markdown("---")
    
    # Example 2: Bulk Processing - Enrich All Menu Items
    show_example_card(
        "Bulk Processing: Generate Marketing Descriptions for All Menu Items",
        "Process entire tables with AI_COMPLETE to enrich data at scale",
        2
    )
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("Generate marketing copy for all menu items in the database")
    with col2:
        model_ex2 = st.selectbox("Model:", AI_COMPLETE_MODELS, key="model_ex2")
    
    if st.button("Enrich All Menu Items", key="bulk_menu"):
        with st.spinner("Processing all menu items..."):
            query = f"""
            SELECT 
                item_name,
                category,
                price,
                description_english as original_description,
                AI_COMPLETE(
                    '{model_ex2}',
                    'Create a compelling 30-word marketing description for this menu item: ' || item_name || 
                    '. Category: ' || category || '. Make it appetizing and highlight unique flavors.',
                    {{'temperature': 0.7}}
                ) as ai_marketing_copy
            FROM AI_FUNCTIONS_PLAYGROUND.DEMO.MENU_ITEMS
            LIMIT 10
            """
            result, error = execute_query(query)
            if result:
                st.success(f"**Generated marketing copy for {len(result)} menu items:**")
                st.dataframe(result, use_container_width=True)
                st.code(query, language="sql")
    
    st.markdown("---")
    
    # Example 3: Bulk Processing - Categorize Support Tickets
    show_example_card(
        "Bulk Processing: Auto-Categorize All Support Tickets",
        "Use AI to classify and prioritize large volumes of support tickets",
        3
    )
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("Automatically categorize and suggest actions for support tickets")
    with col2:
        model_ex3 = st.selectbox("Model:", AI_COMPLETE_MODELS, key="model_ex3")
    
    if st.button("Categorize Tickets", key="bulk_tickets"):
        with st.spinner("Processing support tickets..."):
            query = f"""
            WITH ai_analysis AS (
                SELECT 
                    ticket_id,
                    customer_name,
                    issue_description,
                    urgency,
                    AI_COMPLETE(
                        '{model_ex3}',
                        'Analyze this support ticket and respond in JSON (do not generate ```json\n) format with: category (Food Quality/Service/Payment/Location/Other), priority (High/Medium/Low), and suggested_action (one sentence). Ticket: ' || issue_description,
                        {{'temperature': 0.3}}
                    ) as ai_analysis_json
                FROM AI_FUNCTIONS_PLAYGROUND.DEMO.SUPPORT_TICKETS
            )
            SELECT 
                ticket_id,
                customer_name,
                issue_description,
                urgency,
                TRY_PARSE_JSON(ai_analysis_json):category::STRING as category,
                TRY_PARSE_JSON(ai_analysis_json):priority::STRING as priority,
                TRY_PARSE_JSON(ai_analysis_json):suggested_action::STRING as suggested_action
            FROM ai_analysis;
            """
            result, error = execute_query(query)
            if result:
                st.success(f"**✅ Analyzed {len(result)} support tickets (full dataset):**")
                st.dataframe(result, use_container_width=True)
                
                # Show summary statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    high_priority = sum(1 for row in result if row['PRIORITY'] == 'High')
                    st.metric("High Priority", high_priority)
                with col2:
                    medium_priority = sum(1 for row in result if row['PRIORITY'] == 'Medium')
                    st.metric("Medium Priority", medium_priority)
                with col3:
                    low_priority = sum(1 for row in result if row['PRIORITY'] == 'Low')
                    st.metric("Low Priority", low_priority)
                
                st.code(query, language="sql")
    
    st.markdown("---")
    
    # Example 4: Custom Prompt Playground
    show_example_card(
        "Custom Prompt Playground",
        "Try your own prompts with AI_COMPLETE and different models",
        4
    )
    
    custom_prompt = st.text_area("Enter your custom prompt:", 
                                 "What are 3 creative food truck name ideas for a sushi business?")
    
    col1, col2 = st.columns(2)
    with col1:
        model = st.selectbox("Select model:", AI_COMPLETE_MODELS, key="model_ex4")
        
        # Model guidance
        model_info = {
            "claude-sonnet-4-5": "🌟 Latest Claude - Best quality, reasoning",
            "openai-gpt-5": "🚀 Latest OpenAI - Advanced capabilities",
            "llama4-maverick": "💰 Cost-effective - Great performance/price",
            "claude-3-5-sonnet": "⚡ Proven quality - Fast and reliable",
            "llama3.1-70b": "🎯 Open-source - Good balance"
        }
        st.caption(model_info.get(model, ""))
        
    with col2:
        temperature = st.slider("Temperature:", 0.0, 1.0, 0.7, 0.1)
        st.caption("Higher = more creative, Lower = more focused")
    
    if st.button("Run Custom Prompt", key="custom_prompt"):
        with st.spinner("Processing..."):
            escaped_prompt = escape_sql_string(custom_prompt)
            query = f"""
            SELECT AI_COMPLETE(
                '{model}',
                '{escaped_prompt}',
                {{'temperature': {temperature}}}
            ) as result
            """
            result, error = execute_query(query)
            if result:
                st.success("**Result:**")
                st.markdown(result[0]['RESULT'])
                st.code(query, language="sql")
            elif error:
                st.error(f"Error: {error}")

# =============================================================================
# PAGE: AI_TRANSLATE
# =============================================================================

def page_ai_translate():
    show_header()
    
    st.title("🌍 AI_TRANSLATE")
    
    multimodal_badge = show_multimodal_support(text=True, images=False, documents=False, audio=False)
    st.markdown(f"""
    **AI_TRANSLATE** provides industry-leading translation quality across 24 languages.
    Perfect for internationalizing menus, translating reviews, and creating multilingual content.
    
    {multimodal_badge} &nbsp;&nbsp; 📖 [View Documentation](https://docs.snowflake.com/en/sql-reference/functions/ai_translate)
    
    **💰 Cost:** 1.50 credits per 1M tokens (Table 6a)  
    [View pricing details](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf)
    
    **Supported Languages (24):** English, Spanish, French, German, Japanese, Chinese, Portuguese, Italian, 
    Dutch, Russian, Korean, Arabic, Hindi, Turkish, Polish, Ukrainian, Romanian, Czech, Swedish, 
    Danish, Finnish, Norwegian, Greek, Hebrew
    """, unsafe_allow_html=True)
    
    # Comprehensive language mapping: Display name -> ISO code (all 24 supported languages)
    ALL_LANGUAGES = {
        "English": "en",
        "Spanish": "es",
        "French": "fr",
        "German": "de",
        "Japanese": "ja",
        "Chinese": "zh",
        "Portuguese": "pt",
        "Italian": "it",
        "Dutch": "nl",
        "Russian": "ru",
        "Korean": "ko",
        "Arabic": "ar",
        "Hindi": "hi",
        "Turkish": "tr",
        "Polish": "pl",
        "Ukrainian": "uk",
        "Romanian": "ro",
        "Czech": "cs",
        "Swedish": "sv",
        "Danish": "da",
        "Finnish": "fi",
        "Norwegian": "no",
        "Greek": "el",
        "Hebrew": "he"
    }
    
    # Example 1: Menu Translation
    show_example_card(
        "Translate Menu Descriptions",
        "Translate menu items to any of the 24 supported languages",
        1
    )
    
    result, _ = execute_query("SELECT item_name, description_english FROM AI_FUNCTIONS_PLAYGROUND.DEMO.MENU_ITEMS")
    if result:
        menu_options = {r['ITEM_NAME']: r['DESCRIPTION_ENGLISH'] for r in result}
        
        col1, col2 = st.columns(2)
        with col1:
            selected_item = st.selectbox("Select menu item:", list(menu_options.keys()))
        with col2:
            target_lang_display = st.selectbox("Translate to:", list(ALL_LANGUAGES.keys()))
        
        if st.button("Translate", key="translate_menu"):
            with st.spinner("Translating..."):
                description = escape_sql_string(menu_options[selected_item])
                target_lang_code = ALL_LANGUAGES[target_lang_display]
                query = f"""
                SELECT AI_TRANSLATE(
                    '{description}',
                    'en',
                    '{target_lang_code}'
                ) as translation
                """
                result, error = execute_query(query)
                if result:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Original (English):**")
                        st.write(menu_options[selected_item])
                    with col2:
                        st.markdown(f"**Translation ({target_lang_display}):**")
                        st.write(result[0]['TRANSLATION'])
                    st.code(query, language="sql")
    
    st.markdown("---")
    
    # Example 2: Batch Translation
    show_example_card(
        "Batch Translate All Customer Reviews",
        "Translate all reviews at once to any supported language",
        2
    )
    
    batch_target_lang = st.selectbox(
        "Translate all reviews to:",
        list(ALL_LANGUAGES.keys()),
        index=list(ALL_LANGUAGES.keys()).index("Spanish"),
        key="batch_lang"
    )
    
    if st.button("Translate All Reviews", key="batch_translate"):
        with st.spinner(f"Translating all reviews to {batch_target_lang}..."):
            target_code = ALL_LANGUAGES[batch_target_lang]
            query = f"""
            SELECT 
                customer_name,
                food_truck_name,
                review_text as original,
                AI_TRANSLATE(review_text, 'en', '{target_code}') as translation
            FROM AI_FUNCTIONS_PLAYGROUND.DEMO.CUSTOMER_REVIEWS
            WHERE language = 'English'
            """
            result, error = execute_query(query)
            if result:
                st.success(f"**✅ Translated {len(result)} reviews to {batch_target_lang}:**")
                st.dataframe(result, use_container_width=True)
                st.code(query, language="sql")
    
    st.markdown("---")
    
    # Example 3: Auto-detect Source Language
    show_example_card(
        "Auto-Detect and Translate",
        "AI_TRANSLATE can automatically detect the source language and translate to any target",
        3
    )
    
    custom_text = st.text_area("Enter text in any language:", 
                               "Bonjour! Comment allez-vous aujourd'hui?")
    auto_target_display = st.selectbox("Translate to:", list(ALL_LANGUAGES.keys()), key="auto_target")
    
    if st.button("Auto-Translate", key="auto_translate"):
        with st.spinner("Translating..."):
            escaped_text = escape_sql_string(custom_text)
            auto_target_code = ALL_LANGUAGES[auto_target_display]
            query = f"""
            SELECT AI_TRANSLATE(
                '{escaped_text}',
                '',
                '{auto_target_code}'
            ) as translation
            """
            result, error = execute_query(query)
            if result:
                st.success(f"**Translation ({auto_target_display}):**")
                st.write(result[0]['TRANSLATION'])
                st.code(query, language="sql")

# =============================================================================
# PAGE: AI_SENTIMENT
# =============================================================================

def page_ai_sentiment():
    show_header()
    
    st.title("😊 AI_SENTIMENT")
    
    multimodal_badge = show_multimodal_support(text=True, images=False, documents=False, audio=False)
    st.markdown(f"""
    **AI_SENTIMENT** analyzes sentiment in text with category-specific scores.  
    **SNOWFLAKE.CORTEX.SENTIMENT** returns a simple numerical score from -1 to 1.
    
    Essential for understanding customer feedback, social media, and support tickets.
    
    {multimodal_badge} &nbsp;&nbsp; 📖 [AI_SENTIMENT Docs](https://docs.snowflake.com/en/sql-reference/functions/ai_sentiment) | [SENTIMENT Docs](https://docs.snowflake.com/en/sql-reference/functions/sentiment)
    
    **💰 Cost:** 
    - **AI_SENTIMENT:** 1.60 credits per 1M tokens
    - **SENTIMENT (legacy):** 0.08 credits per 1M tokens
    
    [View pricing details](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf)
    """, unsafe_allow_html=True)
    
    # Example 1: Review Sentiment Analysis
    show_example_card(
        "Analyze All Customer Review Sentiments",
        "Extract numerical sentiment scores and category-specific sentiment for all reviews",
        1
    )
    
    if st.button("Analyze All Reviews", key="analyze_sentiment"):
        with st.spinner("Analyzing all customer reviews..."):
            query = """
            WITH sentiment_analysis AS (
                    SELECT distinct
                        review_id,
                        customer_name,
                        food_truck_name,
                        review_text,
                        rating,
                        SNOWFLAKE.CORTEX.SENTIMENT(review_text) as overall_sentiment,
                        AI_SENTIMENT(review_text, ['Food Quality', 'Service', 'Value', 'Atmosphere']) as category_sentiment_json
                    FROM AI_FUNCTIONS_PLAYGROUND.DEMO.CUSTOMER_REVIEWS
                )
                SELECT 
                    review_id,
                    customer_name,
                    food_truck_name,
                    rating,
                    overall_sentiment,
                    MAX(CASE WHEN f.value:name::STRING = 'overall' THEN f.value:sentiment::STRING END) as overall,
                    MAX(CASE WHEN f.value:name::STRING = 'Atmosphere' THEN f.value:sentiment::STRING END) as atmosphere,
                    MAX(CASE WHEN f.value:name::STRING = 'Food Quality' THEN f.value:sentiment::STRING END) as food_quality,
                    MAX(CASE WHEN f.value:name::STRING = 'Service' THEN f.value:sentiment::STRING END) as service,
                    MAX(CASE WHEN f.value:name::STRING = 'Value' THEN f.value:sentiment::STRING END) as value,
                    review_text
                FROM sentiment_analysis,
                LATERAL FLATTEN(input => category_sentiment_json:categories) f
                GROUP BY review_id, customer_name, food_truck_name, rating, overall_sentiment, category_sentiment_json, review_text
                ORDER BY overall_sentiment DESC;
            """
            result, error = execute_query(query)
            if result:
                st.success(f"**✅ Analyzed {len(result)} customer reviews:**")
                
                # Show summary statistics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    avg_sentiment = sum(row['OVERALL_SENTIMENT'] for row in result) / len(result)
                    st.metric("Average Sentiment", f"{avg_sentiment:.3f}")
                with col2:
                    positive_count = sum(1 for row in result if row['OVERALL_SENTIMENT'] > 0.3)
                    st.metric("Positive Reviews", positive_count)
                with col3:
                    neutral_count = sum(1 for row in result if -0.3 <= row['OVERALL_SENTIMENT'] <= 0.3)
                    st.metric("Neutral Reviews", neutral_count)
                with col4:
                    negative_count = sum(1 for row in result if row['OVERALL_SENTIMENT'] < -0.3)
                    st.metric("Negative Reviews", negative_count)
                
                # Display full results
                st.markdown("**📊 Detailed Sentiment Analysis:**")
                
                # Create display dataframe without review_text for the main view
                display_df = []
                for row in result:
                    display_df.append({
                        'Review ID': row['REVIEW_ID'],
                        'Customer': row['CUSTOMER_NAME'],
                        'Food Truck': row['FOOD_TRUCK_NAME'],
                        'Rating': '⭐' * row['RATING'],
                        'Overall': f"{row['OVERALL_SENTIMENT']:.3f}",
                        'Food Quality': row['FOOD_QUALITY'] or 'N/A',
                        'Service': row['SERVICE'] or 'N/A',
                        'Value': row['VALUE'] or 'N/A',
                        'Atmosphere': row['ATMOSPHERE'] or 'N/A',
                        'Review': row['REVIEW_TEXT'] or 'N/A'
                    })
                
                st.dataframe(display_df, use_container_width=True)
                
                
                st.code(query, language="sql")
    
    st.markdown("---")
    
    # Example 2: Aggregate Sentiment Analysis
    show_example_card(
        "Food Truck Sentiment Comparison",
        "Compare average sentiment across different food trucks using SENTIMENT function",
        2
    )
    
    if st.button("Compare Trucks", key="compare_sentiment"):
        with st.spinner("Analyzing..."):
            query = """
            SELECT 
                food_truck_name,
                AVG(rating) as avg_rating,
                COUNT(*) as review_count,
                AVG(SNOWFLAKE.CORTEX.SENTIMENT(review_text)) as avg_sentiment
            FROM AI_FUNCTIONS_PLAYGROUND.DEMO.CUSTOMER_REVIEWS
            GROUP BY food_truck_name
            ORDER BY avg_sentiment DESC
            """
            result, error = execute_query(query)
            if result:
                st.dataframe(result, use_container_width=True)
                st.code(query, language="sql")
    
    st.markdown("---")
    
    # Example 3: Support Ticket Sentiment
    show_example_card(
        "Prioritize Support Tickets by Sentiment",
        "Use SENTIMENT function to identify negative sentiment for priority handling",
        3
    )
    
    if st.button("Analyze Tickets", key="ticket_sentiment"):
        with st.spinner("Analyzing tickets..."):
            query = """
            SELECT 
                ticket_id,
                customer_name,
                issue_description,
                urgency,
                SNOWFLAKE.CORTEX.SENTIMENT(issue_description) as sentiment_score,
                CASE 
                    WHEN SNOWFLAKE.CORTEX.SENTIMENT(issue_description) < -0.3 THEN 'Urgent - Negative'
                    WHEN SNOWFLAKE.CORTEX.SENTIMENT(issue_description) < 0 THEN 'Needs Attention'
                    ELSE 'Positive/Neutral'
                END as priority_level
            FROM AI_FUNCTIONS_PLAYGROUND.DEMO.SUPPORT_TICKETS
            ORDER BY sentiment_score ASC
            LIMIT 10
            """
            result, error = execute_query(query)
            if result:
                st.dataframe(result, use_container_width=True)
                st.code(query, language="sql")

# =============================================================================
# PAGE: AI_EXTRACT
# =============================================================================

def page_ai_extract():
    show_header()
    
    st.title("🔍 AI_EXTRACT")
    
    multimodal_badge = show_multimodal_support(text=True, images=True, documents=True, audio=False)
    st.markdown(f"""
    **AI_EXTRACT** extracts specific information from text, documents, and images based on your questions.
    Perfect for parsing invoices, extracting entities, and structured data extraction from PDFs.
    
    {multimodal_badge} &nbsp;&nbsp; 📖 [View Documentation](https://docs.snowflake.com/en/sql-reference/functions/ai_extract)
    
    **💰 Cost:** 5.00 credits per 1M tokens (Table 6a)  
    [View pricing details](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf)
    """, unsafe_allow_html=True)
    
    # Example 1: Extract Entities from Reviews
    show_example_card(
        "Extract Menu Items Mentioned in All Reviews",
        "Automatically identify which menu items customers are talking about across all reviews",
        1
    )
    
    if st.button("Extract from All Reviews", key="extract_items"):
        with st.spinner("Extracting information from all reviews..."):
            query = """
            WITH extracted_data AS (
                SELECT 
                    review_id,
                    customer_name,
                    food_truck_name,
                    rating,
                    review_text,
                    AI_EXTRACT(review_text,
                        {
                            'foods_mentioned': 'What food items are mentioned?', 
                            'customer_favorite': 'What did the customer like most?',
                            'customer_complaint': 'What did the customer complain about?'
                         }
                    ) as extracted_details
                FROM AI_FUNCTIONS_PLAYGROUND.DEMO.CUSTOMER_REVIEWS
            )
            SELECT 
                review_id,
                customer_name,
                food_truck_name,
                rating,
                extracted_details:response:foods_mentioned::STRING as foods_mentioned,
                extracted_details:response:customer_favorite::STRING as customer_favorite,
                extracted_details:response:customer_complaint::STRING as customer_complaint,
                review_text
            FROM extracted_data
            ORDER BY rating DESC
            """
            result, error = execute_query(query)
            if result:
                st.success(f"**✅ Extracted information from {len(result)} reviews:**")
                
                # Create display dataframe
                display_df = []
                for row in result:
                    display_df.append({
                        'Review ID': row['REVIEW_ID'],
                        'Customer': row['CUSTOMER_NAME'],
                        'Food Truck': row['FOOD_TRUCK_NAME'],
                        'Rating': '⭐' * row['RATING'],
                        'Food Items': row['FOODS_MENTIONED'] or 'N/A',
                        'Liked Most': row['CUSTOMER_FAVORITE'] or 'N/A',
                        'Complaints': row['CUSTOMER_COMPLAINT'] or 'N/A',
                        'Review': row['REVIEW_TEXT']
                    })
                
                st.dataframe(display_df, use_container_width=True)
                st.code(query, language="sql")
    
    st.markdown("---")
    
    # Example 2: Extract Structured Data from Support Tickets
    show_example_card(
        "Extract Issue Details from All Support Tickets",
        "Parse all support tickets to extract key information",
        2
    )
    
    if st.button("Analyze All Tickets", key="extract_tickets"):
        with st.spinner("Extracting details from all support tickets..."):
            query = """
            WITH extracted_data AS (
                SELECT 
                    ticket_id,
                    customer_name,
                    urgency,
                    status,
                    issue_description,
                    AI_EXTRACT(issue_description, 
                        {
                            'issue_type': 'What type of issue is this? (Food Quality, Service, Payment, Location, Suggestion, Compliment)',
                            'requires_refund': 'Does the customer want a refund? (Yes/No)',
                            'food_item_mentioned': 'What food item is mentioned, if any?'
                        }
                    ) as extracted_details
                FROM AI_FUNCTIONS_PLAYGROUND.DEMO.SUPPORT_TICKETS
            )
            SELECT 
                ticket_id,
                customer_name,
                urgency,
                status,
                extracted_details:response:issue_type::STRING as issue_type,
                extracted_details:response:requires_refund::STRING as requires_refund,
                extracted_details:response:food_item_mentioned::STRING as food_item_mentioned,
                issue_description
            FROM extracted_data
            ORDER BY 
                ticket_id;
            """
            result, error = execute_query(query)
            if result:
                st.success(f"**✅ Extracted information from {len(result)} support tickets:**")
                
                # Show summary statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    refund_count = sum(1 for row in result if row['REQUIRES_REFUND'] and 'yes' in row['REQUIRES_REFUND'].lower())
                    st.metric("Refund Requests", refund_count)
                with col2:
                    high_urgency = sum(1 for row in result if row['URGENCY'] == 'High')
                    st.metric("High Urgency", high_urgency)
                with col3:
                    open_tickets = sum(1 for row in result if row['STATUS'] == 'Open')
                    st.metric("Open Tickets", open_tickets)
                
                # Create display dataframe
                display_df = []
                for row in result:
                    display_df.append({
                        'Ticket ID': row['TICKET_ID'],
                        'Customer': row['CUSTOMER_NAME'],
                        'Urgency': row['URGENCY'],
                        'Status': row['STATUS'],
                        'Issue Type': row['ISSUE_TYPE'] or 'N/A',
                        'Refund?': row['REQUIRES_REFUND'] or 'N/A',
                        'Food Item': row['FOOD_ITEM_MENTIONED'] or 'N/A',
                        'Description': row['ISSUE_DESCRIPTION']
                    })
                
                st.dataframe(display_df, use_container_width=True)
                st.code(query, language="sql")
    
    st.markdown("---")
    
    # Example 3: Custom Extraction
    show_example_card(
        "Custom Extraction Query",
        "Define your own extraction questions",
        3
    )
    
    custom_text = st.text_area("Enter text to analyze:", 
        "I visited the Guac n Roll truck yesterday and ordered 3 carne asada tacos for $13.50. The food was amazing but I had to wait 25 minutes!")
    
    questions = st.text_area("Enter questions (one per line):", 
        "What food items were ordered?\nWhat was the total cost?\nHow long was the wait time?\nWhat was the sentiment?")
    
    if st.button("Extract Information", key="custom_extract"):
        with st.spinner("Extracting..."):
            escaped_text = escape_sql_string(custom_text)
            question_list = [q.strip() for q in questions.split('\n') if q.strip()]
            question_array = str(question_list).replace("[", '').replace("]", '')
            query = f"""
            SELECT AI_EXTRACT(
                '{escaped_text}',
                ARRAY_CONSTRUCT({question_array})
            ) as extraction_result
            """
            result, error = execute_query(query)
            if result:
                st.json(json.loads(result[0]['EXTRACTION_RESULT']))
                st.code(query, language="sql")
    
    st.markdown("---")
    
    # Example 4: Extract from Single Supplier Invoice
    show_example_card(
        "Extract Structured Data from a Supplier Invoice PDF",
        "Use AI_EXTRACT to pull key invoice fields from a PDF document",
        4
    )
    
    # Check if invoices exist in the stage
    stage_check_query = """
        SELECT COUNT(*) as cnt 
        FROM DIRECTORY(@AI_FUNCTIONS_PLAYGROUND.DEMO.SUPPLIER_DOCUMENTS_STAGE) 
        WHERE RELATIVE_PATH LIKE '%supplier_invoice%'
    """
    stage_result, _ = execute_query(stage_check_query)
    invoice_count = stage_result[0]['CNT'] if stage_result else 0
    
    if invoice_count == 0:
        st.warning("""
        ⚠️ **No supplier invoices found in SUPPLIER_DOCUMENTS_STAGE**
        
        To use this demo:
        1. Generate invoices: `python generate_supplier_invoices.py`
        2. Upload to Snowflake: `PUT file://supplier_invoice_*.pdf @SUPPLIER_DOCUMENTS_STAGE AUTO_COMPRESS=FALSE;`
        """)
    else:
        st.success(f"✅ Found {invoice_count} supplier invoice(s) in the stage")
        
        # Get list of available invoices
        invoices_query = """
            SELECT RELATIVE_PATH 
            FROM DIRECTORY(@AI_FUNCTIONS_PLAYGROUND.DEMO.SUPPLIER_DOCUMENTS_STAGE) 
            WHERE RELATIVE_PATH LIKE '%supplier_invoice%'
            ORDER BY RELATIVE_PATH
        """
        invoices_result, _ = execute_query(invoices_query)
        
        if invoices_result:
            invoice_files = [row['RELATIVE_PATH'] for row in invoices_result]
            
            selected_invoice = st.selectbox(
                "Select an invoice to extract:",
                invoice_files,
                index=0,
                key="single_invoice_select"
            )
            
            if st.button("🔍 Extract Invoice Data", key="extract_single_invoice"):
                with st.spinner("Extracting data from invoice PDF..."):
                    query = f"""
                    WITH extracted_json AS (
                        SELECT 
                            '{selected_invoice}' as file_name,
                            BUILD_SCOPED_FILE_URL(@AI_FUNCTIONS_PLAYGROUND.DEMO.SUPPLIER_DOCUMENTS_STAGE, '{selected_invoice}') as file_url,
                            AI_EXTRACT(
                                file => TO_FILE('@AI_FUNCTIONS_PLAYGROUND.DEMO.SUPPLIER_DOCUMENTS_STAGE', '{selected_invoice}'),
                                responseFormat => {{
                                    'invoice_number': 'The invoice number (e.g., INV-1001)',
                                    'invoice_date': 'The invoice date in YYYY-MM-DD format',
                                    'supplier_name': 'The supplier/vendor company name',
                                    'supplier_address': 'The complete supplier address',
                                    'supplier_phone': 'The supplier phone number',
                                    'customer_name': 'The customer company name (should be Guac n Roll)',
                                    'customer_address': 'The complete customer address',
                                    'customer_phone': 'The customer phone number',
                                    'subtotal': 'The subtotal amount before tax as a number',
                                    'tax_amount': 'The tax amount as a number',
                                    'total_amount': 'The total invoice amount as a number',
                                    'payment_terms': 'The payment terms (e.g., Net 30 Days)',
                                    'item_count': 'The number of line items in the invoice'
                                }}
                            ) AS extracted_json
                    )
                    SELECT
                        file_name,
                        file_url,
                        extracted_json:response:invoice_number::string as invoice_number,
                        extracted_json:response:invoice_date::date as invoice_date,
                        extracted_json:response:supplier_name::string as supplier_name,
                        extracted_json:response:supplier_address::string as supplier_address,
                        extracted_json:response:supplier_phone::string as supplier_phone,
                        extracted_json:response:customer_name::string as customer_name,
                        extracted_json:response:customer_address::string as customer_address,
                        extracted_json:response:customer_phone::string as customer_phone,
                        REPLACE(extracted_json:response:subtotal, '$', '')::float as subtotal,
                        REPLACE(extracted_json:response:tax_amount, '$', '')::float as tax_amount,
                        REPLACE(extracted_json:response:total_amount, '$', '')::float as total_amount,
                        extracted_json:response:payment_terms::string as payment_terms,
                        extracted_json:response:item_count::integer as item_count,
                        extracted_json as raw_json
                    FROM extracted_json
                    """
                    
                    result, error = execute_query(query)
                    if result and not error:
                        row = result[0]
                        
                        st.success("✅ Data extracted and parsed successfully!")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("#### 📋 Extracted JSON")
                            st.json(row['RAW_JSON'])
                        
                        with col2:
                            st.markdown("#### 📄 Invoice PDF")
                            # Display PDF
                            try:
                                # Initialize session state for PDF viewing
                                if 'pdf_page' not in st.session_state:
                                    st.session_state['pdf_page'] = 0
                                
                                if 'pdf_url' not in st.session_state:
                                    st.session_state['pdf_url'] = selected_invoice
                                
                                if 'pdf_doc' not in st.session_state or st.session_state['pdf_url'] != selected_invoice:
                                    pdf_stream = session.file.get_stream(f"@AI_FUNCTIONS_PLAYGROUND.DEMO.SUPPLIER_DOCUMENTS_STAGE/{selected_invoice}", decompress=False)
                                    pdf = pdfium.PdfDocument(pdf_stream)
                                    st.session_state['pdf_doc'] = pdf
                                    st.session_state['pdf_url'] = selected_invoice
                                    st.session_state['pdf_page'] = 0
                                
                                # Display current page
                                display_pdf_page()
                                
                                # Download button
                                pdf_stream_download = session.file.get_stream(f"@AI_FUNCTIONS_PLAYGROUND.DEMO.SUPPLIER_DOCUMENTS_STAGE/{selected_invoice}", decompress=False)
                                pdf_binary_data = pdf_stream_download.read()
                                st.download_button(
                                    label="📥 Download Invoice PDF",
                                    data=pdf_binary_data,
                                    file_name=selected_invoice,
                                    mime="application/pdf",
                                    use_container_width=True
                                )
                                
                            except Exception as e:
                                st.error(f"Error retrieving PDF from Snowflake stage: {e}")
                                st.info("Please ensure the stage path and file name are correct and you have necessary permissions.")
                        
                        with st.expander("🔍 View SQL Query"):
                            st.code(query, language="sql")
                    elif error:
                        st.error(f"Error: {error}")
    
    st.markdown("---")
    
    # Example 5: Extract All Invoices and Load into Table
    show_example_card(
        "Batch Extract All Supplier Invoices & Load into Table",
        "Process all invoices at once, extract structured data, and insert into SUPPLIER_INVOICE_DETAILS table",
        5
    )
    
    if invoice_count == 0:
        st.warning("⚠️ No supplier invoices found. Please upload invoices to the stage first.")
    else:
        st.info(f"📄 **Ready to process {invoice_count} invoice(s)**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔍 Extract All Invoices", key="extract_all_invoices"):
                with st.spinner(f"Extracting data from {invoice_count} invoice(s)..."):
                    query = """
                    WITH extracted_json AS (
                        SELECT 
                            RELATIVE_PATH as file_name,
                            BUILD_SCOPED_FILE_URL(@AI_FUNCTIONS_PLAYGROUND.DEMO.SUPPLIER_DOCUMENTS_STAGE, RELATIVE_PATH) as file_url,
                            AI_EXTRACT(
                                file => TO_FILE('@AI_FUNCTIONS_PLAYGROUND.DEMO.SUPPLIER_DOCUMENTS_STAGE', RELATIVE_PATH),
                                responseFormat => {
                                    'invoice_number': 'The invoice number (e.g., INV-1001)',
                                    'invoice_date': 'The invoice date in YYYY-MM-DD format',
                                    'supplier_name': 'The supplier/vendor company name',
                                    'supplier_address': 'The complete supplier address',
                                    'supplier_phone': 'The supplier phone number',
                                    'customer_name': 'The customer company name (should be Guac n Roll)',
                                    'customer_address': 'The complete customer address',
                                    'customer_phone': 'The customer phone number',
                                    'subtotal': 'The subtotal amount before tax as a number',
                                    'tax_amount': 'The tax amount as a number',
                                    'total_amount': 'The total invoice amount as a number',
                                    'payment_terms': 'The payment terms (e.g., Net 30 Days)',
                                    'item_count': 'The number of line items in the invoice'
                                }
                            ) AS extracted_json
                        FROM DIRECTORY(@AI_FUNCTIONS_PLAYGROUND.DEMO.SUPPLIER_DOCUMENTS_STAGE)
                        WHERE RELATIVE_PATH LIKE '%supplier_invoice%'
                    )
                    SELECT
                        file_name,
                        file_url,
                        extracted_json:response:invoice_number::string as invoice_number,
                        extracted_json:response:invoice_date::date as invoice_date,
                        extracted_json:response:supplier_name::string as supplier_name,
                        extracted_json:response:supplier_address::string as supplier_address,
                        extracted_json:response:supplier_phone::string as supplier_phone,
                        extracted_json:response:customer_name::string as customer_name,
                        extracted_json:response:customer_address::string as customer_address,
                        extracted_json:response:customer_phone::string as customer_phone,
                        REPLACE(extracted_json:response:subtotal, '$', '')::float as subtotal,
                        REPLACE(extracted_json:response:tax_amount, '$', '')::float as tax_amount,
                        REPLACE(extracted_json:response:total_amount, '$', '')::float as total_amount,
                        extracted_json:response:payment_terms::string as payment_terms,
                        extracted_json:response:item_count::integer as item_count,
                        extracted_json as raw_json
                    FROM extracted_json
                    ORDER BY file_name
                    """
                    
                    result, error = execute_query(query)
                    if result and not error:
                        st.success(f"**✅ Extracted and parsed data from {len(result)} invoice(s)!**")
                        
                        # Display the extracted data
                        display_data = []
                        for row in result:
                            display_data.append({
                                'File': row['FILE_NAME'],
                                'Invoice #': row['INVOICE_NUMBER'] or 'N/A',
                                'Date': row['INVOICE_DATE'] or 'N/A',
                                'Supplier': row['SUPPLIER_NAME'] or 'N/A',
                                'Subtotal': f"${row['SUBTOTAL']:.2f}" if row['SUBTOTAL'] else 'N/A',
                                'Tax': f"${row['TAX_AMOUNT']:.2f}" if row['TAX_AMOUNT'] else 'N/A',
                                'Total': f"${row['TOTAL_AMOUNT']:.2f}" if row['TOTAL_AMOUNT'] else 'N/A',
                                'Items': row['ITEM_COUNT'] or 'N/A'
                            })
                        
                        st.dataframe(display_data, use_container_width=True)
                        
                        with st.expander("🔍 View SQL Query"):
                            st.code(query, language="sql")
                    elif error:
                        st.error(f"Error: {error}")
        
        with col2:
            if st.button("💾 Extract & Load into Table", key="load_invoices_table"):
                with st.spinner("Extracting and loading data into SUPPLIER_INVOICE_DETAILS table..."):
                    # Truncate table first
                    truncate_query = "TRUNCATE TABLE AI_FUNCTIONS_PLAYGROUND.DEMO.SUPPLIER_INVOICE_DETAILS"
                    session.sql(truncate_query).collect()
                    st.info("🗑️ Table truncated, now extracting and loading...")
                    
                    # Extract and insert
                    insert_query = """
                    INSERT INTO AI_FUNCTIONS_PLAYGROUND.DEMO.SUPPLIER_INVOICE_DETAILS (
                        file_name,
                        file_url,
                        invoice_number,
                        invoice_date,
                        supplier_name,
                        supplier_address,
                        supplier_phone,
                        customer_name,
                        customer_address,
                        customer_phone,
                        subtotal,
                        tax_amount,
                        total_amount,
                        payment_terms,
                        item_count,
                        extraction_date,
                        raw_json
                    )
                    WITH extracted_json AS (
                        SELECT 
                            RELATIVE_PATH as file_name,
                            BUILD_SCOPED_FILE_URL(@AI_FUNCTIONS_PLAYGROUND.DEMO.SUPPLIER_DOCUMENTS_STAGE, RELATIVE_PATH) as file_url,
                            AI_EXTRACT(
                                file => TO_FILE('@AI_FUNCTIONS_PLAYGROUND.DEMO.SUPPLIER_DOCUMENTS_STAGE', RELATIVE_PATH),
                                responseFormat => {
                                    'invoice_number': 'The invoice number (e.g., INV-1001)',
                                    'invoice_date': 'The invoice date in YYYY-MM-DD format',
                                    'supplier_name': 'The supplier/vendor company name',
                                    'supplier_address': 'The complete supplier address',
                                    'supplier_phone': 'The supplier phone number',
                                    'customer_name': 'The customer company name (should be Guac n Roll)',
                                    'customer_address': 'The complete customer address',
                                    'customer_phone': 'The customer phone number',
                                    'subtotal': 'The subtotal amount before tax as a number',
                                    'tax_amount': 'The tax amount as a number',
                                    'total_amount': 'The total invoice amount as a number',
                                    'payment_terms': 'The payment terms (e.g., Net 30 Days)',
                                    'item_count': 'The number of line items in the invoice'
                                }
                            ) AS extracted_json
                        FROM DIRECTORY(@AI_FUNCTIONS_PLAYGROUND.DEMO.SUPPLIER_DOCUMENTS_STAGE)
                        WHERE RELATIVE_PATH LIKE '%supplier_invoice%'
                    )
                    SELECT
                        file_name,
                        file_url,
                        extracted_json:response:invoice_number::string,
                        extracted_json:response:invoice_date::date,
                        extracted_json:response:supplier_name::string,
                        extracted_json:response:supplier_address::string,
                        extracted_json:response:supplier_phone::string,
                        extracted_json:response:customer_name::string,
                        extracted_json:response:customer_address::string,
                        extracted_json:response:customer_phone::string,
                        REPLACE(extracted_json:response:subtotal, '$', '')::float,
                        REPLACE(extracted_json:response:tax_amount, '$', '')::float,
                        REPLACE(extracted_json:response:total_amount, '$', '')::float,
                        extracted_json:response:payment_terms::string,
                        extracted_json:response:item_count::integer,
                        CURRENT_DATE as extraction_date,
                        extracted_json as raw_json
                    FROM extracted_json
                    """
                    
                    try:
                        result, error = execute_query(insert_query)
                        
                        if not error:
                            st.success("✅ Data loaded successfully into SUPPLIER_INVOICE_DETAILS table!")
                            
                            # Show row count
                            count_query = "SELECT COUNT(*) as cnt FROM AI_FUNCTIONS_PLAYGROUND.DEMO.SUPPLIER_INVOICE_DETAILS"
                            count_result, _ = execute_query(count_query)
                            if count_result:
                                st.info(f"📊 Total records loaded: {count_result[0]['CNT']}")
                            
                            # Show loaded data
                            display_query = """
                            SELECT 
                                invoice_number,
                                invoice_date,
                                supplier_name,
                                subtotal,
                                tax_amount,
                                total_amount,
                                payment_terms,
                                item_count
                            FROM AI_FUNCTIONS_PLAYGROUND.DEMO.SUPPLIER_INVOICE_DETAILS
                            ORDER BY invoice_date DESC
                            """
                            display_result, _ = execute_query(display_query)
                            if display_result:
                                st.markdown("**📊 Loaded Invoice Data:**")
                                st.dataframe(display_result, use_container_width=True)
                            
                            with st.expander("🔍 View INSERT SQL Query"):
                                st.code(insert_query, language="sql")
                        else:
                            st.error(f"Error loading data: {error}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    st.markdown("---")
    
    # Example 6: Invoice Analytics
    show_example_card(
        "Analyze Extracted Invoice Data",
        "Query the SUPPLIER_INVOICE_DETAILS table to gain business insights",
        6
    )
    
    # Check if table has data
    count_query = "SELECT COUNT(*) as cnt FROM AI_FUNCTIONS_PLAYGROUND.DEMO.SUPPLIER_INVOICE_DETAILS"
    count_result, _ = execute_query(count_query)
    table_count = count_result[0]['CNT'] if count_result else 0
    
    if table_count == 0:
        st.warning("⚠️ No data in SUPPLIER_INVOICE_DETAILS table. Please run Example 5 to extract and load invoices first.")
    else:
        st.success(f"✅ Analyzing {table_count} invoice(s) from the database")
        
        # Monthly Spending Trends
        st.markdown("#### 📅 Monthly Spending Trends")
        query2 = """
        SELECT 
            DATE_TRUNC('MONTH', invoice_date) as invoice_month,
            COUNT(*) as invoice_count,
            SUM(total_amount) as total_spent,
            AVG(total_amount) as avg_invoice,
            SUM(tax_amount) as total_tax
        FROM AI_FUNCTIONS_PLAYGROUND.DEMO.SUPPLIER_INVOICE_DETAILS
        GROUP BY DATE_TRUNC('MONTH', invoice_date)
        ORDER BY invoice_month DESC
        """
        result2, _ = execute_query(query2)
        if result2:
            st.dataframe(result2, use_container_width=True)
            with st.expander("🔍 View SQL"):
                st.code(query2, language="sql")
        
        st.markdown("---")
        st.markdown("#### 📋 All Invoice Details")
        query4 = """
        SELECT 
            invoice_number,
            invoice_date,
            supplier_name,
            supplier_phone,
            subtotal,
            tax_amount,
            total_amount,
            payment_terms,
            item_count,
            extraction_date
        FROM AI_FUNCTIONS_PLAYGROUND.DEMO.SUPPLIER_INVOICE_DETAILS
        ORDER BY invoice_date DESC
        """
        result4, _ = execute_query(query4)
        if result4:
            st.dataframe(result4, use_container_width=True)
            with st.expander("🔍 View SQL"):
                st.code(query4, language="sql")

# =============================================================================
# PAGE: AI_CLASSIFY
# =============================================================================

def page_ai_classify():
    show_header()
    
    st.title("🏷️ AI_CLASSIFY")
    
    multimodal_badge = show_multimodal_support(text=True, images=True, documents=False, audio=False)
    st.markdown(f"""
    **AI_CLASSIFY** classifies text and images into user-defined categories.
    Ideal for content categorization, ticket routing, and content moderation.
    
    {multimodal_badge} &nbsp;&nbsp; 📖 [View Documentation](https://docs.snowflake.com/en/sql-reference/functions/ai_classify)
    
    **💰 Cost (Table 6a):**
    - **Text:** 1.39 credits per 1M tokens
    - **Images:** 1.20 credits per 1K images (estimated)
    
    [View pricing details](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf)
    """, unsafe_allow_html=True)
    
    # Example 1: Classify Support Tickets
    show_example_card(
        "Auto-Classify Support Tickets",
        "Automatically categorize support tickets for routing",
        1
    )
    
    if st.button("Classify Tickets", key="classify_tickets"):
        with st.spinner("Classifying..."):
            query = """
                WITH classified_data
                AS
                (
                    SELECT 
                        ticket_id,
                        customer_name,
                        issue_description,
                        urgency,
                        AI_CLASSIFY(
                            issue_description,
                            [
                                {'label': 'Food Quality Issue', 'description': 'Complaints about food taste, temperature, freshness, or foreign objects'},
                                {'label': 'Service Issue', 'description': 'Problems with staff, wait times, or order accuracy'},
                                {'label': 'Payment Issue', 'description': 'Billing errors, overcharges, or payment system problems'},
                                {'label': 'Location Issue', 'description': 'Truck not at expected location or incorrect location information'},
                                {'label': 'Positive Feedback', 'description': 'Compliments, praise, or positive experiences'},
                                {'label': 'Feature Request', 'description': 'Suggestions for new menu items, services, or improvements'}
                            ]
                        ) as classification_json
                    FROM AI_FUNCTIONS_PLAYGROUND.DEMO.SUPPORT_TICKETS
                )
                    SELECT 
                        ticket_id,
                        customer_name,
                        issue_description,
                        urgency,
                        REPLACE(REPLACE(classification_json:labels::string, '["', ''), '"]', '') as ticket_classification
                    FROM classified_data;
            """
            result, error = execute_query(query)
            if result:
                st.dataframe(result, use_container_width=True)
                st.code(query, language="sql")
    
    st.markdown("---")
    
    # Example 2: Classify Reviews by Topic
    show_example_card(
        "Classify All Reviews by Topic",
        "Categorize all reviews to understand what customers talk about most",
        2
    )
    
    if st.button("Classify All Reviews", key="classify_reviews"):
        with st.spinner("Classifying all reviews..."):
            query = """
            WITH classified_reviews AS (
                SELECT 
                    review_id,
                    food_truck_name,
                    customer_name,
                    review_text,
                    rating,
                    AI_CLASSIFY(
                        review_text,
                        [
                            {'label': 'Food Quality'},
                            {'label': 'Portion Size'},
                            {'label': 'Customer Service'},
                            {'label': 'Value for Money'},
                            {'label': 'Wait Time'},
                            {'label': 'Atmosphere'}
                        ],
                        {'output_mode': 'multi'}
                    ) as topics_json
                FROM AI_FUNCTIONS_PLAYGROUND.DEMO.CUSTOMER_REVIEWS
            )
            SELECT 
                review_id,
                food_truck_name,
                customer_name,
                rating,
                REPLACE(REPLACE(REPLACE(topics_json:labels::string, '[', ''), ']', ''), '"', '') as topics,
                review_text
            FROM classified_reviews
            ORDER BY rating DESC
            """
            result, error = execute_query(query)
            if result:
                st.success(f"**✅ Classified {len(result)} reviews:**")
                
                # Create display dataframe
                display_df = []
                for row in result:
                    display_df.append({
                        'Review ID': row['REVIEW_ID'],
                        'Customer': row['CUSTOMER_NAME'],
                        'Food Truck': row['FOOD_TRUCK_NAME'],
                        'Rating': '⭐' * row['RATING'],
                        'Topics': row['TOPICS'] or 'N/A',
                        'Review': row['REVIEW_TEXT']
                    })
                
                st.dataframe(display_df, use_container_width=True)
                st.code(query, language="sql")
    
    st.markdown("---")
    
    # Example 3: Batch Classify All Food Images
    show_example_card(
        "Batch Classify All Menu Item Images",
        "Process all images at once using DIRECTORY to categorize by cuisine type",
        3
    )
    
    st.info("📸 **Batch Processing:** Classify all images in the stage with a single query")
    
    if st.button("Classify All Images", key="classify_all_images_btn"):
        with st.spinner("Analyzing all images in stage..."):
            query = """
                 WITH pictures AS (
                     SELECT
                         TO_FILE('@AI_FUNCTIONS_PLAYGROUND.DEMO.IMAGE_STAGE/' || RELATIVE_PATH) AS img,
                         RELATIVE_PATH as FILE_NAME
                     FROM DIRECTORY('@AI_FUNCTIONS_PLAYGROUND.DEMO.IMAGE_STAGE')
                 )
                 SELECT
                     p.FILE_NAME,
                     TO_VARCHAR(GET_PRESIGNED_URL(@AI_FUNCTIONS_PLAYGROUND.DEMO.IMAGE_STAGE, p.FILE_NAME, 3600)) as image_url,
                     AI_CLASSIFY(
                         p.img,
                         [
                             {'label': 'Asian Cuisine', 'description': 'Japanese, Chinese, Korean, Thai, Vietnamese food'},
                             {'label': 'Mexican Cuisine', 'description': 'Tacos, burritos, quesadillas, nachos'},
                             {'label': 'American Cuisine', 'description': 'Burgers, hot dogs, fries, BBQ'},
                             {'label': 'Middle Eastern Cuisine', 'description': 'Gyros, falafel, shawarma, kebabs'},
                             {'label': 'European Cuisine', 'description': 'French, Italian, German, British food'},
                             {'label': 'Dessert', 'description': 'Sweet treats, cakes, ice cream, pastries'}
                         ]
                     ) as cuisine_classification_json,
                     REPLACE(REPLACE(REPLACE(
                         AI_CLASSIFY(
                             p.img,
                             [
                                 {'label': 'Asian Cuisine', 'description': 'Japanese, Chinese, Korean, Thai, Vietnamese food'},
                                 {'label': 'Mexican Cuisine', 'description': 'Tacos, burritos, quesadillas, nachos'},
                                 {'label': 'American Cuisine', 'description': 'Burgers, hot dogs, fries, BBQ'},
                                 {'label': 'Middle Eastern Cuisine', 'description': 'Gyros, falafel, shawarma, kebabs'},
                                 {'label': 'European Cuisine', 'description': 'French, Italian, German, British food'},
                                 {'label': 'Dessert', 'description': 'Sweet treats, cakes, ice cream, pastries'}
                             ]
                         ):labels::string, '[', ''), ']', ''), '"', '') as cuisine_label
                 FROM pictures p
                 ORDER BY p.FILE_NAME;
             """
            result, error = execute_query(query)
            
            if result and len(result) > 0:
                st.success(f"**✅ Successfully classified {len(result)} images:**")
                
                # Display images in a grid with classifications
                cols = st.columns(5)
                for idx, row in enumerate(result):
                    with cols[idx % 5]:
                        # Display image
                        try:
                            if row['IMAGE_URL']:
                                st.image(row['IMAGE_URL'], use_container_width=True)
                            else:
                                st.info("📁 " + row['FILE_NAME'])
                        except:
                            st.info("📁 " + row['FILE_NAME'])
                        
                        # Display filename and classification
                        st.markdown(f"**{row['FILE_NAME']}**")
                        
                        # Get cleaned label
                        label = row['CUISINE_LABEL'] if 'CUISINE_LABEL' in row.as_dict() and row['CUISINE_LABEL'] else 'Unknown'
                        
                        # Color-coded badge based on cuisine type
                        if 'Asian Cuisine' in label:
                            badge_color = "#FF6B6B"
                        elif 'Mexican Cuisine' in label:
                            badge_color = "#4ECDC4"
                        elif 'American Cuisine' in label:
                            badge_color = "#45B7D1"
                        elif 'Middle Eastern Cuisine' in label:
                            badge_color = "#FFA07A"
                        elif 'European Cuisine' in label:
                            badge_color = "#98D8C8"
                        elif 'Dessert' in label:
                            badge_color = "#F7B731"
                        else:
                            badge_color = "#95A5A6"
                        
                        st.markdown(f"""
                        <div style='background-color: {badge_color}; 
                                    padding: 8px; 
                                    border-radius: 6px; 
                                    text-align: center;
                                    color: white;
                                    font-weight: 600;
                                    margin: 5px 0;'>
                            {label}
                        </div>
                        """, unsafe_allow_html=True)
                
                # Show query in expandable section
                with st.expander("🔍 View SQL Query"):
                    st.code(query, language="sql")
                    
            elif error:
                st.error(f"Error: {error}")
    
    st.markdown("---")
    
    # Example 4: Custom Text Classification
    show_example_card(
        "Custom Text Classification",
        "Try classifying your own text with custom categories",
        4
    )
    
    custom_text = st.text_area("Enter text to classify:", 
        "The vegan burger was incredibly delicious! I can't believe it's not real meat. Best plant-based option in the city!")
    
    categories = st.text_area("Enter categories (one per line):", 
        "Very Positive\nPositive\nNeutral\nNegative\nVery Negative")
    
    if st.button("Classify Text", key="custom_classify"):
        with st.spinner("Classifying..."):
            escaped_text = escape_sql_string(custom_text)
            cat_list = [{"label": c.strip()} for c in categories.split('\n') if c.strip()]
            query = f"""
            SELECT AI_CLASSIFY(
                '{escaped_text}',
                {str(cat_list)}
            ) as classification
            """
            result, error = execute_query(query)
            if result:
                st.success("**Classification Result:**")
                st.json(json.loads(result[0]['CLASSIFICATION']))
                st.code(query, language="sql")

# =============================================================================
# PAGE: AI_FILTER
# =============================================================================

def page_ai_filter():
    show_header()
    
    st.title("🎯 AI_FILTER")
    
    multimodal_badge = show_multimodal_support(text=True, images=True, documents=False, audio=False)
    st.markdown(f"""
    **AI_FILTER** returns True/False for yes-or-no questions about text or images.
    Perfect for filtering data in WHERE clauses using natural language.
    
    {multimodal_badge} &nbsp;&nbsp; 📖 [View Documentation](https://docs.snowflake.com/en/sql-reference/functions/ai_filter)
    
    **💰 Cost (Table 6a):**
    - **Text:** 1.39 credits per 1M tokens
    - **Images:** 1.20 credits per 1K images (estimated)
    
    [View pricing details](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf)
    """, unsafe_allow_html=True)
    
    # Example 1: Filter Reviews
    show_example_card(
        "Filter Reviews Using Natural Language",
        "Use AI_FILTER to find reviews matching specific criteria",
        1
    )
    
    # Pre-defined filter options that will return results
    review_filters = [
        "Does this review mention specific food items?",
        "Does this review express positive sentiment?",
        "Does this review mention the customer will return or recommend?",
        "Does this review mention price or value?",
        "Does this review mention wait time or service speed?"
    ]
    
    filter_question = st.selectbox("Select filter question:", review_filters)
    
    if st.button("Apply Filter", key="filter_reviews"):
        with st.spinner("Filtering reviews..."):
            escaped_question = escape_sql_string(filter_question)
            query = f"""
            SELECT 
                review_id,
                customer_name,
                food_truck_name,
                rating,
                review_text
            FROM AI_FUNCTIONS_PLAYGROUND.DEMO.CUSTOMER_REVIEWS
            WHERE AI_FILTER(CONCAT('{escaped_question}', review_text)) = TRUE
            """
            result, error = execute_query(query)
            if result and len(result) > 0:
                st.success(f"**✅ Found {len(result)} matching reviews:**")
                
                # Create display dataframe
                display_df = []
                for row in result:
                    display_df.append({
                        'Review ID': row['REVIEW_ID'],
                        'Customer': row['CUSTOMER_NAME'],
                        'Food Truck': row['FOOD_TRUCK_NAME'],
                        'Rating': '⭐' * row['RATING'],
                        'Review': row['REVIEW_TEXT']
                    })
                
                st.dataframe(display_df, use_container_width=True)
                st.code(query, language="sql")
            else:
                st.info("No reviews matched the filter criteria")
    
    st.markdown("---")
    
    # Example 2: Filter Support Tickets
    show_example_card(
        "Filter Support Tickets Using Natural Language",
        "Find tickets matching specific criteria or issues",
        2
    )
    
    ticket_filters = [
        "Does this mention food or menu items?",
        "Does this mention payment or pricing?",
        "Is this a complaint or negative feedback?",
        "Does this mention location or finding the truck?",
        "Is this positive feedback or a compliment?"
    ]
    
    selected_filter = st.selectbox("Select filter:", ticket_filters)
    
    if st.button("Filter Tickets", key="filter_tickets"):
        with st.spinner("Filtering tickets..."):
            escaped_filter = escape_sql_string(selected_filter)
            query = f"""
            SELECT 
                ticket_id,
                customer_name,
                urgency,
                status,
                issue_description
            FROM AI_FUNCTIONS_PLAYGROUND.DEMO.SUPPORT_TICKETS
            WHERE AI_FILTER(CONCAT('{escaped_filter}', issue_description)) = TRUE
            """
            result, error = execute_query(query)
            if result and len(result) > 0:
                st.success(f"**✅ Found {len(result)} matching tickets:**")
                
                # Create display dataframe
                display_df = []
                for row in result:
                    display_df.append({
                        'Ticket ID': row['TICKET_ID'],
                        'Customer': row['CUSTOMER_NAME'],
                        'Urgency': row['URGENCY'],
                        'Status': row['STATUS'],
                        'Issue': row['ISSUE_DESCRIPTION']
                    })
                
                st.dataframe(display_df, use_container_width=True)
                st.code(query, language="sql")
            else:
                st.info("No tickets matched the filter criteria")
    
    st.markdown("---")
    
    # Example 3: Filter Food Images
    show_example_card(
        "Filter Food Images by Visual Criteria",
        "Use AI_FILTER with DIRECTORY to find images matching specific visual characteristics",
        3
    )
    
    st.info("📸 **Working with Images:** Uses DIRECTORY() to scan all images in the stage and filter with natural language")
    
    # Pre-defined filter options
    filter_options = [
        "Does this image show a dish served in a bowl?",
        "Does this image contain meat?",
        "Is this a dessert or sweet item?",
        "Does this image show a wrapped or handheld food item?",
        "Does this food appear to have vegetables?"
    ]
    
    # Allow custom or predefined question
    filter_type = st.radio("Filter type:", ["Predefined", "Custom"], horizontal=True, key="filter_type")
    
    if filter_type == "Predefined":
        image_filter_question = st.selectbox("Select filter question:", filter_options, key="img_filter_q")
    else:
        image_filter_question = st.text_input("Enter your custom filter question:", 
                                               "Does this image show food with sauce?", 
                                               key="custom_filter_q")
    
    if st.button("Filter Images", key="filter_images"):
        with st.spinner("Scanning and filtering all images in stage..."):
            escaped_question = escape_sql_string(image_filter_question)
            
            # Use DIRECTORY syntax as provided by user
            query = f"""
            WITH pictures AS (
                SELECT
                    TO_FILE('@AI_FUNCTIONS_PLAYGROUND.DEMO.IMAGE_STAGE/' || RELATIVE_PATH) AS img,
                    RELATIVE_PATH as file_name
                FROM DIRECTORY('@AI_FUNCTIONS_PLAYGROUND.DEMO.IMAGE_STAGE')
            )
            SELECT
                file_name,
                TO_VARCHAR(GET_PRESIGNED_URL(@AI_FUNCTIONS_PLAYGROUND.DEMO.IMAGE_STAGE, file_name, 3600)) as image_url
            FROM pictures
            WHERE AI_FILTER('{escaped_question}', img)
            """
            
            result, error = execute_query(query)
            
            if result and len(result) > 0:
                st.success(f"**✅ Found {len(result)} matching images:**")
                
                # Display images in a grid (4 columns for smaller images)
                cols = st.columns(4)
                for idx, row in enumerate(result):
                    with cols[idx % 4]:
                        st.markdown(f"**{row['FILE_NAME']}**")
                        try:
                            if row['IMAGE_URL']:
                                st.image(row['IMAGE_URL'], use_container_width=True)
                            else:
                                st.info("📁 " + row['FILE_NAME'])
                        except Exception as e:
                            st.info("📁 " + row['FILE_NAME'])
                
                st.markdown("**🔍 SQL Query Used:**")
                st.code(query, language="sql")
                
            elif result:
                st.warning("❌ No images matched the filter criteria")
                st.markdown("**🔍 SQL Query Used:**")
                st.code(query, language="sql")
            elif error:
                st.error(f"Error: {error}")

# =============================================================================
# PAGE: AI_SIMILARITY
# =============================================================================

def page_ai_similarity():
    show_header()
    
    st.title("🔗 AI_SIMILARITY")
    
    multimodal_badge = show_multimodal_support(text=True, images=True, documents=False, audio=False)
    st.markdown(f"""
    **AI_SIMILARITY** calculates cosine similarity between two texts and images without explicitly creating embeddings.
    Perfect for finding similar content, duplicate detection, and recommendation systems.
    
    {multimodal_badge} &nbsp;&nbsp; 📖 [View Documentation](https://docs.snowflake.com/en/sql-reference/functions/ai_similarity)
    
    **💰 Cost:** Computed from embeddings (see AI_EMBED pricing in Table 6a)
    - Text embedding models: 0.03-0.07 credits per 1M tokens
    - Image embeddings: 0.004 credits per image
    
    [View pricing details](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf)
    """, unsafe_allow_html=True)
    
    # Example 1: Find Similar Reviews
    show_example_card(
        "Find Similar Customer Reviews",
        "Compare reviews to find similar customer experiences across entire dataset",
        1
    )
    
    result, _ = execute_query("SELECT review_id, customer_name, review_text FROM AI_FUNCTIONS_PLAYGROUND.DEMO.CUSTOMER_REVIEWS")
    if result:
        review_options = {f"{r['CUSTOMER_NAME']}: {r['REVIEW_TEXT'][:50]}...": r['REVIEW_TEXT'] 
                         for r in result}
        selected_review = st.selectbox("Select a reference review:", list(review_options.keys()))
        
        if st.button("Find Similar Reviews", key="similar_reviews"):
            with st.spinner("Calculating similarity across all reviews..."):
                reference_text = escape_sql_string(review_options[selected_review])
                query = f"""
                SELECT 
                    review_id,
                    customer_name,
                    food_truck_name,
                    rating,
                    AI_SIMILARITY(
                        '{reference_text}',
                        review_text
                    ) as similarity_score,
                    review_text
                FROM AI_FUNCTIONS_PLAYGROUND.DEMO.CUSTOMER_REVIEWS
                WHERE review_text != '{reference_text}'
                ORDER BY similarity_score DESC
                """
                result, error = execute_query(query)
                if result:
                    st.success(f"**✅ Found {len(result)} reviews ranked by similarity:**")
                    
                    st.markdown("**📝 Reference Review:**")
                    st.info(review_options[selected_review])
                    
                    st.markdown("**🔍 Similar Reviews:**")
                    
                    # Create display dataframe
                    display_df = []
                    for row in result:
                        display_df.append({
                            'Review ID': row['REVIEW_ID'],
                            'Similarity': f"{row['SIMILARITY_SCORE']:.4f}",
                            'Customer': row['CUSTOMER_NAME'],
                            'Food Truck': row['FOOD_TRUCK_NAME'],
                            'Rating': '⭐' * row['RATING'],
                            'Review': row['REVIEW_TEXT']
                        })
                    
                    st.dataframe(display_df, use_container_width=True)
                    st.code(query, language="sql")
    
    st.markdown("---")
    
    # Example 2: Duplicate Support Ticket Detection
    show_example_card(
        "Detect Duplicate Support Tickets",
        "Find similar support tickets to identify recurring issues across entire dataset",
        2
    )
    
    if st.button("Find Similar Tickets", key="similar_tickets"):
        with st.spinner("Analyzing all ticket pairs..."):
            query = """
            WITH ticket_pairs AS (
                SELECT 
                    t1.ticket_id as ticket1_id,
                    t1.customer_name as customer1,
                    t1.issue_description as issue1,
                    t2.ticket_id as ticket2_id,
                    t2.customer_name as customer2,
                    t2.issue_description as issue2,
                    AI_SIMILARITY(t1.issue_description, t2.issue_description) as similarity
                FROM AI_FUNCTIONS_PLAYGROUND.DEMO.SUPPORT_TICKETS t1
                JOIN AI_FUNCTIONS_PLAYGROUND.DEMO.SUPPORT_TICKETS t2 
                    ON t1.ticket_id < t2.ticket_id
            )
            SELECT 
                ticket1_id,
                customer1,
                ticket2_id,
                customer2,
                similarity,
                issue1,
                issue2
            FROM ticket_pairs
            WHERE similarity > 0.7
            ORDER BY similarity DESC
            """
            result, error = execute_query(query)
            if result:
                st.success(f"**✅ Found {len(result)} similar ticket pairs:**")
                for row in result:
                    with st.expander(f"Similarity: {row['SIMILARITY']:.3f} - Ticket #{row['TICKET1_ID']} & #{row['TICKET2_ID']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**Ticket #{row['TICKET1_ID']} ({row['CUSTOMER1']})**")
                            st.write(row['ISSUE1'])
                        with col2:
                            st.markdown(f"**Ticket #{row['TICKET2_ID']} ({row['CUSTOMER2']})**")
                            st.write(row['ISSUE2'])
                st.code(query, language="sql")
    
    st.markdown("---")
    
    # Example 3: Find Similar Food Images
    show_example_card(
        "Find Similar Food Images",
        "Use visual similarity to find similar-looking menu items",
        3
    )
    
    st.info("📸 **Working with Images:** Compare food images to find visually similar items")
    
    # Get list of available images from stage
    images_query = "SELECT RELATIVE_PATH FROM DIRECTORY('@AI_FUNCTIONS_PLAYGROUND.DEMO.IMAGE_STAGE') ORDER BY RELATIVE_PATH"
    images_result, _ = execute_query(images_query)
    
    if images_result:
        available_images = [row['RELATIVE_PATH'] for row in images_result]
        reference_img = st.selectbox("Select reference image:", available_images, key="ref_img")
        
        # Display reference image thumbnail
        st.markdown("**🖼️ Reference Image:**")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            st.write("")  # Spacer
        with col2:
            try:
                ref_url_query = f"SELECT TO_VARCHAR(GET_PRESIGNED_URL(@AI_FUNCTIONS_PLAYGROUND.DEMO.IMAGE_STAGE, '{reference_img}', 3600)) as img_url"
                ref_result, _ = execute_query(ref_url_query)
                if ref_result and ref_result[0]['IMG_URL']:
                    st.image(ref_result[0]['IMG_URL'], caption=f"Reference: {reference_img}", use_container_width=True)
                else:
                    st.info(f"📁 {reference_img}")
            except Exception as e:
                st.info(f"📁 {reference_img}")
        with col3:
            st.write("")  # Spacer
        
        if st.button("Find Similar Images", key="similar_images"):
            with st.spinner("Analyzing images..."):
                query = f"""
                WITH all_images AS (
                    SELECT
                        RELATIVE_PATH as file_name,
                        TO_FILE('@AI_FUNCTIONS_PLAYGROUND.DEMO.IMAGE_STAGE/' || RELATIVE_PATH) AS img
                    FROM DIRECTORY('@AI_FUNCTIONS_PLAYGROUND.DEMO.IMAGE_STAGE')
                    WHERE RELATIVE_PATH != '{reference_img}'
                )
                SELECT 
                    file_name,
                    TO_VARCHAR(GET_PRESIGNED_URL(@AI_FUNCTIONS_PLAYGROUND.DEMO.IMAGE_STAGE, file_name, 3600)) as image_url,
                    AI_SIMILARITY(
                        TO_FILE('@AI_FUNCTIONS_PLAYGROUND.DEMO.IMAGE_STAGE/{reference_img}'),
                        img
                    ) as similarity_score
                FROM all_images
                ORDER BY similarity_score DESC
                LIMIT 3
                """
                result, error = execute_query(query)
                
                if result and len(result) > 0:
                    st.success(f"**🎯 Top 3 most similar images to {reference_img}:**")
                    
                    # Display top 3 in columns with thumbnails
                    col_spacer1, col1, col2, col3, col_spacer2 = st.columns([0.5, 1, 1, 1, 0.5])
                    cols = [col1, col2, col3]
                    for i, row in enumerate(result):
                        with cols[i]:
                            st.markdown(f"**#{i+1}: Similarity {row['SIMILARITY_SCORE']:.4f}**")
                            try:
                                if row['IMAGE_URL']:
                                    st.image(row['IMAGE_URL'], caption=row['FILE_NAME'], use_container_width=True)
                                else:
                                    st.info(f"📁 {row['FILE_NAME']}")
                            except Exception as e:
                                st.info(f"📁 {row['FILE_NAME']}")
                    
                    st.code(query, language="sql")
                elif error:
                    st.error(f"Error: {error}")
    
    st.markdown("---")
    
    # Example 4: Custom Text Similarity Comparison
    show_example_card(
        "Custom Text Similarity Comparison",
        "Compare any two texts to see how similar they are",
        4
    )
    
    text1 = st.text_area("Text 1:", "The food was cold and tasted terrible. Very disappointed.")
    text2 = st.text_area("Text 2:", "My meal arrived cold and the taste was awful. Won't return.")
    
    if st.button("Calculate Similarity", key="custom_similarity"):
        with st.spinner("Calculating..."):
            escaped_text1 = escape_sql_string(text1)
            escaped_text2 = escape_sql_string(text2)
            query = f"""
            SELECT AI_SIMILARITY(
                '{escaped_text1}',
                '{escaped_text2}'
            ) as similarity_score
            """
            result, error = execute_query(query)
            if result:
                score = result[0]['SIMILARITY_SCORE']
                st.metric("Similarity Score", f"{score:.4f}")
                
                if score > 0.8:
                    st.success("✅ Very similar texts!")
                elif score > 0.6:
                    st.info("🔵 Moderately similar texts")
                elif score > 0.4:
                    st.warning("⚠️ Somewhat similar texts")
                else:
                    st.error("❌ Very different texts")
                
                st.code(query, language="sql")

# =============================================================================
# PAGE: AI_REDACT
# =============================================================================

def page_ai_redact():
    show_header()
    
    st.title("🔒 AI_REDACT")
    
    multimodal_badge = show_multimodal_support(text=True, images=False, documents=False, audio=False)
    st.markdown(f"""
    **AI_REDACT** redacts personally identifiable information (PII) from unstructured text data.
    Perfect for data privacy compliance, anonymization, and secure data sharing.
    
    {multimodal_badge} &nbsp;&nbsp; 📖 [View Documentation](https://docs.snowflake.com/en/sql-reference/functions/ai_redact)
    
    **💰 Cost:** 0.63 credits per 1M tokens (Table 6a)  
    [View pricing details](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf)
    
    **🔍 Detected PII Categories:**  
    NAME, EMAIL, PHONE_NUMBER, DATE_OF_BIRTH, GENDER, AGE, ADDRESS, NATIONAL_ID, PASSPORT, TAX_IDENTIFIER, PAYMENT_CARD_DATA, DRIVERS_LICENSE, IP_ADDRESS
    """, unsafe_allow_html=True)
    
    # Example 1: Redact All PII from Support Tickets
    show_example_card(
        "Redact All PII from Support Tickets",
        "Automatically redact all types of PII from customer support communications",
        1
    )
    
    if st.button("Redact All PII", key="redact_all"):
        with st.spinner("Redacting PII from support tickets..."):
            query = """
            SELECT 
                ticket_id,
                customer_name,
                food_truck_name,
                issue_description as original_text,
                AI_REDACT(issue_description) as redacted_text
            FROM AI_FUNCTIONS_PLAYGROUND.DEMO.SUPPORT_TICKETS_PII
            LIMIT 5
            """
            result, error = execute_query(query)
            if result:
                st.success(f"**✅ Redacted PII from {len(result)} support tickets:**")
                
                for row in result:
                    with st.expander(f"Ticket #{row['TICKET_ID']} - {row['CUSTOMER_NAME']} ({row['FOOD_TRUCK_NAME']})"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("**Original:**")
                            st.write(row['ORIGINAL_TEXT'])
                        with col2:
                            st.markdown("**Redacted:**")
                            st.write(row['REDACTED_TEXT'])
                
                st.code(query, language="sql")
            elif error:
                st.error(f"Error: {error}")
    
    st.markdown("---")
    
    # Example 2: Redact Specific PII Categories
    show_example_card(
        "Redact Specific PII Categories",
        "Choose which types of PII to redact using category filters",
        2
    )
    
    st.info("Select specific PII categories to redact while preserving other information")
    
    # Multi-select for PII categories
    pii_categories = st.multiselect(
        "Select PII categories to redact:",
        ["NAME", "EMAIL", "PHONE_NUMBER", "DATE_OF_BIRTH", "GENDER", "AGE", "ADDRESS", "NATIONAL_ID", "PASSPORT", "TAX_IDENTIFIER", "PAYMENT_CARD_DATA", "DRIVERS_LICENSE", "IP_ADDRESS"],
        default=["NAME", "EMAIL"],
        key="pii_categories"
    )
    
    if st.button("Redact Selected Categories", key="redact_specific"):
        if pii_categories:
            with st.spinner(f"Redacting {', '.join(pii_categories)} from support tickets..."):
                categories_array = str(pii_categories).replace("'", "''")
                query = f"""
                SELECT 
                    ticket_id,
                    customer_name,
                    food_truck_name,
                    issue_description as original_text,
                    AI_REDACT(issue_description, {pii_categories}) as redacted_text
                FROM AI_FUNCTIONS_PLAYGROUND.DEMO.SUPPORT_TICKETS_PII
                LIMIT 5
                """
                result, error = execute_query(query)
                if result:
                    st.success(f"**✅ Redacted {', '.join(pii_categories)} from {len(result)} support tickets:**")
                    
                    for row in result:
                        with st.expander(f"Ticket #{row['TICKET_ID']} - {row['CUSTOMER_NAME']} ({row['FOOD_TRUCK_NAME']})"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown("**Original:**")
                                st.write(row['ORIGINAL_TEXT'])
                            with col2:
                                st.markdown("**Redacted:**")
                                st.write(row['REDACTED_TEXT'])
                    
                    st.code(query, language="sql")
                elif error:
                    st.error(f"Error: {error}")
        else:
            st.warning("Please select at least one PII category to redact")
    
    st.markdown("---")
    
    # Example 3: Custom Text Redaction
    show_example_card(
        "Custom Text Redaction",
        "Test AI_REDACT on your own text",
        3
    )
    
    custom_text = st.text_area(
        "Enter text containing PII:",
        "My name is John Smith and my email is john.smith@example.com. You can reach me at 555-123-4567. My SSN is 123-45-6789.",
        height=100
    )
    
    col1, col2 = st.columns(2)
    with col1:
        redact_all_categories = st.checkbox("Redact all PII categories", value=True, key="custom_redact_all")
    
    with col2:
        if not redact_all_categories:
            custom_categories = st.multiselect(
                "Select categories:",
                ["NAME", "EMAIL", "PHONE_NUMBER", "NATIONAL_ID"],
                default=["EMAIL"],
                key="custom_categories"
            )
    
    if st.button("Redact Custom Text", key="redact_custom"):
        with st.spinner("Redacting PII..."):
            escaped_text = escape_sql_string(custom_text)
            
            if redact_all_categories:
                query = f"""
                SELECT AI_REDACT('{escaped_text}') as redacted_text
                """
            else:
                query = f"""
                SELECT AI_REDACT('{escaped_text}', {custom_categories}) as redacted_text
                """
            
            result, error = execute_query(query)
            if result:
                st.success("**Redaction Result:**")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Original:**")
                    st.info(custom_text)
                with col2:
                    st.markdown("**Redacted:**")
                    st.success(result[0]['REDACTED_TEXT'])
                
                st.code(query, language="sql")
            elif error:
                st.error(f"Error: {error}")
    
    st.markdown("---")
    
    st.markdown("""
    ### 🎯 Key Use Cases
    
    1. **Data Privacy Compliance**: Redact PII before sharing data with partners or analysts
    2. **Secure Analytics**: Anonymize customer data for ML training or testing
    3. **Audit & Logging**: Remove sensitive information from logs and audit trails
    4. **Public Datasets**: Create shareable datasets without exposing personal information
    5. **Cross-Border Data**: Redact PII to comply with regional data protection laws
    
    ### 📋 Supported PII Categories
    
    AI_REDACT automatically detects and redacts:
    - **NAME**: Person names (also identifies FIRST_NAME, MIDDLE_NAME, LAST_NAME)
    - **EMAIL**: Email addresses
    - **PHONE_NUMBER**: Phone numbers in various formats
    - **DATE_OF_BIRTH**: Birth dates
    - **GENDER**: Gender identifiers (MALE, FEMALE, NONBINARY)
    - **AGE**: Age values
    - **ADDRESS**: Physical addresses (includes STREET_ADDRESS, POSTAL_CODE, CITY, etc.)
    - **NATIONAL_ID**: National ID numbers (US Social Security Numbers)
    - **PASSPORT**: Passport numbers (US, UK, CA)
    - **TAX_IDENTIFIER**: Tax identification numbers (ITNs)
    - **PAYMENT_CARD_DATA**: Payment card information (includes PAYMENT_CARD_NUMBER, EXPIRATION_DATE, CVV)
    - **DRIVERS_LICENSE**: Driver's license numbers (US, UK, CA)
    - **IP_ADDRESS**: IP addresses
    
    ### 💡 Pro Tips
    
    - Use category-specific redaction when you need to preserve some types of information
    - Combine with other AI Functions functions for advanced workflows (e.g., sentiment analysis on redacted text)
    - Consider using AI_REDACT as part of your ETL pipeline for automatic PII removal
    """)

# =============================================================================
# PAGE: AI_TRANSCRIBE
# =============================================================================

def page_ai_transcribe():
    show_header()
    
    st.title("🎙️ AI_TRANSCRIBE")
    
    multimodal_badge = show_multimodal_support(text=False, images=False, documents=False, audio=True)
    st.markdown(f"""
    **AI_TRANSCRIBE** converts audio and video files to text with timestamps and speaker identification.
    Supports 31 languages and processes files up to 2 hours long.
    
    {multimodal_badge} &nbsp;&nbsp; 📖 [View Documentation](https://docs.snowflake.com/en/sql-reference/functions/ai_transcribe)
    
    **💰 Cost:** 1.30 credits per 1M tokens (Table 6a)  
    [View pricing details](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf)
    """, unsafe_allow_html=True)
    
    # Available audio files
    audio_files = {
        "call_001_order_issue.wav": "Order Issue - Customer reporting wrong items received",
        "call_002_food_quality.wav": "Food Quality - Complaint about cold food",
        "call_003_allergy_concern.wav": "Allergy Concern - Customer asking about ingredients",
        "call_004_location_issue.wav": "Location Issue - Truck not at expected location",
        "call_005_payment_error.wav": "Payment Error - Billing problem",
        "call_006_positive_feedback.wav": "Positive Feedback - Customer compliment",
        "call_007_catering_inquiry.wav": "Catering Inquiry - Event catering question",
        "call_008_delivery_delay.wav": "Delivery Delay - Order running late",
        "call_009_menu_question.wav": "Menu Question - Asking about ingredients",
        "call_010_refund_request.wav": "Refund Request - Customer requesting refund"
    }
    
    # Example 1: Basic Transcription with Audio Player
    show_example_card(
        "Transcribe Customer Service Call",
        "Convert audio to text and listen to the recording",
        1
    )
    
    selected_audio = st.selectbox(
        "Select a call recording:",
        list(audio_files.keys()),
        format_func=lambda x: f"{x.replace('.wav', '').replace('call_', 'Call #').replace('_', ' ').title()} - {audio_files[x]}"
    )
    
    st.info(f"📞 **Selected Call:** {audio_files[selected_audio]}")
    
    # Audio player - get scoped URL from stage
    try:
        # Get presigned URL for audio playback
        url_query = f"SELECT GET_PRESIGNED_URL(@AI_FUNCTIONS_PLAYGROUND.DEMO.AUDIO_STAGE, '{selected_audio}', 3600) as audio_url"
        url_result, _ = execute_query(url_query)
        if url_result and url_result[0]['AUDIO_URL']:
            audio_url = url_result[0]['AUDIO_URL']
            st.audio(audio_url, format='audio/wav')
        else:
            st.caption("🎵 Audio player unavailable - using BUILD_SCOPED_FILE_URL as fallback")
            # Fallback to scoped file URL
            scoped_query = f"SELECT BUILD_SCOPED_FILE_URL(@AI_FUNCTIONS_PLAYGROUND.DEMO.AUDIO_STAGE, '{selected_audio}') as audio_url"
            scoped_result, _ = execute_query(scoped_query)
            if scoped_result and scoped_result[0]['AUDIO_URL']:
                st.audio(scoped_result[0]['AUDIO_URL'], format='audio/wav')
    except Exception as e:
        st.caption(f"🎵 Audio player unavailable: {str(e)}")
    
    if st.button("Transcribe Audio", key="transcribe_basic"):
        with st.spinner("Transcribing audio..."):
            query = f"""
            SELECT 
                '{selected_audio}' as audio_file,
                AI_TRANSCRIBE(
                    TO_FILE('@AI_FUNCTIONS_PLAYGROUND.DEMO.AUDIO_STAGE/{selected_audio}')
                ) as transcription
            """
            result, error = execute_query(query)
            if result:
                transcription_data = json.loads(result[0]['TRANSCRIPTION'])
                st.success("**Transcription Complete!**")
                st.markdown("**Transcribed Text:**")
                st.info(transcription_data.get('text', 'No text found'))
                st.caption(f"Language: {transcription_data.get('language', 'unknown').upper()}")
                st.code(query, language="sql")
            elif error:
                st.error(f"Error: {error}")
    
    st.markdown("---")
    
    # Example 2: Transcription + Sentiment Analysis
    show_example_card(
        "Post-Processing: Transcribe + Sentiment Analysis",
        "Transcribe call and immediately analyze sentiment",
        2
    )
    
    selected_audio2 = st.selectbox(
        "Select a call recording:",
        list(audio_files.keys()),
        format_func=lambda x: f"{x.replace('.wav', '').replace('call_', 'Call #').replace('_', ' ').title()}",
        key="audio2"
    )
    
    if st.button("Transcribe & Analyze Sentiment", key="transcribe_sentiment"):
        with st.spinner("Transcribing and analyzing..."):
            query = f"""
            WITH transcription AS (
                SELECT 
                    '{selected_audio2}' as audio_file,
                    AI_TRANSCRIBE(
                        TO_FILE('@AI_FUNCTIONS_PLAYGROUND.DEMO.AUDIO_STAGE/{selected_audio2}')
                    ) as transcript_json
            )
            SELECT 
                audio_file,
                transcript_json:text::STRING as transcribed_text,
                SNOWFLAKE.CORTEX.SENTIMENT(transcript_json:text::STRING) as sentiment_score,
                CASE 
                    WHEN SNOWFLAKE.CORTEX.SENTIMENT(transcript_json:text::STRING) > 0.3 THEN 'Positive 😊'
                    WHEN SNOWFLAKE.CORTEX.SENTIMENT(transcript_json:text::STRING) < -0.3 THEN 'Negative 😟'
                    ELSE 'Neutral 😐'
                END as sentiment_category
            FROM transcription
            """
            result, error = execute_query(query)
            if result:
                st.success("**Analysis Complete!**")
                st.markdown("**Transcribed Text:**")
                st.write(result[0]['TRANSCRIBED_TEXT'])
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Sentiment Score", f"{result[0]['SENTIMENT_SCORE']:.3f}")
                with col2:
                    st.metric("Category", result[0]['SENTIMENT_CATEGORY'])
                
                st.code(query, language="sql")
            elif error:
                st.error(f"Error: {error}")
    
    st.markdown("---")
    
    # Example 3: Transcription + AI_COMPLETE Response
    show_example_card(
        "Post-Processing: Transcribe + Generate Response",
        "Transcribe call and generate an appropriate customer service response",
        3
    )
    
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_audio3 = st.selectbox(
            "Select a call recording:",
            list(audio_files.keys()),
            format_func=lambda x: f"{x.replace('.wav', '').replace('call_', 'Call #').replace('_', ' ').title()}",
            key="audio3"
        )
    with col2:
        model_ex3_transcribe = st.selectbox("Model:", AI_COMPLETE_MODELS, key="model_transcribe_ex3")
    
    if st.button("Transcribe & Generate Response", key="transcribe_complete"):
        with st.spinner("Transcribing and generating response..."):
            query = f"""
            WITH transcription AS (
                SELECT 
                    AI_TRANSCRIBE(
                        TO_FILE('@AI_FUNCTIONS_PLAYGROUND.DEMO.AUDIO_STAGE/{selected_audio3}')
                    ) as transcript_json
            )
            SELECT 
                transcript_json:text::STRING as transcribed_text,
                AI_COMPLETE(
                    '{model_ex3_transcribe}',
                    'You are a professional customer service agent for Tasty Bytes food trucks. Based on this transcribed customer call, write a brief, empathetic response addressing their concerns: ' || transcript_json:text::STRING,
                    {{'temperature': 0.5}}
                ) as suggested_response
            FROM transcription
            """
            result, error = execute_query(query)
            if result:
                st.success("**Response Generated!**")
                
                with st.expander("📝 View Transcription"):
                    st.write(result[0]['TRANSCRIBED_TEXT'])
                
                st.markdown("**💬 Suggested Response:**")
                st.markdown(result[0]['SUGGESTED_RESPONSE'])
                
                st.code(query, language="sql")
            elif error:
                st.error(f"Error: {error}")
    
    st.markdown("---")
    
    # Example 4: Comprehensive Call Analysis Dashboard
    show_example_card(
        "Comprehensive Call Analysis Dashboard",
        "Batch process calls with transcription, summary, sentiment, and action recommendations",
        4
    )
    
    st.info("🎯 **Complete Analysis Pipeline:** Transcribe → Summarize → Analyze Sentiment → Generate Actions")
    
    # Select number of calls and model
    col1, col2 = st.columns([3, 1])
    with col1:
        num_calls = st.slider("Number of calls to analyze:", min_value=2, max_value=5, value=3, key="num_calls_dashboard")
    with col2:
        model_ex4_transcribe = st.selectbox("Model:", AI_COMPLETE_MODELS, key="model_transcribe_ex4")
    
    if st.button("Analyze Calls", key="analyze_calls_dashboard"):
        with st.spinner(f"Processing {num_calls} call recordings..."):
            # Get subset of audio files
            audio_list = list(audio_files.keys())[:num_calls]
            
            # Build comprehensive analysis query
            union_parts = []
            for audio in audio_list:
                union_parts.append(f"""
                SELECT 
                    '{audio}' as filename,
                    '{audio_files[audio]}' as call_type,
                    AI_TRANSCRIBE(TO_FILE('@AI_FUNCTIONS_PLAYGROUND.DEMO.AUDIO_STAGE/{audio}')) as transcript_json
                """)
            
            union_query = " UNION ALL ".join(union_parts)
            
            query = f"""
            WITH transcriptions AS (
                {union_query}
            ),
            analyzed_calls AS (
                SELECT 
                    filename,
                    call_type,
                    transcript_json:text::STRING as transcribed_text,
                    AI_COMPLETE(
                        '{model_ex4_transcribe}',
                        'Summarize this customer service call in 2-3 sentences: ' || transcript_json:text::STRING,
                        {{'temperature': 0.3}}
                    ) as call_summary,
                    SNOWFLAKE.CORTEX.SENTIMENT(transcript_json:text::STRING) as sentiment_score,
                    CASE 
                        WHEN SNOWFLAKE.CORTEX.SENTIMENT(transcript_json:text::STRING) > 0.3 THEN 'Positive 😊'
                        WHEN SNOWFLAKE.CORTEX.SENTIMENT(transcript_json:text::STRING) < -0.3 THEN 'Negative 😟'
                        ELSE 'Neutral 😐'
                    END as sentiment_category,
                    AI_COMPLETE(
                        '{model_ex4_transcribe}',
                        'Based on this customer service call transcription, provide exactly 3 specific recommended actions. Format as a numbered list (1., 2., 3.): ' || transcript_json:text::STRING,
                        {{'temperature': 0.4}}
                    ) as recommended_actions
                FROM transcriptions
            )
            SELECT * FROM analyzed_calls
            """
            
            result, error = execute_query(query)
            
            if result:
                st.success(f"**✅ Successfully analyzed {len(result)} calls!**")
                
                # Display each call in a card layout
                for idx, row in enumerate(result, 1):
                    st.markdown(f"### 📞 Call {idx}: {row['CALL_TYPE']}")
                    
                    # Create 3-column layout for key metrics
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.markdown(f"**📁 File:** `{row['FILENAME']}`")
                    with col2:
                        st.metric("Sentiment Score", f"{row['SENTIMENT_SCORE']:.3f}")
                    with col3:
                        st.markdown(f"**Category:** {row['SENTIMENT_CATEGORY']}")
                    
                    # Expandable sections for detailed info
                    with st.expander("📝 Transcribed Text", expanded=False):
                        st.text_area("Full Transcription", row['TRANSCRIBED_TEXT'], height=150, key=f"trans_{idx}")
                    
                    # Summary in a colored box
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%); 
                                padding: 15px; 
                                border-radius: 8px; 
                                border-left: 4px solid {SNOWFLAKE_BLUE};
                                margin: 10px 0;'>
                        <strong>📋 Summary:</strong><br/>
                        {row['CALL_SUMMARY']}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Recommended actions in a styled box
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%); 
                                padding: 15px; 
                                border-radius: 8px; 
                                border-left: 4px solid #22C55E;
                                margin: 10px 0;'>
                        <strong>✅ Recommended Actions:</strong><br/>
                        {row['RECOMMENDED_ACTIONS'].replace(chr(10), '<br/>')}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if idx < len(result):
                        st.markdown("---")
                
                # Show the query
                with st.expander("🔍 View SQL Query"):
                    st.code(query, language="sql")
                    
            elif error:
                st.error(f"Error: {error}")
    
    st.markdown("---")
    
    st.markdown("""
    ### 🎯 Key Capabilities Demonstrated
    
    1. **Basic Transcription**: Convert audio to text with language detection
    2. **Sentiment Analysis**: Understand customer emotions from transcribed calls
    3. **AI Response Generation**: Auto-generate customer service responses
    4. **Batch Processing**: Transcribe and summarize multiple calls at once
    
    ### 📋 Supported Formats
    - **Audio**: FLAC, MP3, MP4, OGG, WAV, WEBM
    - **Video**: MKV, MP4, OGV, WEBM
    - **Max Duration**: 120 minutes (60 min with timestamps)
    - **Max File Size**: 700 MB
    - **Languages**: 31 languages with auto-detection
    """)

# =============================================================================
# PAGE: AI_PARSE_DOCUMENT
# =============================================================================

def page_ai_parse_document():
    show_header()
    
    st.title("📄 AI_PARSE_DOCUMENT")
    
    multimodal_badge = show_multimodal_support(text=False, images=False, documents=True, audio=False)
    st.markdown(f"""
    **AI_PARSE_DOCUMENT** extracts text and layout from documents with high fidelity.
    Supports OCR mode (text only) and LAYOUT mode (preserves tables and structure).
    
    {multimodal_badge} &nbsp;&nbsp; 📖 [View Documentation](https://docs.snowflake.com/en/sql-reference/functions/ai_parse_document)
    
    **💰 Cost (per 1,000 pages - Table 6e):**
    - **OCR Mode:** 0.5 credits per 1K pages
    - **Layout Mode:** 3.33 credits per 1K pages
    
    [View pricing details](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf)
    """, unsafe_allow_html=True)
    
    # Get available PDF documents from stage
    docs_query = "SELECT RELATIVE_PATH FROM DIRECTORY(@AI_FUNCTIONS_PLAYGROUND.DEMO.DOCUMENT_STAGE) ORDER BY RELATIVE_PATH"
    docs_result, docs_error = execute_query(docs_query)
    
    if docs_error or not docs_result:
        st.warning("⚠️ No documents found in DOCUMENT_STAGE. Please upload PDF documents to the stage first.")
        st.info("""
        **To upload documents:**
        1. Use `PUT file://your_document.pdf @AI_FUNCTIONS_PLAYGROUND.DEMO.DOCUMENT_STAGE AUTO_COMPRESS=FALSE;`
        2. Or upload via Snowsight UI to the DOCUMENT_STAGE
        """)
        return
    
    available_docs = [row['RELATIVE_PATH'] for row in docs_result]
    doc_count = len(available_docs)
    
    st.success(f"✅ Found {doc_count} document(s) in DOCUMENT_STAGE")
    
    # Show available documents
    with st.expander("📄 Available Documents", expanded=False):
        for doc in available_docs:
            st.markdown(f"- {doc}")
    
    # Example 1: Parse and Store Documents
    show_example_card(
        "Parse Documents and Store Raw Text",
        "Extract text from all PDFs and store in PARSE_DOC_RAW_TEXT table",
        1
    )
    
    st.info("📄 **Step 1:** Parse documents and extract raw text for downstream processing")
    
    parse_mode = st.radio(
        "Select parsing mode:",
        ["OCR", "LAYOUT"],
        format_func=lambda x: f"{x} Mode - {'Fast, plain text only' if x == 'OCR' else 'Preserves tables and formatting (recommended)'}",
        key="parse_mode",
        horizontal=True
    )
    
    st.caption(f"**{'⚡ OCR Mode:' if parse_mode == 'OCR' else '📋 LAYOUT Mode:'}** "
               f"{'Faster processing, extracts plain text only (0.5 credits/1K pages)' if parse_mode == 'OCR' else 'Preserves document structure, tables, and formatting - slower processing but more accurate (3.33 credits/1K pages)'}")
    
    if st.button("Parse All Documents", key="parse_all_docs"):
        with st.spinner(f"Parsing {doc_count} document(s) in {parse_mode} mode..."):
            # First, truncate existing table
            truncate_query = "TRUNCATE TABLE AI_FUNCTIONS_PLAYGROUND.DEMO.PARSE_DOC_RAW_TEXT;"
            execute_query(truncate_query)
            
            total_docs = 0
            for doc_file in available_docs:
                st.write(f"Processing **{doc_file}**...")
                
                # Parse and store raw text
                parse_query = f"""
                INSERT INTO AI_FUNCTIONS_PLAYGROUND.DEMO.PARSE_DOC_RAW_TEXT (file_name, file_url, raw_text)
                SELECT 
                    '{doc_file}' as file_name,
                    TO_VARCHAR(GET_PRESIGNED_URL(@AI_FUNCTIONS_PLAYGROUND.DEMO.DOCUMENT_STAGE, '{doc_file}', 3600)) as file_url,
                    parsed_json:content::STRING as raw_text
                FROM (
                    SELECT 
                        AI_PARSE_DOCUMENT(
                            TO_FILE('@AI_FUNCTIONS_PLAYGROUND.DEMO.DOCUMENT_STAGE/{doc_file}'),
                            {{'mode': '{parse_mode}'}}
                        ) as parsed_json
                )
                """
                result, error = execute_query(parse_query)
                
                if not error:
                    total_docs += 1
                    st.success(f"✅ {doc_file} parsed successfully")
                else:
                    st.error(f"❌ Error parsing {doc_file}: {error}")
            
            if total_docs > 0:
                st.success(f"**🎉 Successfully parsed {total_docs} document(s) in {parse_mode} mode!**")
                
                # Show sample data from table
                sample_query = """
                SELECT 
                    file_name, 
                    LEFT(raw_text, 500) as preview,
                    LENGTH(raw_text) as text_length,
                    parsed_date
                FROM AI_FUNCTIONS_PLAYGROUND.DEMO.PARSE_DOC_RAW_TEXT
                ORDER BY parsed_date DESC
                """
                sample_result, _ = execute_query(sample_query)
                if sample_result:
                    st.markdown("**📊 Stored Documents:**")
                    for row in sample_result:
                        with st.expander(f"📄 {row['FILE_NAME']} ({row['TEXT_LENGTH']:,} characters)"):
                            st.caption(f"Parsed: {row['PARSED_DATE']}")
                            st.text_area("Text Preview", row['PREVIEW'] + "...", height=150, key=f"preview_{row['FILE_NAME']}")
                
                with st.expander("🔍 View SQL Query"):
                    st.code(f"""
INSERT INTO AI_FUNCTIONS_PLAYGROUND.DEMO.PARSE_DOC_RAW_TEXT (file_name, file_url, raw_text)
SELECT 
    'document.pdf' as file_name,
    TO_VARCHAR(GET_PRESIGNED_URL(@AI_FUNCTIONS_PLAYGROUND.DEMO.DOCUMENT_STAGE, 'document.pdf', 3600)) as file_url,
    parsed_json:content::STRING as raw_text
FROM (
    SELECT 
        AI_PARSE_DOCUMENT(
            TO_FILE('@AI_FUNCTIONS_PLAYGROUND.DEMO.DOCUMENT_STAGE/document.pdf'),
            {{'mode': '{parse_mode}'}}
        ) as parsed_json
)
                    """, language="sql")
    
    st.markdown("---")
    
    # Example 2: Chunk Documents
    show_example_card(
        "Chunk Parsed Documents",
        "Split documents into chunks and store in PARSE_DOC_CHUNKED_TEXT table",
        2
    )
    
    st.info("✂️ **Step 2:** Chunk parsed documents for semantic search and RAG using `SPLIT_TEXT_RECURSIVE_CHARACTER` with markdown format")
    
    col1, col2 = st.columns(2)
    with col1:
        chunk_size = st.number_input("Chunk size (characters):", min_value=500, max_value=5000, value=1512, step=500, key="chunk_size")
        st.caption("Larger chunks retain more context but may be less precise")
    with col2:
        chunk_overlap = st.number_input("Chunk overlap:", min_value=0, max_value=500, value=200, step=50, key="chunk_overlap")
        st.caption("Overlap helps maintain context between chunks")
    
    if st.button("Chunk Documents", key="chunk_docs"):
        with st.spinner("Chunking documents..."):
            # First check if there are documents to chunk
            check_query = "SELECT COUNT(*) as doc_count FROM AI_FUNCTIONS_PLAYGROUND.DEMO.PARSE_DOC_RAW_TEXT"
            check_result, _ = execute_query(check_query)
            
            if check_result and check_result[0]['DOC_COUNT'] == 0:
                st.warning("⚠️ No documents found in PARSE_DOC_RAW_TEXT table. Please run Example 1 first!")
            else:
                # Truncate chunked text table
                truncate_query = "TRUNCATE TABLE AI_FUNCTIONS_PLAYGROUND.DEMO.PARSE_DOC_CHUNKED_TEXT;"
                execute_query(truncate_query)
                
                # Chunk all documents from PARSE_DOC_RAW_TEXT
                chunk_query = f"""
                INSERT INTO AI_FUNCTIONS_PLAYGROUND.DEMO.PARSE_DOC_CHUNKED_TEXT (file_name, file_url, chunk_index, chunk_text, chunk_length)
                SELECT 
                    file_name,
                    file_url,
                    c.INDEX as chunk_index,
                    c.VALUE as chunk_text,
                    LENGTH(c.VALUE) as chunk_length
                FROM AI_FUNCTIONS_PLAYGROUND.DEMO.PARSE_DOC_RAW_TEXT,
                    LATERAL FLATTEN(input => SNOWFLAKE.CORTEX.SPLIT_TEXT_RECURSIVE_CHARACTER(
                        raw_text,
                        'markdown',
                        {chunk_size},
                        {chunk_overlap}
                    )) as c
                """
                result, error = execute_query(chunk_query)
                
                if not error:
                    # Count total chunks created
                    count_query = """
                    SELECT 
                        file_name,
                        COUNT(*) as chunk_count,
                        AVG(chunk_length) as avg_chunk_size
                    FROM AI_FUNCTIONS_PLAYGROUND.DEMO.PARSE_DOC_CHUNKED_TEXT
                    GROUP BY file_name
                    ORDER BY file_name
                    """
                    count_result, _ = execute_query(count_query)
                    
                    if count_result:
                        total_chunks = sum(row['CHUNK_COUNT'] for row in count_result)
                        st.success(f"**🎉 Successfully created {total_chunks} chunks!**")
                        
                        # Show stats per document
                        st.markdown("**📊 Chunking Summary:**")
                        for row in count_result:
                            st.markdown(f"- **{row['FILE_NAME']}**: {row['CHUNK_COUNT']} chunks (avg size: {row['AVG_CHUNK_SIZE']:.0f} chars)")
                        
                        # Show all chunks in a table
                        sample_query = """
                        SELECT 
                            file_name,
                            chunk_index,
                            LEFT(chunk_text, 200) || '...' as chunk_preview,
                            chunk_length
                        FROM AI_FUNCTIONS_PLAYGROUND.DEMO.PARSE_DOC_CHUNKED_TEXT
                        ORDER BY file_name, chunk_index
                        """
                        sample_result, _ = execute_query(sample_query)
                        if sample_result:
                            st.markdown("**📋 All Document Chunks:**")
                            st.dataframe(
                                sample_result,
                                use_container_width=True,
                                column_config={
                                    "FILE_NAME": st.column_config.TextColumn("File Name", width="medium"),
                                    "CHUNK_INDEX": st.column_config.NumberColumn("Chunk #", width="small"),
                                    "CHUNK_PREVIEW": st.column_config.TextColumn("Preview", width="large"),
                                    "CHUNK_LENGTH": st.column_config.NumberColumn("Length (chars)", width="small")
                                }
                            )
                        
                        with st.expander("🔍 View SQL Query"):
                            st.code(f"""
INSERT INTO AI_FUNCTIONS_PLAYGROUND.DEMO.PARSE_DOC_CHUNKED_TEXT 
    (file_name, file_url, chunk_index, chunk_text, chunk_length)
SELECT 
    file_name,
    file_url,
    c.INDEX as chunk_index,
    c.VALUE as chunk_text,
    LENGTH(c.VALUE) as chunk_length
FROM AI_FUNCTIONS_PLAYGROUND.DEMO.PARSE_DOC_RAW_TEXT,
    LATERAL FLATTEN(input => SNOWFLAKE.CORTEX.SPLIT_TEXT_RECURSIVE_CHARACTER(
        raw_text,
        'markdown',
        {chunk_size},
        {chunk_overlap}
    )) as c
                            """, language="sql")
                else:
                    st.error(f"Error chunking documents: {error}")
    
    st.markdown("---")
    
    # Example 3: Create Cortex Search Service
    show_example_card(
        "Create Cortex Search Service",
        "Build a semantic search index over document chunks",
        3
    )
    
    st.info("🔍 **Step 3:** Create a Cortex Search Service over chunked documents (requires Example 2 to be completed)")
    
    st.markdown("""
    This will create a search service that:
    - Automatically generates embeddings for all document chunks
    - Enables semantic (meaning-based) search, not just keyword matching
    - Updates with a 9999-day lag (effectively manual refresh for this demo)
    - Uses the `PARSE_DOC_CHUNKED_TEXT` table as the data source
    """)
    
    if st.button("Create Search Service", key="create_search_service"):
        with st.spinner("Creating Cortex Search Service..."):
            # First check if there are chunks to index
            check_query = "SELECT COUNT(*) as chunk_count FROM AI_FUNCTIONS_PLAYGROUND.DEMO.PARSE_DOC_CHUNKED_TEXT"
            check_result, _ = execute_query(check_query)
            
            if check_result and check_result[0]['CHUNK_COUNT'] == 0:
                st.warning("⚠️ No document chunks found in PARSE_DOC_CHUNKED_TEXT table. Please run Examples 1 and 2 first!")
            else:
                # Drop existing service if exists
                drop_query = """
                DROP CORTEX SEARCH SERVICE IF EXISTS AI_FUNCTIONS_PLAYGROUND.DEMO.DOCUMENT_SEARCH_SERVICE
                """
                execute_query(drop_query)
                
                # Create the search service
                create_service_query = """
                CREATE CORTEX SEARCH SERVICE AI_FUNCTIONS_PLAYGROUND.DEMO.DOCUMENT_SEARCH_SERVICE
                ON chunk_text
                ATTRIBUTES file_name, chunk_index
                WAREHOUSE = CORTEX_SEARCH_WH
                TARGET_LAG = '9999 days'
                AS (
                    SELECT 
                        chunk_text,
                        file_name,
                        chunk_index
                    FROM AI_FUNCTIONS_PLAYGROUND.DEMO.PARSE_DOC_CHUNKED_TEXT
                )
                """
                result, error = execute_query(create_service_query)
                
                if not error:
                    st.success("**✅ Cortex Search Service created successfully!**")
                    st.markdown("""
                    **Service Details:**
                    - **Name:** `AI_FUNCTIONS_PLAYGROUND.DEMO.DOCUMENT_SEARCH_SERVICE`
                    - **Search Column:** `chunk_text`
                    - **Attributes:** `file_name`, `chunk_index`
                    - **Warehouse:** `CORTEX_SEARCH_WH`
                    - **Target Lag:** 9999 days (manual refresh)
                    """)
                    
                    # Test the search service
                    st.markdown("**Test Search:**")
                    test_query = """
                    SELECT 
                        file_name,
                        chunk_index,
                        LEFT(chunk_text, 200) as preview
                    FROM TABLE(
                        AI_FUNCTIONS_PLAYGROUND.DEMO.DOCUMENT_SEARCH_SERVICE!SEARCH(
                            'revenue growth',
                            {'limit': 3}
                        )
                    )
                    """
                    test_result, test_error = execute_query(test_query)
                    if test_result:
                        st.success(f"Found {len(test_result)} relevant chunks for 'revenue growth'")
                        for idx, row in enumerate(test_result, 1):
                            st.caption(f"**{idx}. {row['FILE_NAME']}** (Chunk {row['CHUNK_INDEX']})")
                            st.text(row['PREVIEW'] + "...")
                    
                    with st.expander("🔍 View SQL"):
                        st.code(create_service_query, language="sql")
                else:
                    st.error(f"Error creating search service: {error}")
    
    st.markdown("---")
    
    # Next Steps Section
    st.markdown("""
    ### 🚀 Next Steps: Build an Intelligent Agent
    
    Now that you have a Cortex Search Service, you can create a **Cortex Agent** that references it to build powerful conversational AI experiences!
    
    **What to do next:**
    1. Navigate to **Snowsight** → **AI & ML** → **Cortex Agents**
    2. Create a new Cortex Agent and add your `DOCUMENT_SEARCH_SERVICE` as a tool
    3. Test your agent by asking natural language questions in **[Snowflake Intelligence](https://ai.snowflake.com)**
    
    Your agent will be able to:
    - ✅ Answer "What?" questions (e.g., "What were the Q2 revenue figures?")
    - ✅ Answer "Why?" questions (e.g., "Why did revenue grow in Q2?")
    - ✅ Search across all your parsed documents automatically
    - ✅ Provide citations and source references
    
    📖 **Learn More:** Read about how Snowflake Intelligence excels at answering "Why?" questions in this blog post:  
    [Snowflake Intelligence: Tell Me Why!](https://medium.com/snowflake/snowflake-intelligence-tell-me-why-3e79644b4733)
    """)

# =============================================================================
# PAGE: AI_SUMMARIZE_AGG
# =============================================================================

def page_ai_summarize_agg():
    show_header()
    
    st.title("📝 AI_SUMMARIZE_AGG")
    
    multimodal_badge = show_multimodal_support(text=True, images=False, documents=False, audio=False)
    st.markdown(f"""
    **AI_SUMMARIZE_AGG** is an aggregate function that summarizes multiple rows of text.
    Unlike regular LLMs, it's not limited by context windows - perfect for large datasets!
    
    {multimodal_badge} &nbsp;&nbsp; 📖 [View Documentation](https://docs.snowflake.com/en/sql-reference/functions/ai_summarize_agg)
    
    **💰 Cost:** 1.60 credits per 1M tokens (Table 6a)  
    [View pricing details](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf)
    """, unsafe_allow_html=True)
    
    # Example 1: Summarize All Reviews for a Food Truck
    show_example_card(
        "Summarize All Reviews for a Food Truck",
        "Get a comprehensive summary across all customer feedback",
        1
    )
    
    result, _ = execute_query("SELECT DISTINCT food_truck_name FROM AI_FUNCTIONS_PLAYGROUND.DEMO.CUSTOMER_REVIEWS ORDER BY food_truck_name")
    if result:
        truck_options = [r['FOOD_TRUCK_NAME'] for r in result]
        selected_truck = st.selectbox("Select food truck:", truck_options)
        
        if st.button("Summarize Reviews", key="summarize_truck"):
            with st.spinner("Summarizing all reviews..."):
                query = f"""
                SELECT 
                    '{selected_truck}' as food_truck,
                    COUNT(*) as total_reviews,
                    AVG(rating) as avg_rating,
                    AI_SUMMARIZE_AGG(review_text) as review_summary
                FROM AI_FUNCTIONS_PLAYGROUND.DEMO.CUSTOMER_REVIEWS
                WHERE food_truck_name = '{selected_truck}'
                GROUP BY food_truck_name
                """
                result, error = execute_query(query)
                if result:
                    st.markdown(f"### {result[0]['FOOD_TRUCK']}")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Total Reviews", result[0]['TOTAL_REVIEWS'])
                    with col2:
                        st.metric("Average Rating", f"{'⭐' * int(result[0]['AVG_RATING'])} ({result[0]['AVG_RATING']:.1f}/5)")
                    
                    st.markdown("**Summary of All Reviews:**")
                    st.markdown(f"_{result[0]['REVIEW_SUMMARY']}_")
                    st.code(query, language="sql")
    
    st.markdown("---")
    
    # Example 2: Summarize Support Tickets by Status
    show_example_card(
        "Summarize Open Support Tickets",
        "Get insights into common issues from support tickets",
        2
    )
    
    ticket_status = st.selectbox("Select ticket status:", ["Open", "In Progress", "Closed"])
    
    if st.button("Summarize Tickets", key="summarize_tickets"):
        with st.spinner("Summarizing tickets..."):
            query = f"""
            SELECT 
                status,
                COUNT(*) as ticket_count,
                AI_SUMMARIZE_AGG(issue_description) as issues_summary
            FROM AI_FUNCTIONS_PLAYGROUND.DEMO.SUPPORT_TICKETS
            WHERE status = '{ticket_status}'
            GROUP BY status
            """
            result, error = execute_query(query)
            if result and len(result) > 0:
                st.markdown(f"### {result[0]['STATUS']} Tickets")
                st.metric("Total Tickets", result[0]['TICKET_COUNT'])
                st.markdown("**Summary of Issues:**")
                st.markdown(f"_{result[0]['ISSUES_SUMMARY']}_")
                st.code(query, language="sql")
            else:
                st.warning(f"No {ticket_status} tickets found")
    
    st.markdown("---")
    
    # Example 3: Monthly Review Summaries
    show_example_card(
        "Monthly Review Trends",
        "Summarize reviews by month to identify trends",
        3
    )
    
    if st.button("Generate Monthly Summaries", key="monthly_summaries"):
        with st.spinner("Generating monthly summaries..."):
            query = """
            SELECT 
                DATE_TRUNC('MONTH', review_date) as month,
                COUNT(*) as review_count,
                AVG(rating) as avg_rating,
                AI_SUMMARIZE_AGG(review_text) as monthly_summary
            FROM AI_FUNCTIONS_PLAYGROUND.DEMO.CUSTOMER_REVIEWS
            GROUP BY DATE_TRUNC('MONTH', review_date)
            ORDER BY month DESC
            LIMIT 3
            """
            result, error = execute_query(query)
            if result:
                for row in result:
                    with st.expander(f"{row['MONTH'].strftime('%B %Y')} - {row['REVIEW_COUNT']} reviews (Avg: {'⭐' * int(row['AVG_RATING'])})"):
                        st.markdown(row['MONTHLY_SUMMARY'])
                st.code(query, language="sql")

# =============================================================================
# PAGE: AI_AGG
# =============================================================================

def page_ai_agg():
    show_header()
    
    st.title("📊 AI_AGG")
    
    multimodal_badge = show_multimodal_support(text=True, images=False, documents=False, audio=False)
    st.markdown(f"""
    **AI_AGG** is like AI_SUMMARIZE_AGG but with custom instructions.
    Aggregate and analyze text data with your own specific prompts - not limited by context windows!
    
    {multimodal_badge} &nbsp;&nbsp; 📖 [View Documentation](https://docs.snowflake.com/en/sql-reference/functions/ai_agg)
    
    **💰 Cost:** 1.60 credits per 1M tokens (Table 6a)  
    [View pricing details](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf)
    """, unsafe_allow_html=True)
    
    # Example 1: Extract Common Complaints
    show_example_card(
        "Identify Common Complaints Across Reviews",
        "Use a custom prompt to find specific patterns",
        1
    )
    
    if st.button("Find Common Complaints", key="find_complaints"):
        with st.spinner("Analyzing reviews..."):
            query = """
            SELECT 
                AI_AGG(
                    review_text,
                    'Identify the 5 most common complaints or issues mentioned in these reviews. 
                    For each issue, provide a brief description and estimate how many reviews mention it.'
                ) as common_complaints
            FROM AI_FUNCTIONS_PLAYGROUND.DEMO.CUSTOMER_REVIEWS
            WHERE rating <= 3
            """
            result, error = execute_query(query)
            if result:
                st.markdown("**Common Complaints Analysis:**")
                st.markdown(result[0]['COMMON_COMPLAINTS'])
                st.code(query, language="sql")
    
    st.markdown("---")
    
    # Example 2: Extract Popular Menu Items
    show_example_card(
        "Identify Most Praised Menu Items",
        "Find which menu items customers love the most",
        2
    )
    
    if st.button("Find Popular Items", key="popular_items"):
        with st.spinner("Analyzing positive reviews..."):
            query = """
            SELECT 
                food_truck_name,
                AI_AGG(
                    review_text,
                    'List the specific menu items that customers mentioned positively. 
                    For each item, explain what customers liked about it.'
                ) as popular_items
            FROM AI_FUNCTIONS_PLAYGROUND.DEMO.CUSTOMER_REVIEWS
            WHERE rating >= 4
            GROUP BY food_truck_name
            LIMIT 5
            """
            result, error = execute_query(query)
            if result:
                for row in result:
                    with st.expander(f"🍽️ {row['FOOD_TRUCK_NAME']}"):
                        st.markdown(row['POPULAR_ITEMS'])
                st.code(query, language="sql")
    
    st.markdown("---")
    
    # Example 3: Custom Analysis Prompt
    show_example_card(
        "Custom Analysis with Your Own Prompt",
        "Try your own custom aggregation analysis",
        3
    )
    
    custom_instruction = st.text_area(
        "Enter your custom analysis instruction:",
        "Analyze the customer service quality based on these support tickets. "
        "Identify areas where we excel and areas that need improvement. "
        "Provide specific recommendations."
    )
    
    data_source = st.radio("Analyze:", ["Customer Reviews", "Support Tickets"])
    
    if st.button("Run Custom Analysis", key="custom_agg"):
        with st.spinner("Running custom analysis..."):
            escaped_instruction = escape_sql_string(custom_instruction)
            if data_source == "Customer Reviews":
                query = f"""
                SELECT AI_AGG(
                    review_text,
                    '{escaped_instruction}'
                ) as analysis_result
                FROM AI_FUNCTIONS_PLAYGROUND.DEMO.CUSTOMER_REVIEWS
                """
            else:
                query = f"""
                SELECT AI_AGG(
                    issue_description,
                    '{escaped_instruction}'
                ) as analysis_result
                FROM AI_FUNCTIONS_PLAYGROUND.DEMO.SUPPORT_TICKETS
                """
            
            result, error = execute_query(query)
            if result:
                st.markdown("**Analysis Result:**")
                st.markdown(result[0]['ANALYSIS_RESULT'])
                st.code(query, language="sql")
            elif error:
                st.error(f"Error: {error}")
    
    st.markdown("---")
    
    st.markdown("""
    ### 💡 AI_AGG vs AI_SUMMARIZE_AGG
    
    | Feature | AI_SUMMARIZE_AGG | AI_AGG |
    |---------|------------------|--------|
    | Purpose | General summary | Custom analysis |
    | Prompt | Fixed (summarize) | Custom instruction |
    | Use Case | Quick summaries | Specific insights |
    | Flexibility | Low | High |
    
    **Use AI_AGG when you need:**
    - Specific insights (not just summaries)
    - Custom analysis with your own instructions
    - Extraction of particular patterns
    - Comparative analysis
    - Actionable recommendations
    """)

# =============================================================================
# MAIN APP ROUTING
# =============================================================================

def main():
    # Route to the appropriate page
    if current_page == "home":
        page_home()
    elif current_page == "ai_complete":
        page_ai_complete()
    elif current_page == "ai_translate":
        page_ai_translate()
    elif current_page == "ai_sentiment":
        page_ai_sentiment()
    elif current_page == "ai_extract":
        page_ai_extract()
    elif current_page == "ai_classify":
        page_ai_classify()
    elif current_page == "ai_filter":
        page_ai_filter()
    elif current_page == "ai_similarity":
        page_ai_similarity()
    elif current_page == "ai_redact":
        page_ai_redact()
    elif current_page == "ai_transcribe":
        page_ai_transcribe()
    elif current_page == "ai_parse_document":
        page_ai_parse_document()
    elif current_page == "ai_summarize_agg":
        page_ai_summarize_agg()
    elif current_page == "ai_agg":
        page_ai_agg()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #F8FAFC 0%, #E8EEF2 100%); border-radius: 12px; margin-top: 40px;'>
        <p style='font-size: 18px; font-weight: 600; color: #1E293B; margin-bottom: 8px;'>
            ❄️ Snowflake Cortex AI Functions Playground ❄️
        </p>
        <p style='color: #64748b; font-size: 14px; margin-bottom: 0;'>
            Built with Snowflake Cortex AI | Powered by Streamlit in Snowflake
        </p>
        <p style='color: #64748b; font-size: 12px; margin-top: 8px;'>
            🍔 Tasty Bytes Demo Data | 12 Cortex AI Functions Showcased
        </p>
    </div>
    """, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()

