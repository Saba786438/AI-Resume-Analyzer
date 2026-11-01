# AI Resume Analyzer

A Flask web app that reviews a resume and compares its listed skills with a job description. It accepts PDF and DOCX files and returns a resume checklist score, detected skills, missing job-related skills, and suggestions.

> The analysis uses keyword matching and simple rules. It does not use a trained AI model or replace a recruiter’s judgment.

## Features

- Upload a PDF or DOCX resume (up to 5 MB)
- Paste a job description for a skills comparison
- See detected skills and skills from the job description that were not found
- Get a checklist score and suggestions for improving the resume
- Uploaded files are removed after processing

## Built with

- Python
- Flask
- PyPDF2
- python-docx

## Getting started

### Requirements

- Python 3.8 or later

