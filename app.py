import streamlit as st
from chatbot import get_response
from pdf_generator import create_pdf

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Travel Assistant",
    page_icon="✈️",
    layout="wide"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #f5f7ff 0%, #eef7ff 100%);
}

/* Main title */
.hero-title {
    text-align: center;
    font-size: 46px;
    font-weight: 800;
    margin-top: 10px;
    margin-bottom: 5px;
    color: #172554;
}

.hero-subtitle {
    text-align: center;
    font-size: 19px;
    color: #64748b;
    margin-bottom: 30px;
}

/* Cards */
.feature-card {
    background: white;
    padding: 22px;
    border-radius: 18px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.07);
    text-align: center;
    min-height: 130px;
}

.feature-card h3 {
    margin-bottom: 5px;
    color: #172554;
}

.feature-card p {
    color: #64748b;
}

/* Section titles */
.section-title {
    font-size: 27px;
    font-weight: 700;
    color: #172554;
    margin-top: 20px;
}

/* Trip cards */
.trip-card {
    background: white;
    padding: 20px;
    border-radius: 16px;
    border-left: 5px solid #6366f1;
    box-shadow: 0 4px 15px rgba(0,0,0,0.06);
    margin-bottom: 15px;
}

/* Buttons */
.stButton > button {
    border-radius: 12px;
    font-weight: 600;
}

/* Chat */
.chat-box {
    background: white;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.06);
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE
# ============================================================

if "itinerary" not in st.session_state:
    st.session_state.itinerary = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

if "favorite" not in st.session_state:
    st.session_state.favorite = ""

if "packing" not in st.session_state:
    st.session_state.packing = []

# ============================================================
# HERO SECTION
# ============================================================

st.markdown(
    '<div class="hero-title">✈️ AI Travel Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-subtitle">'
    'Plan smarter. Travel better. Explore more. 🌍'
    '</div>',
    unsafe_allow_html=True
)

# ============================================================
# FEATURE CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>🤖 AI Powered</h3>
        <p>Smart travel recommendations using Llama AI.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>🗺️ Personalized</h3>
        <p>Create trips based on your interests.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3>💰 Budget Friendly</h3>
        <p>Plan trips according to your budget.</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-card">
        <h3>📄 PDF Guide</h3>
        <p>Download your complete travel plan.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🌍 Trip Planner")

st.sidebar.markdown("### 📍 Destination")

destination = st.sidebar.text_input(
    "Where do you want to go?",
    placeholder="Example: Goa"
)

days = st.sidebar.number_input(
    "🗓️ Number of Days",
    min_value=1,
    max_value=30,
    value=3
)

budget = st.sidebar.selectbox(
    "💰 Budget",
    [
        "Budget",
        "Moderate",
        "Luxury"
    ]
)

travel_style = st.sidebar.selectbox(
    "✨ Travel Style",
    [
        "Relaxing",
        "Adventure",
        "Family",
        "Romantic",
        "Cultural"
    ]
)

interests = st.sidebar.multiselect(
    "❤️ Interests",
    [
        "Beaches",
        "Food",
        "Adventure",
        "History",
        "Shopping",
        "Nature",
        "Nightlife"
    ]
)

# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🗺️ Travel Planner",
        "💬 AI Chatbot",
        "🧳 Packing List",
        "ℹ️ About"
    ]
)

# ============================================================
# TAB 1 - TRAVEL PLANNER
# ============================================================

