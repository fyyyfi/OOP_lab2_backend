"""Unit tests for the OOP domain hierarchy."""
import pytest

from app.services.domain import Dispatcher, Person, SpecialistWorker, Tenant


def test_person_is_abstract():
    with pytest.raises(TypeError):
        Person("nobody")  # type: ignore[abstract]


def test_role_polymorphism():
    people = [
        Tenant("Olena"),
        Dispatcher("Ivan"),
        SpecialistWorker("Petro", "electrical"),
    ]
    assert [p.role() for p in people] == ["tenant", "dispatcher", "specialist"]


def test_specialist_can_handle():
    electrician = SpecialistWorker("Petro", "electrical")
    assert electrician.can_handle("electrical")
    assert not electrician.can_handle("plumbing")

    handyman = SpecialistWorker("Mykola", "general")
    assert handyman.can_handle("plumbing")  # general handles anything


def test_describe_uses_role():
    assert Tenant("Olena").describe() == "tenant: Olena"
