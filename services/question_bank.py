from models.question import Question
from services.db import SessionLocal
import random


class QuestionBank:

    def get_questions_by_category(self, category):
        session = SessionLocal()
        try:
            questions = (
                session.query(Question).filter(Question.category == category).all()
            )
            session.expunge_all()

            if not questions:
                return []
            limit = min(len(questions), 10)
            shuffled_questions = random.sample(questions, limit)

            return shuffled_questions
        finally:
            session.close()

    def get_categories(self):
        session = SessionLocal()
        try:
            categories_tuples = session.query(Question.category).distinct().all()
            return [cat[0] for cat in categories_tuples]
        finally:
            session.close()

    def get_all_questions(self):
        session = SessionLocal()
        try:
            questions = session.query(Question).all()
            session.expunge_all()
            return questions
        finally:
            session.close()

    def get_question_by_id(self, question_id):
        session = SessionLocal()
        try:
            question = (
                session.query(Question)
                .filter(Question.question_id == question_id)
                .first()
            )
            if question:
                session.expunge(question)
            return question
        finally:
            session.close()

    def add_question(self, text, category, options, correct_option):
        session = SessionLocal()
        try:
            new_question = Question(
                text=text,
                category=category,
                options=options,
                correct_option=correct_option,
            )
            session.add(new_question)
            session.commit()
            session.refresh(new_question)
            session.expunge(new_question)
            return new_question
        except Exception as e:
            session.rollback()
            print(f"Помилка при додаванні питання: {e}")
            return None
        finally:
            session.close()

    def edit_question(
        self,
        question_id,
        new_text=None,
        new_category=None,
        new_options=None,
        new_correct_option=None,
    ):
        session = SessionLocal()
        try:
            question = (
                session.query(Question)
                .filter(Question.question_id == question_id)
                .first()
            )
            if not question:
                return False
            if new_text is not None:
                question.update_text(new_text)
            if new_category is not None:
                question.category = new_category
            if new_options is not None:
                question.update_options(new_options)
            if new_correct_option is not None:
                question.update_correct_option(new_correct_option)

            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Помилка при редагуванні: {e}")
            return False
        finally:
            session.close()

    def delete_question(self, question_id):
        session = SessionLocal()
        try:
            question = (
                session.query(Question)
                .filter(Question.question_id == question_id)
                .first()
            )
            if not question:
                return False
            session.delete(question)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Помилка при видаленні: {e}")
            return False
        finally:
            session.close()

    def format_questions_list(self):
        questions = self.get_all_questions()
        if not questions:
            return "Список питань порожній."

        lines = ["Список питань:"]
        for question in questions:
            lines.append(
                f"{question.question_id}. [{question.category}] {question.text}"
            )
        return "\n".join(lines)
