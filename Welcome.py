import streamlit as st

# Set the page configuration
st.set_page_config(
    page_title="Quant Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Welcome message
st.title("📊 Welcome to the Quant Dashboard")
st.markdown("""
### Your all-in-one platform for financial data analysis and quantitative insights.

This dashboard provides tools and insights to empower your quantitative finance workflow:
- **Portfolio Analysis**: Analyze portfolio performance and risk metrics.
- **Quant GPT Chatbot**: Get AI-powered answers to your quantitative finance questions.
- **Fundamental Data Analysis**: Examine key metrics for stocks and companies.
- **Black-Scholes Calculator**: Price options using the Black-Scholes model.

---

### Available Features
Choose a component to get started:
""")

# Add navigation buttons for each component
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 📂 Portfolio Analysis
    Monitor and assess your portfolio’s performance, allocation, and risk metrics.
    """)
    st.markdown("""
    <a href="/Portfolio_Analysis" target="_self">
        <button style="background-color:#4CAF50; color:white; border:none; padding:10px 20px; text-align:center; font-size:16px; border-radius:5px; cursor:pointer;">
            Explore Portfolio Analysis
        </button>
    </a>
    """, unsafe_allow_html=True)

    st.markdown("""
    ### 🤖 Quant GPT Chatbot
    Interact with a GPT-powered assistant for quantitative finance guidance.
    """)
    st.markdown("""
    <a href="/Quant_Gpt" target="_self">
        <button style="background-color:#0078D7; color:white; border:none; padding:10px 20px; text-align:center; font-size:16px; border-radius:5px; cursor:pointer;">
            Try Quant GPT Chatbot
        </button>
    </a>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    ### 📊 Fundamental Data Analysis
    Dive into detailed financial metrics and fundamentals for companies.
    """)
    st.markdown("""
    <a href="/Fundamental_Data" target="_self">
        <button style="background-color:#FFA500; color:white; border:none; padding:10px 20px; text-align:center; font-size:16px; border-radius:5px; cursor:pointer;">
            Start Fundamental Analysis
        </button>
    </a>
    """, unsafe_allow_html=True)

    st.markdown("""
    ### 🧮 Black-Scholes Calculator
    Calculate theoretical option prices with the Black-Scholes model.
    """)
    st.markdown("""
    <a href="/Black_Scholes_Calculator" target="_self">
        <button style="background-color:#E91E63; color:white; border:none; padding:10px 20px; text-align:center; font-size:16px; border-radius:5px; cursor:pointer;">
            Open Black-Scholes Calculator
        </button>
    </a>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
🔒 **Secure** | 📈 **Real-Time Data** | 🤝 **Reliable Insights**
""")
