const {
     apiUrl: BASE_EXPERIENCE_ENDPOINT,
     createExperienceUrl: CREATE_EXPERIENCE_ENDPOINT,
     deleteUrlTemplate,
     editUrlTemplate,
     starUrlTemplate,
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
}

const escapeHtml = (value) => {
     return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
}

const buildExperienceCard = (item) => {
     const experience = item.fields;
     const experienceId = String(item.pk ?? "");

     const title = escapeHtml(experience.title);
     const description = escapeHtml(experience.description);
     const categoryDisplay = escapeHtml(experience.category_display);
     const starCount = escapeHtml(experience.star_count);
     const starredByNames = escapeHtml(experience.starred_by_names);

     const statusText = experience.is_ongoing ? "Sedang berlangsung" : "Selesai";
     const editUrl = editUrlTemplate.replace(UUID_PLACEHOLDER, experienceId);
     const starUrl = starUrlTemplate.replace(UUID_PLACEHOLDER, experienceId);
     const deleteUrl = deleteUrlTemplate.replace(UUID_PLACEHOLDER, experienceId);
     const csrfInput = `<input type="hidden" name="csrfmiddlewaretoken" value="${escapeHtml(csrfToken)}">`;

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
          ? `<form method="post" action="${escapeHtml(starUrl)}" class="star-form">
                  ${csrfInput}
                  <button type="submit" class="button button-star${starClass}" title="${escapeHtml(starTitle)}">
                      <span aria-hidden="true">★</span>
                      ${starText}
                      <span class="star-count">${starCount}</span>
                  </button>
             </form>`
          : "";

     const deleteModalId = `delete-experience-${escapeHtml(experienceId)}`;
     const deleteHtml = IS_SUPERUSER
          ? `<div class="experience-card__delete">
                  <button type="button"
                          class="button button-danger"
                          popovertarget="${deleteModalId}"
                          aria-label="Hapus ${title}">
                      Hapus
                  </button>
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
                      <h2 id="${deleteModalId}-title">Hapus Experience?</h2>
                      <p>Apakah Anda yakin ingin menghapus <strong>${title}</strong>?</p>
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
     `
     return articleElement;
}


const fetchExperiences = async (query = "") => {
     if (experiencesAbortController) experiencesAbortController.abort();

     experiencesAbortController = new AbortController();

     try {
          //tampilkan loading
          displayExperienceSection({ showLoading: true });

          //tampung url api, jika ada query sertaka title=, kalau ga, cuman nembak ke base url doang
          const url = query ? `${BASE_EXPERIENCE_ENDPOINT}?title=${encodeURIComponent(query)}` : BASE_EXPERIENCE_ENDPOINT;

          //lakukan fetching, tampung responsenya dalam variabel, gunakan await karena fetching functionnya async
          const response = await fetch(url, {
               headers: { Accept: "application/json" },
               signal: experiencesAbortController.signal,
          });

          //kalau response != 200, maka throw error, nanti dioper ke catch
          if (!response.ok) {
               throw new Error("Failed to fetch experiecnces");
          };

          //tampung data dalam bentuk json
          const experienceData = await response.json();

          if (experienceData.length === 0) {
               gridContainer.innerHTML = "";
               displayExperienceSection({ showEmpty:true });
               return;
          }

          gridContainer.innerHTML = "";


          experienceData.forEach((item) => {
               gridContainer.appendChild(buildExperienceCard(item));
          });

          displayExperienceSection({showGrid:true})
     } catch (error) {
          if (error.name === "AbortError") {
               return;
          }
          console.error("Error occured: ", error);
          displayExperienceSection({ showError: true });
     }

}

const SEARCH_DEBOUNCE_DELAY = 300;
let searchDebounceTimer;

const searchExperiences = () => {
     fetchExperiences(searchInput.value.trim());
}

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
})

const experienceForm = document.getElementById("experience-form");

const closeExperienceModal = () => {
     document.getElementById("add-experience-modal").hidePopover();

}

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
}

const addExperience = async (event) => {
     event.preventDefault()

     const submitButton = experienceForm.querySelector(
          'button[type="submit"]'
     );

     submitButton.disabled = true;

     try {
          const response = await fetch(CREATE_EXPERIENCE_ENDPOINT, {
               method: 'POST',
               headers: {
                    "X-CSRFToken": getCookie("csrftoken")
               },
               body: new FormData(experienceForm),
          });

          const result = await response.json().catch(() => ({}));

          if (response.ok) {
               experienceForm.reset();
               closeExperienceModal();

               showToast("Berhasil", "Experience berhasil ditambahkan", "success");

               fetchExperiences(searchInput.value.trim());
          } else {
               const errorMessages = result.errors
                ? Object.values(result.errors)
                    .flat()
                    .map((error) => error.message)
                : [
                    result.message
                    || `Terjadi kesalahan (status ${response.status}).`,
                ];

               showToast(
                    "Gagal menambahkan pengalaman",
                    errorMessages.join(" "),
                    "error"
               );
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
}

if (experienceForm) {
     experienceForm.addEventListener("submit", addExperience);
}


fetchExperiences(searchInput.value.trim());
