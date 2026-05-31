"""
Tests for task API endpoints (in-memory CRUD).
"""
import pytest


class TestTaskEndpoints:
    """Test suite for /api/tasks endpoints.

    The task store is module-level global state shared across requests, so each
    test that creates a task deletes it again to stay independent and avoid
    leaking state into other tests.
    """

    def test_get_all_tasks(self, client):
        """Test getting all tasks returns a list."""
        response = client.get("/api/tasks")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)

    def test_create_task(self, client):
        """Test creating a task returns the created task with defaults applied."""
        response = client.post("/api/tasks", json={
            "title": "Restock circuit boards",
            "priority": "high",
            "dueDate": "2025-07-01"
        })
        assert response.status_code == 200

        task = response.json()
        assert "id" in task
        assert task["title"] == "Restock circuit boards"
        assert task["priority"] == "high"
        assert task["dueDate"] == "2025-07-01"
        assert task["status"] == "pending"

        # Clean up
        client.delete(f"/api/tasks/{task['id']}")

    def test_create_task_uses_defaults(self, client):
        """Test that priority/status default when only a title is provided."""
        response = client.post("/api/tasks", json={"title": "Audit inventory"})
        assert response.status_code == 200

        task = response.json()
        assert task["priority"] == "medium"
        assert task["status"] == "pending"
        assert task["dueDate"] is None

        client.delete(f"/api/tasks/{task['id']}")

    def test_create_task_appears_in_list(self, client):
        """Test that a created task is returned by the list endpoint."""
        created = client.post("/api/tasks", json={"title": "Reconcile orders"}).json()

        response = client.get("/api/tasks")
        assert response.status_code == 200
        ids = [t["id"] for t in response.json()]
        assert created["id"] in ids

        client.delete(f"/api/tasks/{created['id']}")

    def test_create_task_validation_error(self, client):
        """Test that creating a task without a title returns 422."""
        response = client.post("/api/tasks", json={"priority": "low"})
        assert response.status_code == 422

        data = response.json()
        assert "detail" in data

    def test_toggle_task_status(self, client):
        """Test toggling a task flips pending <-> completed."""
        created = client.post("/api/tasks", json={"title": "Toggle me"}).json()
        task_id = created["id"]

        # pending -> completed
        response = client.patch(f"/api/tasks/{task_id}")
        assert response.status_code == 200
        assert response.json()["status"] == "completed"

        # completed -> pending
        response = client.patch(f"/api/tasks/{task_id}")
        assert response.status_code == 200
        assert response.json()["status"] == "pending"

        client.delete(f"/api/tasks/{task_id}")

    def test_delete_task(self, client):
        """Test deleting a task removes it from the store."""
        created = client.post("/api/tasks", json={"title": "Delete me"}).json()
        task_id = created["id"]

        response = client.delete(f"/api/tasks/{task_id}")
        assert response.status_code == 200
        assert "message" in response.json()

        # It should no longer be present
        ids = [t["id"] for t in client.get("/api/tasks").json()]
        assert task_id not in ids

    def test_delete_nonexistent_task(self, client):
        """Test deleting a task that doesn't exist returns 404."""
        response = client.delete("/api/tasks/nonexistent-task-999")
        assert response.status_code == 404

        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_toggle_nonexistent_task(self, client):
        """Test toggling a task that doesn't exist returns 404."""
        response = client.patch("/api/tasks/nonexistent-task-999")
        assert response.status_code == 404

        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()
