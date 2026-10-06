import os
import streamlit as st
from dotenv import load_dotenv

from agno.agent import Agent
from agno.models.groq import Groq
from agno.team import Team


# =========================================================
# 1. Load Environment Variables
# =========================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY not found. Please add it to your .env file.")
    st.stop()


# =========================================================
# 2. Page Configuration
# =========================================================

st.set_page_config(
    page_title="AI Language Translator",
    page_icon="🌍",
    layout="wide"
)


# =========================================================
# 3. Custom CSS
# =========================================================

st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    margin-top: 20px;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #777;
    font-size: 18px;
    margin-bottom: 35px;
}

.input-box {
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #ddd;
    background-color: #fafafa;
}

.result-box {
    padding: 25px;
    border-radius: 15px;
    border: 1px solid #ddd;
    background-color: #f7f7f7;
    margin-top: 20px;
}

.result-title {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 4. Language Agents
# =========================================================

eng_agent = Agent(
    name="English Agent",

    description=(
        "You are an English translation expert. "
        "Translate the user's text into natural and correct English."
    ),

    instructions=[
        "Translate the given text into English.",
        "Preserve the original meaning.",
        "Do not add unnecessary information.",
        "Return only the translated text."
    ],

    model=Groq(
        id="openai/gpt-oss-120b"
    )
)


chi_agent = Agent(
    name="Chinese Agent",

    description=(
        "You are a Chinese translation expert. "
        "Translate the user's text into natural Chinese."
    ),

    instructions=[
        "Translate the given text into Chinese.",
        "Preserve the original meaning.",
        "Do not add unnecessary information.",
        "Return only the translated text."
    ],

    model=Groq(
        id="openai/gpt-oss-120b"
    )
)


hindi_agent = Agent(
    name="Hindi Agent",

    description=(
        "You are a Hindi translation expert. "
        "Translate the user's text into natural Hindi."
    ),

    instructions=[
        "Translate the given text into Hindi.",
        "Preserve the original meaning.",
        "Do not add unnecessary information.",
        "Return only the translated text."
    ],

    model=Groq(
        id="openai/gpt-oss-120b"
    )
)


# =========================================================
# 5. Create Team
# =========================================================

team_leader = Team(

    name="AI Translation Team",

    members=[
        eng_agent,
        chi_agent,
        hindi_agent
    ],

    model=Groq(
        id="openai/gpt-oss-120b"
    ),

    markdown=True,

    show_members_responses=True,

    instructions=[
        "Translate the user's text according to the requested target language.",
        "If the target language is English, use the English Agent.",
        "If the target language is Chinese, use the Chinese Agent.",
        "If the target language is Hindi, use the Hindi Agent.",
        "Preserve the original meaning.",
        "Do not explain the translation.",
        "Return only the translated text."
    ]
)


# =========================================================
# 6. Header
# =========================================================

st.markdown(
    '<div class="main-title">🌍 AI Language Translator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Translate your text into your preferred language using AI'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# 7. Input Section
# =========================================================

st.markdown(
    '<div class="input-box">',
    unsafe_allow_html=True
)

st.subheader("✍️ Enter Your Text")

user_text = st.text_area(
    "Text to translate",
    placeholder=(
        "Type or paste your text here...\n\n"
        "Example: Hello, how are you today?"
    ),
    height=180,
    label_visibility="collapsed"
)

st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# 8. Target Language
# =========================================================

st.subheader("🌐 Choose Translation Language")

target_language = st.selectbox(
    "Select your preferred language",
    [
        "English 🇬🇧",
        "Chinese 🇨🇳",
        "Hindi 🇮🇳"
    ]
)


# =========================================================
# 9. Translate Button
# =========================================================

translate_button = st.button(
    "🔄 Translate",
    use_container_width=True
)


# =========================================================
# 10. Translation
# =========================================================

if translate_button:

    if not user_text.strip():

        st.warning("⚠️ Please enter some text to translate.")

    else:

        # Determine target language
        if target_language.startswith("English"):
            language = "English"

        elif target_language.startswith("Chinese"):
            language = "Chinese"

        else:
            language = "Hindi"


        # Create translation prompt
        translation_prompt = f"""
Translate the following text into {language}.

Important rules:
- Preserve the exact meaning.
- Keep the tone natural.
- Do not add extra information.
- Do not explain the translation.
- Return only the translated text.

Text:
{user_text}
"""


        # Run AI
        with st.spinner(
            f"🤖 Translating into {language}..."
        ):

            try:

                response = team_leader.run(
                    translation_prompt
                )

                # Store result
                st.session_state["translation"] = response.content
                st.session_state["language"] = language

            except Exception as e:

                st.error(
                    f"❌ Translation Error: {e}"
                )


# =========================================================
# 11. Display Translation
# =========================================================

if "translation" in st.session_state:

    st.markdown("---")

    st.markdown(
        '<div class="result-box">',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="result-title">'
        f'✅ {st.session_state["language"]} Translation'
        f'</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        st.session_state["translation"]
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )