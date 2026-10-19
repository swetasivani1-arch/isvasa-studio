import pandas as pd
import streamlit as st
from utils.database import save_orders_dataframe

from utils.order_processor import (
    create_clean_orders_dataframe,
    detect_etsy_columns,
    remove_price_columns,
)


def show_import_orders():
    st.title("📥 Import Etsy Orders")

    st.write(
        "Upload the Etsy CSV file that you download manually."
    )

    uploaded_file = st.file_uploader(
        "Choose an Etsy CSV file",
        type=["csv"],
    )

    if uploaded_file is None:
        st.info(
            "Select an Etsy CSV file to begin."
        )
        return
    st.session_state["uploaded_filename"] = uploaded_file.name

    try:
        original_df = pd.read_csv(
            uploaded_file
        )

        st.success(
            f"File loaded successfully: {uploaded_file.name}"
        )

        information_column1, information_column2 = st.columns(2)

        with information_column1:
            st.metric(
                "Original Rows",
                len(original_df),
            )

        with information_column2:
            st.metric(
                "Original Columns",
                len(original_df.columns),
            )

        cleaned_source_df = remove_price_columns(
            original_df
        )

        detected_columns = detect_etsy_columns(
            cleaned_source_df
        )

        cleaned_orders_df = create_clean_orders_dataframe(
            cleaned_source_df,
            detected_columns,
        )

        show_detected_columns(
            detected_columns
        )

        show_product_summary(
            cleaned_orders_df
        )

        show_cleaned_orders(
            cleaned_orders_df,
            original_df,
            cleaned_source_df,
        )

    except Exception as error:
        st.error(
            f"Unable to process this CSV file: {error}"
        )


def show_detected_columns(
    detected_columns,
):
    st.subheader("Detected Etsy Columns")

    detection_table = pd.DataFrame(
        [
            {
                "Required Field": field,
                "Detected CSV Column": (
                    column
                    if column
                    else "Not Found"
                ),
            }
            for field, column
            in detected_columns.items()
        ]
    )

    st.dataframe(
        detection_table,
        use_container_width=True,
        hide_index=True,
    )

    required_fields = [
        "order_id",
        "order_date",
        "buyer_name",
        "product_title",
    ]

    missing_required_fields = [
        field
        for field in required_fields
        if detected_columns.get(field) is None
    ]

    optional_fields = [
        field
        for field, column
        in detected_columns.items()
        if column is None
        and field not in required_fields
    ]

    if missing_required_fields:
        st.error(
            "Required columns were not detected: "
            + ", ".join(missing_required_fields)
        )

    if optional_fields:
        st.warning(
            "Optional columns were not detected: "
            + ", ".join(optional_fields)
        )

    if (
        not missing_required_fields
        and not optional_fields
    ):
        st.success(
            "All expected columns were detected."
        )


def show_product_summary(
    cleaned_orders_df,
):
    st.subheader("Product Summary")

    product_summary = (
        cleaned_orders_df[
            "Product Category"
        ]
        .value_counts()
        .reset_index()
    )

    product_summary.columns = [
        "Product Category",
        "Number of Orders",
    ]

    st.dataframe(
        product_summary,
        use_container_width=True,
        hide_index=True,
    )


def show_cleaned_orders(
    cleaned_orders_df,
    original_df,
    cleaned_source_df,
):
    st.subheader("Cleaned Order Preview")

    status_options = sorted(
        cleaned_orders_df[
            "Customization Status"
        ]
        .dropna()
        .unique()
        .tolist()
    )

    status_filter = st.multiselect(
        "Filter by Customization Status",
        options=status_options,
        default=status_options,
    )

    category_options = sorted(
        cleaned_orders_df[
            "Product Category"
        ]
        .dropna()
        .unique()
        .tolist()
    )

    category_filter = st.multiselect(
        "Filter by Product Category",
        options=category_options,
        default=category_options,
    )

    filtered_orders_df = cleaned_orders_df[
        cleaned_orders_df[
            "Product Category"
        ].isin(category_filter)
        &
        cleaned_orders_df[
            "Customization Status"
        ].isin(status_filter)
    ]

    missing_customization_count = len(
        cleaned_orders_df[
            cleaned_orders_df[
                "Customization Status"
            ].isin(
                [
                    "Missing",
                    "Needs Review",
                ]
            )
        ]
    )

    if missing_customization_count > 0:
        st.warning(
            "Orders requiring customization review: "
            f"{missing_customization_count}"
        )
    else:
        st.success(
            "All orders have customization information."
        )

    st.dataframe(
        filtered_orders_df,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    if st.button(
        "Save Orders to Database",
        type="primary",
        use_container_width=True,
    ):
        inserted_count, updated_count = (
            save_orders_dataframe(
                cleaned_orders_df,
                st.session_state.get(
                    "uploaded_filename",
                    "etsy_orders.csv",
                ),
            )
        )

        st.success(
            f"New order items saved: {inserted_count}. "
            f"Existing order items updated: {updated_count}."
        )

    removed_column_count = (
        len(original_df.columns)
        - len(cleaned_source_df.columns)
    )

    st.write(
        "Removed pricing and tax-related columns: "
        f"{removed_column_count}"
    )

    cleaned_csv = filtered_orders_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Cleaned Orders",
        data=cleaned_csv,
        file_name="cleaned_etsy_orders.csv",
        mime="text/csv",
    )