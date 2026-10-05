import streamlit as st
from chatbot import get_response
from pdf_generator import create_pdf


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Travel Assistant",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# ============================================================

if "itinerary" not in st.session_state:
    st.session_state.itinerary = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

if "favorite" not in st.session_state:
    st.session_state.favorite = ""

if "selected_destination" not in st.session_state:
    st.session_state.selected_destination = ""

if "travel_mood" not in st.session_state:
    st.session_state.travel_mood = ""


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

/* =========================================================
   MAIN BACKGROUND
========================================================= */

.stApp {
    background: linear-gradient(
        135deg,
        #f5f9ff 0%,
        #eef7ff 50%,
        #f5f1ff 100%
    );
}

.block-container {
    max-width: 1250px;
    padding-top: 25px;
}


/* =========================================================
   NORMAL TEXT
========================================================= */

p {
    color: #111827 !important;
}

label {
    color: #111827 !important;
}

[data-testid="stMarkdownContainer"] p {
    color: #111827 !important;
}

[data-testid="stCaptionContainer"] {
    color: #374151 !important;
}


/* =========================================================
   HEADINGS
========================================================= */

h1,
h2,
h3,
h4,
h5,
h6 {
    color: #172554 !important;
}


/* =========================================================
   HERO SECTION
========================================================= */

.hero-box {
    background: linear-gradient(
        120deg,
        #2563eb,
        #4f46e5,
        #0891b2
    );

    padding: 45px;
    border-radius: 28px;
    text-align: center;

    margin-bottom: 35px;

    box-shadow:
        0 15px 35px rgba(37, 99, 235, 0.20);
}

.hero-box h1 {
    color: white !important;
    font-size: 46px;
    font-weight: 800;
}

.hero-box p {
    color: white !important;
    font-size: 18px;
    line-height: 1.7;
}


/* =========================================================
   SECTION HEADINGS
========================================================= */

.section-heading {
    font-size: 28px;
    font-weight: 750;
    color: #172554 !important;
    margin-top: 25px;
    margin-bottom: 8px;
}


/* =========================================================
   SIDEBAR
========================================================= */

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #eef7ff,
        #f5f1ff
    );
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    color: #111827 !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #172554 !important;
}


/* =========================================================
   BUTTONS
========================================================= */

.stButton > button {
    border-radius: 12px;
    font-weight: 600;
    min-height: 42px;
}


/* =========================================================
   CARDS
========================================================= */

.card {
    background: white;
    padding: 22px;
    border-radius: 20px;
    text-align: center;

    border: 1px solid #e2e8f0;

    box-shadow:
        0 7px 20px rgba(15, 23, 42, 0.06);
}


/* =========================================================
   ITINERARY
========================================================= */

.itinerary {
    background: white;
    padding: 25px;
    border-radius: 20px;

    border: 1px solid #e2e8f0;

    box-shadow:
        0 7px 20px rgba(15, 23, 42, 0.06);
}

.itinerary p {
    color: #111827 !important;
}


/* =========================================================
   METRICS
========================================================= */

[data-testid="stMetricValue"] {
    color: #172554 !important;
}

[data-testid="stMetricLabel"] {
    color: #374151 !important;
}


/* =========================================================
   ALERTS
========================================================= */

[data-testid="stAlert"] p {
    color: inherit !important;
}


/* =========================================================
   TABS
========================================================= */

button[data-baseweb="tab"] {
    color: #172554 !important;
    font-weight: 600;
}


/* =========================================================
   INPUT TEXT
========================================================= */

input {
    color: #111827 !important;
}

textarea {
    color: #111827 !important;
}


/* =========================================================
   DIVIDERS
========================================================= */

