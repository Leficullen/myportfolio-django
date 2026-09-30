const {
    apiUrl: BASE_PROJECTS_ENDPOINT,
    deleteUrlTemplate,
    editUrlTemplate,
    starUrlTemplate,
    csrfToken,
    isSuperuser: IS_SUPERUSER,
     canEdit: CAN_EDIT,
    createProjectUrl: CREATE_PROJECT_ENDPOINT,
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

// Mengubah karakter khusus HTML menjadi entity agar ditampilkan sebagai teks
function escapeHtml(value) {
     return String(value ?? '')
          .replaceAll('&', '&amp;')
          .replaceAll('<', '&lt;')
          .replaceAll('>', '&gt;')
          .replaceAll('"', '&quot;')
          .replaceAll("'", '&#39;');
}

function buildProjectCardElement(item) {
    const project = item.fields;
    const projectId = String(item.pk ?? "");
    const escapedProjectId = escapeHtml(projectId);
    const projectTitle = escapeHtml(project.title);
    const projectImage = escapeHtml(project.image);
    const projectUrlLink = escapeHtml(project.url_link);
    const projectDescription = escapeHtml(project.description);
    const projectTechStack = escapeHtml(project.tech_stack || "-");
    const projectStarCount = escapeHtml(project.star_count);
    const starredByNames = escapeHtml(project.starred_by_names);
    const articleElement = document.createElement("div");
    articleElement.className = "project-card";

    const imageHtml = project.image
        ? `<img class="project-img" src="${projectImage}" alt="Photo of ${projectTitle}">`
        : "";
    const visitHtml = project.url_link
        ? `<a href="${projectUrlLink}" target="_blank" rel="noopener noreferrer" class="btn btn-secondary">Visit →</a>`
        : "";

    const deleteUrl = deleteUrlTemplate.replace(UUID_PLACEHOLDER, projectId);
    const editUrl = editUrlTemplate.replace(UUID_PLACEHOLDER, projectId);
    const starUrl = starUrlTemplate.replace(UUID_PLACEHOLDER, projectId);
    const csrfInput = `<input type="hidden" name="csrfmiddlewaretoken" value="${escapeHtml(csrfToken)}">`;

    const editHtml = CAN_EDIT
        ? `<a href="${escapeHtml(editUrl)}" class="btn btn-secondary btn-sm">Edit</a>`
        : "";
    const deleteModalId = `delete-project-${escapedProjectId}`;
    const deleteHtml = IS_SUPERUSER
        ? `<div class="project-card-actions">
                <button type="button"
                        class="button button-danger"
                        popovertarget="${deleteModalId}"
                        aria-label="Hapus ${projectTitle}"
                        title="Hapus proyek">Hapus</button>
           </div>
           <div id="${deleteModalId}"
                class="project-delete-modal"
                popover="auto"
                role="dialog"
                aria-modal="true"
                aria-labelledby="${deleteModalId}-title">
                <button type="button"
                        class="project-delete-modal__backdrop"
                        popovertarget="${deleteModalId}"
                        popovertargetaction="hide"
                        aria-label="Tutup konfirmasi hapus"></button>
                <div class="project-delete-modal__content">
                    <button type="button"
                            class="project-delete-modal__close"
                            popovertarget="${deleteModalId}"
                            popovertargetaction="hide"
                            aria-label="Tutup konfirmasi hapus">×</button>
                    <h2 id="${deleteModalId}-title">Hapus Projek?</h2>
                    <p>Apakah Anda yakin ingin menghapus <strong>${projectTitle}</strong>?</p>
                    <div class="project-delete-modal__actions">
                        <form method="post" action="${escapeHtml(deleteUrl)}">
                            ${csrfInput}
                            <input type="password"
                                   name="edit_secret"
                                   class="project-delete-modal__secret"
                                   placeholder="Kode rahasia"
                                   required>
                            <button type="submit" class="button button-danger">Ya, Hapus</button>
                        </form>
                    </div>
                </div>
           </div>`
        : "";

    const starText = project.is_starred ? "Unstar" : "Star";
    const starClass = project.is_starred ? " is-starred" : "";
    const starTitle = project.star_count > 0
        ? `Dibintangi oleh ${starredByNames}`
        : "Jadilah yang pertama memberi star";

    articleElement.innerHTML = `
        ${imageHtml}
        ${deleteHtml}
        <div class="project-desc">
            <h3>${projectTitle}</h3>
            <h4>Tech Stack: ${projectTechStack}</h4>
            <p>${projectDescription}</p>
            <div class="project-actions">
                ${editHtml}
                <form method="post" action="${escapeHtml(starUrl)}" class="star-form">
                    ${csrfInput}
                    <button type="submit" class="button button-star${starClass}" title="${escapeHtml(starTitle)}">
                        <span aria-hidden="true">★</span>
                        ${starText}
                        <span class="star-count">${projectStarCount}</span>
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

function closeProjectModal() {
    document.getElementById("add-project-modal").hidePopover();
}

const projectForm = document.getElementById('project-form');

// Membaca nilai cookie, digunakan untuk mengambil token CSRF
function getCookie(name) {
     let cookieValue = null;
     if (document.cookie && document.cookie !== '') {
          const cookies = document.cookie.split(';');
          for (let i = 0; i < cookies.length; i++) {
               const cookie = cookies[i].trim();
               if (cookie.substring(0, name.length + 1) === (name + '=')) {
               cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
               break;
               }
          }
     }
     return cookieValue;
}

// Mengirim data form ke server
async function addProject(event) {
     event.preventDefault();

     const submitButton = projectForm.querySelector('button[type="submit"]');
     submitButton.disabled = true;

     try {
          const response = await fetch(CREATE_PROJECT_ENDPOINT, {
               method: 'POST',
               headers: { 'X-CSRFToken': getCookie('csrftoken') },
               body: new FormData(projectForm),
          });
          const result = await response.json().catch(() => ({}));

          if (response.ok) {
               projectForm.reset();
               closeProjectModal();
               showToast('Berhasil', 'Proyek baru berhasil ditambahkan!', 'success');
               fetchProjects(searchInput.value.trim());
          } else {
               const errorMessages = result.errors
               ? Object.values(result.errors).flat().map(error => error.message)
               : [result.message || `Terjadi kesalahan (status ${response.status}).`];
               showToast('Gagal menambahkan proyek', errorMessages.join(' '), 'error');
          }
     } catch (error) {
          console.error('Error adding project:', error);
          showToast('Gagal menambahkan proyek', 'Tidak dapat terhubung ke server. Silakan coba lagi.', 'error');
     } finally {
          submitButton.disabled = false;
     }
}

if (projectForm) {
     projectForm.addEventListener('submit', addProject);
}

fetchProjects(searchInput.value.trim());
