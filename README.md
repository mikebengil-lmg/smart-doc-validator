# Smart Document Validator

An AI-powered FastAPI service that:
- Classifies uploaded documents (e.g. passport, driver's license, payslip)
- Extracts metadata like name, date of birth, ID numbers, expiry, issuer
- Assesses fraud risk and outputs confidence scores
- Performs relationship and identity validation across documents
- Supports multiple AI providers (Claude, Gemini, OpenAI)

## 🛠️ Setup

Clone the repo and install dependencies:

```bash
git clone https://github.com/mikebengil-lmg/smart-doc-validator.git
cd smart-doc-validator
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -r requirements.txt
```

## ⚙️ Configuration

Create a `.env` file with your secrets:

```env
OPENAI_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
AWS_PROFILE=myAWSProfile
```

> ⚠️ `.env` is gitignored by default to prevent secret leaks.

## 🚀 Running the App

Start the FastAPI server with:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8383 --reload
```

- `--reload`: Enables auto-reload on code changes (useful for development).
- `--port 8383`: Default project port. You can change this for local testing:
  ```bash
  uvicorn app.main:app --port 9000 --reload
  ```

Once running, access the API at:

- 🔗 http://localhost:8383/docs – Swagger UI
- 🔗 http://localhost:8383/redoc – ReDoc documentation

✅ Ensure your `.env` file is configured before launching the server.

## 📦 Features

- **1st Pass (Classification):** Each file is individually analyzed and metadata is extracted.
- **2nd Pass (Validation):** All files are reviewed in context of family structure, fraud signals, and consistency.
- **Error Handling:** Files that can't be classified are tracked and returned as unprocessable.
- **Modular AI Backend:** Easily switch between Claude, Gemini, or OpenAI.

## 🧪 Testing

You can test the endpoints using Postman or Swagger UI.

- **Classification (1st Pass):**  
  Upload a file using:
  ```
  POST http://localhost:8383/api/v1/smart_document_classify_test
  ```

- **Validation (2nd Pass):**  
  Validate all extracted documents and relationships:
  ```
  POST http://localhost:8383/api/v1/validate_batch
  ```

### 🧾 Sample Payload for `/validate_batch`
```json
{
  "documents": [
    {
      "type": "Tax Notice",
      "name": "Mike Bell",
      "id_number": "123 456 789",
      "issuer": "Australian Taxation Office",
      "document_date": "15/07/2024",
      "country": "Australia",
      "document_context": "Financial",
      "confidence": 0.85,
      "confidence_label": "Reasonable",
      "fraud_risk": "medium",
      "fraud_notes": "Minor inconsistency in name spelling (Bell vs Belle). May indicate document from alternate identity.",
      "summary": "Tax notice for Mike Bell for tax year 2023-2024 showing amount owed of AUD 12,345.67. Document appears suitable for CRM upload despite minor typos in original text.",
      "document_index": 0,
      "file_name": "File5_typos.txt"
    },
    {
      "type": "Utility Bill",
      "name": "Mike Belle",
      "id_number": "UB123456789",
      "country": "Australia",
      "issuer": "AusGrid Electricity",
      "document_date": "05/06/2024",
      "document_context": "Financial",
      "confidence": 0.95,
      "confidence_label": "High",
      "fraud_risk": "low",
      "fraud_notes": "No anomalies detected.",
      "summary": "Electricity bill from AusGrid for Mike Belle for May 2024 billing period. Contains clear account details, billing address and amount due. Suitable for CRM upload as proof of address and identity verification.",
      "document_index": 1,
      "file_name": "File4.docx"
    },
    {
      "type": "Loan Agreement",
      "name": "Mike Belle",
      "id_number": "LN-AU-20240601-7890",
      "expiry": "01/06/2029",
      "country": "Australia",
      "issuer": "Sydney Credit Union",
      "document_date": "01/06/2024",
      "document_context": "Financial",
      "confidence": 0.95,
      "confidence_label": "High",
      "fraud_risk": "low",
      "fraud_notes": "No fraud patterns detected.",
      "summary": "Personal loan agreement issued by Sydney Credit Union to Mike Belle for AUD 50,000 for home renovation purposes. Valid from June 1, 2024 to June 1, 2029. Document appears complete and suitable for CRM upload.",
      "document_index": 2,
      "file_name": "File3.docx"
    },
    {
      "type": "Passport",
      "name": "Mike Belle",
      "dob": "11/07/1980",
      "id_number": "N12345678",
      "expiry": "11/07/2033",
      "country": "Australia",
      "issuer": "Australian Government",
      "document_date": "11/07/2023",
      "document_context": "Identification",
      "confidence": 0.95,
      "confidence_label": "High",
      "fraud_risk": "low",
      "fraud_notes": "Standard format, no red flags.",
      "summary": "Australian biometric passport issued in Canberra. Document appears to be a standard Australian passport with 10-year validity period. Contains all required identification fields and is suitable for CRM upload.",
      "document_index": 3,
      "file_name": "File2.jpg"
    },
    {
      "type": "Driver's License",
      "name": "John Smith",
      "dob": "31/02/1987",
      "id_number": "NSW1234ABC",
      "expiry": "35/12/2029",
      "country": "Australia",
      "issuer": "New South Wales Transport Auth",
      "document_date": "11/07/2023",
      "document_context": "Identification",
      "confidence": 0.60,
      "confidence_label": "Weak",
      "fraud_risk": "high",
      "fraud_notes": "Impossible date of birth (31/02/1987) and expiry (35/12/2029). Fake issuer format. Potentially tampered template.",
      "summary": "Australian driver's license with multiple validity issues including impossible dates and suspicious issuer formatting. Not suitable for CRM upload due to high likelihood of being a mock or tampered document.",
      "document_index": 4,
      "file_name": "FakeLicense.jpg"
    }
  ],
  "clients": [
    {
      "client_name": "Belle",
      "role": "dependent",
      "gender": "female",
      "dob": "2014-01-24"
    },
    {
      "client_name": "Dad Belle",
      "role": "client",
      "gender": "male",
      "dob": "1980-05-10"
    },
    {
      "client_name": "Mom Belle",
      "role": "client",
      "gender": "female",
      "dob": "1983-09-15"
    },
    {
      "client_name": "Afam Afam",
      "role": "guarantor",
      "gender": "afam",
      "dob": "1983-09-17"
    }
  ],
  "enum_filetypes": [
    "passport",
    "passport_australia",
    "student_id_card",
    "school_information",
    "birth_certificate",
    "drivers_license",
    "drivers_license_australia",
    "marriage_certificate",
    "payslip",
    "otherDocs"
  ]
}
```

## 🧑‍💻 Dev Notes

This is designed for internal hackathon prototyping. Scrappy UI is welcome. Contributions appreciated.

---