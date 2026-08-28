const API_URL = "https://jsonplaceholder.typicode.com/todos";

const els = {
  loading: document.getElementById("loading"),
  error: document.getElementById("error"),
  card: document.getElementById("detailCard"),
  title: document.getElementById("detailTitle"),
  id: document.getElementById("detailId"),
  userId: document.getElementById("detailUserId"),
  fullTitle: document.getElementById("detailFullTitle"),
  completed: document.getElementById("detailCompleted"),
};

function getTodoId() {
  const params = new URLSearchParams(window.location.search);
  return params.get("id");
}

async function loadTodo() {
  const id = getTodoId();

  if (!id) {
    showError("No todo id was provided in the URL.");
    return;
  }

  try {
    const res = await fetch(`${API_URL}/${encodeURIComponent(id)}`);
    if (!res.ok) throw new Error(`Request failed with status ${res.status}`);
    const todo = await res.json();

    if (!todo || !todo.id) {
      showError(`Todo with id "${id}" was not found.`);
      return;
    }

    renderTodo(todo);
  } catch (err) {
    showError(`Failed to load todo: ${err.message}`);
  } finally {
    els.loading.classList.add("hidden");
  }
}

function renderTodo(todo) {
  document.title = `Todo #${todo.id} - ${todo.title}`;

  els.title.textContent = todo.title;
  els.id.textContent = todo.id;
  els.userId.textContent = todo.userId;
  els.fullTitle.textContent = todo.title;

  const badge = document.createElement("span");
  badge.className = `badge ${todo.completed ? "completed" : "pending"}`;
  badge.textContent = todo.completed ? "Completed" : "Not completed";
  els.completed.innerHTML = "";
  els.completed.appendChild(badge);

  els.card.classList.remove("hidden");
}

function showError(message) {
  els.error.textContent = message;
  els.error.classList.remove("hidden");
  els.loading.classList.add("hidden");
}

loadTodo();
