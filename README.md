# TalentLens – AI-Powered ATS Resume Screening System

## Overview

TalentLens is an AI-powered Applicant Tracking System (ATS) designed to help recruiters efficiently screen and rank resumes based on a given Job Description (JD). The system analyzes multiple resumes, evaluates their relevance, assigns ATS scores, ranks candidates, and provides insights into matching and missing skills.

This project demonstrates how Artificial Intelligence and Natural Language Processing can streamline the recruitment process while reducing manual effort.

---

## Features

* Upload multiple resumes (PDF/TXT)
* Upload a Job Description
* Automatic resume parsing
* Resume cleaning and preprocessing
* AI-powered resume ranking using a CrossEncoder model
* Skill matching between resume and job description
* Keyword matching
* ATS score generation
* Candidate ranking
* Matching and missing skills identification
* Interactive Streamlit dashboard
* CSV export of ranked candidates

---

## Tech Stack

### Programming Language

* Python

### Framework

* Streamlit

### AI / Machine Learning

* Sentence Transformers
* CrossEncoder (`cross-encoder/ms-marco-MiniLM-L-6-v2`)
* Scikit-learn

### NLP

* Resume preprocessing
* Keyword extraction
* Skill matching
* Semantic similarity

### Data Processing

* Pandas
* NumPy
* Regex

### File Handling

* PDFPlumber
* TXT Parser

---

## Project Structure

TalentLens/

├── combined_app.py

├── requirements.txt

├── README.md

├── sample_resumes/

├── sample_jd/

├── outputs/

└── assets/

---

## ATS Scoring Method

The final ATS score is calculated using multiple evaluation metrics.

* Skill Match
* Keyword Match
* Semantic Similarity (used for candidate ranking)

The system ranks resumes based on their overall relevance to the uploaded Job Description.

---

## Workflow

1. Upload one Job Description.
2. Upload one or more resumes.
3. Resume text is extracted.
4. Resume and JD are cleaned.
5. Skills and keywords are extracted.
6. ATS score is calculated.
7. Candidates are ranked.
8. Results are displayed in an interactive dashboard.

---

## Future Enhancements

* Support for multiple job domains (Web Development, DevOps, Data Science, Cybersecurity, etc.)
* Dynamic skill extraction from Job Descriptions
* AI-generated resume improvement suggestions
* Recruiter login and candidate management
* Resume recommendation system
* Interview prediction
* Dashboard analytics
* Database integration
* Cloud deployment
## Installation
Clone the repository
git clone https://github.com/Dhanushchappa/TalentLens.git
Navigate to the project
cd TalentLens
Install dependencies
pip install -r requirements.txt
Run the application
streamlit run combined_app.py
## Sample Input
* AI/ML Job Description
* Multiple PDF resumes
## Output
* ATS Score
* Candidate Ranking
* Match Status
* Skill Match Analysis
* Downloadable Results
## Author
**Dhanush Sai**
AI & Machine Learning Enthusiast

---

## License

This project is intended for educational and portfolio purposes.
