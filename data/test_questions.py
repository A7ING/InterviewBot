from models.question import Question

QUESTIONS = [
    # === PYTHON ===
    Question(
        text="Python — це мова, що інтерпретується чи компілюється?",
        category="Python",
        options=[
            "Тільки компілюється",
            "Інтерпретується (байт-код виконується віртуальною машиною)",
            "Транслюється в машинний код перед запуском",
            "Виконується безпосередньо процесором",
        ],
        correct_option=1,
    ),
    Question(
        text="Який з наведених типів даних у Python є змінним (mutable)?",
        category="Python",
        options=["tuple (кортеж)", "str (рядок)", "list (список)", "int (ціле число)"],
        correct_option=2,
    ),
    Question(
        text="Що таке PEP 8?",
        category="Python",
        options=[
            "Вбудований фреймворк для веб-розробки",
            "Посібник зі стилю написання та оформлення коду",
            "Нова версія інтерпретатора Python",
            "Бібліотека для машинного навчання",
        ],
        correct_option=1,
    ),
    Question(
        text="У чому головна різниця між операторами `==` та `is`?",
        category="Python",
        options=[
            "`==` порівнює значення, а `is` порівнює посилання на об'єкти в пам'яті",
            "`==` порівнює посилання, а `is` порівнює значення",
            "Це абсолютно однакові оператори",
            "`is` використовується тільки для чисел, `==` для рядків",
        ],
        correct_option=0,
    ),
    Question(
        text="Що таке множинне наслідування (multiple inheritance)?",
        category="Python",
        options=[
            "Коли клас створює багато об'єктів",
            "Коли клас успадковує властивості та методи від двох і більше батьківських класів",
            "Коли один батьківський клас має багато дочірніх",
            "Такого поняття в Python не існує",
        ],
        correct_option=1,
    ),
    Question(
        text="Як називається короткий синтаксис для створення нових списків на основі існуючих?",
        category="Python",
        options=["lambda", "map()", "list comprehension", "generator"],
        correct_option=2,
    ),
    Question(
        text="Що таке `__init__` у класах Python?",
        category="Python",
        options=[
            "Метод для видалення об'єкта",
            "Метод-конструктор, який ініціалізує атрибути при створенні об'єкта",
            "Декоратор для статичних методів",
            "Функція для імпорту модулів",
        ],
        correct_option=1,
    ),
    Question(
        text="Яке ключове слово використовується для обробки винятків (помилок)?",
        category="Python",
        options=["if...else", "switch...case", "try...except", "catch...throw"],
        correct_option=2,
    ),
    Question(
        text="Що поверне виклик `type(lambda: None)`?",
        category="Python",
        options=[
            "<class 'NoneType'>",
            "<class 'function'>",
            "<class 'lambda'>",
            "<class 'object'>",
        ],
        correct_option=1,
    ),
    Question(
        text="Який метод додає всі елементи з одного списку до кінця іншого?",
        category="Python",
        options=["append()", "add()", "insert()", "extend()"],
        correct_option=3,
    ),
    # === JAVA ===
    Question(
        text="Який з цих типів даних НЕ є примітивним у Java?",
        category="Java",
        options=["int", "boolean", "String", "double"],
        correct_option=2,
    ),
    Question(
        text="Що таке JVM?",
        category="Java",
        options=[
            "Java Variable Manager - менеджер змінних",
            "Java Virtual Machine - віртуальна машина, що виконує байт-код",
            "Joint Version Manager - система контролю версій",
            "Java Visual Model - інструмент для побудови інтерфейсів",
        ],
        correct_option=1,
    ),
    Question(
        text="У чому перевага конструкції `try-with-resources` перед звичайним `try-catch`?",
        category="Java",
        options=[
            "Вона працює швидше",
            "Вона автоматично закриває ресурси (наприклад, файли або з'єднання), які реалізують AutoCloseable",
            "Вона дозволяє не писати блок catch",
            "Вона самостійно виправляє помилки в коді",
        ],
        correct_option=1,
    ),
    Question(
        text="Об'єкти якого з цих класів є незмінними (immutable) в Java?",
        category="Java",
        options=["ArrayList", "StringBuilder", "String", "HashMap"],
        correct_option=2,
    ),
    Question(
        text="В якому випадку виникає `OutOfMemoryError`?",
        category="Java",
        options=[
            "Коли програма намагається поділити на нуль",
            "Коли JVM не може виділити більше пам'яті для створення нових об'єктів",
            "Коли жорсткий диск комп'ютера повністю заповнений",
            "Коли втрачається з'єднання з базою даних",
        ],
        correct_option=1,
    ),
    Question(
        text="Що таке Hibernate?",
        category="Java",
        options=[
            "Мова запитів до бази даних",
            "Популярний фреймворк для реалізації ORM (Object-Relational Mapping)",
            "Вбудований веб-сервер Java",
            "Інструмент для автоматичного тестування",
        ],
        correct_option=1,
    ),
    Question(
        text="Яке ключове слово використовується, щоб заборонити зміну значення змінної після її ініціалізації?",
        category="Java",
        options=["static", "private", "final", "const"],
        correct_option=2,
    ),
    Question(
        text="У чому ключова різниця між ArrayList та LinkedList?",
        category="Java",
        options=[
            "ArrayList повільніший при читанні, але швидший при вставці в середину",
            "ArrayList використовує динамічний масив, а LinkedList — двонаправлений список зв'язаних вузлів",
            "LinkedList не дозволяє зберігати дублікати",
            "Різниці немає, це просто синоніми",
        ],
        correct_option=1,
    ),
    Question(
        text="Який метод є стандартною точкою входу в будь-яку самостійну Java програму?",
        category="Java",
        options=[
            "public void start()",
            "public static void main(String[] args)",
            "private static void init()",
            "public class Main()",
        ],
        correct_option=1,
    ),
    Question(
        text="Для чого використовується ключове слово `super`?",
        category="Java",
        options=[
            "Для створення супер-класу",
            "Для виклику методів або конструктора батьківського класу",
            "Для надання методу найвищого пріоритету виконання",
            "Для збільшення виділеної пам'яті",
        ],
        correct_option=1,
    ),
    # === QA ===
    Question(
        text="Що таке баг (Bug)?",
        category="QA",
        options=[
            "Некоректно написаний тест-кейс",
            "Відхилення фактичного результату роботи програми від очікуваного",
            "Збій у роботі операційної системи",
            "Нова фіча, яку запросив клієнт",
        ],
        correct_option=1,
    ),
    Question(
        text="Що перевіряє Regression Testing (Регресійне тестування)?",
        category="QA",
        options=[
            "Чи працює система під максимальним навантаженням",
            "Чи не зламався існуючий функціонал після додавання нового коду або виправлення багів",
            "Зручність інтерфейсу користувача",
            "Безпеку передачі даних",
        ],
        correct_option=1,
    ),
    Question(
        text="У чому різниця між Priority (Пріоритет) та Severity (Серйозність)?",
        category="QA",
        options=[
            "Це синоніми",
            "Severity вказує, наскільки швидко треба виправити баг, а Priority — який модуль він зачіпає",
            "Priority визначає черговість виправлення (бізнес-вимога), а Severity вказує на ступінь технічного впливу на систему",
            "Priority використовується тільки розробниками, а Severity — тестувальниками",
        ],
        correct_option=2,
    ),
    Question(
        text="У чому суть техніки Аналізу граничних значень (Boundary Value Analysis)?",
        category="QA",
        options=[
            "Перевірка системи на межі її пропускної здатності",
            "Тестування поведінки програми на межах діапазонів класів еквівалентності (наприклад, якщо поле приймає 1-10, тестуємо 0, 1, 10, 11)",
            "Перевірка меж екрану на мобільних пристроях",
            "Аналіз часу завантаження сторінки",
        ],
        correct_option=1,
    ),
    Question(
        text="Що таке Smoke Testing?",
        category="QA",
        options=[
            "Тестування системи до тих пір, поки вона не 'задимиться' (не впаде)",
            "Поверхнева перевірка найбільш критичного функціоналу для визначення, чи має сенс проводити глибше тестування",
            "Перевірка роботи програми без інтернету",
            "Тестування дизайну",
        ],
        correct_option=1,
    ),
    Question(
        text="Яке з цих полів є обов'язковим та найважливішим у якісному баг-репорті?",
        category="QA",
        options=[
            "Ім'я розробника, який зробив помилку",
            "Steps to reproduce (Кроки для відтворення)",
            "Шматок коду з помилкою",
            "Побажання щодо покращення дизайну",
        ],
        correct_option=1,
    ),
    Question(
        text="Що таке Test Case (Тестовий сценарій)?",
        category="QA",
        options=[
            "Автоматичний скрипт, написаний на Python або Java",
            "Документ з набором кроків, тестових даних та очікуваних результатів для перевірки певної функції",
            "Загальний звіт про результати тестування",
            "Список інструментів для тестувальника",
        ],
        correct_option=1,
    ),
    Question(
        text="Що передбачає Black Box Testing (Тестування чорного ящика)?",
        category="QA",
        options=[
            "Тестування без доступу до внутрішнього коду або архітектури програми",
            "Тестування серверної частини без UI",
            "Тестування додатку в темній темі",
            "Процес, коли розробники самі перевіряють свій код",
        ],
        correct_option=0,
    ),
    Question(
        text="Який HTTP статус-код зазвичай означає 'Успішний запит' (OK)?",
        category="QA",
        options=["404", "500", "200", "403"],
        correct_option=2,
    ),
    Question(
        text="Що означає абревіатура QA?",
        category="QA",
        options=[
            "Quality Analysis (Аналіз якості)",
            "Quantity Assessment (Оцінка кількості)",
            "Quality Assurance (Забезпечення якості)",
            "Quick Answers (Швидкі відповіді)",
        ],
        correct_option=2,
    ),
]
