const {
     apiUrl: BASE_EXPERIENCE_ENDPOINT,
     editUrlTemplate,
     csrfToken,
     isAuthenticated: IS_AUTHENTICATED,
     isSuperuser: IS_SUPERUSER,
     canEdit: CAN_EDIT,
} = window.experiencesConfig;

const UUID_PLACEHOLDER = "00000000-0000-0000-0000-000000000000";
let experiencesAbortController;

const loadingState = document.getElementById("experience-loading");
const errorState = document.getElementById("experience-error");
const emptyState = document.getElementById("experience-empty");
const gridContainer = document.getElementById("experience-grid");
const searchForm = document.getElementById("experience-search-form");
const searchInput = document.getElementById("experience-search-input");

const displayExperienceSection = (
     { showLoading = false, showError = false, showEmpty = false, showGrid = false }
) => {
     loadingState.classList.toggle("hide", !showLoading);
     errorState.classList.toggle("hide", !showError);
     emptyState.classList.toggle("hide", !showEmpty);
     gridContainer.classList.toggle("hide", !showGrid);
};

const escapeHtml = (value) => {
     return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
};

const buildExperienceCard = (experience) => {
     const experienceId = String(experience.id ?? "");

     const title = escapeHtml(experience.title);
     const description = escapeHtml(experience.description);
     const categoryDisplay = escapeHtml(experience.category_display);
     const starCount = escapeHtml(experience.star_count);
     const starredByNames = escapeHtml(experience.starred_by_names);
     const statusText = experience.is_current ? "Sedang berlangsung" : "Selesai";

     const editUrl = editUrlTemplate.replace(UUID_PLACEHOLDER, experienceId);
     const editHtml = CAN_EDIT
          ? `<a href="${escapeHtml(editUrl)}" class="btn btn-outline btn-sm">Edit</a>`
          : "";

     const isStarred = experience.is_starred;
     const starText = isStarred ? "Unstar" : "Star";
     const starClass = isStarred ? " is-starred" : "";
     const starTitle = experience.star_count > 0
          ? `Dibintangi oleh ${starredByNames}`
          : "Jadilah yang pertama memberi star";
     const starHtml = IS_AUTHENTICATED
          ? `<button type="button" class="button button-star${starClass}"
                     data-star-id="${escapeHtml(experienceId)}"
                     title="${escapeHtml(starTitle)}">
                 <span aria-hidden="true">★</span>
                 ${starText}
                 <span class="star-count">${starCount}</span>
             </button>`
          : "";

     const deleteHtml = IS_SUPERUSER
          ? `<button type="button" class="button button-danger"
                     data-delete-id="${escapeHtml(experienceId)}"
                     data-delete-title="${title}">Hapus</button>`
          : "";

     const articleElement = document.createElement("article");
     articleElement.className = "experience-card";
     articleElement.innerHTML = `
          <div class="experience-card__meta">
               <span class="experience-category">${categoryDisplay}</span>
               <span class="experience-status">${statusText}</span>
          </div>
          <h2>${title}</h2>
          <p class="experience-description">${description}</p>
          <div class="experience-card__actions">
               ${editHtml}
               ${starHtml}
               ${deleteHtml}
          </div>
     `;
     return articleElement;
};

const fetchExperiences = async (query = "") => {
     if (experiencesAbortController) experiencesAbortController.abort();
     experiencesAbortController = new AbortController();

     try {
          displayExperienceSection({ showLoading: true });

          const url = query
               ? `${BASE_EXPERIENCE_ENDPOINT}?title=${encodeURIComponent(query)}`
               : BASE_EXPERIENCE_ENDPOINT;

          const response = await fetch(url, {
               headers: { Accept: "application/json" },
               signal: experiencesAbortController.signal,
          });

          if (!response.ok) {
               throw new Error("Failed to fetch experiences");
          }

          const experienceData = await response.json();

          if (experienceData.length === 0) {
               gridContainer.innerHTML = "";
               displayExperienceSection({ showEmpty: true });
               return;
          }

          gridContainer.innerHTML = "";
          experienceData.forEach((experience) => {
               gridContainer.appendChild(buildExperienceCard(experience));
          });

          displayExperienceSection({ showGrid: true });
     } catch (error) {
          if (error.name === "AbortError") {
               return;
          }
          console.error("Error occured: ", error);
          displayExperienceSection({ showError: true });
     }
};

