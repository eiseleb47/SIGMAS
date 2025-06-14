document.addEventListener('DOMContentLoaded', () => {
    const showButtonsBtn = document.getElementById('showButtons');
    const showOtherBtn = document.getElementById('showOther');
    const buttonsSection = document.getElementById('button-container');
    const otherSection = document.getElementById('calibs');

    buttonsSection.style.display = 'flex';
    otherSection.style.display = 'none';
    showButtonsBtn.classList.add('active');
    showOtherBtn.classList.remove('active');

    showButtonsBtn.addEventListener('click', () => {
        showButtonsBtn.classList.add('active');
        showOtherBtn.classList.remove('active');
        buttonsSection.style.display = 'flex';
        otherSection.style.display = 'none';
    });

    showOtherBtn.addEventListener('click', () => {
        showOtherBtn.classList.add('active');
        showButtonsBtn.classList.remove('active');
        buttonsSection.style.display = 'none';
        otherSection.style.display = 'flex';
    });
});