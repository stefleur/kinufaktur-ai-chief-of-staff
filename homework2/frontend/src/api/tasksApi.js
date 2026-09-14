const now = new Date().toISOString();

let mockTasks = [
  {
    id: "task-1",
    title: "Automate invoice intake",
    description: "Map the current invoice workflow and identify repetitive steps.",
    category: "AI Automation",
    priority: "High",
    status: "analyzing",
    created_at: now,
    updated_at: now,
  },
  {
    id: "task-2",
    title: "Consolidate customer data",
    description: "Define the source of truth for active customer records.",
    category: "Data",
    priority: "High",
    status: "planned",
    created_at: now,
    updated_at: now,
  },
  {
    id: "task-3",
    title: "Document weekly review",
    description: "Create a lightweight checklist for the weekly operations review.",
    category: "Internal Operations",
    priority: "Medium",
    status: "incoming",
    created_at: now,
    updated_at: now,
  },
  {
    id: "task-4",
    title: "Prepare support workflow",
    description: "Draft the hand-off steps for incoming support requests.",
    category: "Other",
    priority: "Low",
    status: "done",
    created_at: now,
    updated_at: now,
  },
];

function clone(value) {
  return structuredClone(value);
}

function waitForMockResponse(result) {
  return new Promise((resolve) => {
    window.setTimeout(() => resolve(clone(result)), 120);
  });
}

export async function listTasks() {
  return waitForMockResponse(mockTasks);
}

export async function createTask(taskInput) {
  const timestamp = new Date().toISOString();
  const task = {
    ...taskInput,
    id: crypto.randomUUID(),
    created_at: timestamp,
    updated_at: timestamp,
  };

  mockTasks = [task, ...mockTasks];
  return waitForMockResponse(task);
}

export async function updateTask(taskId, changes) {
  const taskIndex = mockTasks.findIndex((task) => task.id === taskId);

  if (taskIndex === -1) {
    throw new Error("Task not found.");
  }

  const updatedTask = {
    ...mockTasks[taskIndex],
    ...changes,
    id: taskId,
    updated_at: new Date().toISOString(),
  };

  mockTasks = mockTasks.map((task) =>
    task.id === taskId ? updatedTask : task,
  );
  return waitForMockResponse(updatedTask);
}

export async function deleteTask(taskId) {
  const taskExists = mockTasks.some((task) => task.id === taskId);

  if (!taskExists) {
    throw new Error("Task not found.");
  }

  mockTasks = mockTasks.filter((task) => task.id !== taskId);
  return waitForMockResponse({ id: taskId });
}
