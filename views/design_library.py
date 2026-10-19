from pathlib import Path

import streamlit as st

from utils.design_database import (
    get_all_designs,
    save_design,
    update_design_status,
)


DESIGN_IMAGE_DIRECTORY = Path(
    "images/design_library"
)


PRODUCT_CATEGORIES = [
    "Crown",
    "Diary",
    "Apron",
    "Blanket",
    "Cushion",
    "Tote Bag",
    "Other",
]


def show_design_library():
    st.title("Design Library")

    st.caption(
        "Upload and organise predefined ISVASA product designs."
    )

    upload_design_section()

    st.divider()

    display_design_library()


def upload_design_section():
    st.subheader("Add New Design")

    with st.form(
        "add_design_form",
        clear_on_submit=True,
    ):
        design_name = st.text_input(
            "Design Name",
            placeholder="Example: Floral Crown Design 01",
        )

        product_category = st.selectbox(
            "Product Category",
            options=PRODUCT_CATEGORIES,
        )

        design_code = st.text_input(
            "Design Code",
            placeholder="Example: CR-FL-001",
        )

        design_notes = st.text_area(
            "Design Notes",
            placeholder=(
                "Describe important fixed details such as "
                "flower placement, border, layout or styling."
            ),
        )

        reference_image = st.file_uploader(
            "Upload Reference Design Image",
            type=[
                "png",
                "jpg",
                "jpeg",
                "webp",
            ],
        )

        submitted = st.form_submit_button(
            "Save Design",
            type="primary",
            use_container_width=True,
        )

        if submitted:
            if not design_name.strip():
                st.error(
                    "Please enter a design name."
                )
                return

            if reference_image is None:
                st.error(
                    "Please upload a reference design image."
                )
                return

            DESIGN_IMAGE_DIRECTORY.mkdir(
                parents=True,
                exist_ok=True,
            )

            file_extension = Path(
                reference_image.name
            ).suffix.lower()

            safe_design_name = (
                design_name
                .strip()
                .lower()
                .replace(" ", "_")
                .replace("/", "_")
            )

            saved_filename = (
                f"{product_category.lower().replace(' ', '_')}"
                f"_{safe_design_name}"
                f"{file_extension}"
            )

            saved_path = (
                DESIGN_IMAGE_DIRECTORY
                / saved_filename
            )

            saved_path.write_bytes(
                reference_image.getbuffer()
            )

            save_design(
                design_name=design_name.strip(),
                product_category=product_category,
                design_code=design_code.strip(),
                reference_image_path=str(saved_path),
                design_notes=design_notes.strip(),
            )

            st.success(
                "Design saved successfully."
            )

            st.rerun()


def display_design_library():
    st.subheader("Saved Designs")

    designs_df = get_all_designs()

    if designs_df.empty:
        st.info(
            "No designs have been uploaded yet."
        )
        return

    category_options = sorted(
        designs_df[
            "product_category"
        ]
        .dropna()
        .unique()
        .tolist()
    )

    selected_categories = st.multiselect(
        "Filter by Product Category",
        options=category_options,
        default=category_options,
    )

    filtered_designs_df = designs_df[
        designs_df[
            "product_category"
        ].isin(selected_categories)
    ]

    for _, design in filtered_designs_df.iterrows():
        with st.container(border=True):
            column1, column2 = st.columns(
                [1, 2]
            )

            with column1:
                image_path = design[
                    "reference_image_path"
                ]

                if (
                    image_path
                    and Path(image_path).exists()
                ):
                    st.image(
                        image_path,
                        use_container_width=True,
                    )
                else:
                    st.warning(
                        "Reference image not found."
                    )

            with column2:
                st.subheader(
                    design["design_name"]
                )

                st.write(
                    f"**Product:** "
                    f"{design['product_category']}"
                )

                st.write(
                    f"**Design Code:** "
                    f"{design['design_code'] or 'Not provided'}"
                )

                st.write(
                    f"**Notes:** "
                    f"{design['design_notes'] or 'No notes'}"
                )

                is_active = bool(
                    design["is_active"]
                )

                new_status = st.checkbox(
                    "Active Design",
                    value=is_active,
                    key=f"design_status_{design['id']}",
                )

                if new_status != is_active:
                    update_design_status(
                        design_id=design["id"],
                        is_active=new_status,
                    )

                    st.rerun()