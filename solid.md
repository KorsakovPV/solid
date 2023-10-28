# Solid это не сложно с примерами на Python

## Введение
Привет, Хабр! Меня зовут Павел Корсаков, я python-разработчик, backend-developer в 
облачном провайдере [beeline cloud](https://cloud.beeline.ru/?utm_source=owned_media&utm_medium=habr&utm_campaign=beeline_cloud&utm_term=bpod-kapotom-python-tonkosti-populyarnyh-konstrukciy-with-i-contextmanager).

Почти на всех на собеседованиях есть вопрос про SOLID. Что такое SOLID. Зачем он нужен.
Как кандидат его применяет. Как понимает принципы из него. Спрашиваем про SOLID потому что 
он часто бывает аргументом на ревью. Разработчики с опытом на больших и энтерпайзных 
проектах частенько предлагают применить какой-нибудь из принципов SOLID там где он на первый 
взгляд вроде бы и не нужен.

Но вернемся к кандидатам. Чаше всего кандидат рассказывает что SOLID это акроним, называет 
все принципы, но объяснить и привести примеры может только для половины. На остальных либо 
плавает, либо сливается.

Интернет по SOLID предлагает множество статей. Как на русском, так и на иностранном языке. 
Но в тех что я просмотрел объяснение было построено так. Брался принцип, давалась его 
определение и приводился какой-то пример кода с комментариями. Чтоб эта статья не получилась
еще одной очередной статьей про SOLID я поменяю принцип подачи информации. Я буду добавлять 
код не большими инкрементами и на каждом инкременте писать какие принципы SOLID в данном 
инкременте применены. Это авторский текст (не перевод) с теми примерами которые я использую 
для объяснения принципов SOLID. Прошу отнестись к тексту снисходительно.

## Теория
Я не буду повторяться. В интернете много материала. Приведу только пару ссылок Википедия [SOLID](https://ru.wikipedia.org/wiki/SOLID_(программирование)). Ну и первоисточник [butunclebob.com](http://butunclebob.com/ArticleS.UncleBob.PrinciplesOfOod).

## Принцип инверсии зависимостей, 
В моем идеальном мире SOLID начинается с принципа инверсии зависимостей. Если у вас нет 
зависимости на абстракциях, то SOLID не полноценный и понять его значительно сложнее.

```python
# Здесь и далее весь код убрать под спойлеры.
import abc


class AbstractAuthUser(abc.ABC):
    """Абстрактный класс, реализующий обязательные методы."""

    @abc.abstractmethod
    def is_authentication(self) -> bool:
        """
        Метод проверяет аутентификацию пользователя.
        Возвращает True если аутентифицирован и False если не аутентифицирован
        """
        pass

    @property
    @abc.abstractmethod
    def get_email(self) -> str:
        """Метод возвращает email пользователя"""
        pass

    @property
    @abc.abstractmethod
    def get_department(self) -> str:
        """Метод возвращает отдел в котором работает пользователь"""
        pass
```
 
Начнем разбираться по порядку. ABC это класс помощник который всего только указывает 
метакласс `metaclass=ABCMeta` вариант `class AbstractAuthUser(metaclass=abc.ABCMeta):` 
тоже рабочий но Python предлагает нам синтаксический сахар мы его и используем. Оставим 
первый вариант.

Декоратор `abstractmethod` гарантирует что у всех методов дочернего класса будут 
все методы которые декорированы этим декоратором. Этим декоратором нужно декорировать 
все методы которые будет использовать бизнес логика. Коллеги которые из своего кода будут 
обращаться к классу аутентификации могут быть уверены, что у него всегда есть методы 
`is_authentication`, `get_email`, `get_department`.

Отнаследуемся от абстрактного класса. Создадим класс, который будет проверять аутентификацию 
через Active Directory. Если все сделано правильно, то код ниже выдаст ошибку.

```python
class AuthUserAD(AbstractAuthUser):
    pass

auth = AuthUserAD()

#Traceback (most recent call last):
#  File "/home/pavel/Projects/solid/solid.py", line 38, in <module>
#    auth = AuthUserAD()
#           ^^^^^^^^^^^^
#TypeError: Can't instantiate abstract class AuthUserAD with abstract methods get_department, get_email, is_authentication
```

Это происходит потому что в нашем классе нет обязательных методов. Но когда эти методы добавим
все станет хорошо.
```python
class AuthUserAD(AbstractAuthUser):
    def is_authentication(self) -> bool:
        raise NotImplementedError()

    def get_email(self) -> str:
        raise NotImplementedError()

    def get_department(self) -> str:
        raise NotImplementedError()

auth = AuthUserAD()
```

Мы знаем какие ошибки могут прилететь из AD и очень крутой идеей будет написать свои кастомные 
ошибки. Не пробрасывать ошибки из AD, а обрабатывать их в классе и райзить свои.

```python
class AuthException1(Exception):
    pass


class AuthException2(Exception):
    pass
```

## Принцип открытости/закрытости
Давайте предположим что AuthUserAD это жуткое легаси которому лет 6. И из тех разработчиков 
которые его писали уже никого нет. AuthUserAD регулярно DDOS-ит и роняет сервер аутентификации.
Админ предлагает дешевое решение поднять несколько инстансов Keycloak. Инстансы Keycloak будет 
по крону ходить в AD и брать на себя нагрузку, которая лежала на AD. 

Вносить изменения в класс AuthUserAD плохая идея. Трудно спрогнозировать риски, которые могут 
произойти от новых изменений. К тому же после внесения изменений его захочется переименовать,
а это равносильно удалению класса. Если мы не исправим все места где он вызывается по старому
имени, то гарантированно уроним код.

Сейчас самое время вспомнить про принцип `Принцип открытости/закрытости`. Хорошей идеей будет 
не трогать класс AuthUserAD. Сделать его осуждаемым и написать новый класс для работы с новой 
схемой аутентификации. В новом классе вместо ошибок из Keycloak мы будем райзить наши 
кастомные ошибки.

```python
import abc
import logging

logger = logging.getLogger('root')


class AuthException1(Exception):
    pass


class AuthException2(Exception):
    pass


class AbstractAuthUser(metaclass=abc.ABCMeta):
    """Абстрактный класс, реализующий обязательные методы."""

    @abc.abstractmethod
    def is_authentication(self) -> bool:
        """
        Метод проверяет аутентификацию пользователя.
        Возвращает True если аутентифицирован и False если не аутентифицирован
        """
        pass

    @property
    @abc.abstractmethod
    def get_email(self) -> str:
        """Метод возвращает email пользователя"""
        pass

    @property
    @abc.abstractmethod
    def get_department(self) -> str:
        """Метод возвращает отдел в котором работает пользователь"""
        pass


class AuthUserAD(AbstractAuthUser):

    def __init__(self, *args, **kwargs):
        logger.error('Class AuthUserAD is deprecated. You should use AuthUserKeycloak.')
        super().__init__(*args, **kwargs)

    def is_authentication(self) -> bool:
        raise NotImplementedError()

    def get_email(self) -> str:
        raise NotImplementedError()

    def get_department(self) -> str:
        raise NotImplementedError()


class AuthUserKeycloak(AbstractAuthUser):
    def is_authentication(self) -> bool:
        raise NotImplementedError()

    def get_email(self) -> str:
        raise NotImplementedError()

    def get_department(self) -> str:
        raise NotImplementedError()
```

Если мы где-то не заменили старый класс на новый у нас все рано все будет работать лучше
так как старый клас все еще существует и работает, а нагрузка на AD уменьшится. В логах 
мы будем видеть ошибку при каждом создании инстанса AuthUserAD и постепенно 
безболезненно выпилим его из всех возможных мест.
Принцип открытости/закрытости работает на нас.

## Принцип подстановки Лисков
В наших классах кроме обязательных методов могут быть различные свои методы. Например, разные 
методы для http запроса на сервис аутентификации. Могут быть разные методы для проверки токена, 
получения почты и названия отдела. Это не противоречит SOLID. Главное чтоб бизнес логика работала 
только с методами из абстрактного класса.

Так как новый класс AuthUserKeycloak реализует такие-же методы, как и AuthUserAD. 
И райзит те же самые ошибки то в ручке (или миделваре) где использовался класс AuthUserAD
или его инстансы мы можем безболезненно заменить его на новый AuthUserKeycloak.
При такой реализации принцип подстановки Лисков работает.

С наиболее сложными для понимания принципами закончили. Остались те которые обычно не 
вызывают трудностей.

## Принцип единственной ответственности
Здесь все просто если например класс AuthUserKeycloak сохраняет какие-то данные то нужно создать 
метод, а он уже будет работать с классом для хранения.

То есть создать абстрактный класc для хранения, а потом от него наследуем дочерние классы например 
для хранения в файле, в базе данных через ORM, в Монго и др. И инстанс для нужного способа хранения
использовать в AuthUserKeycloak.

```python
class AbstractStore(abc.ABC):
    def get(self, *args, **kwargs):
        pass

    def get_multi(self, *args, **kwargs):
        pass

    def create(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass


class StoreFile(AbstractStore):
    def get(self, *args, **kwargs):
        raise NotImplementedError

    def get_multi(self, *args, **kwargs):
        raise NotImplementedError

    def create(self, *args, **kwargs):
        raise NotImplementedError

    def update(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError


class StoreDB(AbstractStore):  # Для ORM
    def get(self, *args, **kwargs):
        raise NotImplementedError

    def get_multi(self, *args, **kwargs):
        raise NotImplementedError

    def create(self, *args, **kwargs):
        raise NotImplementedError

    def update(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError


class StoreMongo(AbstractStore):
    def get(self, *args, **kwargs):
        raise NotImplementedError

    def get_multi(self, *args, **kwargs):
        raise NotImplementedError

    def create(self, *args, **kwargs):
        raise NotImplementedError

    def update(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError
```

## Принцип разделения интерфейса
И последний незатронутый принцип. Для того чтоб его понять нужно определиться с понятиями.
Что же такое интерфейс? Проблема в том что в Python нет явного понятия интерфейса как в некоторых 
других языках программирования. Есть внешняя библиотека zope.interface которая реализует интерфейсы 
в Python. Если своими словами, то интерфейс это абстракция которая позволяет определить методы без 
конкретной реализации. И если в классе есть все методы интерфейса то в можно сказать что класс 
реализует интерфейс.

Получается что интерфейсам про которые говорится в `принципе разделения интерфейса` больше всего 
соответствуют методы абстрактного класса. После этого пояснения принцип становится совсем 
очевидным. И что означает "много интерфейсов, специально предназначенных для клиентов, лучше, 
чем один интерфейс общего назначения" теперь понятно. 

Приведу пример с абстрактным классом для коллектора.

```python
class AbstractCollector(abc.ABC):
    """Один интерфейс общего назначения collect"""

    def __init__(self) -> None:
        self.metrics = []
        self.prepared_metric = []

    @abc.abstractmethod
    def collect(self) -> None:
        pass

class AbstractCollector(abc.ABC):
    """Несколько интерфейсов специального назначения. Разделенные по принципу ETL"""

    def __init__(self) -> None:
        self.metrics = []
        self.prepared_metric = []

    def collect(self) -> None:
        self.get_metric_from_service()
        self.prepare_metric_for_save()
        self.write_metric_to_database()

    @abc.abstractmethod
    def get_metric_from_service(self) -> None:
        """Extract."""
        pass

    @abc.abstractmethod
    def prepare_metric_for_save(self) -> None:
        """Transform."""
        pass

    @abc.abstractmethod
    def write_metric_to_database(self) -> None:
        """Load."""
        pass
```

## Заключение
Все правила, в том числе и SOLID, можно нарушать. В небольших проектах строгое соблюдение всех
принципов SOLID избыточно. Но программисты, которые пишут небольшие проекты, растут. Растут 
и их проекты. Становятся большими и очень большими, архитектурно сложными. В таких проектах 
соблюдение принципов SOLID крайне желательно или обязательно.

Я надеюсь что приведенные примеры и комментарии помогли понять SOLID лучше. Если в тексте есть
неточности или ошибки поправте меня. Это тема сложная и тут есть где ошибиться.