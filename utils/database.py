import sqlite3
from pathlib import Path

import pandas as pd


DATABASE_PATH = Path("data/orders.db")


def get_connection():
    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    connection = sqlite3.connect(
        DATABASE_PATH,
        check_same_thread=False,
    )

    connection.row_factory = sqlite3.Row

    return connection

def add_column_if_missing(
    connection,
    table_name,
    column_name,
    column_type,
):
    existing_columns = connection.execute(
        f"PRAGMA table_info({table_name})"
    ).fetchall()

    existing_column_names = {
        column[1]
        for column in existing_columns
    }

    if column_name not in existing_column_names:
        connection.execute(
            f"""
            ALTER TABLE {table_name}
            ADD COLUMN {column_name} {column_type}
            """
        )


def create_orders_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            order_id TEXT NOT NULL,
            transaction_id TEXT NOT NULL,

            order_date TEXT,
            buyer_name TEXT,
            recipient_name TEXT,

            product_category TEXT,
            product_title TEXT,

            embroidered_name TEXT,
            add_any_name_or_text TEXT,
            product_colour TEXT,
            thread_colour TEXT,
            design TEXT,
            initials TEXT,
            custom_date TEXT,
            vows_text TEXT,
            font TEXT,
            size TEXT,

            quantity TEXT,

            customization_status TEXT,
            production_status TEXT,
            image_status TEXT,
            tracing_status TEXT,

            personalization TEXT,
            notes TEXT,

            import_filename TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            UNIQUE(order_id, transaction_id)
        )
        """
    )

    add_column_if_missing(
        connection=connection,
        table_name="orders",
        column_name="add_any_name_or_text",
        column_type="TEXT",
    )

    connection.commit()
    connection.close()

def clean_database_value(value):
    if pd.isna(value):
        return ""

    return str(value).strip()


def save_orders_dataframe(
    orders_dataframe,
    import_filename,
):
    connection = get_connection()
    cursor = connection.cursor()

    inserted_count = 0
    updated_count = 0

    for row_number, row in orders_dataframe.iterrows():
        order_id = clean_database_value(
            row.get("Order ID", "")
        )

        transaction_id = clean_database_value(
            row.get("Transaction ID", "")
        )

        if not transaction_id:
            transaction_id = (
                f"{order_id}-{row_number}"
            )

        existing_order = cursor.execute(
            """
            SELECT id
            FROM orders
            WHERE order_id = ?
            AND transaction_id = ?
            """,
            (
                order_id,
                transaction_id,
            ),
        ).fetchone()

        values = {
            "order_id": order_id,
            "transaction_id": transaction_id,
            "order_date": clean_database_value(
                row.get("Order Date", "")
            ),
            "buyer_name": clean_database_value(
                row.get("Buyer Name", "")
            ),
            "recipient_name": clean_database_value(
                row.get("Recipient Name", "")
            ),
            "product_category": clean_database_value(
                row.get("Product Category", "")
            ),
            "product_title": clean_database_value(
                row.get("Product Title", "")
            ),
            "embroidered_name": clean_database_value(
                row.get("Embroidered Name", "")
            ),
            "product_colour": clean_database_value(
                row.get("Product Colour", "")
            ),
            "add_any_name_or_text": clean_database_value(
                row.get("Add Any Name or Text", "")
            ),
            "thread_colour": clean_database_value(
                row.get("Thread Colour", "")
            ),
            "design": clean_database_value(
                row.get("Design", "")
            ),
            "initials": clean_database_value(
                row.get("Initials", "")
            ),
            "custom_date": clean_database_value(
                row.get("Custom Date", "")
            ),
            "vows_text": clean_database_value(
                row.get("Vows / Text", "")
            ),
            "font": clean_database_value(
                row.get("Font", "")
            ),
            "size": clean_database_value(
                row.get("Size", "")
            ),
            "quantity": clean_database_value(
                row.get("Quantity", "")
            ),
            "customization_status": clean_database_value(
                row.get(
                    "Customization Status",
                    "Needs Review",
                )
            ),
            "production_status": clean_database_value(
                row.get(
                    "Production Status",
                    "New",
                )
            ),
            "image_status": clean_database_value(
                row.get(
                    "Image Status",
                    "Pending",
                )
            ),
            "tracing_status": clean_database_value(
                row.get(
                    "Tracing Status",
                    "Pending",
                )
            ),
            "personalization": clean_database_value(
                row.get("Personalization", "")
            ),
            "notes": clean_database_value(
                row.get("Notes", "")
            ),
            "import_filename": import_filename,
        }

        if existing_order:
            cursor.execute(
                """
                UPDATE orders
                SET
                    order_date = :order_date,
                    buyer_name = :buyer_name,
                    recipient_name = :recipient_name,
                    product_category = :product_category,
                    product_title = :product_title,
                    embroidered_name = :embroidered_name,
                    add_any_name_or_text = :add_any_name_or_text,
                    product_colour = :product_colour,
                    thread_colour = :thread_colour,
                    design = :design,
                    initials = :initials,
                    custom_date = :custom_date,
                    vows_text = :vows_text,
                    font = :font,
                    size = :size,
                    quantity = :quantity,
                    customization_status = :customization_status,
                    personalization = :personalization,
                    notes = :notes,
                    import_filename = :import_filename,
                    updated_at = CURRENT_TIMESTAMP
                WHERE order_id = :order_id
                AND transaction_id = :transaction_id
                """,
                values,
            )

            updated_count += 1

        else:
            cursor.execute(
                """
                INSERT INTO orders (
                    order_id,
                    transaction_id,
                    order_date,
                    buyer_name,
                    recipient_name,
                    product_category,
                    product_title,
                    embroidered_name,
                    add_any_name_or_text,
                    product_colour,
                    thread_colour,
                    design,
                    initials,
                    custom_date,
                    vows_text,
                    font,
                    size,
                    quantity,
                    customization_status,
                    production_status,
                    image_status,
                    tracing_status,
                    personalization,
                    notes,
                    import_filename
                )
                VALUES (
                    :order_id,
                    :transaction_id,
                    :order_date,
                    :buyer_name,
                    :recipient_name,
                    :product_category,
                    :product_title,
                    :embroidered_name,
                    :add_any_name_or_text,
                    :product_colour,
                    :thread_colour,
                    :design,
                    :initials,
                    :custom_date,
                    :vows_text,
                    :font,
                    :size,
                    :quantity,
                    :customization_status,
                    :production_status,
                    :image_status,
                    :tracing_status,
                    :personalization,
                    :notes,
                    :import_filename
                )
                """,
                values,
            )

            inserted_count += 1

    connection.commit()
    connection.close()

    return inserted_count, updated_count


def get_all_orders():
    connection = get_connection()

    query = """
        SELECT *
        FROM orders
        ORDER BY
            order_date DESC,
            id DESC
    """

    orders_dataframe = pd.read_sql_query(
        query,
        connection,
    )

    connection.close()

    return orders_dataframe


def get_order_counts():
    connection = get_connection()
    cursor = connection.cursor()

    total_orders = cursor.execute(
        """
        SELECT COUNT(*)
        FROM orders
        """
    ).fetchone()[0]

    pending_orders = cursor.execute(
        """
        SELECT COUNT(*)
        FROM orders
        WHERE production_status != 'Completed'
        """
    ).fetchone()[0]

    completed_orders = cursor.execute(
        """
        SELECT COUNT(*)
        FROM orders
        WHERE production_status = 'Completed'
        """
    ).fetchone()[0]

    crown_orders = cursor.execute(
        """
        SELECT COUNT(*)
        FROM orders
        WHERE product_category = 'Crown'
        """
    ).fetchone()[0]

    diary_orders = cursor.execute(
        """
        SELECT COUNT(*)
        FROM orders
        WHERE product_category = 'Diary'
        """
    ).fetchone()[0]

    missing_customization = cursor.execute(
        """
        SELECT COUNT(*)
        FROM orders
        WHERE customization_status IN (
            'Missing',
            'Needs Review'
        )
        """
    ).fetchone()[0]

    connection.close()

    return {
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "completed_orders": completed_orders,
        "crown_orders": crown_orders,
        "diary_orders": diary_orders,
        "missing_customization": missing_customization,
    }