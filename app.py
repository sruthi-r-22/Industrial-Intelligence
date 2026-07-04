import os
import re

import google.generativeai as genai
from dotenv import load_dotenv
from pypdf import PdfReader
import streamlit as st

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(page_title="Industrial Knowledge Brain", layout="wide")

# =====================================================
# GEMINI SETUP
# =====================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY not found.")
    st.stop()

genai.configure(api_key=api_key)

model = genai.GenerativeModel("models/gemini-2.5-flash")

# =====================================================
# SESSION STATE
# =====================================================

if "chunks" not in st.session_state:
    st.session_state.chunks = []

# =====================================================
# HERO SECTION
# =====================================================
st.markdown(
    """
<div style="
text-align:center;
padding:40px 30px;
border-radius:18px;
background:linear-gradient(180deg,#161B22,#1B2430);
border:1px solid #2D3748;
margin-bottom:25px;
">

<h1 style="
color:#14B8A6;
font-size:46px;
font-weight:700;
margin-bottom:12px;
">
Industrial Knowledge Brain
</h1>

<h3 style="
color:#F8FAFC;
font-weight:500;
font-size:28px;
margin-bottom:18px;
">
Enterprise Document Intelligence Platform
</h3>

<p style="
color:#CBD5E1;
font-size:16px;
line-height:1.8;
max-width:850px;
margin:auto;
">
Search industrial manuals, technical reports, research papers,
company documentation and engineering knowledge using
AI-powered retrieval.
</p>

</div>
""",
    unsafe_allow_html=True,
)

