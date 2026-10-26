"""
Unit test for comparison service normalization and validation.
"""
import pytest
from app.services.comparison import ComparisonService
from app.schemas import CompareResponse

def test_normalize_comparison_result():
    service = ComparisonService()
    job_id = "test-job-123"
    loaded_papers = [
        {"paper_id": "56d84895-02f4-49c3-87bc-949b86a2c9d6", "title": "Paper A"},
        {"paper_id": "009a89bd-1939-488a-afae-cc0f32f8f236", "title": "Paper B"}
    ]
    raw_llm_payload = {
        "summary": "Comparing Paper A and Paper B.",
        "research_problem": {
            "56d84895-02f4-49c3-87bc-949b86a2c9d6": "Medical image classification",
            "009a89bd-1939-488a-afae-cc0f32f8f236": "Skin lesion detection"
        },
        "methodology": {
            "56d84895-02f4-49c3-87bc-949b86a2c9d6": "Vision Transformer",
            "009a89bd-1939-488a-afae-cc0f32f8f236": "ResNet-50"
        },
        "dataset": {
            "56d84895-02f4-49c3-87bc-949b86a2c9d6": "ISIC 2019",
            "009a89bd-1939-488a-afae-cc0f32f8f236": "HAM10000"
        },
        "evaluation_metrics": {
            "56d84895-02f4-49c3-87bc-949b86a2c9d6": "AUC, Accuracy",
            "009a89bd-1939-488a-afae-cc0f32f8f236": "Accuracy, F1"
        },
        "reported_results": {
            "56d84895-02f4-49c3-87bc-949b86a2c9d6": {"accuracy": "86.0%", "precision": "85.2%"},
            "009a89bd-1939-488a-afae-cc0f32f8f236": {"accuracy": "82.0%", "precision": "81.0%"}
        },
        "limitations": {
            "56d84895-02f4-49c3-87bc-949b86a2c9d6": "Small sample size",
            "009a89bd-1939-488a-afae-cc0f32f8f236": "Single center data"
        },
        "future_work": {
            "56d84895-02f4-49c3-87bc-949b86a2c9d6": "Multi-center trial",
            "009a89bd-1939-488a-afae-cc0f32f8f236": "Federated learning"
        },
        "evidence_references": {
            "56d84895-02f4-49c3-87bc-949b86a2c9d6": {"page_number": 3, "text": "Model achieved 86.0% accuracy."},
            "009a89bd-1939-488a-afae-cc0f32f8f236": [{"page_number": 4, "text": "ResNet-50 reached 82.0%."}]
        },
        "uncertainty_notes": {
            "56d84895-02f4-49c3-87bc-949b86a2c9d6": "Impact not evaluated."
        },
        "research_gaps": {
            "cross_institution_validation": "Patterns are not explored."
        },
        "comparison_matrix": {
            "precision": {
                "56d84895-02f4-49c3-87bc-949b86a2c9d6": 0.85,
                "009a89bd-1939-488a-afae-cc0f32f8f236": 0.81
            },
            "cross_validation_folds": {
                "56d84895-02f4-49c3-87bc-949b86a2c9d6": 5,
                "009a89bd-1939-488a-afae-cc0f32f8f236": 3
            }
        }
    }

    normalized = service._normalize_comparison_result(job_id, raw_llm_payload, loaded_papers)
    validated = CompareResponse(**normalized)

    assert validated.job_id == job_id
    assert "accuracy: 86.0%" in validated.reported_results["56d84895-02f4-49c3-87bc-949b86a2c9d6"]
    assert isinstance(validated.evidence_references, list)
    assert len(validated.evidence_references) == 2
    assert isinstance(validated.uncertainty_notes, list)
    assert len(validated.uncertainty_notes) == 1
    assert isinstance(validated.research_gaps, list)
    assert len(validated.research_gaps) == 1
    assert validated.comparison_matrix["precision"]["56d84895-02f4-49c3-87bc-949b86a2c9d6"] == "0.85"
    assert validated.comparison_matrix["cross_validation_folds"]["56d84895-02f4-49c3-87bc-949b86a2c9d6"] == "5"
