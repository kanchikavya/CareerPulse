document.addEventListener("DOMContentLoaded", function () {
  // AJAX Bookmark / Save Job Handler
  const saveButtons = document.querySelectorAll(".btn-save-job");
  saveButtons.forEach((button) => {
    button.addEventListener("click", function (e) {
      e.preventDefault();
      const jobId = this.getAttribute("data-job-id");
      const url = `/jobs/${jobId}/save/`;

      fetch(url, {
        method: "GET",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
        },
      })
        .then((response) => {
          if (response.status === 403) {
            alert("Only candidates can save jobs. Please log in as a candidate.");
            return null;
          }
          return response.json();
        })
        .then((data) => {
          if (!data) return;
          if (data.status === "ok") {
            const icon = button.querySelector("i");
            if (data.is_saved) {
              icon.classList.remove("bi-bookmark");
              icon.classList.add("bi-bookmark-fill");
              button.classList.add("text-primary");
            } else {
              icon.classList.remove("bi-bookmark-fill");
              icon.classList.add("bi-bookmark");
              button.classList.remove("text-primary");
            }
          }
        })
        .catch((err) => {
          console.error("Error saving job:", err);
        });
    });
  });

  // Resume upload toggle on application page
  const useProfileCheckbox = document.getElementById("use_profile_resume_checkbox");
  const resumeFileInput = document.getElementById("resume_file_input");
  if (useProfileCheckbox && resumeFileInput) {
    function toggleResumeInput() {
      if (useProfileCheckbox.checked) {
        resumeFileInput.disabled = true;
        resumeFileInput.required = false;
      } else {
        resumeFileInput.disabled = false;
        resumeFileInput.required = true;
      }
    }
    useProfileCheckbox.addEventListener("change", toggleResumeInput);
    toggleResumeInput();
  }
});
