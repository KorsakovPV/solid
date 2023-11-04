import abc
import logging

logger = logging.getLogger('root')

from typing import Protocol


class AuthException(Exception):
    pass


class InvalidCredential(AuthException):
    pass


class AuthenticationServerIsNotAvailable(AuthException):
    pass


class AbstractAuthUser(abc.ABC):
    """Абстрактный класс, реализующий обязательные методы."""

    @abc.abstractmethod
    def is_authenticated(self, x: int) -> bool:
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
