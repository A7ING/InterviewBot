from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Question(Base):
    __tablename__ = 'questions'

    question_id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    category = Column(String, nullable=False)
    options = Column(JSON, nullable=False) 
    correct_option = Column(Integer, nullable=False)

    def is_correct(self, option_index):
        return option_index == self.correct_option

    def update_text(self, new_text):
        self.text = new_text

    def update_options(self, new_options):
        self.options = new_options

    def update_correct_option(self, new_correct_option):
        self.correct_option = new_correct_option

    def __repr__(self):
        return f"<Question(id={self.question_id}, category='{self.category}')>"