# =====================================================
# GET STARTED
# =====================================================
with st.container(border=True):

    st.markdown(
        """
    <h2 style="
    color:#F8FAFC;
    font-size:30px;
    margin-bottom:5px;
    ">
    Get Started
    </h2>

    <p style="
    color:#94A3B8;
    font-size:16px;
    margin-bottom:5px;
    ">
    Complete these simple steps to build your searchable knowledge base.
    </p>
    """,
        unsafe_allow_html=True,
    )

    with st.container(border=True):

        # =====================================================
        # SUPPORTED DOCUMENT TYPES
        # =====================================================

        st.markdown(
            """
        <h3 style="color:#F8FAFC;font-size:24px;">
        Supported Document Types
        </h3>
        """,
            unsafe_allow_html=True,
        )

        left, center, right = st.columns([1, 2, 1])

        with center:

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("""
        • Industrial Manuals

        • Research Papers

        • Technical Reports

        • Academic Textbooks

        • Company Documentation
        """)
            with col2:
                st.markdown("""
        • User Guides

        • Product Catalogs

        • SOP Documents

        • Training Manuals

        • Engineering Reports
        """)

    # =====================================================
    # DOCUMENT UPLOAD & SEARCH
    # =====================================================

    with st.container(border=True):

        st.markdown(
            """
        <h3 style="color:#F8FAFC;font-size:28px;">
        Upload Documents
        </h3>
        """,
            unsafe_allow_html=True,
        )

        uploaded_files = st.file_uploader(
            "",
            type=["pdf"],
            accept_multiple_files=True,
            label_visibility="collapsed",
        )

        # FIX: Added defensive flag so it parses documents ONLY when memory is empty
        if uploaded_files and len(st.session_state.chunks) == 0:

            with st.spinner("Processing documents..."):

                all_chunks = []

                for file in uploaded_files:

                    reader = PdfReader(file)

                    text = ""

                    for page in reader.pages:

                        page_text = page.extract_text()

                        if page_text:
                            text += page_text + " "

                    text = re.sub(r"\s+", " ", text)

                    # Give chunks more room and overlap them so words don't break in half
                    chunk_size = 1000
                    overlap = 200

                    chunks = [
                        text[i : i + chunk_size]
                        for i in range(0, len(text), chunk_size - overlap)
                    ]

                    all_chunks.extend(chunks)

                st.session_state.chunks = all_chunks

        if uploaded_files:
            st.success("Documents uploaded successfully!")
            st.info(
                f"Knowledge Base Created with {len(st.session_state.chunks)} chunks."
            )

        st.markdown("---")

        st.markdown(
            """
        <h3 style="color:#F8FAFC;font-size:28px;">
        Search Knowledge Base
        </h3>
        """,
            unsafe_allow_html=True,
        )

        question = st.text_input(
            "",
            placeholder="Ask anything about your uploaded document...",
            label_visibility="collapsed",
        )

        ask_button = st.button("Search Documents", use_container_width=True)

        answer_placeholder = st.container()

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown(
        """
        <h2 style="
        color:#14B8A6;
        text-align:center;
        margin-bottom:5px;
        ">
        Industrial Knowledge Brain
        </h2>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.subheader("About")

    st.markdown(
        """
    <div style="
    background-color:#1E2230;
    border:1px solid #2D3748;
    border-radius:12px;
    padding:18px;
    ">

    <p style="color:#F8FAFC; font-size:18px; font-weight:600; margin-bottom:12px;">
    Industrial Knowledge Brain
    </p>

    <p style="color:#E5E7EB; font-size:16px; line-height:1.7; margin-bottom:10px;">
    Upload PDF documents and ask questions in natural language.
    </p>

    <p style="color:#CBD5E1; font-size:15px; line-height:1.7;">
    Answers are generated only from the uploaded documents, ensuring accurate and context-aware responses.
    </p>

    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.subheader("Technologies")

    st.markdown(
        """
    <div style="
    background-color:#1E2230;
    border:1px solid #2D3748;
    border-radius:12px;
    padding:16px;
    ">
    <p style="color:#F8FAFC; font-size:16px; margin-bottom:8px;">Python</p>
    <p style="color:#F8FAFC; font-size:16px; margin-bottom:8px;">Streamlit</p>
    <p style="color:#F8FAFC; font-size:16px; margin-bottom:8px;">Google Gemini 2.5 Flash</p>
    <p style="color:#F8FAFC; font-size:16px;">PyPDF</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.subheader("Statistics")

    pdf_count = len(uploaded_files) if uploaded_files else 0
    chunk_count = len(st.session_state.chunks)

    st.markdown(
        f"""
    <div style="
    background-color:#1E2230;
    border:1px solid #2D3748;
    border-radius:12px;
    padding:16px;
    ">
    <p style="color:#14B8A6; font-size:16px; font-weight:600;">Uploaded PDFs</p>
    <p style="color:#F8FAFC; font-size:28px; font-weight:bold; margin-top:-8px;">{pdf_count}</p>
    <hr style="border:0.5px solid #2D3748;">
    <p style="color:#14B8A6; font-size:16px; font-weight:600;">Knowledge Chunks</p>
    <p style="color:#F8FAFC; font-size:28px; font-weight:bold; margin-top:-8px;">{chunk_count}</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.caption("Developed for ET AI Hackathon 2.0")

# =====================================================
# QUESTION ANSWERING
# =====================================================

if ask_button:
    if not question.strip():
        with answer_placeholder:
            st.warning("Please enter a question.")
    elif len(st.session_state.chunks) == 0:
        with answer_placeholder:
            st.error("Please upload at least one PDF.")
    else:
        # Punctuation-safe word evaluation
        raw_words = re.findall(r"\b\w+\b", question.lower())
        stop_words = {
            "what",
            "is",
            "the",
            "a",
            "an",
            "and",
            "or",
            "of",
            "for",
            "in",
            "to",
            "about",
        }
        search_terms = [word for word in raw_words if word not in stop_words]

        chunk_scores = []
        for chunk in st.session_state.chunks:
            score = 0
            chunk_lower = chunk.lower()
            for word in search_terms:
                if word in chunk_lower:
                    score += 10
            chunk_scores.append((score, chunk))

        chunk_scores.sort(key=lambda x: x[0], reverse=True)
        top_chunks = [chunk for score, chunk in chunk_scores if score > 0][:4]
        context = "\n\n".join(top_chunks) if top_chunks else ""

        # Tight RAG prompt constraints
        prompt = f"""
You are an intelligent AI document assistant.

Your task is to answer the user's question using ONLY the information provided in the document context.

Instructions:
- Never use outside knowledge.
- Answer clearly, accurately, and professionally.
- Use headings whenever appropriate.
- Use bullet points for lists.
- If the document contains a definition, explain it in simple language.
- If the document contains a procedure, include every step in the correct order.
- If formulas, examples, or important facts are relevant, include them.
- Combine information from multiple document sections if needed.
- Do not invent or assume any information.
- Do not mention information that is not present in the document.
- If the answer cannot be found in the document, reply exactly:
"I could not find sufficient information in the uploaded document."

DOCUMENT:
{context}

QUESTION:
{question}

ANSWER:
"""

        try:
            with answer_placeholder:
                with st.spinner("Analyzing your documents..."):
                    response = model.generate_content(prompt)
                    answer = response.text

                    st.markdown("## Retrieved Information")
                    with st.container(border=True):
                        st.subheader("Answer Summary")
                        st.write(answer)

                    with st.expander("Source References", expanded=False):
                        if top_chunks:
                            for i, chunk in enumerate(top_chunks, start=1):
                                st.markdown(f"### Source {i}")
                                st.write(chunk)
                                st.divider()
                        else:
                            st.info("No matching source section found.")
        except Exception as e:
            with answer_placeholder:
                error_msg = str(e)
                if "429" in error_msg:
                    st.error(
                        "⚠️ Gemini API rate limit reached. Please try after some time"
                    )
                else:
                    st.error(f"Error calling Gemini API: {error_msg}")

# =====================================================
# FOOTER
# =====================================================
st.markdown("---")
st.markdown(
    """
<div style="text-align:center; padding:15px; color:#9CA3AF; font-size:14px;">
<b>Industrial Knowledge Brain</b><br>
Developed for <b>ET AI Hackathon 2.0</b><br>
</div>
""",
    unsafe_allow_html=True,
)