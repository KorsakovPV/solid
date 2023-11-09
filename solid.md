# Solid это не сложно с примерами на Python

## Введение

Привет, Хабр! Меня зовут Павел Корсаков, я python-разработчик, backend-developer в облачном
провайдере [beeline cloud](https://cloud.beeline.ru/?utm_source=owned_media&utm_medium=habr&utm_campaign=beeline_cloud&utm_term=bpod-kapotom-python-tonkosti-populyarnyh-konstrukciy-with-i-contextmanager).

Почти на всех на собеседованиях есть вопрос про SOLID. Что такое SOLID. Зачем он нужен. Как кандидат его применяет. Как
понимает принципы из него. Спрашиваем про SOLID потому, что он часто бывает аргументом на ревью. Разработчики с опытом на
больших и энтерпайзных проектах частенько предлагают применить какой-нибудь из принципов SOLID там, где он на первый
взгляд вроде бы и не нужен.

Но вернемся к кандидатам. Чаше всего кандидат рассказывает что SOLID это акроним, называет все принципы, но объяснить и
привести примеры может только для половины. На остальных либо плавает, либо сливается.

Интернет по SOLID предлагает множество статей. Как на русском, так и на иностранном языке. Но в тех, что я просмотрел
объяснение было построено так. Брался принцип, давалась его определение и приводился какой-то пример кода с
комментариями. Чтоб эта статья не получилась еще одной очередной статьей про SOLID я поменяю принцип подачи информации. Я
буду добавлять код не большими инкрементами и на каждом инкременте писать какие принципы SOLID в данном инкременте
применены. Это авторский текст (не перевод) с теми примерами которые я обычно использую для объяснения принципов SOLID.
Прошу отнестись к тексту снисходительно.

## Теория

Я не буду повторяться. В интернете много материала. Приведу только пару ссылок
Википедия [SOLID](https://ru.wikipedia.org/wiki/SOLID_(программирование)). Ну и
первоисточник [butunclebob.com](http://butunclebob.com/ArticleS.UncleBob.PrinciplesOfOod).

## Принцип инверсии зависимостей,

В моем идеальном мире SOLID начинается с принципа инверсии зависимостей. Если у вас нет зависимости на абстракциях, то
SOLID не полноценный и понять его значительно сложнее.

```python
# Здесь и далее весь код убрать под спойлеры.
from abc import ABC, abstractmethod


class AbstractAuthUser(ABC):
    """Абстрактный класс, реализующий обязательные методы."""

    @abstractmethod
    def is_authenticated(self) -> bool:
        """
        Метод проверяет аутентификацию пользователя.
        Возвращает True если аутентифицирован и False если не аутентифицирован
        """

    @abstractmethod
    def get_email(self) -> str:
        """Метод возвращает email пользователя"""

    @abstractmethod
    def get_department(self) -> str:
        """Метод возвращает отдел в котором работает пользователь"""
```

Начнем разбираться по порядку. ABC это класс помощник который всего только указывает метакласс `metaclass=ABCMeta`
вариант `class AbstractAuthUser(metaclass=abc.ABCMeta):` тоже рабочий, но Python предлагает нам синтаксический сахар мы
его и используем. Оставим первый вариант.

Декоратор `abstractmethod` гарантирует что у всех методов дочернего класса будут все методы которые декорированы этим
декоратором. Этим декоратором нужно оборачивать все методы которые будет использовать бизнес логика. Коллеги которые из
своего кода будут обращаться к классу аутентификации могут быть уверены, что у него всегда есть
методы `is_authenticated`, `get_email`, `get_department` потому, что они декарированы `abstractmethod` и поэтому 
обязательны для реализации в классах дочерних от абстрактного.

Отнаследуемся от абстрактного класса. Создадим класс, который будет проверять аутентификацию через Active Directory.
Если все сделано правильно, то код ниже в момент запуска выдаст ошибку.

```python
from abc import ABC, abstractmethod


class AbstractAuthUser(ABC):
    """Абстрактный класс, реализующий обязательные методы."""

    @abstractmethod
    def is_authenticated(self) -> bool:
        """
        Метод проверяет аутентификацию пользователя.
        Возвращает True если аутентифицирован и False если не аутентифицирован
        """

    @abstractmethod
    def get_email(self) -> str:
        """Метод возвращает email пользователя"""

    @abstractmethod
    def get_department(self) -> str:
        """Метод возвращает отдел в котором работает пользователь"""


class AuthUserAD(AbstractAuthUser):
    pass


auth = AuthUserAD()

# Traceback (most recent call last):
#  File "/home/pavel/Projects/solid/solid.py", line 38, in <module>
#    auth = AuthUserAD()
#           ^^^^^^^^^^^^
# TypeError: Can't instantiate abstract class AuthUserAD with abstract methods get_department, get_email, is_authenticated
```

Это происходит потому, что в нашем классе нет обязательных методов. Но когда эти методы добавим все станет хорошо.

```python
from abc import ABC, abstractmethod


class AbstractAuthUser(ABC):
    """Абстрактный класс, реализующий обязательные методы."""

    @abstractmethod
    def is_authenticated(self) -> bool:
        """
        Метод проверяет аутентификацию пользователя.
        Возвращает True если аутентифицирован и False если не аутентифицирован
        """

    @abstractmethod
    def get_email(self) -> str:
        """Метод возвращает email пользователя"""

    @abstractmethod
    def get_department(self) -> str:
        """Метод возвращает отдел в котором работает пользователь"""


class AuthUserAD(AbstractAuthUser):
    def is_authenticated(self) -> bool:
        raise NotImplementedError()

    def get_email(self) -> str:
        raise NotImplementedError()

    def get_department(self) -> str:
        raise NotImplementedError()


auth = AuthUserAD()
```

В абстрактном классе стоит указывать методы, которые будут вызываться из вне. Это своего рода API класса (компонента). Те же методы 
которые не должны использоваться из вне не нужно указывать в абстрактном классе. При реализации `AuthUserAD` методы не 
являются частью API класса можно пометить одним подчеркиванием в начале имени. [PEP8](https://peps.python.org/pep-0008/#descriptive-naming-styles) 

Если вы в своем коде используете абстрактные классы, то скоре всего у вас в коде с SOLID все хорошо. Ниже при описании
остальных принципов мы часто будем возвращаться к этому принципу.

## Принцип открытости/закрытости

Давайте предположим что `AuthUserAD` это жуткое легаси которому лет 6. И из тех разработчиков которые его писали уже
никого нет. `AuthUserAD` регулярно DDOS-ит и роняет сервер аутентификации. Админ предлагает дешевое решение поднять
несколько инстансов [Keycloak](https://ru.wikipedia.org/wiki/Keycloak). Инстансы Keycloak будет по крону ходить в AD и
брать на себя нагрузку, которая лежала на AD.

Вносить изменения в класс `AuthUserAD` плохая идея. Трудно спрогнозировать риски, которые могут произойти от новых
изменений. К тому же после внесения изменений его захочется переименовать, а это равносильно удалению класса. Если мы не
исправим все места где он вызывается по старому имени, то гарантированно уроним код.

Сейчас самое время вспомнить про принцип `Принцип открытости/закрытости`. Хорошей идеей будет не трогать класс
`AuthUserAD`. Сделать его осуждаемым и написать новый класс для работы с новой схемой аутентификации. В новом классе
вместо ошибок из Keycloak мы будем райзить наши кастомные ошибки.

```python
from abc import ABC, abstractmethod, ABCMeta
import logging

logger = logging.getLogger('root')


class AbstractAuthUser(metaclass=ABCMeta):
    """Абстрактный класс, реализующий обязательные методы."""

    @abstractmethod
    def is_authenticated(self) -> bool:
        """
        Метод проверяет аутентификацию пользователя.
        Возвращает True если аутентифицирован и False если не аутентифицирован
        """

    @abstractmethod
    def get_email(self) -> str:
        """Метод возвращает email пользователя"""

    @abstractmethod
    def get_department(self) -> str:
        """Метод возвращает отдел в котором работает пользователь"""


class AuthUserAD(AbstractAuthUser):

    def __init__(self, *args, **kwargs):
        logger.error('Class AuthUserAD is deprecated. You should use AuthUserKeycloak.')
        super().__init__(*args, **kwargs)

    def is_authenticated(self) -> bool:
        raise NotImplementedError()

    def get_email(self) -> str:
        raise NotImplementedError()

    def get_department(self) -> str:
        raise NotImplementedError()


class AuthUserKeycloak(AbstractAuthUser):
    def is_authenticated(self) -> bool:
        raise NotImplementedError()

    def get_email(self) -> str:
        raise NotImplementedError()

    def get_department(self) -> str:
        raise NotImplementedError()
```

Если мы где-то не заменили класс `AuthUserAD` на `AuthUserKeycloak` у нас все рано все будет работать так как класс
`AuthUserAD` мы не удалили и он все еще существует и работает лучше, чем прежде, так как нагрузка на AD уменьшится. В
логах мы будем видеть ошибку при каждом создании инстанса `AuthUserAD` и постепенно безболезненно выпилим его из всех
возможных мест. Принцип открытости/закрытости работает на нас.

## Принцип подстановки Лисков

В наших классах кроме обязательных методов, описанных в абстрактном классе, могут быть различные свои методы. У таких
методов могут быть отличные сигнатуры. Могут отличиться названия методов. Ну и может отличиться реализация. Как же без
полиморфизма. Например, разные методы для http запроса на сервис аутентификации. Могут быть разные методы для проверки
токена, получения почты и названия отдела. Это не противоречит SOLID. Главное чтоб бизнес логика работала только с
методами из абстрактного класса. И сигнатуры методов с которыми буде работать бизнес логика были одинаковые.

Может показаться не очевидным, но в Python для принципа подстановки Лисков ограничиваться только методами описанными в
абстрактном классе может быть не достаточно. Если класс `AuthUserAD` и класс `AuthUserKeycloak` райзит разные ошибки, то
получается что классы не удовлетворяют принципа подстановки Лисков. В контексте SOLID использование кастомных исключений
это больше чем хорошая практика. Это расширение понимания принципа подстановки Лисков.

Мы знаем какие ошибки могут прилететь поэтому очень крутой идеей будет написать свои кастомные ошибки. Не пробрасывать
ошибки из AD и из Keycloak, а обрабатывать их в классе и райзить свои.

```python
class AuthException(Exception):
    pass


class InvalidCredential(AuthException):
    pass


class AuthenticationServerIsNotAvailable(AuthException):
    pass
```

Так как новый класс `AuthUserKeycloak` реализует такие-же обязательные методы, как и `AuthUserAD`. И райзит те же самые
ошибки то в ручке (или миделваре) где использовался класс `AuthUserAD` или его инстансы мы можем безболезненно заменить
его на новый `AuthUserKeycloak`. При такой реализации принцип подстановки Лисков работает.

Здесь хочу сделать не большое замечание. Декоратор abstractmethod гарантирует что обязательные методы будут созданы, но
он позволяет создать их с различными сигнатурами. А для `Принципа подстановки Лисков` важно чтоб сигнатуры были
одинаковые или хотя бы совместимые. Без этого заменить базовый класс дочерним или один дочерний другим дочерним классом
без не получится.

Возможно кто-то скажет что принцип подстановки Лисков это про базовый тип и дочерний. И определение в википедии говорит
об этом. `"Функции, которые используют базовый тип, должны иметь возможность использовать подтипы базового типа не зная 
об этом"`. Но нам ни чего не мешает сделать наследование так.

```python
class AuthUserAD(AbstractAuthUser):

    def __init__(self, *args, **kwargs):
        logger.error('Class AuthUserAD is deprecated. You should use AuthUserKeycloak.')
        super().__init__(*args, **kwargs)

    def is_authenticated(self) -> bool:
        raise NotImplementedError()

    def get_email(self) -> str:
        raise NotImplementedError()

    def get_department(self) -> str:
        raise NotImplementedError()


class AuthUserKeycloak(AuthUserAD):
    def is_authenticated(self) -> bool:
        raise NotImplementedError()
```

Так как у нас `AuthUserKeycloak` реализует такие-же обязательные методы, как и `AuthUserAD` это ни как не повлияет на
возможность использования одного класса вместо другого. Если например реализация методов `get_email` и `get_department` в
`AuthUserKeycloak` такое же как в `AuthUserAD` то такое наследование возможно.

Но если у `AuthUserKeycloak` своя реализация всех методов API класса то такое наследование не нужно. Кроме этого мы
получим нежелательный побочный эффект. В экземпляре метода `AuthUserKeycloak` нам доступны все методы базового класса.

Я считаю что при любом, даже сложном, наследовании. Если мы можем один класс заменить другим то они соответствуют
принципу подстановки Лисков.

С наиболее сложными для понимания принципами закончили. Остались те которые обычно не вызывают трудностей.

## Принцип единственной ответственности

Здесь все просто, если например класс `AuthUserKeycloak` сохраняет какие-то данные, то можно создать метод для этого
действия, а он уже будет работать с экземпляром класса для хранения. Логика открытия файла или открытия соединения,
логика сохранения файла в файл или базу, закрытия файла или соеденения должны быть вынесена в метод соответствующего
класса.

То есть создать абстрактный класс для хранения, а потом от него наследуем дочерние классы например для хранения в файле,
в базе данных через ORM, в Монго и др. И инстанс для нужного способа хранения использовать в `AuthUserKeycloak`. У меня
обычно есть один абстрактный и одни класс для ORM. Который я и использую для хранения например StoreFile или StoreDB

```python
from abc import ABC, abstractmethod


class AbstractStore(ABC):
    @abstractmethod
    def get(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_multi(self, *args, **kwargs):
        pass

    @abstractmethod
    def create(self, *args, **kwargs):
        pass

    @abstractmethod
    def update(self, *args, **kwargs):
        pass

    @abstractmethod
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

И последний незатронутый принцип. Для того чтоб его понять нужно определиться с понятиями. Что же такое интерфейс?
Проблема в том что в Python нет явного понятия интерфейса как в некоторых других языках программирования. Но правда есть
внешняя библиотека [zope.interface](https://pypi.org/project/zope.interface/) которая реализует интерфейсы в Python. 
Потом с python 3.8 появились [Protocol](https://typing.readthedocs.io/en/latest/source/protocols.html#simple-user-defined-protocols). Они близки как к абстрактным классам, так и к интерфейсам.

Если своими словами, то интерфейс это
абстракция которая позволяет определить методы без конкретной реализации. И если в классе есть все методы интерфейса то
в можно сказать что класс реализует интерфейс.

Получается что интерфейсам про которые говорится в `принципе разделения интерфейса` больше всего соответствуют 
абстрактные классы. После этого пояснения принцип становится очевидным. И что означает "много интерфейсов,
специально предназначенных для клиентов, лучше, чем один интерфейс общего назначения" теперь понятно.

Приведу пример с абстрактным классом для коллектора. 

```python
from abc import ABC, abstractmethod


class AbstractCollector(ABC):

    def __init__(self) -> None:
        self.metrics = []
        self.prepared_metrics = []

    def collect(self) -> None:
        self.get_metrics_from_service()
        self.process_metrics()
        self.save_metrics()

    @abstractmethod
    def get_metrics_from_service(self) -> None:
        """Extract."""

    @abstractmethod
    def process_metrics(self) -> None:
        """Transform."""

    @abstractmethod
    def save_metrics(self) -> None:
        """Load."""


class AbstractStore(ABC):
    @abstractmethod
    def get(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_multi(self, *args, **kwargs):
        pass

    @abstractmethod
    def create(self, *args, **kwargs):
        pass

    @abstractmethod
    def update(self, *args, **kwargs):
        pass

    @abstractmethod
    def delete(self, *args, **kwargs):
        pass


class AbstractReadOnlyStore(ABC):
    @abstractmethod
    def get(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_multi(self, *args, **kwargs):
        pass


class GetStoreDB:
    def get(self, *args, **kwargs):
        raise NotImplementedError

    def get_multi(self, *args, **kwargs):
        raise NotImplementedError


class CreateStoreDB:
    def create(self, *args, **kwargs):
        raise NotImplementedError


class UpdateStoreDB:
    def update(self, *args, **kwargs):
        raise NotImplementedError


class DeleteStoreDB:
    def delete(self, *args, **kwargs):
        raise NotImplementedError


class StoreReadOnlyDB(AbstractReadOnlyStore, GetStoreDB):
    pass


class StoreDB(AbstractStore, GetStoreDB, CreateStoreDB, UpdateStoreDB, DeleteStoreDB):
    pass
```

Прежде чем объяснять что тут происходит вспомним теорию.

```
Роберт С. Мартин определил[1] этот принцип так:

Программные сущности не должны зависеть от методов, которые они не используют.

Принцип разделения интерфейсов говорит о том, что слишком «толстые» интерфейсы необходимо разделять на более маленькие и
специфические, чтобы программные сущности маленьких интерфейсов знали только о методах, которые необходимы им в работе.
В итоге, при изменении метода интерфейса не должны меняться программные сущности, которые этот метод не используют.
```
[Wiki](https://ru.wikipedia.org/wiki/Принцип_разделения_интерфейса)

В примере реализовано два абстрактных класса для работы с данными AbstractStore, AbstractReadOnlyStore и класс 
абстрактного коллектора AbstractCollector. 

Метод коллектора get_metrics_from_service ходит в инфраструктуру и имеет доступ к критичным данным. В разных коллекторах 
данные собираются из различных источников (api, базы данных, файлы и др.) Но это всегда выполняется только сбор данных 
(только безопасные методы). Методы, которые принято относить к опасным, не 
будут в нем использоваться. Поэтому при написании класса для сбора данных нужно использовать AbstractReadOnlyStore.
Тогда потенциально опасные методы будут исключены на уровне интерфейса (архитектуры).

Метод коллектора save_metrics обычно выполняет только запись в базу данных. Получается что для написания класса 
сохранения в базу достаточно реализовать только create и update. И данная реализация позволяет нам легко собрать такой 
класс.

```python
class StoreReadOnlyDB(CreateStoreDB, UpdateStoreDB):
    pass
```

Хотя это и будет наиболее соответствующий принципу разделения интерфейса класс на практике мы так не делаем. А 
наследуемся от AbstractStore и в нем реализуются все методы CRUD.


## Заключение

Все правила, в том числе и SOLID, можно нарушать. В небольших проектах строгое соблюдение всех принципов SOLID
избыточно. Но программисты, которые пишут небольшие проекты, растут. Растут и их проекты. Становятся большими, очень
большими и архитектурно сложными. В таких проектах соблюдение принципов SOLID крайне желательно или обязательно.

Я надеюсь что приведенные примеры и комментарии помогли понять SOLID лучше. Если в тексте есть неточности или ошибки
поправьте меня. Это тема сложная и тут есть где ошибиться.
