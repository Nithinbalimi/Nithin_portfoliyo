/**
 * Balimi Nithin — GSAP Dark Chalkboard Portfolio Interactions
 * Features: Mobile drawer toggle, Category filtering, Lightbox document viewer
 */

document.addEventListener("DOMContentLoaded", () => {
  // --- 1. Mobile Menu Drawer Navigation ---
  const mobileToggle = document.querySelector(".mobile-toggle");
  const mobileMenu = document.querySelector(".mobile-menu");
  const mobileLinks = document.querySelectorAll(".mobile-nav-link");

  if (mobileToggle && mobileMenu) {
    mobileToggle.addEventListener("click", () => {
      const isExpanded = mobileToggle.getAttribute("aria-expanded") === "true";
      mobileToggle.setAttribute("aria-expanded", String(!isExpanded));
      mobileMenu.classList.toggle("is-open", !isExpanded);
      mobileMenu.setAttribute("aria-hidden", String(isExpanded));
    });

    mobileLinks.forEach((link) => {
      link.addEventListener("click", () => {
        mobileToggle.setAttribute("aria-expanded", "false");
        mobileMenu.classList.remove("is-open");
        mobileMenu.setAttribute("aria-hidden", "true");
      });
    });
  }

  // --- 2. Credentials & Academic Documents Category Filter ---
  const filterPills = document.querySelectorAll(".filter-pill");
  const docCards = document.querySelectorAll(".doc-card");
  const certCards = document.querySelectorAll(".cert-card");

  filterPills.forEach((pill) => {
    pill.addEventListener("click", () => {
      const selectedFilter = pill.getAttribute("data-filter");

      filterPills.forEach((p) => {
        p.classList.remove("active");
        p.setAttribute("aria-selected", "false");
      });
      pill.classList.add("active");
      pill.setAttribute("aria-selected", "true");

      // Filter Document Cards
      docCards.forEach((card) => {
        const cardCat = card.getAttribute("data-category");
        if (selectedFilter === "all" || cardCat === selectedFilter) {
          card.classList.remove("is-hidden");
        } else {
          card.classList.add("is-hidden");
        }
      });

      // Filter Certifications Summary Cards
      certCards.forEach((card) => {
        const cardCat = card.getAttribute("data-category");
        if (selectedFilter === "all" || selectedFilter === "cert") {
          card.classList.remove("is-hidden");
        } else {
          card.classList.add("is-hidden");
        }
      });
    });
  });

  // --- 3. Lightbox Modal for Academic Documents & Marks Sheets ---
  const lightboxModal = document.getElementById("lightbox-modal");
  const lightboxBackdrop = document.querySelector(".lightbox-backdrop");
  const lightboxCloseBtn = document.getElementById("lightbox-close");
  const lightboxImg = document.getElementById("lightbox-img");
  const lightboxTitle = document.getElementById("lightbox-title");
  const lightboxOpenExternal = document.getElementById("lightbox-open-external");

  function openLightbox(imgSrc, title) {
    if (!lightboxModal || !lightboxImg) return;
    lightboxImg.src = imgSrc;
    lightboxImg.alt = title;
    if (lightboxTitle) lightboxTitle.textContent = title;
    if (lightboxOpenExternal) lightboxOpenExternal.href = imgSrc;
    lightboxModal.classList.add("is-active");
    lightboxModal.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
  }

  function closeLightbox() {
    if (!lightboxModal) return;
    lightboxModal.classList.remove("is-active");
    lightboxModal.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
    if (lightboxImg) lightboxImg.src = "";
  }

  docCards.forEach((card) => {
    card.addEventListener("click", () => {
      const imgSrc = card.getAttribute("data-img");
      const title = card.getAttribute("data-title") || "Academic Document";
      if (imgSrc) {
        openLightbox(imgSrc, title);
      }
    });
  });

  if (lightboxCloseBtn) {
    lightboxCloseBtn.addEventListener("click", closeLightbox);
  }

  if (lightboxBackdrop) {
    lightboxBackdrop.addEventListener("click", closeLightbox);
  }

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && lightboxModal?.classList.contains("is-active")) {
      closeLightbox();
    }
  });
});
