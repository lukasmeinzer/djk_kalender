document.getElementById('requestButton').addEventListener('click', function() {
    const selectedTeam = document.getElementById('folderSelect').value;
    const overlay = document.getElementById('overlay');
    const listContainer = document.getElementById('listContainer');

    // Show overlay (which includes the spinner)
    overlay.classList.remove('hidden');
    listContainer.innerHTML = ''; // Clear any existing content

    fetch(`/get-ics-files/${selectedTeam}`)
        .then(response => {
            return response.json();
        })
        .then(files => {
            console.log('Files received:', files);
            // Sort files by date
            files.sort((a, b) => new Date(a.Datum) - new Date(b.Datum));

            const table = document.createElement('table');
            table.classList.add('ics-table');

            const thead = document.createElement('thead');
            const headerRow = document.createElement('tr');
            ['Datum', 'Gegner', 'Kalendereintrag'].forEach(text => {
                const th = document.createElement('th');
                th.textContent = text;
                headerRow.appendChild(th);
            });
            thead.appendChild(headerRow);
            table.appendChild(thead);

            const tbody = document.createElement('tbody');
            files.forEach(file => {
                const row = document.createElement('tr');

                const datumCell = document.createElement('td');
                datumCell.textContent = file.Datum;
                row.appendChild(datumCell);

                const gegnerCell = document.createElement('td');
                gegnerCell.textContent = file.Gegner;
                row.appendChild(gegnerCell);

                const linkCell = document.createElement('td');
                const a = document.createElement('a');
                a.href = `/static/spieltermine_${encodeURIComponent(selectedTeam)}/${encodeURIComponent(file.Datei)}`;
                a.textContent = 'Download';
                a.download = file.Datei;
                linkCell.appendChild(a);
                row.appendChild(linkCell);

                tbody.appendChild(row);
            });
            table.appendChild(tbody);
            listContainer.appendChild(table);

            // Scroll back to the top of the container
            listContainer.scrollIntoView({ behavior: 'smooth' });
        })
        .catch(error => {
            console.error('Error fetching files:', error);
        })
        .finally(() => {
            // Hide the overlay regardless of success or error
            overlay.classList.add('hidden');
        });
});
