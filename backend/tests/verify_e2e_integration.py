"""
End-to-End Live Integration Verification Script for SafeTriage.
Tests live HTTP endpoints on running FastAPI backend (port 8000) and Next.js frontend (port 3000).
"""

import httpx
import sys

BACKEND_URL = "http://127.0.0.1:8000/api/v1"
FRONTEND_URL = "http://localhost:3000"


def test_live_integration():
    client = httpx.Client(timeout=15.0)

    print("\n--- 1. Testing Frontend Home Page ---")
    res_front = client.get(FRONTEND_URL)
    print(f"GET {FRONTEND_URL} -> HTTP {res_front.status_code}")
    assert res_front.status_code == 200, "Frontend did not respond with 200"

    print("\n--- 2. Testing Backend Health Endpoint ---")
    res_health = client.get(f"{BACKEND_URL}/health")
    print(f"GET {BACKEND_URL}/health -> HTTP {res_health.status_code}")
    assert res_health.status_code == 200, "Backend health failed"
    health_data = res_health.json()
    print(f"  Rules loaded: {health_data['rules_loaded']}, ML Ready: {health_data['ml_baseline_ready']}")

    print("\n--- 2b. Testing User Registration & Sign In (Indian Clinician Profile) ---")
    import random
    rand_id = random.randint(1000, 9999)
    test_user_payload = {
        "email": f"dr.verma.{rand_id}@aiims.edu.in",
        "password": "SecurePassword123!",
        "full_name": "Dr. Sejal Verma",
        "role": "clinician"
    }
    res_reg = client.post(f"{BACKEND_URL}/auth/register", json=test_user_payload)
    print(f"POST {BACKEND_URL}/auth/register -> HTTP {res_reg.status_code}")
    assert res_reg.status_code == 201, "Registration failed"
    reg_data = res_reg.json()
    auth_token = reg_data["access_token"]
    print(f"  User Registered: {reg_data['user']['full_name']} ({reg_data['user']['email']})")

    # Test Login
    res_login = client.post(f"{BACKEND_URL}/auth/login", json={
        "email": test_user_payload["email"],
        "password": test_user_payload["password"]
    })
    print(f"POST {BACKEND_URL}/auth/login -> HTTP {res_login.status_code}")
    assert res_login.status_code == 200, "Login failed"

    # Test Profile /me
    res_me = client.get(f"{BACKEND_URL}/auth/me", headers={"Authorization": f"Bearer {auth_token}"})
    print(f"GET {BACKEND_URL}/auth/me -> HTTP {res_me.status_code}")
    assert res_me.status_code == 200, "User profile /me failed"
    print(f"  Authenticated User: {res_me.json()['full_name']}, Role: {res_me.json()['role']}")

    print("\n--- 3. Testing Symptom Assessment (Routine / Level 3) ---")
    payload_routine = {
        "text": "I have had a mild headache since yesterday, and today I started vomiting.",
        "duration": "yesterday",
        "severity": "moderate"
    }
    res_ass = client.post(f"{BACKEND_URL}/assessments", json=payload_routine)
    print(f"POST {BACKEND_URL}/assessments -> HTTP {res_ass.status_code}")
    assert res_ass.status_code == 201, "Assessment submission failed"
    ass_data = res_ass.json()
    ass_id = ass_data["id"]
    print(f"  Assessment ID: {ass_id}")
    print(f"  Triage Level: {ass_data['triage_level']} ({ass_data['title']})")
    print(f"  Detected Symptoms: {[s['name'] for s in ass_data['symptoms']]}")

    print("\n--- 4. Testing Adversarial Emergency Non-Downgrade Invariant ---")
    payload_emergency = {
        "text": "Crushing chest pain radiating down my left arm with severe shortness of breath.",
        "severity": "severe"
    }
    res_em = client.post(f"{BACKEND_URL}/assessments", json=payload_emergency)
    assert res_em.status_code == 201
    em_data = res_em.json()
    print(f"  Adversarial Emergency Triage Level: {em_data['triage_level']}")
    assert em_data["triage_level"] == "Level 1", "Emergency safety invariant violated!"
    assert em_data["is_emergency"] is True, "Emergency flag was not set!"

    print("\n--- 5. Testing Assessment Retrieval by ID ---")
    res_get = client.get(f"{BACKEND_URL}/assessments/{ass_id}")
    print(f"GET {BACKEND_URL}/assessments/{ass_id} -> HTTP {res_get.status_code}")
    assert res_get.status_code == 200
    assert res_get.json()["id"] == ass_id

    print("\n--- 6. Testing Assessment History Listing ---")
    res_list = client.get(f"{BACKEND_URL}/assessments")
    assert res_list.status_code == 200
    list_data = res_list.json()
    print(f"  Total historical assessments in SQLite: {list_data['total']}")
    assert list_data["total"] >= 2

    print("\n--- 7. Testing Research Dataset Stats Endpoint ---")
    res_stats = client.get(f"{BACKEND_URL}/research/dataset-stats")
    print(f"GET {BACKEND_URL}/research/dataset-stats -> HTTP {res_stats.status_code}")
    assert res_stats.status_code == 200
    stats = res_stats.json()
    print(f"  Total cases: {stats['total_cases']}, Families: {stats['template_families_count']}")
    print(f"  Splits: {stats['splits']}")
    assert stats["total_cases"] == 1000
    assert stats["splits"]["train"] == 700
    assert stats["splits"]["val"] == 150
    assert stats["splits"]["test"] == 150

    print("\n--- 8. Testing Synthetic Cases by Split ---")
    res_cases = client.get(f"{BACKEND_URL}/research/synthetic-cases?split=test")
    print(f"GET {BACKEND_URL}/research/synthetic-cases?split=test -> HTTP {res_cases.status_code}")
    assert res_cases.status_code == 200
    cases_test = res_cases.json()
    print(f"  Received {len(cases_test)} cases in held-out test split.")
    assert len(cases_test) == 150

    print("\n--- 9. Testing Research Evaluation Laboratory (Held-Out Test Split) ---")
    res_eval = client.post(
        f"{BACKEND_URL}/research/evaluate",
        json={"model_types": ["rule_based", "ml_baseline", "hybrid"], "dataset_name": "synthetic_bundled", "split": "test"}
    )
    print(f"POST {BACKEND_URL}/research/evaluate (split=test) -> HTTP {res_eval.status_code}")
    assert res_eval.status_code == 200
    eval_runs = res_eval.json()
    print(f"  Evaluated {len(eval_runs)} models on held-out test split (150 cases).")
    for run in eval_runs:
        print(f"    - Model: {run['model_type']:<15} Cases: {run['num_cases']}  Acc: {run['metrics']['accuracy']*100:.1f}%  Macro F1: {run['metrics']['macro_f1']:.3f}  Under-Triage: {run['metrics']['under_triage_rate_overall']*100:.1f}%")

    run_id = eval_runs[0]["run_id"]

    print("\n--- 10. Testing Evaluation Result Export (CSV & JSON) ---")
    res_export_csv = client.get(f"{BACKEND_URL}/research/export/{run_id}?format=csv")
    print(f"GET {BACKEND_URL}/research/export/{run_id}?format=csv -> HTTP {res_export_csv.status_code}")
    assert res_export_csv.status_code == 200
    assert "run_id,model_type" in res_export_csv.text

    res_export_json = client.get(f"{BACKEND_URL}/research/export/{run_id}?format=json")
    assert res_export_json.status_code == 200
    assert "metrics" in res_export_json.json()

    print("\n--- 11. Testing Assessment Deletion ---")
    res_del = client.delete(f"{BACKEND_URL}/assessments/{ass_id}")
    print(f"DELETE {BACKEND_URL}/assessments/{ass_id} -> HTTP {res_del.status_code}")
    assert res_del.status_code == 200

    print("\n========================================================")
    print("ALL 12 LIVE INTEGRATION TESTS PASSED SUCCESSFULLY!")
    print("========================================================\n")


if __name__ == "__main__":
    try:
        test_live_integration()
    except Exception as e:
        print(f"Integration Test FAILED: {str(e)}")
        sys.exit(1)
