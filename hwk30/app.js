const API_URL = "https://jsonplaceholder.typicode.com/todos";

const state = {
  todos: [],
  filtered: [],
  search: "",
  userId: "all",
  completed: "all",
  pageSize: 10,
  page: 1,
};

const els = {
  search: document.getElementById("search"),
  userFilter: document.getElementById("userFilter"),
  completedFilter: document.getElementById("completedFilter"),
  pageSize: document.getElementById("pageSize"),
  resultsInfo: document.getElementById("resultsInfo"),
  loading: document.getElementById("loading"),
  error: document.getElementById("error"),
  todoList: document.getElementById("todoList"),
  pagination: document.getElementById("pagination"),
};

function debounce(fn, delay) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}

async function loadTodos() {
  try {
    const res = await fetch(API_URL);
    if (!res.ok) throw new Error(`Request failed with status ${res.status}`);
    state.todos = await res.json();
    populateUserFilter();
    applyFilters();
  } catch (err) {
    els.error.textContent = `Failed to load todos: ${err.message}`;
    els.error.classList.remove("hidden");
  } finally {
    els.loading.classList.add("hidden");
  }
}

function populateUserFilter() {
  const userIds = [...new Set(state.todos.map((t) => t.userId))].sort((a, b) => a - b);
  for (const id of userIds) {
    const option = document.createElement("option");
    option.value = String(id);
    option.textContent = `User ${id}`;
    els.userFilter.appendChild(option);
  }
}

function applyFilters() {
  const search = state.search.trim().toLowerCase();

  state.filtered = state.todos.filter((todo) => {
    const matchesSearch = !search || todo.title.toLowerCase().includes(search);
    const matchesUser = state.userId === "all" || todo.userId === Number(state.userId);
    const matchesCompleted =
      state.completed === "all" || String(todo.completed) === state.completed;
    return matchesSearch && matchesUser && matchesCompleted;
  });

  state.page = 1;
  render();
}

function render() {
  renderList();
  renderPagination();
  renderResultsInfo();
}

function renderResultsInfo() {
  const total = state.filtered.length;
  if (total === 0) {
    els.resultsInfo.textContent = "No todos match your filters.";
    return;
  }
  const start = (state.page - 1) * state.pageSize + 1;
  const end = Math.min(start + state.pageSize - 1, total);
  els.resultsInfo.textContent = `Showing ${start}-${end} of ${total} todos`;
}

function renderList() {
  els.todoList.innerHTML = "";

  if (state.filtered.length === 0) {
    const li = document.createElement("li");
    li.className = "no-results";
    li.textContent = "No todos found.";
    els.todoList.appendChild(li);
    return;
  }

  const start = (state.page - 1) * state.pageSize;
  const pageItems = state.filtered.slice(start, start + state.pageSize);

  for (const todo of pageItems) {
    const li = document.createElement("li");
    li.className = "todo-item";

    const link = document.createElement("a");
    link.className = "todo-link";
    link.href = `detail.html?id=${todo.id}`;

    const dot = document.createElement("span");
    dot.className = `status-dot ${todo.completed ? "completed" : "pending"}`;

    const title = document.createElement("span");
    title.className = "todo-title";
    title.textContent = todo.title;

    link.appendChild(dot);
    link.appendChild(title);
    li.appendChild(link);
    els.todoList.appendChild(li);
  }
}

function renderPagination() {
  els.pagination.innerHTML = "";

  const totalPages = Math.ceil(state.filtered.length / state.pageSize);
  if (totalPages <= 1) return;

  const makeButton = (label, page, opts = {}) => {
    const btn = document.createElement("button");
    btn.textContent = label;
    if (opts.active) btn.classList.add("active");
    if (opts.disabled) btn.disabled = true;
    btn.addEventListener("click", () => {
      state.page = page;
      render();
    });
    return btn;
  };

  els.pagination.appendChild(
    makeButton("Prev", state.page - 1, { disabled: state.page === 1 })
  );

  const pageNumbers = getPageWindow(state.page, totalPages);
  for (const p of pageNumbers) {
    if (p === "...") {
      const span = document.createElement("span");
      span.className = "ellipsis";
      span.textContent = "...";
      els.pagination.appendChild(span);
    } else {
      els.pagination.appendChild(makeButton(String(p), p, { active: p === state.page }));
    }
  }

  els.pagination.appendChild(
    makeButton("Next", state.page + 1, { disabled: state.page === totalPages })
  );
}

function getPageWindow(current, total) {
  const delta = 2;
  const pages = [];
  for (let i = 1; i <= total; i++) {
    if (i === 1 || i === total || (i >= current - delta && i <= current + delta)) {
      pages.push(i);
    }
  }

  const withEllipsis = [];
  let prev = null;
  for (const p of pages) {
    if (prev !== null && p - prev > 1) withEllipsis.push("...");
    withEllipsis.push(p);
    prev = p;
  }
  return withEllipsis;
}

els.search.addEventListener(
  "input",
  debounce((e) => {
    state.search = e.target.value;
    applyFilters();
  }, 250)
);

els.userFilter.addEventListener("change", (e) => {
  state.userId = e.target.value;
  applyFilters();
});

els.completedFilter.addEventListener("change", (e) => {
  state.completed = e.target.value;
  applyFilters();
});

els.pageSize.addEventListener("change", (e) => {
  state.pageSize = Number(e.target.value);
  state.page = 1;
  render();
});

loadTodos();
