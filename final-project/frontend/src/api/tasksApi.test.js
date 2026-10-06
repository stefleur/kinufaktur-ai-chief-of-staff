import { expect, it, vi } from "vitest";
import { API_BASE_URL, listTasks } from "./tasksApi";

it("decodes a successful JSON response", async () => {
  const tasks = [{ id: "demo-1", title: "Synthetic task" }];
  const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify(tasks), {
    status: 200, headers: { "Content-Type": "application/json" },
  }));
  vi.stubGlobal("fetch", fetchMock);
  await expect(listTasks()).resolves.toEqual(tasks);
  expect(fetchMock).toHaveBeenCalledWith(`${API_BASE_URL}/tasks`, {});
});

it("reports the backend's error message", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({ detail: "Task not found." }), {
    status: 404, headers: { "Content-Type": "application/json" },
  })));
  await expect(listTasks()).rejects.toThrow("Task not found.");
});

it("reports a useful connection error on network failure", async () => {
  vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new TypeError("Failed to fetch")));
  await expect(listTasks()).rejects.toThrow("Could not connect to the KinuFlow backend.");
});
