"""Domain abstractions for the people involved in the ЖКГ process.

The hierarchy below demonstrates the four OOP pillars:

* **Encapsulation** — attributes are protected and exposed via properties.
* **Inheritance** — every participant inherits from :class:`Person`.
* **Polymorphism** — :meth:`Person.role` is overridden by each subclass.
* **Abstraction** — :class:`Person` is abstract and cannot be instantiated.
"""
from abc import ABC, abstractmethod


class Person(ABC):
    """Base class for every participant of the process."""

    def __init__(self, full_name: str) -> None:
        self._full_name = full_name

    @property
    def full_name(self) -> str:
        return self._full_name

    @abstractmethod
    def role(self) -> str:
        """Return the participant's role. Overridden by each subclass."""

    def describe(self) -> str:
        return f"{self.role()}: {self._full_name}"


class Tenant(Person):
    """Квартиронаймач — submits requests."""

    def role(self) -> str:
        return "tenant"


class Dispatcher(Person):
    """Диспетчер — assembles brigades and fills the work plan."""

    def role(self) -> str:
        return "dispatcher"


class SpecialistWorker(Person):
    """Спеціаліст — performs the work of a given specialty."""

    def __init__(self, full_name: str, specialty: str) -> None:
        super().__init__(full_name)
        self._specialty = specialty

    @property
    def specialty(self) -> str:
        return self._specialty

    def role(self) -> str:
        return "specialist"

    def can_handle(self, work_type: str) -> bool:
        """A specialist can handle work matching their specialty or general work."""
        return self._specialty in (work_type, "general")
