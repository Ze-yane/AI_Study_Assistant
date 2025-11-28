import os
import json
import random
import re
from typing import List, Tuple, Optional
from datetime import datetime
from collections import Counter

# Optional imports used by Streamlit runtime
try:
    from PyPDF2 import PdfReader
except Exception:
    PdfReader = None


class StudyAssistant:
    """AI Study Assistant with improved Gemini 2.5 integration, flashcards, quiz, and UI."""

    def __init__(self, session_dir: str = "study_sessions"):
        self.session_dir = session_dir
        os.makedirs(session_dir, exist_ok=True)
        self.stats_file = os.path.join(session_dir, "stats.json")
        self._load_stats()

    # ------------------------- Stats helpers -------------------------
    def _load_stats(self):
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, "r", encoding="utf-8") as f:
                    self.stats = json.load(f)
            except Exception:
                self.stats = self._default_stats()
        else:
            self.stats = self._default_stats()

    def _default_stats(self):
        return {
            "total_cards": 0,
            "total_quizzes": 0,
            "best_score": 0,
            "study_sessions": [],
            "cards_mastered": 0,
        }

    def save_stats(self):
        with open(self.stats_file, "w", encoding="utf-8") as f:
            json.dump(self.stats, f, indent=2)

    # ------------------------- File extractors -------------------------
    def _extract_pdf_text(self, pdf_file) -> str:
        if PdfReader is None:
            return "⚠️ PyPDF2 not installed. Install with `pip install PyPDF2`."
        try:
            try:
                pdf_file.seek(0)
            except Exception:
                pass
            reader = PdfReader(pdf_file)
            text_chunks = [page.extract_text() or "" for page in reader.pages]
            text = "\n".join(text_chunks).strip()
            return text or "⚠️ Unable to extract text from PDF."
        except Exception as e:
            return f"⚠️ PDF extraction error: {e}"

    def _extract_txt_text(self, uploaded_file) -> str:
        try:
            uploaded_file.seek(0)
            raw = uploaded_file.read()
            if isinstance(raw, bytes):
                return raw.decode("utf-8", errors="replace")
            return str(raw)
        except Exception as e:
            return f"⚠️ TXT extraction error: {e}"

    # ------------------------- Gemini 2.5 integration -------------------------
    def _call_gemini(self, prompt: str, api_key: str, model: str = "gemini-2.0-flash") -> str:
        """Call Gemini 2.5 and return plain text output."""
        try:
            import google.generativeai as genai
        except Exception:
            raise RuntimeError("google-generativeai not installed. Install: pip install google-generativeai")

        if not api_key:
            raise RuntimeError("Gemini API key missing.")

        genai.configure(api_key=api_key)
        model_instance = genai.GenerativeModel(model)
        try:
            response = model_instance.generate_content(prompt)
            # Gemini 2.5 returns text in response.text
            if hasattr(response, "text") and response.text:
                return response.text.strip()
            return str(response).strip()
        except Exception as e:
            raise RuntimeError(f"Gemini API call failed: {e}")

    # ------------------------- AI Wrappers -------------------------
    def summarize(self, text: str, api_key: str = None) -> str:
        if not text.strip():
            return "No text provided for summarization."

        prompt = (
            "You are an intelligent assistant. Summarize the following text into a concise paragraph "
            "and three bullet points. Return plain text (no JSON or markdown), clearly separated:\n\n"
            f"{text}\n\nSummary:"
        )

        api_key = api_key or os.environ.get("GEMINI_API_KEY", "")
        if api_key:
            try:
                return self._call_gemini(prompt, api_key)
            except Exception as e:
                return f"AI summarization error: {e}"
        # Fallback
        return self._summarize_heuristic(text)

    def generate_flashcards(self, text: str, max_cards: int = 10, api_key: str = None) -> List[Tuple[str, str]]:
        prompt = (
            f"You are a study assistant. From the text below, generate up to {max_cards} flashcards. "
            "Each flashcard should have a question and an answer. Return plain text, clearly separate each card:\n\n"
            f"{text}\n\nFlashcards:"
        )
        api_key = api_key or os.environ.get("GEMINI_API_KEY", "")
        if api_key:
            try:
                output = self._call_gemini(prompt, api_key)
                cards = []
                for block in re.split(r'\n-{2,}\n', output):
                    parts = block.split("\n")
                    if len(parts) >= 2:
                        q = parts[0].strip()
                        a = " ".join(parts[1:]).strip()
                        cards.append((q, a))
                        if len(cards) >= max_cards:
                            break
                if cards:
                    return cards
            except Exception:
                pass
        # Fallback
        return self._generate_heuristic(text, max_cards)

    def generate_quiz(self, text: str, num_questions: int = 5, api_key: str = None):
        prompt = (
            f"Generate {num_questions} multiple-choice questions from the text below. "
            "Each question must have 4 options and indicate the correct answer. Return plain text.\n\n"
            f"{text}\n\nQuiz:"
        )
        api_key = api_key or os.environ.get("GEMINI_API_KEY", "")
        if api_key:
            try:
                output = self._call_gemini(prompt, api_key)
                # Parse simple text into quiz
                quiz = []
                for q_block in re.split(r'\n-{2,}\n', output):
                    lines = [line.strip() for line in q_block.split("\n") if line.strip()]
                    if len(lines) >= 6:
                        question = lines[0]
                        options = lines[1:5]
                        correct = lines[5].replace("Answer:", "").strip()
                        quiz.append({"question": question, "options": options, "correct": correct})
                        if len(quiz) >= num_questions:
                            break
                if quiz:
                    return quiz
            except Exception:
                pass
        # Fallback
        return self._generate_quiz(text, num_questions)

    # ------------------------- Heuristic Fallbacks -------------------------
    def _summarize_heuristic(self, text: str, max_sentences: int = 5) -> str:
        sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]
        return " ".join(sentences[:max_sentences]) if sentences else "No text to summarize."

    def _generate_heuristic(self, text: str, max_cards: int) -> List[Tuple[str, str]]:
        sentences = [s.strip() for s in re.split(r'[.!?]', text) if s.strip()]
        cards = []
        for sent in sentences[:max_cards]:
            q = "What is the main idea of this sentence?"
            a = sent
            cards.append((q, a))
        return cards or [("No material", "Unable to generate flashcards")]

    def _generate_quiz(self, text: str, num_questions: int) -> List[dict]:
        sentences = [s.strip() for s in text.replace("\n", " ").split('.') if len(s.split()) > 5]
        random.shuffle(sentences)
        quiz = []
        for sent in sentences[:num_questions]:
            words = [w.strip(',.!?') for w in sent.split() if len(w.strip(',.!?')) > 2]
            correct = random.choice(words) if words else "N/A"
            question = sent.replace(correct, "_____")
            options = {correct}
            while len(options) < 4 and len(words) > 0:
                options.add(random.choice(words))
            options = list(options)
            random.shuffle(options)
            quiz.append({"question": question, "options": options, "correct": correct})
        return quiz or [{"question": "N/A", "options": ["N/A"], "correct": "N/A"}]

    # ------------------------- Streamlit UI -------------------------
    def ui(self):
        import streamlit as st

        st.title("📚 AI Study Assistant")
        st.write("Generate flashcards, quizzes, and summaries from your study material.")

        max_cards = st.sidebar.number_input("Max Flashcards", 1, 50, 10)
        num_questions = st.sidebar.number_input("Quiz Questions", 1, 20, 5)
        api_key = os.environ.get("GEMINI_API_KEY", "")

        uploaded = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])
        text = st.text_area("Or paste text", height=200)
        extracted_text = text

        if uploaded:
            if uploaded.type == "application/pdf":
                extracted_text = self._extract_pdf_text(uploaded)
            else:
                extracted_text = self._extract_txt_text(uploaded)
            st.success("File text extracted.")

        # Summarize
        if st.button("Summarize"):
            summary = self.summarize(extracted_text, api_key)
            st.subheader("Summary")
            st.text(summary)

        # Flashcards with flipping
        if st.button("Generate Flashcards"):
            cards = self.generate_flashcards(extracted_text, max_cards, api_key)
            st.subheader("Flashcards")
            for idx, (q, a) in enumerate(cards, 1):
                with st.expander(f"Q{idx}: {q}"):
                    st.write(a)

        # Quiz with answer after submit
        if st.button("Generate Quiz"):
            quiz = self.generate_quiz(extracted_text, num_questions, api_key)
            st.subheader("Quiz")
            for idx, q_item in enumerate(quiz, 1):
                st.markdown(f"**Q{idx}:** {q_item['question']}")
                options = q_item.get("options", [])
                correct = q_item.get("correct", "")
                selected = st.radio(f"Select answer for Q{idx}", options, key=f"q{idx}")
                if st.button(f"Check Answer Q{idx}", key=f"btn{idx}"):
                    if selected == correct:
                        st.success("✅ Correct!")
                    else:
                        st.error(f"❌ Incorrect. Correct answer: {correct}")  