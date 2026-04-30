
---
# Functional Specification Document (FSD)

## 1. Overview

The PDF Compressor is a Windows desktop application that enables users to reduce PDF file size using configurable compression settings powered by Ghostscript.

---

## 2. Objectives

- Provide simple UI for PDF compression
- Allow control over quality vs size
- Deliver real-time feedback (progress/logs)

---

## 3. Functional Requirements

### 3.1 File Selection
- User can select input PDF
- User can define output path

### 3.2 Compression Modes
- Preset Mode:
  - Fast
  - Balanced
  - High Quality
- Manual Mode:
  - DPI input
  - JPEG quality input

### 3.3 Compression Execution
- Triggered via "Start" button
- Runs asynchronously (non-blocking UI)

### 3.4 Progress Tracking
- Progress bar reflects pages processed
- Uses Ghostscript output parsing

### 3.5 Logging
- Displays:
  - Start message
  - Parameters used
  - Completion status

### 3.6 Cancellation
- User can cancel ongoing compression

---

## 4. Non-Functional Requirements

| Requirement | Description |
|------------|------------|
| Performance | Must handle PDFs up to 1000+ pages |
| Usability | Simple, minimal UI |
| Reliability | Must not crash on invalid input |
| Portability | Windows-based |

---

## 5. Assumptions

- Ghostscript is installed
- Input file is a valid PDF

---

## 6. Constraints

- Compression effectiveness depends on PDF content
- No guarantee of specific output size
