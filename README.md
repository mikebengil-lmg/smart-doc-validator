# README.md
# Smart Document Validator

An AI-powered FastAPI service that:
- Classifies documents (passport, license, payslip, etc.)
- Extracts metadata like name, DOB, expiry
- Outputs confidence scores

Run with:
```bash
uvicorn app.main:app --reload