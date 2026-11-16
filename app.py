
import streamlit as st
import pandas as pd

from database import db
from modules import patient_service
from modules.ai_service import generate_health_remarks


st.set_page_config(
    page_title="Health Prediction Application",
    page_icon="🩺",
    layout="wide"
)

# Initialize the database and patient service
patient_service.initialize_patient_service()


st.title("🩺 Health Prediction Application")
st.write(
    "Register patients, manage blood test records, and generate "
    "AI-assisted health observations."
)

st.warning(
    "Important: AI-generated remarks are informational only and are "
    "not a medical diagnosis. Please consult a qualified healthcare "
    "professional for medical interpretation."
)


def get_patient_options():
    patients = patient_service.list_patients()

    return {
        f"{patient['id']} - {patient['full_name']}": patient["id"]
        for patient in patients
    }


def generate_and_save_remarks(patient_id):
    patient = patient_service.get_patient(patient_id)

    remarks = generate_health_remarks(
        patient["dob"],
        patient["glucose"],
        patient["haemoglobin"],
        patient["cholesterol"]
    )

    db.update_patient_remarks(patient_id, remarks)
    return remarks


tab_add, tab_records, tab_edit, tab_delete, tab_ai = st.tabs(
    [
        "Add Patient",
        "Patient Records",
        "Edit Patient",
        "Delete Patient",
        "AI Remarks"
    ]
)


# --------------------------------------------------
# ADD PATIENT
# --------------------------------------------------

with tab_add:
    st.subheader("Register a New Patient")

    with st.form("add_patient_form"):
        full_name = st.text_input("Full Name")
        dob = st.text_input(
            "Date of Birth",
            placeholder="DD/MM/YYYY"
        )
        email = st.text_input("Email Address")

        col1, col2, col3 = st.columns(3)

        with col1:
            glucose = st.text_input("Glucose")

        with col2:
            haemoglobin = st.text_input("Haemoglobin")

        with col3:
            cholesterol = st.text_input("Cholesterol")

        submitted = st.form_submit_button(
            "Save Patient",
            use_container_width=True
        )

    if submitted:
        try:
            patient_id = patient_service.add_patient(
                full_name,
                dob,
                email,
                glucose,
                haemoglobin,
                cholesterol
            )

            st.success(
                f"Patient record saved successfully. Patient ID: {patient_id}"
            )

            try:
                with st.spinner("Generating AI health remarks..."):
                    remarks = generate_and_save_remarks(patient_id)

                st.subheader("AI-Generated Health Remarks")
                st.info(remarks)

            except Exception as ai_error:
                st.warning(
                    "The patient record was saved, but AI remarks could "
                    "not be generated. You can retry from the AI Remarks tab."
                )
                st.caption(f"AI service message: {ai_error}")

            st.rerun()

        except ValueError as error:
            st.error(f"Validation error: {error}")

        except Exception as error:
            st.error(f"Unable to save patient: {error}")


# --------------------------------------------------
# VIEW PATIENT RECORDS
# --------------------------------------------------

with tab_records:
    st.subheader("All Patient Records")

    patients = patient_service.list_patients()

    if patients:
        display_records = []

        for patient in patients:
            display_records.append({
                "Patient ID": patient["id"],
                "Full Name": patient["full_name"],
                "Date of Birth": patient["dob"],
                "Email": patient["email"],
                "Glucose": patient["glucose"],
                "Haemoglobin": patient["haemoglobin"],
                "Cholesterol": patient["cholesterol"],
                "AI Remarks": patient["remarks"] or "Not generated yet"
            })

        dataframe = pd.DataFrame(display_records)

        st.dataframe(
            dataframe,
            use_container_width=True,
            hide_index=True
        )

        st.caption(f"Total patient records: {len(patients)}")

    else:
        st.info("No patient records found. Add a patient to get started.")


# --------------------------------------------------
# EDIT PATIENT
# --------------------------------------------------

