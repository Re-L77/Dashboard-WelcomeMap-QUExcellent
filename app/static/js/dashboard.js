/**
 * Dashboard Navigation and Page Communication
 * Handles routing between different dashboard sections
 */

// Current page state
let currentPage = "dashboard";
let currentLang = "es";

// Initialize dashboard on page load
document.addEventListener("DOMContentLoaded", function () {
  initializeNavigation();
  initializeLanguageSwitcher();
  setupEventListeners();
  showPage("dashboard");
});

/**
 * Initialize navigation links
 */
function initializeNavigation() {
  const navLinks = document.querySelectorAll(".nav-link");

  navLinks.forEach((link) => {
    link.addEventListener("click", function (e) {
      e.preventDefault();

      // Determine which page to show based on the link text
      const text = this.querySelector("span").getAttribute("data-es");
      let pageId = mapLinkToPage(text);

      // Update navigation active state
      navLinks.forEach((l) => l.classList.remove("active"));
      this.classList.add("active");

      // Show the page
      showPage(pageId);
    });
  });
}

/**
 * Map link text to page ID
 */
function mapLinkToPage(linkText) {
  const mapping = {
    Panel: "dashboard",
    "Asistente de Datos": "assistant",
    Inducción: "induction",
    Integración: "integration",
    Notificaciones: "notifications",
    Perfil: "profile",
    Configuración: "settings",
  };

  return mapping[linkText] || "dashboard";
}

/**
 * Show a specific page/section
 */
function showPage(pageId) {
  currentPage = pageId;

  // Hide all page sections
  const sections = document.querySelectorAll("[data-page]");
  sections.forEach((section) => {
    section.style.display = "none";
  });

  // Show the requested page
  const targetPage = document.querySelector(`[data-page="${pageId}"]`);
  if (targetPage) {
    targetPage.style.display = "block";

    // Update header title
    updateHeaderTitle(pageId);

    // Call page-specific initialization if needed
    onPageShow(pageId);
  } else {
    console.warn(`Page "${pageId}" not found`);
    // Fallback to dashboard
    const dashboardPage = document.querySelector('[data-page="dashboard"]');
    if (dashboardPage) {
      dashboardPage.style.display = "block";
    }
  }
}

/**
 * Update header title based on current page
 */
function updateHeaderTitle(pageId) {
  const titles = {
    dashboard: { es: "Panel", en: "Dashboard" },
    assistant: { es: "Asistente de Datos", en: "Data Assistant" },
    induction: { es: "Inducción", en: "Induction" },
    integration: { es: "Integración", en: "Integration" },
    notifications: { es: "Notificaciones", en: "Notifications" },
    profile: { es: "Perfil", en: "Profile" },
    settings: { es: "Configuración", en: "Settings" },
  };

  const titleObj = titles[pageId] || titles["dashboard"];
  const headerTitle = document.querySelector(".header-title");
  if (headerTitle) {
    headerTitle.textContent = currentLang === "es" ? titleObj.es : titleObj.en;
  }
}

/**
 * Page-specific initialization
 */
function onPageShow(pageId) {
  switch (pageId) {
    case "assistant":
      initializeAssistant();
      break;
    case "induction":
      initializeInduction();
      break;
    case "integration":
      initializeIntegration();
      break;
    case "notifications":
      initializeNotifications();
      break;
    case "profile":
      initializeProfile();
      break;
    case "settings":
      initializeSettings();
      break;
    case "dashboard":
    default:
      initializeDashboard();
      break;
  }
}

/**
 * Initialize Dashboard page
 */
function initializeDashboard() {
  // Add click handlers to metric cards if they have specific actions
  const metricCards = document.querySelectorAll(
    '[data-page="dashboard"] .metric-card.clickable'
  );
  metricCards.forEach((card) => {
    card.addEventListener("click", function () {
      // Navigate to the corresponding section
      const cardText =
        this.querySelector("p")?.getAttribute("data-es") || "dashboard";
      const pageId = mapLinkToPage(cardText);

      // Update nav link active state
      const correspondingLink = Array.from(
        document.querySelectorAll(".nav-link")
      ).find(
        (link) =>
          mapLinkToPage(link.querySelector("span").getAttribute("data-es")) ===
          pageId
      );

      if (correspondingLink) {
        document
          .querySelectorAll(".nav-link")
          .forEach((l) => l.classList.remove("active"));
        correspondingLink.classList.add("active");
      }

      showPage(pageId);
    });
  });
}

