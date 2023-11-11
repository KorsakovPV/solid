from abc import ABC, abstractmethod
import logging

logger = logging.getLogger('root')

from typing import Protocol


class AuthException(Exception):
    pass


class InvalidCredential(AuthException):
    pass


class AuthenticationServerIsNotAvailable(AuthException):
    pass


class AbstractAuthUser(ABC):
    """Абстрактный класс, реализующий обязательные методы."""

    @abstractmethod
    def is_authenticated(self, x: int) -> bool:
        """
        Метод проверяет аутентификацию пользователя.
        Возвращает True если аутентифицирован и False если не аутентифицирован
        """

    # @property
    @abstractmethod
    def get_email(self) -> str:
        """Метод возвращает email пользователя"""

    # @property
    @abstractmethod
    def get_department(self) -> str:
        """Метод возвращает отдел в котором работает пользователь"""


class AuthUserAD(AbstractAuthUser):
    """Класс аутентификации через AD"""

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
        super().get_department()
        # raise NotImplementedError()


auth = AuthUserKeycloak()


class AbstractGetStore(ABC):
    def get(self, *args, **kwargs):
        pass

    def get_multi(self, *args, **kwargs):
        pass


class AbstractCreateStore(ABC):

    def create(self, *args, **kwargs):
        pass


class AbstractUpdateStore(ABC):

    def update(self, *args, **kwargs):
        pass


class AbstractDeleteStore(ABC):

    def delete(self, *args, **kwargs):
        pass


class AbstractStore(
    AbstractGetStore,
    AbstractCreateStore,
    AbstractUpdateStore,
    AbstractDeleteStore,
):
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


s = StoreDB()