with tab1:

    st.markdown(
        '<div class="section-title">🗺️ Create Your Perfect Trip</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Tell us your preferences and AI will create a personalized travel plan."
    )

    # Popular destinations

    st.subheader("🌍 Popular Destinations")

    d1, d2, d3, d4 = st.columns(4)

    with d1:
        if st.button("🏖️ Goa"):
            destination = "Goa"

    with d2:
        if st.button("🏔️ Manali"):
            destination = "Manali"

    with d3:
        if st.button("🌴 Kerala"):
            destination = "Kerala"

    with d4:
        if st.button("🏛️ Hyderabad"):
            destination = "Hyderabad"

    st.write("")

    # Trip summary

    st.subheader("📋 Trip Summary")

    s1, s2, s3, s4 = st.columns(4)

    with s1:
        st.metric("📍 Destination", destination if destination else "Not selected")

    with s2:
        st.metric("🗓️ Days", days)

    with s3:
        st.metric("💰 Budget", budget)

    with s4:
        st.metric("✨ Style", travel_style)

    st.write("")

    # Generate button

    if st.button(
        "✨ Generate My Travel Plan",
        use_container_width=True
    ):

        if not destination:

            st.warning(
                "⚠️ Please enter a destination first."
            )

        else:

            interest_text = ", ".join(interests)

            prompt = f"""
You are an expert AI Travel Assistant.

Create a detailed {days}-day travel itinerary for {destination}.

Trip Details:

Destination: {destination}
Number of Days: {days}
Budget: {budget}
Travel Style: {travel_style}
Interests: {interest_text}

Include:

1. Day-by-day schedule
2. Morning, afternoon and evening activities
3. Places to visit
4. Food recommendations
5. Transportation suggestions
6. Approximate daily expenses
7. Important travel tips

Make the itinerary realistic, practical and easy to understand.

Use clear headings for every day.
"""

            with st.spinner(
                "🤖 Llama AI is creating your personalized trip..."
            ):

                try:

                    response = get_response(prompt)

                    st.session_state.itinerary = response
                    st.session_state.favorite = destination

                    st.success(
                        "🎉 Your travel plan has been created!"
                    )

                except Exception as e:

                    st.error(
                        "Unable to connect to Ollama."
                    )

                    st.error(str(e))

    # ========================================================
    # DISPLAY ITINERARY
    # ========================================================

    if st.session_state.itinerary:

        st.divider()

        st.subheader(
            f"🌟 Your {days}-Day {destination} Adventure"
        )

        st.write(
            st.session_state.itinerary
        )

        # Action buttons

        st.write("")

        a1, a2, a3 = st.columns(3)

        with a1:

            if st.button(
                "❤️ Save Favourite",
                use_container_width=True
            ):

                st.session_state.favorite = destination

                st.success(
                    f"{destination} saved!"
                )

        with a2:

            if st.button(
                "🔄 Reset Trip",
                use_container_width=True
            ):

                st.session_state.itinerary = ""
                st.session_state.favorite = ""

                st.rerun()

        with a3:

            pdf_file = "travel_itinerary.pdf"

            try:

                create_pdf(
                    st.session_state.itinerary,
                    pdf_file
                )

                with open(
                    pdf_file,
                    "rb"
                ) as file:

                    st.download_button(
                        "📄 Download PDF",
                        data=file,
                        file_name="AI_Travel_Itinerary.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

            except Exception as e:

                st.error(
                    "PDF generation failed."
                )

                st.error(str(e))

        # Favourite destination

        if st.session_state.favorite:

            st.info(
                f"❤️ Favourite destination: "
                f"{st.session_state.favorite}"
            )

# ============================================================
# TAB 2 - AI CHATBOT
# ============================================================

with tab2:

    st.markdown(
        '<div class="section-title">💬 AI Travel Chatbot</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Ask anything about destinations, food, activities, transportation or travel planning."
    )

    # Suggested questions

    st.subheader("💡 Try asking")

    q1, q2, q3, q4 = st.columns(4)

    with q1:
        st.write("🌴 Best places to visit")

    with q2:
        st.write("🍴 Local food")

    with q3:
        st.write("💰 Budget tips")

    with q4:
        st.write("🚗 Transportation")

    st.divider()

    # Display chat history

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.write(
                message["content"]
            )

    # Chat input

    question = st.chat_input(
        "Ask your AI Travel Assistant..."
    )

    if question:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):

            st.write(question)

        conversation = ""

        for message in st.session_state.messages:

            conversation += (
                f"{message['role']}: "
                f"{message['content']}\n"
            )

        prompt = f"""
You are a friendly expert AI Travel Assistant.

Conversation history:

{conversation}

Answer the latest user question clearly.

Give practical and useful travel advice.
"""

        with st.chat_message("assistant"):

            with st.spinner("🤖 Thinking..."):

                try:

                    answer = get_response(prompt)

                    st.write(answer)

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer
                        }
                    )

                except Exception as e:

                    st.error(
                        "Unable to connect to Ollama."
                    )

                    st.error(str(e))

    # Clear chat

    if st.session_state.messages:

        if st.button(
            "🗑️ Clear Chat"
        ):

            st.session_state.messages = []

            st.rerun()

# ============================================================
# TAB 3 - PACKING LIST
# ============================================================

with tab3:

    st.markdown(
        '<div class="section-title">🧳 Smart Packing Checklist</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Prepare your luggage before your journey."
    )

    packing_items = [
        "👕 Clothes",
        "👟 Comfortable Shoes",
        "🧴 Toiletries",
        "💊 Medicines",
        "🔌 Phone Charger",
        "🔋 Power Bank",
        "🪪 ID / Documents",
        "💳 Wallet / Cards",
        "🕶️ Sunglasses",
        "☂️ Umbrella",
        "📱 Phone",
        "🎧 Earphones"
    ]

    selected_items = []

    for item in packing_items:

        if st.checkbox(item):

            selected_items.append(item)

    st.write("")

    if selected_items:

        st.success(
            f"✅ {len(selected_items)} items packed!"
        )

        st.subheader("🎒 Your Packed Items")

        for item in selected_items:

            st.write(
                f"✓ {item}"
            )

    else:

        st.info(
            "Select the items you have packed."
        )

# ============================================================
# TAB 4 - ABOUT
# ============================================================

with tab4:

    st.markdown(
        '<div class="section-title">ℹ️ About the Project</div>',
        unsafe_allow_html=True
    )

    st.write(
        """
        ### ✈️ AI Travel Assistant

        AI Travel Assistant is an AI-powered travel planning
        application designed to help users create personalized
        travel itineraries.

        The system uses Llama 3.2:3b through Ollama to generate
        intelligent travel recommendations based on destination,
        budget, travel style and interests.
        """
    )

    st.subheader("🛠️ Technologies Used")

    technologies = [
        "🐍 Python 3.12.0",
        "🎨 Streamlit",
        "🤖 Ollama",
        "🧠 Llama 3.2:3b",
        "📄 ReportLab"
    ]

    for technology in technologies:

        st.write(
            f"• {technology}"
        )

    st.subheader("⭐ Main Features")

    features = [
        "Personalized travel itineraries",
        "AI-powered travel chatbot",
        "Budget-based planning",
        "Travel style selection",
        "Interest-based recommendations",
        "Popular destination suggestions",
        "Favourite destination",
        "Smart packing checklist",
        "PDF itinerary generation",
        "Conversation history",
        "Reset and clear options"
    ]

    for feature in features:

        st.write(
            f"✓ {feature}"
        )

    st.success(
        "🤖 Powered by Llama 3.2:3b + Ollama"
    )