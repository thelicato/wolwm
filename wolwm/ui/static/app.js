(() => {
  "use strict";

  const root = document.documentElement;
  const themeStorageKey = "wolwm-color-theme";

  const preferredTheme = () => {
    try {
      const storedTheme = window.localStorage.getItem(themeStorageKey);
      if (storedTheme === "dark" || storedTheme === "light") {
        return storedTheme;
      }
    } catch {
      // The system preference remains a safe fallback when storage is unavailable.
    }
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  };

  const setTheme = (theme) => {
    root.dataset.theme = theme;
    try {
      window.localStorage.setItem(themeStorageKey, theme);
    } catch {
      // Theme persistence is optional.
    }
  };

  setTheme(preferredTheme());

  document.querySelector("[data-theme-toggle]")?.addEventListener("click", () => {
    setTheme(root.dataset.theme === "dark" ? "light" : "dark");
  });

  const navShell = document.querySelector("[data-nav-shell]");
  const navToggle = document.querySelector("[data-nav-toggle]");

  const closeNavigation = () => {
    navShell?.classList.remove("is-open");
    document.body.classList.remove("nav-open");
    navToggle?.setAttribute("aria-expanded", "false");
  };

  navToggle?.addEventListener("click", () => {
    const willOpen = !navShell?.classList.contains("is-open");
    navShell?.classList.toggle("is-open", willOpen);
    document.body.classList.toggle("nav-open", willOpen);
    navToggle.setAttribute("aria-expanded", String(willOpen));
  });

  navShell?.addEventListener("click", (event) => {
    if (event.target === navShell) {
      closeNavigation();
    }
  });

  window.addEventListener("resize", () => {
    if (window.innerWidth >= 768) {
      closeNavigation();
    }
  });

  const setDialogState = (dialog, isOpen) => {
    document.documentElement.classList.toggle("modal-open", isOpen);
    if (!isOpen) {
      const addForm = dialog.querySelector("[data-add-form]");
      if (addForm) {
        addForm.reset();
        addForm.querySelector("button[type='submit']").disabled = true;
      }
    }
  };

  const localDateTimeValue = (date) => {
    const offset = date.getTimezoneOffset() * 60_000;
    return new Date(date.getTime() - offset).toISOString().slice(0, 16);
  };

  const prepareScheduleForm = (form) => {
    const timezoneInput = form.querySelector("[data-timezone-input]");
    const timezoneLabel = form.querySelector("[data-timezone-label]");
    const scheduleTime = form.querySelector("[data-schedule-time]");
    const timezone =
      Intl.DateTimeFormat().resolvedOptions().timeZone || "UTC";

    if (timezoneInput) {
      timezoneInput.value = timezone;
    }
    if (timezoneLabel) {
      timezoneLabel.textContent = timezone;
    }
    if (scheduleTime) {
      const now = new Date();
      scheduleTime.min = localDateTimeValue(now);
      if (!scheduleTime.value) {
        scheduleTime.value = localDateTimeValue(
          new Date(now.getTime() + 5 * 60_000),
        );
      }
    }
  };

  document.querySelectorAll("[data-schedule-form]").forEach(prepareScheduleForm);

  document.querySelectorAll("[data-open-dialog]").forEach((button) => {
    button.addEventListener("click", () => {
      const dialog = document.getElementById(button.dataset.openDialog);
      if (!(dialog instanceof HTMLDialogElement)) {
        return;
      }

      if (button.dataset.deleteAction) {
        const deleteForm = dialog.querySelector("[data-delete-form]");
        if (deleteForm) {
          deleteForm.action = button.dataset.deleteAction;
        }
      }

      dialog.showModal();
      setDialogState(dialog, true);
      const scheduleForm = dialog.querySelector("[data-schedule-form]");
      if (scheduleForm) {
        prepareScheduleForm(scheduleForm);
      }
    });
  });

  document.querySelectorAll("dialog").forEach((dialog) => {
    dialog.addEventListener("close", () => setDialogState(dialog, false));
    dialog.addEventListener("click", (event) => {
      if (event.target === dialog) {
        dialog.close();
      }
    });
  });

  document.querySelectorAll("[data-close-dialog]").forEach((button) => {
    button.addEventListener("click", () => button.closest("dialog")?.close());
  });

  document.querySelectorAll("[data-add-form]").forEach((form) => {
    const submit = form.querySelector("button[type='submit']");
    const updateValidity = () => {
      submit.disabled = !form.checkValidity();
    };
    form.addEventListener("input", updateValidity);
    form.addEventListener("change", updateValidity);
  });

  const loadingOverlay = document.querySelector("[data-loading-overlay]");
  document.querySelectorAll("[data-loading-form]").forEach((form) => {
    form.addEventListener("submit", () => {
      if (!form.checkValidity()) {
        return;
      }
      loadingOverlay?.setAttribute("data-visible", "");
      loadingOverlay?.setAttribute("aria-hidden", "false");
    });
  });

  const toast = document.querySelector("[data-toast-visible]");
  if (toast) {
    window.setTimeout(() => toast.classList.add("is-visible"), 30);
    window.setTimeout(() => toast.classList.remove("is-visible"), 3400);
  }

  const searchForm = document.querySelector("[data-search-form]");
  const searchInput = document.querySelector("[data-event-search]");
  let searchTimer;
  searchInput?.addEventListener("input", () => {
    window.clearTimeout(searchTimer);
    searchTimer = window.setTimeout(() => searchForm?.requestSubmit(), 300);
  });
})();
