const {
    apiUrl: BASE_PROJECTS_ENDPOINT,
    deleteUrlTemplate,
    editUrlTemplate,
    starUrlTemplate,
    csrfToken,
    isSuperuser: IS_SUPERUSER,
    canEdit: CAN_EDIT,
} = window.projectsConfig;

let projectsAbortController;

// Elemen DOM
const loadingState = document.getElementById("loading");
const errorState = document.getElementById("error");
const emptyState = document.getElementById("empty");
const gridContainer = document.getElementById("grid");
const searchForm = document.getElementById("project-search-form");
const searchInput = document.getElementById("search-input");

const SEARCH_DEBOUNCE_DELAY = 300;
const UUID_PLACEHOLDER = "00000000-0000-0000-0000-000000000000";
let searchDebounceTimer;

function displayPageSection({ showLoading = false, showError = false, showEmpty = false, showGrid = false }) {
    loadingState.classList.toggle("hide", !showLoading);
    errorState.classList.toggle("hide", !showError);
    emptyState.classList.toggle("hide", !showEmpty);
    gridContainer.classList.toggle("hide", !showGrid);
}

function buildProjectCardElement(item) {
    const project = item.fields;
    const projectId = item.pk;
    const articleElement = document.createElement("div");
    articleElement.className = "project-card";

    const imageHtml = project.image
        ? `<img class="project-img" src="${project.image}" alt="Photo of ${project.title}">`
        : "";
    const visitHtml = project.url_link
        ? `<a href="${project.url_link}" target="_blank" rel="noopener noreferrer" class="btn btn-secondary">Visit →</a>`
        : "";

    const deleteUrl = deleteUrlTemplate.replace(UUID_PLACEHOLDER, projectId);
    const editUrl = editUrlTemplate.replace(UUID_PLACEHOLDER, projectId);
    const starUrl = starUrlTemplate.replace(UUID_PLACEHOLDER, projectId);
    const csrfInput = `<input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">`;

    const editHtml = CAN_EDIT
        ? `<a href="${editUrl}" class="btn btn-secondary btn-sm">Edit</a>`
        : "";
    const deleteHtml = IS_SUPERUSER
        ? `<div class="project-card-actions"><form method="post" action="${deleteUrl}" class="project-delete-form">
                ${csrfInput}
                <input type="password" name="edit_secret" placeholder="Kode rahasia" required>
                <button type="submit" class="button button-danger" onclick="return confirm('Yakin ingin menghapus project ini?');">Hapus</button>
           </form></div>`
        : "";

    const starText = project.is_starred ? "Unstar" : "Star";
    const starClass = project.is_starred ? " is-starred" : "";
    const starTitle = project.star_count > 0
        ? `Dibintangi oleh ${project.starred_by_names}`
        : "Jadilah yang pertama memberi star";

    articleElement.innerHTML = `
        ${imageHtml}
        ${deleteHtml}
        <div class="project-desc">
            <h3>${project.title}</h3>
            <h4>Tech Stack: ${project.tech_stack || "-"}</h4>
            <p>${project.description}</p>
            <div class="project-actions">
                ${editHtml}
                <form method="post" action="${starUrl}" class="star-form">
                    ${csrfInput}
                    <button type="submit" class="button button-star${starClass}" title="${starTitle}">
                        <span aria-hidden="true">★</span>
                        ${starText}
                        <span class="star-count">${project.star_count}</span>
                    </button>
                </form>
                ${visitHtml}
            </div>
        </div>
    `;

    return articleElement;
}

async function fetchProjects(searchQuery = "") {
    if (projectsAbortController) projectsAbortController.abort();
    projectsAbortController = new AbortController();

    try {
        displayPageSection({ showLoading: true });
        const url = searchQuery
            ? `${BASE_PROJECTS_ENDPOINT}?title=${encodeURIComponent(searchQuery)}`
            : BASE_PROJECTS_ENDPOINT;
        const response = await fetch(url, {
            headers: { Accept: "application/json" },
            signal: projectsAbortController.signal,
        });

        if (!response.ok) throw new Error("Failed to fetch projects");

        const projectData = await response.json();
        if (projectData.length === 0) {
            gridContainer.innerHTML = "";
            displayPageSection({ showEmpty: true });
            return;
        }

        gridContainer.innerHTML = "";
        projectData.forEach((item) => gridContainer.appendChild(buildProjectCardElement(item)));
        displayPageSection({ showGrid: true });
    } catch (error) {
        if (error.name === "AbortError") return;
        console.error("Error loading projects:", error);
        displayPageSection({ showError: true });
    }
}

searchInput.addEventListener("input", () => {
    clearTimeout(searchDebounceTimer);
    searchDebounceTimer = setTimeout(() => fetchProjects(searchInput.value.trim()), SEARCH_DEBOUNCE_DELAY);
});

searchForm.addEventListener("submit", (event) => {
    event.preventDefault();
    clearTimeout(searchDebounceTimer);
    fetchProjects(searchInput.value.trim());
});

fetchProjects(searchInput.value.trim());