with tab_edit:
    st.subheader("Update Patient Information")

    patient_options = get_patient_options()

    if patient_options:
        selected_label = st.selectbox(
            "Select Patient",
            list(patient_options.keys()),
            key="edit_patient_selection"
        )

        selected_id = patient_options[selected_label]
        selected_patient = patient_service.get_patient(selected_id)

        with st.form("edit_patient_form"):
            edit_name = st.text_input(
                "Full Name",
                value=selected_patient["full_name"]
            )

            edit_dob = st.text_input(
                "Date of Birth",
                value=selected_patient["dob"]
            )

            edit_email = st.text_input(
                "Email Address",
                value=selected_patient["email"]
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                edit_glucose = st.text_input(
                    "Glucose",
                    value=str(selected_patient["glucose"])
                )

            with col2:
                edit_haemoglobin = st.text_input(
                    "Haemoglobin",
                    value=str(selected_patient["haemoglobin"])
                )

            with col3:
                edit_cholesterol = st.text_input(
                    "Cholesterol",
                    value=str(selected_patient["cholesterol"])
                )

            update_submitted = st.form_submit_button(
                "Update Patient",
                use_container_width=True
            )

        if update_submitted:
            try:
                patient_service.edit_patient(
                    selected_id,
                    edit_name,
                    edit_dob,
                    edit_email,
                    edit_glucose,
                    edit_haemoglobin,
                    edit_cholesterol
                )

                st.success("Patient information updated successfully.")

                try:
                    with st.spinner("Refreshing AI health remarks..."):
                        remarks = generate_and_save_remarks(selected_id)

                    st.info("AI remarks refreshed successfully.")

                except Exception as ai_error:
                    st.warning(
                        "Patient information was updated, but AI remarks "
                        "could not be refreshed. Use the AI Remarks tab to retry."
                    )
                    st.caption(f"AI service message: {ai_error}")

                st.rerun()

            except ValueError as error:
                st.error(f"Validation error: {error}")

            except Exception as error:
                st.error(f"Unable to update patient: {error}")

    else:
        st.info("No patient records available to edit.")


# --------------------------------------------------
# DELETE PATIENT
# --------------------------------------------------

with tab_delete:
    st.subheader("Delete Patient Record")

    patient_options = get_patient_options()

    if patient_options:
        selected_label = st.selectbox(
            "Select Patient to Delete",
            list(patient_options.keys()),
            key="delete_patient_selection"
        )

        selected_id = patient_options[selected_label]
        selected_patient = patient_service.get_patient(selected_id)

        st.write(
            f"Selected patient: **{selected_patient['full_name']}**"
        )

        confirm_delete = st.checkbox(
            "I confirm that I want to permanently delete this record."
        )

        if st.button(
            "Delete Patient",
            type="primary",
            disabled=not confirm_delete
        ):
            try:
                patient_service.remove_patient(selected_id)
                st.success("Patient record deleted successfully.")
                st.rerun()

            except Exception as error:
                st.error(f"Unable to delete patient: {error}")

    else:
        st.info("No patient records available to delete.")


# --------------------------------------------------
# GENERATE OR REFRESH AI REMARKS
# --------------------------------------------------

with tab_ai:
    st.subheader("AI Health Remarks")

    patient_options = get_patient_options()

    if patient_options:
        selected_label = st.selectbox(
            "Select Patient",
            list(patient_options.keys()),
            key="ai_patient_selection"
        )

        selected_id = patient_options[selected_label]
        selected_patient = patient_service.get_patient(selected_id)

        st.write(f"**Patient:** {selected_patient['full_name']}")

        st.write("**Current AI Remarks:**")

        if selected_patient["remarks"]:
            st.info(selected_patient["remarks"])
        else:
            st.info("AI remarks have not been generated yet.")

        if st.button(
            "Generate / Refresh AI Remarks",
            use_container_width=True
        ):
            try:
                with st.spinner("Contacting the AI service..."):
                    remarks = generate_and_save_remarks(selected_id)

                st.success("AI remarks generated and saved successfully.")
                st.info(remarks)
                st.rerun()

            except Exception as error:
                st.error(f"Unable to generate AI remarks: {error}")

    else:
        st.info("Add a patient record before generating AI remarks.")


st.divider()

st.caption(
    "Health Prediction Application | Python, Streamlit, SQLite and Gemini AI"
)
