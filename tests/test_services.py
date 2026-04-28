import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.question import Base, Question
from models.result import Result
from models.session import InterviewSession
from services.history_service import HistoryService
from services.question_bank import QuestionBank
from services.session_service import SessionService, SESSION_TIMEOUT_SECONDS
from services.statistics_service import StatisticsService


def make_test_sessionlocal():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)


def test_interview_session_counts_correct_answer_and_finishes():
    question = Question(
        text="2 + 2 = ?",
        category="Math",
        options=["3", "4", "5"],
        correct_option=1,
    )
    session = InterviewSession(user_id=1, direction="Math", questions=[question])

    result = session.submit_answer(1)

    assert result is True
    assert session.result.correct_answers == 1
    assert session.result.wrong_answers == 0
    assert session.result.total_score == 10
    assert session.finished is True
    assert len(session.result.answer_details) == 1
    assert session.result.answer_details[0]["user_answer"] == "4"


def test_interview_session_counts_wrong_answer():
    question = Question(
        text="Capital of France?",
        category="Geography",
        options=["Berlin", "Paris", "Rome"],
        correct_option=1,
    )
    session = InterviewSession(user_id=2, direction="Geography", questions=[question])

    result = session.submit_answer(0)

    assert result is False
    assert session.result.correct_answers == 0
    assert session.result.wrong_answers == 1
    assert session.result.total_score == 0
    assert session.finished is True
    assert session.result.answer_details[0]["correct_answer"] == "Paris"


def test_session_service_returns_none_for_expired_session():
    service = SessionService()
    try:
        session = service.create_session(user_id=10, direction="Python", questions=[])
        session.created_at = time.time() - SESSION_TIMEOUT_SECONDS - 1

        result = service.get_session(10)

        assert result is None
        assert 10 not in service.sessions
    finally:
        service.shutdown()


def test_session_service_create_session_replaces_previous_one():
    service = SessionService()
    try:
        old_session = service.create_session(
            user_id=5, direction="Python", questions=[]
        )
        new_session = service.create_session(user_id=5, direction="Java", questions=[])

        assert service.get_session(5) is new_session
        assert old_session is not new_session
        assert new_session.direction == "Java"
        assert len(service.sessions) == 1
    finally:
        service.shutdown()


def test_statistics_service_accumulates_results():
    stats = StatisticsService()

    first = Result()
    first.correct_answers = 3
    first.wrong_answers = 1

    second = Result()
    second.correct_answers = 2
    second.wrong_answers = 2

    stats.save_result(100, first)
    stats.save_result(100, second)
    user_stats = stats.get_user_statistics(100)

    assert user_stats["tests_passed"] == 2
    assert user_stats["total_correct"] == 5
    assert user_stats["total_wrong"] == 3
    assert user_stats["total_score"] == 50


def test_question_bank_add_get_edit_delete_question(monkeypatch):
    test_sessionlocal = make_test_sessionlocal()
    monkeypatch.setattr("services.question_bank.SessionLocal", test_sessionlocal)

    bank = QuestionBank()
    added = bank.add_question(
        text="What is Python?",
        category="Python",
        options=["Language", "Animal", "IDE"],
        correct_option=0,
    )

    assert added is not None
    assert added.question_id is not None

    fetched = bank.get_question_by_id(added.question_id)
    assert fetched.text == "What is Python?"
    assert fetched.category == "Python"

    updated = bank.edit_question(
        question_id=added.question_id,
        new_text="What is Java?",
        new_category="Java",
        new_options=["Language", "Drink"],
        new_correct_option=0,
    )
    assert updated is True

    edited = bank.get_question_by_id(added.question_id)
    assert edited.text == "What is Java?"
    assert edited.category == "Java"
    assert edited.options == ["Language", "Drink"]

    deleted = bank.delete_question(added.question_id)
    assert deleted is True
    assert bank.get_question_by_id(added.question_id) is None


def test_question_bank_format_questions_list_for_empty_db(monkeypatch):
    test_sessionlocal = make_test_sessionlocal()
    monkeypatch.setattr("services.question_bank.SessionLocal", test_sessionlocal)

    bank = QuestionBank()

    assert bank.format_questions_list() == "Список питань порожній."


def test_history_service_saves_and_formats_user_history(monkeypatch):
    test_sessionlocal = make_test_sessionlocal()
    monkeypatch.setattr("services.history_service.SessionLocal", test_sessionlocal)

    history = HistoryService()
    result = Result()
    result.correct_answers = 4
    result.wrong_answers = 1

    history.save_test_result(
        user_id=77,
        username="serg",
        category="Python",
        result=result,
    )

    report = history.format_user_history(77)

    assert "Ваші результати за весь час:" in report
    assert "Python" in report
    assert "Бал: 40" in report


def test_history_service_returns_empty_message_when_no_results(monkeypatch):
    test_sessionlocal = make_test_sessionlocal()
    monkeypatch.setattr("services.history_service.SessionLocal", test_sessionlocal)

    history = HistoryService()

    assert history.format_user_history(999) == "Історія тестів порожня."
