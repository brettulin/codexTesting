document.addEventListener('DOMContentLoaded', function() {
    const button = document.getElementById('change-text');
    const output = document.getElementById('output');
    button.addEventListener('click', function() {
        output.textContent = 'You clicked the button!';
    });
});
