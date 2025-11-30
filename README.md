# 🚀 ZinAI

A comprehensive Streamlit application combining study tools, budget tracking, and CV building—all in one place.

## ✨ Features

### 📚 Study Assistant
- **Flashcard Generation**: Create fill-in-the-blank flashcards from any text
- **Quiz Generator**: Generate multiple-choice quizzes with instant feedback
- **File Upload**: Support for PDF and TXT file uploads
- **AI Integration**: Optional OpenAI integration for smarter question generation

### 💰 Budget Tracker
- **Transaction Management**: Add, view, and delete expenses
- **CSV Import/Export**: Bulk import transactions or export for analysis
- **Category Tracking**: Organize spending by categories (Food, Transport, Entertainment, etc.)
- **Visual Analytics**: Pie charts showing spending distribution
- **Summary Reports**: Category-based spending breakdown

### 📄 CV Builder
- **Professional CV Creation**: Build resumes with customizable sections
- **PDF Export**: Download CVs as formatted PDF documents
- **DOCX Export**: Export as Microsoft Word documents
- **Live Preview**: See your CV in real-time
- **Multiple Entries**: Add up to 5 work experiences and 3 education entries

## 🚀 Quick Start

### Requirements
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone or download the project**
   ```bash
   cd final project
   ```

2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv .venv
   # On Windows:
   .\.venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
final project/
├── app.py                 # Main Streamlit entrypoint
├── study.py              # Study Assistant module
├── budget.py             # Budget Tracker module
├── cv_builder.py         # CV Builder module
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── budget.db            # SQLite database (created automatically)
```

## 🎯 Usage Guide

### Study Assistant
1. Navigate to "📚 Study Assistant" from the sidebar
2. Paste study material or upload a PDF/TXT file
3. Choose number of flashcards to generate
4. Click "Generate Flashcards" to create fill-in-the-blank cards
5. Review cards and take quizzes
6. Sessions are automatically saved

**Tips:**
- Use clear, well-structured text for best results
- Generate 5-10 cards per study session
- Review multiple times for retention

### Budget Tracker
1. Navigate to "💰 Budget Tracker" from the sidebar
2. Add transactions with date, category, amount, and optional note
3. View all transactions in the list
4. Import transactions from CSV or export current data
5. View pie charts and category breakdown

**CSV Format for Import:**
```
date,category,amount,note
2024-01-15,Food,25.50,Lunch with team
2024-01-15,Transport,8.00,Uber to office
```

### CV Builder
1. Navigate to "📄 CV Builder" from the sidebar
2. Fill in personal information (name, email, phone)
3. Add professional summary, work experience, and education
4. Click "Preview CV" to see how it looks
5. Download as PDF or DOCX with one click

## 📊 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | 1.50.0 | Web framework |
| pandas | 2.1.3 | Data manipulation |
| matplotlib | 3.8.2 | Data visualization |
| PyPDF2 | 3.0.1 | PDF parsing |
| fpdf | 1.7.2 | PDF generation |
| python-docx | 0.8.11 | DOCX generation |
| scikit-learn | 1.3.2 | ML utilities |
| numpy | 1.24.3 | Numerical computing |
| openai | 1.3.5 | Optional: AI features |

## 🔧 Advanced Configuration

### Enable AI Features
To use OpenAI integration for smarter flashcard generation:

1. Get an OpenAI API key from https://platform.openai.com/api-keys
2. In the app, go to Settings → AI / API Settings
3. Enter your API key
4. Enable "Use AI" when generating flashcards

### Database Management
The budget data is stored in `budget.db` (SQLite). To reset:
```bash
rm budget.db
```
The database will be recreated on next run.

### Session Storage
Study sessions are saved in `study_sessions/` directory. Clear this folder to remove old sessions.

## 🐛 Troubleshooting

**"Import could not be resolved"**
- Select the correct Python interpreter in VS Code (Command Palette → Python: Select Interpreter)

**"PyPDF2 not installed"**
```bash
pip install PyPDF2
```

**"Can't export as PDF/DOCX"**
```bash
pip install fpdf python-docx
```

**Port already in use (Error: Address already in use)**
```bash
streamlit run app.py --server.port 8502
```

## 🚀 Future Enhancements

- [ ] Cloud storage integration (Google Drive, Dropbox)
- [ ] User authentication and profiles
- [ ] Mobile-responsive design improvements
- [ ] Real OpenAI integration for question generation
- [ ] Dark mode support
- [ ] Spending forecasting with ML
- [ ] Collaborative study sessions
- [ ] Calendar integration

## 📝 Version History

**v2.0 - Advanced Edition**
- Added PDF/TXT file uploads for Study Assistant
- CSV import/export for Budget Tracker
- PDF and DOCX export for CV Builder
- Enhanced UI with professional styling
- Charts and data visualization

**v1.0 - Initial Release**
- Basic flashcard and quiz generation
- Simple budget tracking
- CV builder with preview

## 📄 License

This project is open source and available for educational use.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Improve documentation
- Submit pull requests

## 💬 Support

For questions or issues:
1. Check the troubleshooting section above
2. Review the inline help text in the app
3. Check Streamlit documentation: https://docs.streamlit.io

## 🎓 Educational Use

This project is designed for educational purposes and can be used in:
- Computer Science courses
- Personal productivity projects
- Portfolio building
- Learning Streamlit development

---

([Check out the live app](https://zinai-studysuite.streamlit.app/)
)

**Happy studying! 📚 Good luck managing your finances! 💰 Build amazing CVs! 📄**

