from textwrap import dedent

import pandas as pd
import streamlit as st

from utils.database import (
    get_all_orders,
    get_order_counts,
)


def show_dashboard():
    counts = get_order_counts()
    orders_df = get_all_orders()

    show_dashboard_styles()
    show_dashboard_header()
    show_summary_cards(counts)

    st.markdown("<div class='section-gap'></div>", unsafe_allow_html=True)

    left_column, right_column = st.columns(
        [2, 1],
        gap="large",
    )

    with left_column:
        show_recent_orders(orders_df)

    with right_column:
        show_work_summary(counts)

    st.markdown("<div class='section-gap'></div>", unsafe_allow_html=True)

    show_product_summary(orders_df)


def show_dashboard_styles():
    st.markdown(
        """
<style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }

    .isvasa-header {
        background:
            linear-gradient(
                135deg,
                rgba(55, 73, 63, 0.95),
                rgba(24, 29, 27, 0.98)
            );
        border: 1px solid rgba(174, 190, 179, 0.18);
        border-radius: 22px;
        padding: 34px 36px;
        margin-bottom: 28px;
        box-shadow: 0 18px 50px rgba(0, 0, 0, 0.22);
    }

    .isvasa-title {
        font-size: 42px;
        font-weight: 700;
        color: #f6f3ec;
        margin: 0;
        line-height: 1.1;
    }

    .isvasa-tagline {
        margin-top: 8px;
        font-size: 17px;
        letter-spacing: 1.2px;
        color: #b8c8bd;
    }

    .isvasa-description {
        margin-top: 18px;
        max-width: 720px;
        font-size: 15px;
        line-height: 1.6;
        color: #d5ddd7;
    }

    .metric-card {
        background: #171c1a;
        border: 1px solid rgba(174, 190, 179, 0.14);
        border-radius: 18px;
        padding: 22px 22px 18px 22px;
        min-height: 120px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.18);
    }

    .metric-label {
        color: #aeb8b1;
        font-size: 14px;
        margin-bottom: 8px;
    }

    .metric-value {
        color: #f5f2eb;
        font-size: 34px;
        font-weight: 700;
        line-height: 1;
    }

    .metric-note {
        color: #7f9186;
        font-size: 12px;
        margin-top: 10px;
    }

    .panel-card {
        background: #151a18;
        border: 1px solid rgba(174, 190, 179, 0.14);
        border-radius: 18px;
        padding: 22px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.16);
    }

    .section-title {
        color: #f4f1ea;
        font-size: 22px;
        font-weight: 650;
        margin-bottom: 14px;
    }

    .summary-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 13px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        color: #d6ddd8;
    }

    .summary-item:last-child {
        border-bottom: none;
    }

    .summary-value {
        font-weight: 700;
        color: #f0d9a0;
    }

    .attention-box {
        background: rgba(151, 93, 62, 0.18);
        border: 1px solid rgba(205, 139, 99, 0.28);
        border-radius: 14px;
        padding: 14px;
        margin-top: 16px;
        color: #f0c7ad;
    }

    .success-box {
        background: rgba(67, 109, 82, 0.22);
        border: 1px solid rgba(111, 162, 127, 0.28);
        border-radius: 14px;
        padding: 14px;
        margin-top: 16px;
        color: #c8dfce;
    }

    .section-gap {
        height: 18px;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid rgba(174, 190, 179, 0.12);
        border-radius: 14px;
        overflow: hidden;
    }
</style>
        """,
        unsafe_allow_html=True,
    )


def show_dashboard_header():
    st.markdown(
        """
<div class="isvasa-header">
    <div class="isvasa-title">ISVASA Studio</div>
    <div class="isvasa-tagline">
        Manage • Create • Personalise
    </div>
    <div class="isvasa-description">
        Your central workspace for managing orders,
        personalised products, customer requirements
        and production activity.
    </div>
</div>
        """,
        unsafe_allow_html=True,
    )


