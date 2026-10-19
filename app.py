import streamlit as st

from utils.database import create_orders_table
from utils.design_database import create_designs_table
from views.creative_studio import show_creative_studio
from views.dashboard import show_dashboard
from views.design_library import show_design_library
from views.import_orders import show_import_orders
from views.master_orders import show_master_orders



st.set_page_config(
    page_title="ISVASA Studio",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)


create_orders_table()
create_designs_table()


st.markdown(
    """
<style>
    .block-container {
        padding-top: 1.5rem;
    }

    [data-testid="stAppViewContainer"] {
        background-color: #0d1110;
    }

    [data-testid="stSidebar"] {
        background-color: #131816;
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }

    [data-testid="stSidebarContent"] {
        padding-top: 1.25rem;
    }

    .isvasa-sidebar-title {
        font-size: 27px;
        font-weight: 700;
        color: #f4f1ea;
        margin-bottom: 4px;
    }

    .isvasa-sidebar-tagline {
        font-size: 13px;
        color: #91a096;
        margin-bottom: 24px;
        letter-spacing: 0.4px;
    }

    .stButton > button {
        border-radius: 10px;
    }

    div[data-testid="stRadio"] label {
        padding-top: 4px;
        padding-bottom: 4px;
    }
</style>
    """,
    unsafe_allow_html=True,
)


st.sidebar.markdown(
    """
<div class="isvasa-sidebar-title">
    ISVASA Studio
</div>

<div class="isvasa-sidebar-tagline">
    Manage • Create • Personalise
</div>
    """,
    unsafe_allow_html=True,
)


page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Import Orders",
        "Master Orders",
        "Design Library",
        "Creative Studio",
        "Customers",
        "Reports",
    ],
)

if page == "Dashboard":
    show_dashboard()

elif page == "Import Orders":
    show_import_orders()

elif page == "Master Orders":
    show_master_orders()

elif page == "Design Library":
    show_design_library()

elif page == "Creative Studio":
    show_creative_studio()

else:
    st.title(page)

    st.info(
        f"The {page} page will be added later."
    )