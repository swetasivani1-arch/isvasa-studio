import sqlite3
from pathlib import Path

import pandas as pd


DESIGN_DATABASE_PATH = Path("data/designs.db")


def get_design_connection():
    DESIGN_DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    connection = sqlite3.connect(
        DESIGN_DATABASE_PATH,
        check_same_thread=False,
    )

    connection.row_factory = sqlite3.Row

    return connection


def create_designs_table():
    connection = get_design_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS designs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            design_name TEXT NOT NULL,
            product_category TEXT NOT NULL,
            design_code TEXT,
            reference_image_path TEXT NOT NULL,
            design_notes TEXT,
            is_active INTEGER DEFAULT 1,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    connection.commit()
    connection.close()


def save_design(
    design_name,
    product_category,
    design_code,
    reference_image_path,
    design_notes,
):
    connection = get_design_connection()

    connection.execute(
        """
        INSERT INTO designs (
            design_name,
            product_category,
            design_code,
            reference_image_path,
            design_notes,
            is_active
        )
        VALUES (?, ?, ?, ?, ?, 1)
        """,
        (
            design_name,
            product_category,
            design_code,
            reference_image_path,
            design_notes,
        ),
    )

    connection.commit()
    connection.close()


def get_all_designs():
    connection = get_design_connection()

    designs_df = pd.read_sql_query(
        """
        SELECT *
        FROM designs
        ORDER BY
            product_category,
            design_name
        """,
        connection,
    )

    connection.close()

    return designs_df


def get_active_designs():
    connection = get_design_connection()

    designs_df = pd.read_sql_query(
        """
        SELECT *
        FROM designs
        WHERE is_active = 1
        ORDER BY
            product_category,
            design_name
        """,
        connection,
    )

    connection.close()

    return designs_df


def update_design_status(
    design_id,
    is_active,
):
    connection = get_design_connection()

    connection.execute(
        """
        UPDATE designs
        SET
            is_active = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (
            1 if is_active else 0,
            design_id,
        ),
    )

    connection.commit()
    connection.close()