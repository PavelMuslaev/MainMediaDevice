from datetime import datetime


class Review:
    def __init__(self, title: str, content: str, author='Эксперт', date=datetime.now(),
                 pros=None, cons=None):
        # Присвоение через свойства
        self.title = title
        self.content = content
        self.author = author
        self.date = date                # if date is not None else datetime.today()
        self.pros = pros                # pros.copy() if pros is not None else []
        self.cons = cons                # (cons or []).copy()

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value: str):
        if isinstance(value, str):
            self.__title = value
        else:
            print('Заголовок может быть только строкой')

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value: str):
        if isinstance(value, str):
            self.__content = value
        else:
            print('Описание может быть только строкой')

    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self, value: str):
        if isinstance(value, str):
            self.__author = value
        else:
            print('Автор может быть только строкой')

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, new_date: datetime):
        if isinstance(new_date, datetime):
            self.__date = new_date
        else:
            print('Ожидается экземпляр класса datetime')

    @property
    def pros(self):
        return self.__pros.copy()

    @pros.setter
    def pros(self, new_pros: list[str]):
        if new_pros is None:
            self.__pros = []
        elif isinstance(new_pros, list):
            self.__pros = new_pros.copy()
        else:
            print('Ожидается экземпляр класса list')

    @property
    def cons(self):
        return self.__cons.copy()

    @cons.setter
    def cons(self, new_cons: list[str]):
        if new_cons is None:
            self.__cons = []
        elif isinstance(new_cons, list):
            self.__cons = new_cons.copy()
        else:
            print('Ожидается экземпляр класса list')

    def add_pro(self, pro_text: str) -> None:
        if not isinstance(pro_text, str):
            print('Плюс должен быть описан с помощью текста')
        elif not pro_text.strip():
            print('Вы пытаетесь передать пустую строку!')
        elif len(pro_text) > 200:
            print('Текст плюса слишком большой')
        else:
            self.__pros.append(pro_text)

    def add_con(self, con_text: str) -> None:
        if not isinstance(con_text, str):
            print('Минус должен быть описан с помощью текста')
        elif not con_text.strip():
            print('Вы пытаетесь передать пустую строку!')
        elif len(con_text) > 200:
            print('Текст минуса слишком большой')
        else:
            self.__cons.append(con_text)

    def remove_pro(self, index: int) -> None:
        if index >= len(self.__pros) or index < -len(self.__pros):
            print('Индекс находится за пределами массива')
        else:
            self.__pros.pop(index)

    def remove_con(self, index: int) -> None:
        if index >= len(self.__cons) or index < -len(self.__cons):
            print('Индекс находится за пределами массива')
        else:
            self.__cons.pop(index)


