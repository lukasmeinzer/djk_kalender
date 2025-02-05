document.querySelectorAll('.download-link').forEach(link => {
    link.addEventListener('click', function (event) {
        const overlay = document.getElementById('overlay');
        
        // Show the overlay with the spinner
        overlay.classList.remove('hidden');

        // Allow the browser to follow the link after showing the spinner
        setTimeout(() => {
            overlay.classList.add('hidden');
        }, 5000); // Fallback to hide spinner after 5 seconds if no response
    });
});
