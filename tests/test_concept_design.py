"""Tests pour unified-design concept_design."""

from src.concept_design import ConceptDesign, build_concept_design


def test_build_concept_design() -> None:
    instance = build_concept_design()
    assert isinstance(instance, ConceptDesign)


def test_health_concept_design() -> None:
    instance = build_concept_design()
    health = instance.health()
    assert health["status"] == "ok"
