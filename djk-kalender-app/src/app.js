document.getElementById('requestButton').addEventListener('click', function() {
    const selectedFolder = document.getElementById('folderSelect').value;
    fetch(`/get-ics-files/${selectedFolder}`)
        .then(response => response.json())
        .then(files => {
            // Extract date from filename and sort files as strings
            files.sort((a, b) => {
                const dateA = a.split('_')[1].replace('.ics', '');
                const dateB = b.split('_')[1].replace('.ics', '');
                return dateA.localeCompare(dateB);
            });

            const listContainer = document.getElementById('listContainer');
            listContainer.innerHTML = ''; // Clear any existing content
            const ol = document.createElement('ol');
            files.forEach(file => {
                const li = document.createElement('li');
                const a = document.createElement('a');
                a.href = `/static/${selectedFolder}/${file}`;
                a.textContent = file;
                a.download = file;
                li.appendChild(a);
                ol.appendChild(li);
            });
            listContainer.appendChild(ol);
        })
        .catch(error => console.error('Error fetching files:', error));
});