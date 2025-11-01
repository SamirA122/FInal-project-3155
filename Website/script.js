/**
 * Toggles the display of an individual team member's bio
 * @param {string} bioId - The ID of the bio section to show or hide
 */
function toggleBio(bioId) {
    const bio = document.getElementById(bioId);
    const button = event.target;

    // Toggle between showing and hiding the bio section
    if (bio.style.display === "none" || bio.style.display === "") {
        bio.style.display = "block";
        button.textContent = "Hide Bio";
    } else {
        bio.style.display = "none";
        button.textContent = "Show Bio";
    }
}

/**
 * Toggles the display of an individual team member's moodboard
 * @param {string} moodboardId - The ID of the moodboard section to show or hide
 */
function toggleMoodboard(moodboardId) {
    const moodboard = document.getElementById(moodboardId);
    const button = event.target;

    // Toggle between showing and hiding the moodboard section
    if (moodboard.style.display === "none" || moodboard.style.display === "") {
        moodboard.style.display = "block";
        button.textContent = "Hide Moodboard";
        // Add animation class
        moodboard.style.animation = "fadeIn 0.5s ease";
    } else {
        moodboard.style.display = "none";
        button.textContent = "Show Moodboard";
    }
}

/**
 * Shows the specified section ('bios', 'vision', or 'rules') and hides the others
 * @param {string} sectionId - The ID of the section to display
 */
function showSection(sectionId) {
    const biosSection = document.getElementById("bios");
    const visionSection = document.getElementById("vision");
    const rulesSection = document.getElementById("rules");

    // Hide all sections first
    biosSection.style.display = "none";
    visionSection.style.display = "none";
    if (rulesSection) {
        rulesSection.style.display = "none";
    }

    // Display the selected section
    if (sectionId === "bios") {
        biosSection.style.display = "flex";
    } else if (sectionId === "vision") {
        visionSection.style.display = "flex";
    } else if (sectionId === "rules" && rulesSection) {
        rulesSection.style.display = "flex";
    }
}

// Add smooth fade-in animation style
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);

// Initialize: ensure bios section is shown by default
document.addEventListener('DOMContentLoaded', function() {
    showSection('bios');

    // Add hover effect to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
});

// Console Easter Egg
console.log('%c Welcome to Team 21! 🚀', 'font-size: 20px; color: #4A90E2; font-weight: bold;');
console.log('%c Created by Yousef Ayesh & Samir Abukar', 'font-size: 14px; color: #7B68EE;');
console.log('%c UNCC Computer Science - Fall 2024', 'font-size: 12px; color: #666;');