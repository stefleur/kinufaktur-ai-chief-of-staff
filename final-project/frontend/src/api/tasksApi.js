// Resolution order:
// 1. `VITE_API_BASE_URL` (preferred repository/CI variable)
// 2. `VITE_API_BASE` (existing variable for compatibility)
// 3. Local dev: `http://localhost:8000` when running vite in dev mode
// 4. Production default: live FastAPI backend URL (used when no build-time var set)
const PROD_DEFAULT = "https://kinufaktur-ai-chief-of-staff-89a42968.fastapicloud.dev";
export const API_BASE_URL =
  import.meta.env?.VITE_API_BASE_URL ||
  import.meta.env?.VITE_API_BASE ||
  (import.meta.env.DEV ? "http://localhost:8000" : PROD_DEFAULT);

async function request(path, options = {}) {
  let response;

  try {
    response = await fetch(`${API_BASE_URL}${path}`, options);
  } catch {
    throw new Error("Could not connect to the KinuFlow backend.");
  }

  const contentType = response.headers.get("content-type") ?? "";
  const data = contentType.includes("application/json")
    ? await response.json()
    : null;

  if (!response.ok) {
    const message =
      typeof data?.detail === "string"
        ? data.detail
        : `Request failed with status ${response.status}.`;
    throw new Error(message);
  }

  return data;
}

function jsonRequest(method, body) {
  return {
    method,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  };
}

export function listTasks() {
  return request("/tasks");
}

export function getTask(taskId) {
  return request(`/tasks/${encodeURIComponent(taskId)}`);
}

export function createTask(taskInput) {
  return request("/tasks", jsonRequest("POST", taskInput));
}

export function updateTask(taskId, changes) {
  return request(
    `/tasks/${encodeURIComponent(taskId)}`,
    jsonRequest("PATCH", changes),
  );
}

export function deleteTask(taskId) {
  return request(`/tasks/${encodeURIComponent(taskId)}`, { method: "DELETE" });
}
