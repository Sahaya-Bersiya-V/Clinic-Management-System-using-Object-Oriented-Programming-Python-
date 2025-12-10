# Hospital Management System - Project Workflow

This document outlines the operational workflows for the various modules within the Hospital Management System (HMS).

## 1. Authentication & System Access
*   **Login**: All users (Admin, Doctor, Receptionist, Pharmacist, Lab Technician) must log in using their secure credentials (`username` and `password`).
*   **Role-Based Access Control**: Upon successful login, the system detects the user's role and redirects them to their specific dashboard, ensuring they only access authorized features.

---

## 2. Administrator Workflow
The Admin is responsible for the overall setup and management of the hospital's staff and resources.

1.  **Staff Management**:
    *   **Register Staff**: Admin adds new employees (Doctors, Receptionists, Pharmacists, Lab Techs), creating their system credentials and assigning roles.
    *   **Manage Schedule**: Admin sets and updates shift timings (Start/End times) for staff members.
    *   **Deactivate Users**: Admin can remove or deactivate staff accounts to revoke system access.
2.  **Doctor Management**:
    *   Admin maintains the list of active doctors and their specializations.

---

## 3. Receptionist Workflow
The Receptionist acts as the first point of contact for patients.

1.  **Patient Registration**:
    *   New patients are registered with personal details (Name, Age, Contact, Blood Group, Address).
    *   System generates a unique **Patient ID**.
2.  **Appointment Booking**:
    *   Receptionist checks **Doctor Availability** (viewing doctor's existing appointments).
    *   Books an appointment for a registered patient with a specific doctor on a chosen date.
3.  **Patient Check-In**:
    *   On the day of the visit, the receptionist fetches the **Appointment ID** (via "View Booked Appointments") and marks the patient status as **"Checked-In"**.
4.  **Billing (Consultation)**:
    *   Generates a bill for the consultation or administrative fees.
    *   Status is updated to **"Paid"** or **"Unpaid"**.

---

## 4. Doctor Workflow
The Doctor manages the clinical treatment of the patient.

1.  **View Appointments**:
    *   Doctor logs in to see their list of scheduled and checked-in appointments.
2.  **Consultation**:
    *   **Medical History**: Doctor views the patient's past history.
    *   **Diagnosis & Prescription**: Doctor records the diagnosis and prescribes medication. This data is saved and accessible to the Pharmacist.
3.  **Lab Requests**:
    *   If tests are needed, the Doctor selects a test from the catalog and creates a **Lab Request**.
4.  **Completion**:
    *   Doctor marks the appointment status as **"Diagnosed"** or **"Completed"**.

---

## 5. Lab Technician Workflow
The Lab Tech processes the diagnostic tests requested by doctors.

1.  **Manage Test Catalog**:
    *   Adds new test types and costs to the system.
2.  **Process Requests**:
    *   Views **"Pending"** lab requests initiated by doctors.
    *   Updates status to **"Processing"**.
3.  **Enter Results**:
    *   Once the test is done, the Tech enters the **Result** and updates status to **"Completed"**.
    *   This action automatically populates the **Lab Reports** for the patient.
4.  **View/Correct Reports**:
    *   Tech can view patient history and correct report details if necessary.

---

## 6. Pharmacist Workflow
The Pharmacist dispenses medication and manages inventory.

1.  **Inventory Management**:
    *   **Add Medicine**: Inputs details for new stock (Name, Price, Quantity, Expiry, Batch No).
    *   **Update Stock**: Adjusts quantities or details; empty inputs preserve existing data.
    *   **Alerts**: Checks for **Low Stock** and **Expiring Medicines**.
2.  **Dispensing & Billing**:
    *   **View Prescription**: Fetches the medication list prescribed by the Doctor for a specific patient.
    *   **Generate Bill**:
        *   Selects the medicine and quantity.
        *   System checks stock availability and validates the Patient/Appointment IDs.
        *   Auto-selects "Today's Date".
        *   Status must be strictly **"Paid"** or **"Unpaid"**.
        *   Stock is automatically deducted upon billing.

---

## End-to-End Patient Journey Example
1.  **Arrival**: Patient walks in. Receptionist registers them and books an appointment with Dr. X.
2.  **Wait**: Receptionist checks the patient in.
3.  **Consultation**: Dr. X sees the patient, diagnosing "Flu" and prescribing "Paracetamol". Dr. X also requests a "Blood Count".
4.  **Lab**: Patient goes to Lab. Lab Tech sees the request, performs the test, enters results, and completes the report.
5.  **Pharmacy**: Patient goes to Pharmacy. Pharmacist views the prescription for "Paracetamol", generates a bill (status: Paid), and hands over the medicine.
6.  **Exit**: Patient leaves with treatment complete and all records stored centrally.