hr {
    border-color: #dbeafe;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🌍 Plan Your Journey")

st.sidebar.write(
    "Tell us about your dream trip."
)


destination = st.sidebar.text_input(
    "📍 Destination",
    value=st.session_state.selected_destination,
    placeholder="Example: Goa"
)

if destination:
    st.session_state.selected_destination = destination


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


st.sidebar.divider()

st.sidebar.subheader("💡 Quick Tip")

st.sidebar.info(
    "Choose your destination, budget and interests. "
    "Our AI will create a personalized travel experience."
)


# ============================================================
# BEAUTIFUL HOME PAGE
# ============================================================

st.markdown(
    """
    <div class="hero-box">
        <h1>✈️ AI Travel Assistant</h1>
        <p>
            Turn your travel ideas into unforgettable journeys.
            <br>
            Plan your itinerary, discover amazing places,
            manage your budget and get intelligent travel advice.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DESTINATION SECTION
# ============================================================

st.markdown(
    '<div class="section-heading">🌎 Where will your journey take you?</div>',
    unsafe_allow_html=True
)

st.write(
    "Explore popular destinations or enter your own destination in the sidebar."
)


d1, d2, d3, d4 = st.columns(4)


with d1:

    st.markdown("### 🏖️ Goa")
    st.caption("Beaches & nightlife")

    if st.button(
        "Explore Goa",
        key="goa",
        use_container_width=True
    ):

        st.session_state.selected_destination = "Goa"
        st.rerun()


with d2:

    st.markdown("### 🏔️ Manali")
    st.caption("Mountains & adventure")

    if st.button(
        "Explore Manali",
        key="manali",
        use_container_width=True
    ):

        st.session_state.selected_destination = "Manali"
        st.rerun()


with d3:

    st.markdown("### 🌴 Kerala")
    st.caption("Nature & backwaters")

    if st.button(
        "Explore Kerala",
        key="kerala",
        use_container_width=True
    ):

        st.session_state.selected_destination = "Kerala"
        st.rerun()


with d4:

    st.markdown("### 🏛️ Hyderabad")
    st.caption("Culture & food")

    if st.button(
        "Explore Hyderabad",
        key="hyderabad",
        use_container_width=True
    ):

        st.session_state.selected_destination = "Hyderabad"
        st.rerun()


# ============================================================
# TRAVEL MOODS
# ============================================================

st.write("")

st.markdown(
    '<div class="section-heading">✨ Choose your travel mood</div>',
    unsafe_allow_html=True
)

st.write(
    "Your mood helps personalize the kind of experience AI creates."
)


# ------------------------------------------------------------
# FIRST ROW
# ------------------------------------------------------------

m1, m2, m3 = st.columns(3)


with m1:

    st.markdown("### 🌊 Relax")
    st.caption("Peaceful and refreshing experiences")


with m2:

    st.markdown("### 🏔️ Adventure")
    st.caption("Exciting and thrilling activities")


with m3:

    st.markdown("### 👨‍👩‍👧‍👦 Family")
    st.caption("Fun and family-friendly places")


# ------------------------------------------------------------
# SECOND ROW
# ------------------------------------------------------------

m4, m5, m6 = st.columns(3)


with m4:

    st.markdown("### 🌿 Nature")
    st.caption("Scenic places and outdoor experiences")


with m5:

    st.markdown("### 🍜 Food")
    st.caption("Local food and culinary experiences")


with m6:

    st.markdown("### 🏛️ Culture")
    st.caption("History, heritage and traditions")


# ------------------------------------------------------------
# THIRD ROW
# ------------------------------------------------------------

m7, m8, m9 = st.columns(3)


with m7:

    st.markdown("### 🏙️ City Explorer")
    st.caption("Discover cities and urban attractions")


with m8:

    st.markdown("### 📸 Photography")
    st.caption("Beautiful and Instagram-worthy locations")


with m9:

    st.markdown("### 🌴 Leisure")
    st.caption("Relaxed sightseeing and free time")


# ============================================================
# FEATURES
# ============================================================

st.write("")

st.markdown(
    '<div class="section-heading">🚀 Everything you need for your trip</div>',
    unsafe_allow_html=True
)

st.write(
    "Your AI travel companion helps you plan every part of your journey."
)


f1, f2, f3, f4 = st.columns(4)


with f1:

    st.markdown("### 🤖 AI Trip Planner")

    st.write(
        "Create personalized day-by-day travel itineraries."
    )


with f2:

    st.markdown("### 💰 Budget Planning")

    st.write(
        "Plan your journey according to your budget."
    )


with f3:

    st.markdown("### 🧳 Packing Assistant")

    st.write(
        "Prepare your luggage using a simple checklist."
    )


with f4:

    st.markdown("### 💬 AI Travel Chat")

    st.write(
        "Ask questions and get intelligent travel advice."
    )


st.divider()


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
        '<div class="section-heading">🗺️ Create Your Travel Plan</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Give us your preferences and let AI design your journey."
    )


    # --------------------------------------------------------
    # TRIP SUMMARY
    # --------------------------------------------------------

    st.subheader("📋 Your Trip Summary")


    s1, s2, s3, s4 = st.columns(4)


    with s1:

        st.metric(
            "📍 Destination",
            destination if destination else "Not selected"
        )


    with s2:

        st.metric(
            "🗓️ Days",
            days
        )


    with s3:

        st.metric(
            "💰 Budget",
            budget
        )


    with s4:

        st.metric(
            "✨ Style",
            travel_style
        )


    st.write("")


    # --------------------------------------------------------
    # TRAVEL MOOD SELECTION
    # --------------------------------------------------------

    st.subheader("✨ Select Your Travel Mood")


    travel_mood = st.selectbox(
        "Choose the experience you want:",
        [
            "Relax",
            "Adventure",
            "Family",
            "Nature",
            "Food",
            "Culture",
            "City Explorer",
            "Photography",
            "Leisure"
        ]
    )


    st.session_state.travel_mood = travel_mood


    # --------------------------------------------------------
    # GENERATE TRAVEL PLAN
    # --------------------------------------------------------

    if st.button(
        "✨ Create My Travel Journey",
        use_container_width=True
    ):

        if not destination:

            st.warning(
                "📍 Please enter a destination in the sidebar."
            )

        else:

            interest_text = ", ".join(interests)


            if not interest_text:

                interest_text = (
                    "General sightseeing and local experiences"
                )


            prompt = f"""
You are an expert AI Travel Assistant.

Create a detailed {days}-day travel itinerary for {destination}.

Trip Details:

Destination: {destination}
Number of Days: {days}
Budget: {budget}
Travel Style: {travel_style}
Travel Mood: {travel_mood}
Interests: {interest_text}

The travel mood is important. Personalize the itinerary
according to the selected mood.

For example:

Relax:
Include peaceful locations, scenic spots and less crowded activities.

Adventure:
Include exciting outdoor activities and adventurous experiences.

Family:
Include safe, family-friendly places and activities.

Nature:
Include parks, waterfalls, mountains, beaches and natural attractions.

Food:
Include local restaurants, famous dishes and food experiences.

Culture:
Include historical places, museums, temples, monuments and local traditions.

City Explorer:
Include famous city attractions, markets, shopping areas and urban experiences.

Photography:
Include scenic viewpoints, beautiful locations and photography spots.

Leisure:
Include relaxed sightseeing, free time and comfortable activities.

Include:

1. Short trip overview
2. Day-by-day itinerary
3. Morning activities
4. Afternoon activities
5. Evening activities
6. Places to visit
7. Food recommendations
8. Transportation suggestions
9. Approximate daily expenses
10. Important travel tips

Make the itinerary realistic, practical and easy to understand.

Use clear headings for each day.
"""


            with st.spinner(
                "🤖 AI is designing your journey..."
            ):

                try:

                    response = get_response(prompt)

                    st.session_state.itinerary = response

                    st.success(
                        "🎉 Your personalized journey is ready!"
                    )

                except Exception as e:

                    st.error(
                        "Unable to connect to Ollama."
                    )

                    st.error(str(e))


    # --------------------------------------------------------
    # DISPLAY ITINERARY
    # --------------------------------------------------------

    if st.session_state.itinerary:

        st.divider()


        st.subheader(
            f"🌟 Your {days}-Day {destination} Journey"
        )


        st.info(
            f"✨ Travel Mood: {st.session_state.travel_mood}"
        )


        st.markdown(
            '<div class="itinerary">',
            unsafe_allow_html=True
        )


        st.write(
            st.session_state.itinerary
        )


        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


        st.write("")


        # ----------------------------------------------------
        # FAVOURITES
        # ----------------------------------------------------

        a1, a2, a3 = st.columns(3)


        with a1:

            if st.button(
                "❤️ Save Favourite",
                use_container_width=True
            ):

                st.session_state.favorite = destination

                st.success(
                    f"{destination} saved to favourites!"
                )


        with a2:

            if st.session_state.favorite:

                if st.button(
                    "💔 Remove Favourite",
                    use_container_width=True
                ):

                    removed = st.session_state.favorite

                    st.session_state.favorite = ""

                    st.success(
                        f"{removed} removed from favourites!"
                    )

            else:

                st.button(
                    "💔 No Favourite Saved",
                    disabled=True,
                    use_container_width=True
                )


        with a3:

            if st.button(
                "🔄 Reset Trip",
                use_container_width=True
            ):

                st.session_state.itinerary = ""
                st.session_state.favorite = ""
                st.session_state.travel_mood = ""

                st.rerun()


        if st.session_state.favorite:

            st.info(
                f"❤️ Favourite destination: "
                f"**{st.session_state.favorite}**"
            )


        # ----------------------------------------------------
        # PDF DOWNLOAD
        # ----------------------------------------------------

        st.write("")

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
                    label="📄 Download Travel Guide",
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


# ============================================================
# TAB 2 - AI CHATBOT
# ============================================================

with tab2:

    st.markdown(
        '<div class="section-heading">💬 Your AI Travel Companion</div>',
        unsafe_allow_html=True
    )


    st.write(
        "Ask anything about destinations, food, activities, "
        "transportation or travel planning."
    )


    st.subheader("💡 Popular Questions")


    q1, q2, q3, q4 = st.columns(4)


    with q1:

        st.info(
            "🌴 Best places to visit"
        )


    with q2:

        st.info(
            "🍴 Local food"
        )


    with q3:

        st.info(
            "💰 Budget tips"
        )


    with q4:

        st.info(
            "🚗 Transportation"
        )


    st.divider()


    # --------------------------------------------------------
    # DISPLAY CHAT HISTORY
    # --------------------------------------------------------

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.write(
                message["content"]
            )


    # --------------------------------------------------------
    # CHAT INPUT
    # --------------------------------------------------------

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
You are a friendly and knowledgeable AI Travel Assistant.

Conversation history:

{conversation}

Answer the latest user question clearly.

Give practical and useful travel advice.
"""


        with st.chat_message("assistant"):

            with st.spinner(
                "🤖 Thinking..."
            ):

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
        '<div class="section-heading">🧳 Smart Packing Checklist</div>',
        unsafe_allow_html=True
    )


    st.write(
        "Check the items as you pack for your journey."
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


    p1, p2 = st.columns(2)


    for index, item in enumerate(packing_items):

        if index % 2 == 0:

            with p1:

                if st.checkbox(
                    item,
                    key=f"packing_{index}"
                ):

                    selected_items.append(item)

        else:

            with p2:

                if st.checkbox(
                    item,
                    key=f"packing_{index}"
                ):

                    selected_items.append(item)


    st.write("")


    if selected_items:

        st.success(
            f"🎒 {len(selected_items)} items packed!"
        )


        st.subheader("✅ Packed Items")


        for item in selected_items:

            st.write(
                f"✓ {item}"
            )


    else:

        st.info(
            "Start checking items as you pack."
        )


# ============================================================
# TAB 4 - ABOUT
# ============================================================

with tab4:

    st.markdown(
        '<div class="section-heading">ℹ️ About AI Travel Assistant</div>',
        unsafe_allow_html=True
    )


    st.write(
        """
        ### ✈️ AI Travel Assistant

        AI Travel Assistant is an AI-powered travel planning
        application designed to help users create personalized
        and practical travel experiences.

        Users can provide their destination, trip duration,
        budget, travel style, travel mood and interests.
        The AI then creates a personalized itinerary using
        Llama 3.2:3b through Ollama.
        """
    )


    st.subheader("🛠️ Technologies Used")

    st.write("🐍 Python 3.12.0")
    st.write("🎨 Streamlit")
    st.write("🤖 Ollama")
    st.write("🧠 Llama 3.2:3b")
    st.write("📄 ReportLab")


    st.subheader("⭐ Main Features")

    st.write("✓ Personalized AI travel itineraries")
    st.write("✓ Destination-based planning")
    st.write("✓ Budget selection")
    st.write("✓ Travel style selection")
    st.write("✓ Travel mood personalization")
    st.write("✓ Interest-based recommendations")
    st.write("✓ Popular destination suggestions")
    st.write("✓ Favourite destination management")
    st.write("✓ Remove favourite option")
    st.write("✓ Smart packing checklist")
    st.write("✓ AI travel chatbot")
    st.write("✓ Conversation history")
    st.write("✓ PDF travel guide generation")
    st.write("✓ Reset and clear options")


    st.subheader("✨ Travel Mood Options")

    st.write("🌊 Relax")
    st.write("🏔️ Adventure")
    st.write("👨‍👩‍👧‍👦 Family")
    st.write("🌿 Nature")
    st.write("🍜 Food")
    st.write("🏛️ Culture")
    st.write("🏙️ City Explorer")
    st.write("📸 Photography")
    st.write("🌴 Leisure")


    st.success(
        "🤖 Powered by Llama 3.2:3b + Ollama"
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "✈️ AI Travel Assistant  •  "
    "Plan smarter • Travel better • Explore more 🌍"
)
