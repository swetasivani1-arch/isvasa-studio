import re

import pandas as pd


PRICE_COLUMNS_KEYWORDS = [
    "price",
    "tax",
    "vat",
    "currency",
    "discount",
    "subtotal",
    "total",
    "fee",
    "shipping cost",
]


def normalize_column_name(column_name):
    return (
        str(column_name)
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
    )


def remove_price_columns(dataframe):
    columns_to_remove = []

    for column in dataframe.columns:
        normalized_column = normalize_column_name(column)

        if any(
            keyword.replace(" ", "_") in normalized_column
            for keyword in PRICE_COLUMNS_KEYWORDS
        ):
            columns_to_remove.append(column)

    return dataframe.drop(
        columns=columns_to_remove,
        errors="ignore",
    )


def find_column(dataframe, possible_names):
    normalized_columns = {
        normalize_column_name(column): column
        for column in dataframe.columns
    }

    for possible_name in possible_names:
        normalized_possible_name = normalize_column_name(
            possible_name
        )

        if normalized_possible_name in normalized_columns:
            return normalized_columns[
                normalized_possible_name
            ]

    return None


def detect_etsy_columns(dataframe):
    return {
        "order_id": find_column(
            dataframe,
            [
                "Order ID",
                "Receipt ID",
                "Sale ID",
            ],
        ),
        "order_date": find_column(
            dataframe,
            [
                "Sale Date",
                "Order Date",
                "Date",
            ],
        ),
        "buyer_name": find_column(
            dataframe,
            [
                "Buyer",
                "Buyer Name",
                "Buyer User ID",
                "Full Name",
                "Customer Name",
            ],
        ),
        "recipient_name": find_column(
            dataframe,
            [
                "Ship Name",
                "Recipient Name",
                "Delivery Name",
            ],
        ),
        "product_title": find_column(
            dataframe,
            [
                "Item Name",
                "Title",
                "Product Name",
            ],
        ),
        "personalization": find_column(
            dataframe,
            [
                "Personalization",
                "Personalisation",
                "Customization",
                "Customisation",
                "Variations",
            ],
        ),
        "quantity": find_column(
            dataframe,
            [
                "Quantity",
                "Qty",
            ],
        ),
        "transaction_id": find_column(
            dataframe,
            [
                "Transaction ID",
                "Listing ID",
            ],
        ),
    }


def categorize_product(product_title):
    title = str(product_title).strip().lower()

    if "crown" in title:
        return "Crown"

    if "diary" in title:
        return "Diary" 
           
    if "apron" in title:
        return "Apron"

    return "Other"


def extract_value(text, labels):
    text = str(text or "").strip()

    for label in labels:
        pattern = (
            rf"(?:^|[\n,;|])\s*"
            rf"{re.escape(label)}"
            rf"\s*[:=\-]\s*"
            rf"([^,\n;|]+)"
        )

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if match:
            return match.group(1).strip()

    return ""


def extract_name_from_text(text):
    return extract_value(
        text,
        [
            "name",
            "embroidered name",
            "personalised name",
            "personalized name",
            "name on product",
            "child name",
            "baby name",
        ],
    )
def extract_add_any_name_or_text(text):
    return extract_value(
        text,
        [
            "add any name or text",
            "Add any name or Text",
            "name or text",
        ],
    )

def extract_product_colour(text):
    return extract_value(
        text,
        [
            "product colour",
            "product color",
            "crown colour",
            "crown color",
            "diary colour",
            "diary color",
            "fabric colour",
            "fabric color",
            "colour",
            "color",
        ],
    )


def extract_thread_colour(text):
    return extract_value(
        text,
        [
            "thread colour",
            "thread color",
            "embroidery colour",
            "embroidery color",
            "font colour",
            "font color",
        ],
    )


def extract_design(text):
    return extract_value(
        text,
        [
            "design",
            "design number",
            "style",
            "pattern",
            "flower design",
        ],
    )


def extract_initials(text):
    return extract_value(
        text,
        [
            "initials",
            "initial",
            "monogram",
        ],
    )


def extract_custom_date(text):
    return extract_value(
        text,
        [
            "date",
            "wedding date",
            "birth date",
            "event date",
        ],
    )


