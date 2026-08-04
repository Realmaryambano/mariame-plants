// Theme Toggle Logic
const themeToggle = document.getElementById('theme-toggle');
const body = document.body;

themeToggle.addEventListener('click', () => {
    const currentTheme = body.getAttribute('data-theme');
    if (currentTheme === 'light') {
        body.setAttribute('data-theme', 'dark');
        themeToggle.innerHTML = '<i class="fa-solid fa-sun"></i>';
    } else {
        body.setAttribute('data-theme', 'light');
        themeToggle.innerHTML = '<i class="fa-solid fa-moon"></i>';
    }
});

// Falling Leaves Animation on Scroll
window.addEventListener('scroll', () => {
    if (Math.random() < 0.1) {
        createFallingLeaf();
    }
});

function createFallingLeaf() {
    const leaf = document.createElement('div');
    leaf.innerHTML = '<i class="fa-solid fa-leaf"></i>';
    leaf.style.position = 'fixed';
    leaf.style.left = Math.random() * window.innerWidth + 'px';
    leaf.style.top = '-20px';
    leaf.style.color = '#2E7D32';
    leaf.style.fontSize = (Math.random() * 10 + 12) + 'px';
    leaf.style.zIndex = '9999';
    leaf.style.opacity = '0.8';
    leaf.style.transition = 'transform 3s linear, top 3s linear, opacity 3s linear';
    
    document.body.appendChild(leaf);
    
    setTimeout(() => {
        leaf.style.top = window.innerHeight + 'px';
        leaf.style.transform = `rotate(${Math.random() * 360}deg) translateX(${Math.random() * 100 - 50}px)`;
        leaf.style.opacity = '0';
    }, 50);
    
    setTimeout(() => {
        leaf.remove();
    }, 3000);
}