def show_summary_cards(counts):
    row1_col1, row1_col2, row1_col3 = st.columns(
        3,
        gap="large",
    )

    with row1_col1:
        metric_card(
            "Total Orders",
            counts["total_orders"],
            "All saved order items",
        )

    with row1_col2:
        metric_card(
            "Pending Orders",
            counts["pending_orders"],
            "Still in progress",
        )

    with row1_col3:
        metric_card(
            "Completed Orders",
            counts["completed_orders"],
            "Finished production",
        )

    row2_col1, row2_col2, row2_col3 = st.columns(
        3,
        gap="large",
    )

    with row2_col1:
        metric_card(
            "Crown Orders",
            counts["crown_orders"],
            "Current crown items",
        )

    with row2_col2:
        metric_card(
            "Diary Orders",
            counts["diary_orders"],
            "Current diary items",
        )

    with row2_col3:
        metric_card(
            "Needs Review",
            counts["missing_customization"],
            "Customization requires attention",
        )


def metric_card(label, value, note):
    st.markdown(
        f"""
<div class="metric-card">
    <div class="metric-label">{label}</div>
    <div class="metric-value">{value}</div>
    <div class="metric-note">{note}</div>
</div>
        """,
        unsafe_allow_html=True,
    )


def show_recent_orders(orders_df):
    st.markdown(
        """
<div class="section-title">Recent Orders</div>
        """,
        unsafe_allow_html=True,
    )

    if orders_df.empty:
        st.info("No orders have been saved yet.")
        return

    recent_orders = orders_df.head(8).copy()

    preferred_columns = [
        "order_date",
        "order_id",
        "buyer_name",
        "product_category",
        "embroidered_name",
        "add_any_name_or_text",
        "production_status",
    ]

    available_columns = [
        column
        for column in preferred_columns
        if column in recent_orders.columns
    ]

    recent_orders = recent_orders[
        available_columns
    ]

    recent_orders = recent_orders.rename(
        columns={
            "order_date": "Order Date",
            "order_id": "Order ID",
            "buyer_name": "Buyer",
            "product_category": "Product",
            "embroidered_name": "Name",
            "add_any_name_or_text": "Personalised Text",
            "production_status": "Status",
        }
    )

    st.dataframe(
        recent_orders,
        use_container_width=True,
        hide_index=True,
    )


def show_work_summary(counts):
    review_count = counts["missing_customization"]

    with st.container(border=True):
        st.subheader("Work Summary")

        row1_col1, row1_col2 = st.columns([3, 1])

        with row1_col1:
            st.write("Orders awaiting work")

        with row1_col2:
            st.metric(
                label="",
                value=counts["pending_orders"],
            )

        row2_col1, row2_col2 = st.columns([3, 1])

        with row2_col1:
            st.write("Customization review")

        with row2_col2:
            st.metric(
                label="",
                value=review_count,
            )

        row3_col1, row3_col2 = st.columns([3, 1])

        with row3_col1:
            st.write("Completed orders")

        with row3_col2:
            st.metric(
                label="",
                value=counts["completed_orders"],
            )

        st.divider()

        if review_count > 0:
            st.warning(
                f"{review_count} order items require customization review."
            )
        else:
            st.success(
                "No customization issues are pending."
            )

def show_product_summary(orders_df):
    st.markdown(
        """
<div class="section-title">
    Orders by Product
</div>
        """,
        unsafe_allow_html=True,
    )

    if orders_df.empty:
        st.info(
            "Product summary will appear after orders are imported."
        )
        return

    product_summary = (
        orders_df["product_category"]
        .fillna("Other")
        .replace("", "Other")
        .value_counts()
        .reset_index()
    )

    product_summary.columns = [
        "Product",
        "Orders",
    ]

    chart_data = product_summary.set_index(
        "Product"
    )

    st.bar_chart(chart_data)