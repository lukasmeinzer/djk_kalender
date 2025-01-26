document.getElementById('requestButton').addEventListener('click', function() {
    const selectedFolder = document.getElementById('folderSelect').value;
    fetch(`/get-ics-files/${selectedFolder}`)
        .then(response => response.json())
        .then(files => {
            const listContainer = document.getElementById('listContainer');
            listContainer.innerHTML = ''; // Clear any existing content
            const ul = document.createElement('ul');
            files.forEach(file => {
                const li = document.createElement('li');
                const a = document.createElement('a');
                a.href = `/static/${selectedFolder}/${file}`;
                a.textContent = file;
                a.download = file;
                li.appendChild(a);
                ul.appendChild(li);
            });
            listContainer.appendChild(ul);
        })
        .catch(error => console.error('Error fetching files:', error));
});