/**
 * Initialize Data Assistant page
 */
function initializeAssistant() {
  console.log("Initializing Data Assistant page");
  // Add specific logic for assistant page
}

/**
 * Initialize Induction page
 */
function initializeInduction() {
  console.log("Initializing Induction page");
  // Add specific logic for induction page
}

/**
 * Initialize Integration page
 */
function initializeIntegration() {
  console.log("Initializing Integration page");
  // Add specific logic for integration page
}

/**
 * Initialize Notifications page
 */
function initializeNotifications() {
  console.log("Initializing Notifications page");
  // Add specific logic for notifications page
}

/**
 * Initialize Profile page
 */
function initializeProfile() {
  console.log("Initializing Profile page");
  // Add specific logic for profile page
}

/**
 * Initialize Settings page
 */
function initializeSettings() {
  console.log("Initializing Settings page");
  // Add specific logic for settings page
}

/**
 * Initialize language switcher
 */
function initializeLanguageSwitcher() {
  const langBtns = document.querySelectorAll(".lang-btn");

  langBtns.forEach((btn) => {
    btn.addEventListener("click", function () {
      const lang = this.getAttribute("data-lang");
      changeLanguage(lang);

      // Update active button
      langBtns.forEach((b) => b.classList.remove("active"));
      this.classList.add("active");
    });
  });
}

/**
 * Change language across all elements
 */
function changeLanguage(lang) {
  currentLang = lang;

  // Get all elements with data-es and data-en attributes
  const translatableElements = document.querySelectorAll("[data-es][data-en]");

  translatableElements.forEach((element) => {
    if (lang === "es") {
      element.textContent = element.getAttribute("data-es");
    } else if (lang === "en") {
      element.textContent = element.getAttribute("data-en");
    }
  });

  // Update header title with new language
  updateHeaderTitle(currentPage);
}

/**
 * Setup common event listeners
 */
function setupEventListeners() {
  // Notifications popup toggle
  const notificationBtn = document.getElementById("notificationBtn");
  const notificationsPopup = document.getElementById("notificationsPopup");

  if (notificationBtn && notificationsPopup) {
    notificationBtn.addEventListener("click", function (e) {
      e.stopPropagation();
      notificationsPopup.classList.toggle("show");
    });

    // Close popup when clicking outside
    document.addEventListener("click", function (e) {
      if (notificationBtn && notificationsPopup) {
        if (
          !notificationBtn.contains(e.target) &&
          !notificationsPopup.contains(e.target)
        ) {
          notificationsPopup.classList.remove("show");
        }
      }
    });

    // Prevent popup from closing when clicking inside it
    notificationsPopup.addEventListener("click", function (e) {
      e.stopPropagation();
    });
  }
}

/**
 * Make global function to navigate to specific page (for external calls)
 */
window.navigateTo = function (pageId) {
  showPage(pageId);

  // Update nav link active state
  const navLinks = document.querySelectorAll(".nav-link");
  navLinks.forEach((link) => {
    const linkPageId = mapLinkToPage(
      link.querySelector("span").getAttribute("data-es")
    );
    if (linkPageId === pageId) {
      link.classList.add("active");
    } else {
      link.classList.remove("active");
    }
  });
};

/**
 * Make global function to call API endpoints
 */
window.callAPI = async function (endpoint, method = "GET", data = null) {
  try {
    const options = {
      method: method,
      headers: {
        "Content-Type": "application/json",
      },
    };

    if (data && (method === "POST" || method === "PUT")) {
      options.body = JSON.stringify(data);
    }

    const response = await fetch(`http://localhost:8001${endpoint}`, options);

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("API Call Error:", error);
    throw error;
  }
};
