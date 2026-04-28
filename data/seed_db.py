from services.db import SessionLocal, init_db
from models.question import Question
from data.test_questions import QUESTIONS


def seed_database():
    print("1. Ініціалізація бази даних")
    init_db()
    session = SessionLocal()

    try:
        questions_count = session.query(Question).count()

        if questions_count == 0:
            print("2. База порожня. Починаємо додавання запитань")
            for question_obj in QUESTIONS:
                session.add(question_obj)

            session.commit()
            print("3. Запитання успішно додано до interview_bot.db")
        else:
            print(f"База вже заповнена (знайдено {questions_count} запитань)")

    except Exception as e:
        session.rollback()
        print(f"Помилка під час заповнення: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    seed_database()
