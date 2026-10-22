document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.getElementById("sidebar");
    const toggleBtn = document.getElementById("sidebar-toggle");
    const navLinks = document.querySelectorAll(".sidebar-nav .nav-link");
    if (!sidebar) return;

    function setOpen(open) {
        sidebar.classList.toggle("is-open", open);
        toggleBtn.setAttribute("aria-expanded", String(open));
    }
    const isOpen = () => sidebar.classList.contains("is-open");

    sidebar.addEventListener("click", (e) => {
        if (e.target.closest(".nav-link, .user-link, .logout-link")) return;
        setOpen(!isOpen());
    });

    // Klik di luar sidebar menutup
    document.addEventListener("click", (e) => {
        if (isOpen() && !sidebar.contains(e.target)) setOpen(false);
    });

    // Esc menutup
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && isOpen()) setOpen(false);
    });

    /* ---------- Menu aktif ---------- */
    function setActive(link) {
        navLinks.forEach((l) => {
            l.classList.remove("active");
            l.removeAttribute("aria-current");
        });
        link.classList.add("active");
        link.setAttribute("aria-current", "page");
    }

    // Klik menu: pindah active + tutup sidebar
    navLinks.forEach((link) => {
        link.addEventListener("click", () => {
            setActive(link);
            setOpen(false);
        });
    });

    // Deteksi saat halaman dimuat (URL antar-app maupun anchor #hash)
    function syncFromLocation() {
        const path = window.location.pathname;
        const hash = window.location.hash;
        let match = null;

        navLinks.forEach((l) => {
            if (l.pathname !== path) return;
            if (l.hash && l.hash === hash) match = l;           // anchor persis
            else if (!l.hash && !hash && !match) match = l;     // halaman tanpa anchor
        });
        // Path cocok tapi hash tidak ada di menu → pakai link tanpa hash di path tsb
        if (!match) {
            navLinks.forEach((l) => { if (!match && l.pathname === path && !l.hash) match = l; });
        }
        if (match) setActive(match);
    }
    syncFromLocation();
    window.addEventListener("hashchange", syncFromLocation);
});