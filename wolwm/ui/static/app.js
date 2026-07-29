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
    const scheduleTime = form.querySelector("[data-schedule-time]");

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
  let toastHideTimer;
  if (toast) {
    window.setTimeout(() => toast.classList.add("is-visible"), 30);
    toastHideTimer = window.setTimeout(
      () => toast.classList.remove("is-visible"),
      3400,
    );
  }

  const showToast = (message, kind = "success") => {
    if (!toast) {
      return;
    }
    window.clearTimeout(toastHideTimer);
    toast.textContent = message;
    toast.classList.toggle("toast--error", kind === "error");
    toast.classList.toggle("toast--success", kind !== "error");
    toast.classList.add("is-visible");
    toastHideTimer = window.setTimeout(
      () => toast.classList.remove("is-visible"),
      3400,
    );
  };

  const wakeCooldownTimers = new WeakMap();

  const stopWakeCountdown = (form) => {
    const timer = wakeCooldownTimers.get(form);
    if (timer) {
      window.clearInterval(timer);
      wakeCooldownTimers.delete(form);
    }
  };

  const applyWakeCooldown = (form, seconds) => {
    const button = form.querySelector("[data-wake-button]");
    if (!button) {
      return;
    }

    stopWakeCountdown(form);
    const readyAt = Date.now() + Math.max(0, seconds) * 1000;
    const renderCountdown = () => {
      const remainingSeconds = Math.max(
        0,
        Math.ceil((readyAt - Date.now()) / 1000),
      );
      button.disabled = remainingSeconds > 0;
      button.textContent =
        remainingSeconds > 0 ? `Wake (${remainingSeconds}s)` : "Wake";

      if (remainingSeconds === 0) {
        stopWakeCountdown(form);
      }
    };

    renderCountdown();
    if (readyAt > Date.now()) {
      wakeCooldownTimers.set(
        form,
        window.setInterval(renderCountdown, 250),
      );
    }
  };

  const refreshWakeCooldown = async (form) => {
    const button = form.querySelector("[data-wake-button]");
    try {
      const response = await window.fetch(form.dataset.cooldownUrl, {
        headers: { Accept: "application/json" },
      });
      if (!response.ok) {
        throw new Error("Unable to retrieve wake cooldown");
      }
      const cooldown = await response.json();
      applyWakeCooldown(form, cooldown.remainingSeconds);
      return true;
    } catch {
      stopWakeCountdown(form);
      if (button) {
        button.disabled = true;
        button.textContent = "Wake unavailable";
      }
      showToast("Unable to check wake cooldown", "error");
      return false;
    }
  };

  document.querySelectorAll("[data-wake-form]").forEach((form) => {
    const button = form.querySelector("[data-wake-button]");
    refreshWakeCooldown(form);

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      if (!button || button.disabled) {
        return;
      }

      stopWakeCountdown(form);
      button.disabled = true;
      button.textContent = "Waking…";

      try {
        const response = await window.fetch("/api/v1/wake", {
          method: "POST",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ deviceId: form.dataset.deviceId }),
        });
        if (!response.ok) {
          throw new Error("Wake request failed");
        }
        showToast("Magic Packet correctly sent");
      } catch {
        showToast("Unable to wake device", "error");
      } finally {
        await refreshWakeCooldown(form);
      }
    });
  });

  const eventsPage = document.querySelector("[data-events-page]");
  if (eventsPage) {
    const table = eventsPage.querySelector("[data-event-table]");
    const tableBody = table?.querySelector("tbody");
    const tableContainer = eventsPage.querySelector(
      "[data-event-table-container]",
    );
    const rows = Array.from(
      eventsPage.querySelectorAll("[data-event-row]"),
    );
    const searchInput = eventsPage.querySelector("[data-event-search]");
    const emptyState = eventsPage.querySelector("[data-event-empty]");
    const pagination = eventsPage.querySelector("[data-event-pagination]");
    const pageStatus = eventsPage.querySelector("[data-page-status]");
    const sortButtons = Array.from(
      eventsPage.querySelectorAll("[data-sort-key]"),
    );
    const pageButtons = Array.from(
      eventsPage.querySelectorAll("[data-page-action]"),
    );
    const pageSize =
      Number.parseInt(eventsPage.dataset.pageSize || "", 10) || 10;
    const originalPositions = new Map(
      rows.map((row, index) => [row, index]),
    );
    const collator = new Intl.Collator(undefined, {
      numeric: true,
      sensitivity: "base",
    });

    let activeSortKey = "";
    let sortDirection = "asc";
    let currentPage = 1;
    let pageCount = 1;

    const normalizedSearchText = (row) =>
      `${row.dataset.eventType || ""} ${row.dataset.eventData || ""}`
        .replaceAll("_", " ")
        .toLocaleLowerCase();

    const compareRows = (left, right) => {
      const leftValue = left.dataset[activeSortKey] || "";
      const rightValue = right.dataset[activeSortKey] || "";
      const comparison = collator.compare(leftValue, rightValue);
      if (comparison !== 0) {
        return sortDirection === "asc" ? comparison : -comparison;
      }
      return originalPositions.get(left) - originalPositions.get(right);
    };

    const updateSortIndicators = () => {
      sortButtons.forEach((button) => {
        const isActive = button.dataset.sortKey === activeSortKey;
        const heading = button.closest("th");
        const indicator = button.querySelector(".sort-indicator");
        heading?.setAttribute(
          "aria-sort",
          isActive
            ? sortDirection === "asc"
              ? "ascending"
              : "descending"
            : "none",
        );
        if (indicator) {
          indicator.textContent = isActive
            ? sortDirection === "asc"
              ? "▲"
              : "▼"
            : "";
        }
      });
    };

    const renderEvents = () => {
      const query = (searchInput?.value || "").trim().toLocaleLowerCase();
      const orderedRows = [...rows];
      if (activeSortKey) {
        orderedRows.sort(compareRows);
      }

      const matchingRows = orderedRows.filter(
        (row) => !query || normalizedSearchText(row).includes(query),
      );
      const matchingSet = new Set(matchingRows);
      tableBody?.append(
        ...matchingRows,
        ...orderedRows.filter((row) => !matchingSet.has(row)),
      );

      pageCount = Math.max(
        1,
        Math.ceil(matchingRows.length / pageSize),
      );
      currentPage = Math.min(Math.max(currentPage, 1), pageCount);
      const firstVisibleRow = (currentPage - 1) * pageSize;
      const visibleRows = new Set(
        matchingRows.slice(firstVisibleRow, firstVisibleRow + pageSize),
      );

      rows.forEach((row) => {
        row.hidden = !visibleRows.has(row);
      });

      const hasMatches = matchingRows.length > 0;
      if (tableContainer) {
        tableContainer.hidden = !hasMatches;
      }
      if (emptyState) {
        emptyState.hidden = hasMatches;
      }
      if (pagination) {
        pagination.hidden = !hasMatches || pageCount <= 1;
      }
      if (pageStatus) {
        pageStatus.textContent = `${currentPage} of ${pageCount}`;
      }

      pageButtons.forEach((button) => {
        const action = button.dataset.pageAction;
        button.disabled =
          (currentPage === 1 &&
            (action === "first" || action === "previous")) ||
          (currentPage === pageCount &&
            (action === "next" || action === "last"));
      });

      updateSortIndicators();
    };

    sortButtons.forEach((button) => {
      button.addEventListener("click", () => {
        const selectedKey = button.dataset.sortKey;
        if (activeSortKey === selectedKey) {
          sortDirection = sortDirection === "asc" ? "desc" : "asc";
        } else {
          activeSortKey = selectedKey;
          sortDirection = "asc";
        }
        currentPage = 1;
        renderEvents();
      });
    });

    pageButtons.forEach((button) => {
      button.addEventListener("click", () => {
        const action = button.dataset.pageAction;
        if (action === "first") {
          currentPage = 1;
        } else if (action === "previous") {
          currentPage -= 1;
        } else if (action === "next") {
          currentPage += 1;
        } else if (action === "last") {
          currentPage = pageCount;
        }
        renderEvents();
      });
    });

    searchInput?.addEventListener("input", () => {
      currentPage = 1;
      renderEvents();
    });

    renderEvents();
  }
})();
