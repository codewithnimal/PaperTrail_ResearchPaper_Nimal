"""
Tests for evidence verification service.
"""
from app.services.evidence_verifier import EvidenceVerifier


def test_supported_numeric_claim():
    verifier = EvidenceVerifier()
    papers = [{
        "paper_id": "p1",
        "title": "BERT Paper",
        "extracted_text": "On the GLUE benchmark, BERT achieved an accuracy of 80.5% on MNLI and 93.2% accuracy on MRPC."
    }]

    # Exact matching number and unit
    result = verifier.verify("BERT achieved 80.5% on MNLI", papers)
    assert result["verification_status"] == "SUPPORTED"
    assert len(result["evidence"]) > 0


def test_contradicted_numeric_claim():
    verifier = EvidenceVerifier()
    papers = [{
        "paper_id": "p1",
        "title": "ResNet Paper",
        "extracted_text": "Our model achieves an error rate of 3.57% on the ImageNet test set."
    }]

    # Contradicting number
    result = verifier.verify("The model achieved 9.5% error rate on ImageNet", papers)
    assert result["verification_status"] == "CONTRADICTED"
    assert "contradicted" in result["verification_status"].lower() or "3.57" in result["explanation"]


def test_insufficient_evidence():
    verifier = EvidenceVerifier()
    papers = [{
        "paper_id": "p1",
        "title": "Quantum Computing",
        "extracted_text": "We examine superconducting qubits and cryogenic circuit architecture."
    }]

    result = verifier.verify("Convolutional neural networks outperform vision transformers on CIFAR-10", papers)
    assert result["verification_status"] == "INSUFFICIENT_EVIDENCE"


def test_not_comparable_metrics():
    verifier = EvidenceVerifier()
    papers = [{
        "paper_id": "p1",
        "title": "NLP Translation",
        "extracted_text": "Our model achieved a 41.8 BLEU score on English-to-French translation."
    }]

    # Claim talks about accuracy instead of BLEU
    result = verifier.verify("The translation model achieved 41.8% accuracy", papers)
    assert result["verification_status"] in ("NOT_COMPARABLE", "CONTRADICTED")