def extract_vows(text):
    return extract_value(
        text,
        [
            "vows",
            "vow text",
            "journal text",
            "book text",
            "text",
        ],
    )


def extract_font(text):
    return extract_value(
        text,
        [
            "font",
            "font style",
            "writing style",
        ],
    )


def extract_size(text):
    return extract_value(
        text,
        [
            "size",
            "crown size",
            "book size",
        ],
    )


def determine_customization_status(row):
    category = row["Product Category"]

    embroidered_name = str(
        row["Embroidered Name"]
    ).strip()

    product_colour = str(
        row["Product Colour"]
    ).strip()

    thread_colour = str(
        row["Thread Colour"]
    ).strip()

    personalization = str(
        row["Personalization"]
    ).strip()

    if not personalization:
        return "Missing"

    if category == "Crown":
        if (
            embroidered_name
            and product_colour
            and thread_colour
        ):
            return "Complete"

        return "Needs Review"

    if category == "Diary":
        if embroidered_name or row["Initials"]:
            return "Complete"

        return "Needs Review"

    return "Needs Review"


def create_clean_orders_dataframe(
    dataframe,
    detected_columns,
):
    cleaned_data = pd.DataFrame()

    column_mapping = {
        "Order ID": detected_columns.get("order_id"),
        "Order Date": detected_columns.get("order_date"),
        "Buyer Name": detected_columns.get("buyer_name"),
        "Recipient Name": detected_columns.get(
            "recipient_name"
        ),
        "Product Title": detected_columns.get(
            "product_title"
        ),
        "Personalization": detected_columns.get(
            "personalization"
        ),
        "Quantity": detected_columns.get("quantity"),
        "Transaction ID": detected_columns.get(
            "transaction_id"
        ),
    }

    for output_column, source_column in column_mapping.items():
        if source_column:
            cleaned_data[output_column] = dataframe[
                source_column
            ]
        else:
            cleaned_data[output_column] = ""

    cleaned_data = cleaned_data.fillna("")

    cleaned_data["Product Category"] = cleaned_data[
        "Product Title"
    ].apply(categorize_product)

    cleaned_data["Embroidered Name"] = cleaned_data[
        "Personalization"
    ].apply(extract_name_from_text)

    cleaned_data["Add Any Name or Text"] = cleaned_data[
    "Personalization"
    ].apply(extract_add_any_name_or_text)

    cleaned_data["Product Colour"] = cleaned_data[
        "Personalization"
    ].apply(extract_product_colour)

    cleaned_data["Thread Colour"] = cleaned_data[
        "Personalization"
    ].apply(extract_thread_colour)

    cleaned_data["Design"] = cleaned_data[
        "Personalization"
    ].apply(extract_design)

    cleaned_data["Initials"] = cleaned_data[
        "Personalization"
    ].apply(extract_initials)

    cleaned_data["Custom Date"] = cleaned_data[
        "Personalization"
    ].apply(extract_custom_date)

    cleaned_data["Vows / Text"] = cleaned_data[
        "Personalization"
    ].apply(extract_vows)

    cleaned_data["Font"] = cleaned_data[
        "Personalization"
    ].apply(extract_font)

    cleaned_data["Size"] = cleaned_data[
        "Personalization"
    ].apply(extract_size)

    cleaned_data["Notes"] = cleaned_data[
        "Personalization"
    ]

    cleaned_data["Customization Status"] = cleaned_data.apply(
        determine_customization_status,
        axis=1,
    )

    cleaned_data["Production Status"] = "New"
    cleaned_data["Image Status"] = "Pending"
    cleaned_data["Tracing Status"] = "Pending"

    preferred_columns = [
        "Order ID",
        "Order Date",
        "Buyer Name",
        "Recipient Name",
        "Product Category",
        "Product Title",
        "Embroidered Name",
        "Add Any Name or Text",
        "Product Colour",
        "Thread Colour",
        "Design",
        "Initials",
        "Custom Date",
        "Vows / Text",
        "Font",
        "Size",
        "Quantity",
        "Customization Status",
        "Production Status",
        "Image Status",
        "Tracing Status",
        "Personalization",
        "Notes",
        "Transaction ID",
    ]

    return cleaned_data[preferred_columns]