const SEARCH_DEBOUNCE_DELAY = 300;
let searchDebounceTimer;

const searchExperiences = () => {
     fetchExperiences(searchInput.value.trim());
};

searchInput.addEventListener("input", () => {
     clearTimeout(searchDebounceTimer);
     searchDebounceTimer = setTimeout(() => {
          searchExperiences();
     }, SEARCH_DEBOUNCE_DELAY);
});

searchForm.addEventListener("submit", (event) => {
     event.preventDefault();
     clearTimeout(searchDebounceTimer);
     searchExperiences();
});

const experienceForm = document.getElementById("experience-form");

const closeExperienceModal = () => {
     document.getElementById("add-experience-modal").hidePopover();
};

const getCookie = (name) => {
     let cookieValue = null;
     if (document.cookie && document.cookie !== "") {
          const cookies = document.cookie.split(";");
          for (let i = 0; i < cookies.length; i += 1) {
               const cookie = cookies[i].trim();
               if (cookie.startsWith(`${name}=`)) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
               }
          }
     }
     return cookieValue;
};

const addExperience = async (event) => {
     event.preventDefault();

     const submitButton = experienceForm.querySelector('button[type="submit"]');
     submitButton.disabled = true;

     try {
          const response = await fetch(BASE_EXPERIENCE_ENDPOINT, {
               method: "POST",
               headers: { "X-CSRFToken": getCookie("csrftoken") },
               body: new FormData(experienceForm),
          });

          const result = await response.json().catch(() => ({}));

          if (response.ok) {
               experienceForm.reset();
               closeExperienceModal();
               showToast("Berhasil", "Experience berhasil ditambahkan", "success");
               fetchExperiences(searchInput.value.trim());
          } else {
               const errorMessages = Object.values(result).flat().join(" ")
                    || `Terjadi kesalahan (status ${response.status}).`;
               showToast("Gagal menambahkan pengalaman", errorMessages, "error");
          }
     } catch (error) {
          console.error("Error adding experience:", error);
          showToast(
               "Gagal menambahkan pengalaman",
               "Tidak dapat terhubung ke server. Silakan coba lagi.",
               "error"
          );
     } finally {
          submitButton.disabled = false;
     }
};

if (experienceForm) {
     experienceForm.addEventListener("submit", addExperience);
}

const toggleStar = async (id) => {
     try {
          const response = await fetch(`${BASE_EXPERIENCE_ENDPOINT}${id}/star/`, {
               method: "POST",
               headers: { "X-CSRFToken": getCookie("csrftoken") },
          });
          if (!response.ok) {
               const msg = response.status === 403
                    ? "Anda harus login untuk memberi star."
                    : `Terjadi kesalahan (status ${response.status}).`;
               showToast("Gagal", msg, "error");
               return;
          }
          fetchExperiences(searchInput.value.trim());
     } catch (error) {
          showToast("Gagal", "Tidak dapat terhubung ke server.", "error");
     }
};

const deleteExperience = async (id, title) => {
     if (!confirm(`Hapus experience "${title}"?`)) return;
     try {
          const response = await fetch(`${BASE_EXPERIENCE_ENDPOINT}${id}/`, {
               method: "DELETE",
               headers: { "X-CSRFToken": getCookie("csrftoken") },
          });
          if (response.status === 204) {
               showToast("Berhasil", "Experience dihapus.", "success");
               fetchExperiences(searchInput.value.trim());
          } else if (response.status === 403) {
               showToast("Ditolak", "Anda tidak punya izin menghapus.", "error");
          } else {
               showToast("Gagal", `Terjadi kesalahan (status ${response.status}).`, "error");
          }
     } catch (error) {
          showToast("Gagal", "Tidak dapat terhubung ke server.", "error");
     }
};

gridContainer.addEventListener("click", (event) => {
     const starBtn = event.target.closest("[data-star-id]");
     if (starBtn) { toggleStar(starBtn.dataset.starId); return; }

     const delBtn = event.target.closest("[data-delete-id]");
     if (delBtn) { deleteExperience(delBtn.dataset.deleteId, delBtn.dataset.deleteTitle); return; }
});

fetchExperiences(searchInput.value.trim());
