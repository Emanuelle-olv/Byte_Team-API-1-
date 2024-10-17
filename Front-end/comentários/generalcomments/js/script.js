const icons = document.querySelectorAll('.floating-icon');

// Mover o ícone para uma posição aleatória na lateral ao clicar
icons.forEach(icon => {
    icon.addEventListener('click', () => {
        const y = Math.random() * (window.innerHeight - 50); // 50 é a altura do ícone

        icon.style.top = `${y}px`; // Mover verticalmente
    });
});
