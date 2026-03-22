from datetime import datetime


class Review:
    """Модель Review для работы с отзывами."""

    def __init__(self, title: str, content: str, author='Эксперт', date=None,
                 status: str = "published", pros=None, cons=None):
        """
        Инициализирует объект отзыва.

        Примечания:
            - Все присвоения проходят через свойства (setters), которые
              выполняют проверку типов и, при необходимости, подстановку значений
              по умолчанию.
            - При передаче некорректных типов свойства выводят сообщение об ошибке
              (в текущей реализации). В будущем планируется замена на исключения.
        :param title:   Заголовок отзыва. Не может быть пустой строкой.
        :param content: Содержание (текст) отзыва.
        :param author:  Имя автора. По умолчанию 'Эксперт'.
        :param date: Дата и время создания. Если не указана,
                будет установлена текущая дата и время (через сеттер date).
        :param pros: Список преимуществ.
                Если передан список, создаётся его копия. Если None, создаётся пустой список.
        :param cons: Список недостатков.
                Если передан список, создаётся его копия. Если None, создаётся пустой список.
        """
        # Присвоение через свойства
        self.title = title
        self.content = content
        self.author = author
        self.status = status
        self.date = date                # if date is not None else datetime.today()
        self.pros = pros                # pros.copy() if pros is not None else []
        self.cons = cons                # (cons or []).copy()

    @property
    def title(self) -> str:
        """Возвращает заголовок обзора."""
        return self.__title

    @title.setter
    def title(self, value: str) -> None:
        """
        Присваивает заголовку новое значение.
        :param value: Новый текст заголовка.
        :return: None.
        """
        if isinstance(value, str):
            self.__title = value
        else:
            print('Заголовок может быть только строкой')

    @property
    def content(self) -> str:
        """Возвращает содержание обзора."""
        return self.__content

    @content.setter
    def content(self, value: str) -> None:
        """
        Присваивает содержанию статьи новое значение.
        :param value: Новый текст содержания.
        :return: None.
        """
        if isinstance(value, str):
            self.__content = value
        else:
            print('Описание может быть только строкой')

    @property
    def author(self) -> str:
        """Возвращает автора обзора."""
        return self.__author

    @author.setter
    def author(self, value: str) -> None:
        """
        Присваивает автору статьи новое значение.
        :param value: Новое имя автора.
        :return:
        """
        if isinstance(value, str):
            self.__author = value
        else:
            print('Автор может быть только строкой')

    @property
    def status(self) -> str:
        """Возвращает статус обзора."""
        return self.__status

    @status.setter
    def status(self, value: str) -> None:
        """
        Устанавливает статус обзора.
        :param value: Состояние обзора.
        :return: None.
        """
        if not isinstance(value, str):
            print(f'{value} must be str')
        else:
            self.__status = value

    @property
    def date(self) -> datetime:
        """Возвращает дату создания обзора."""
        return self.__date

    @date.setter
    def date(self, new_date: datetime) -> None:
        """
        Изменяет дату создание статьи на new_date.
        Если значение new_date - None, то дата автоматически сменится на актуальную.
        :param new_date: Новая дата, когда была создана статья.
        :return: None.
        """
        if new_date is None:
            self.__date = datetime.now()
        elif isinstance(new_date, datetime):
            self.__date = new_date
        else:
            print('Ожидается экземпляр класса datetime')

    @property
    def pros(self) -> list[str]:
        """Возвращает список плюсов обзора."""
        return self.__pros.copy()

    @pros.setter
    def pros(self, new_pros: list[str]) -> None:
        """
        Переопределяет список плюсов.
        Если значение new_pros - None, то список минусов - [].
        :param new_pros: Новый список плюсов.
        :return: None.
        """
        if new_pros is None:
            self.__pros = []
        elif isinstance(new_pros, list):
            self.__pros = new_pros.copy()
        else:
            print('Ожидается экземпляр класса list')

    @property
    def cons(self) -> list[str]:
        """Возвращает список минусов обзора."""
        return self.__cons.copy()

    @cons.setter
    def cons(self, new_cons: list[str]) -> None:
        """
        Переопределяет список минусов.
        Если значение new_cons - None, то список минусов - [].
        :param new_cons: Новый список минусов.
        :return: None.
        """
        if new_cons is None:
            self.__cons = []
        elif isinstance(new_cons, list):
            self.__cons = new_cons.copy()
        else:
            print('Ожидается экземпляр класса list')

    def add_pro(self, pro_text: str) -> None:
        """
        Добавляет новый плюс, в исходный список плюсов.
        :param pro_text: Новый плюс. Не может превышать 200 символов.
        :return: None.
        """
        if not isinstance(pro_text, str):
            print('Плюс должен быть описан с помощью текста')
        elif not pro_text.strip():
            print('Вы пытаетесь передать пустую строку!')
        elif len(pro_text) > 200:
            print('Текст плюса слишком большой')
        else:
            self.__pros.append(pro_text)

    def add_con(self, con_text: str) -> None:
        """
        Добавляет новый минус, в исходный список минусов.
        :param con_text: Новый минус. Не может превышать 200 символов.
        :return: None.
        """
        if not isinstance(con_text, str):
            print('Минус должен быть описан с помощью текста')
        elif not con_text.strip():
            print('Вы пытаетесь передать пустую строку!')
        elif len(con_text) > 200:
            print('Текст минуса слишком большой')
        else:
            self.__cons.append(con_text)

    def remove_pro(self, index: int) -> None:
        """
        Удаляет плюс из общего списка плюсов по индексу.
        С проверкой диапазона.
        :param index: Индекс элементы, который нужно удалить.
        :return: None.
        """
        if len(self.__pros) > index >= -len(self.__pros):
            self.__pros.pop(index)
        else:
            print('Индекс находится за пределами массива')

    def remove_con(self, index: int) -> None:
        """
        Удаляет минус из общего списка минусов по индексу.
        С проверкой диапазона.
        :param index: Индекс элементы, который нужно удалить.
        :return: None.
        """
        if len(self.__cons) > index >= -len(self.__cons):
            self.__cons.pop(index)
        else:
            print('Индекс находится за пределами массива')

    @classmethod
    def from_dict(cls, data: dict) -> Review | None:
        """
        Преобразует словарь данных в экземпляр класса Device.
        :param data: Словарь с обязательными ключами: title, content
                    и опциональными: author, date, pros, cons.
        :return: экземпляр класса Review.
        """
        base_keys = ['title', 'content']

        for key in base_keys:
            if key not in data:
                print(f'ПРОПУЩЕН БАЗОВЫЙ КЛЮЧ: {key}! 🚨')  # TODO: ЗАМЕНИТЬ НА ИСКЛЮЧЕНИЕ
                return None

        return cls(
            title=data['title'],
            content=data['content'],
            author=data.get('author', 'Эксперт'),
            date=data.get('date', None),
            pros=data.get('pros', None),
            cons=data.get('cons', None),
        )
