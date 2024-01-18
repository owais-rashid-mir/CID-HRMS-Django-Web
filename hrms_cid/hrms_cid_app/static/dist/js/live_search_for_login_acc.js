// Live Search - for 6 Login accounts on the Admin side
document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('searchInput');
    const tableRows = document.querySelectorAll('.table tbody tr');

    searchInput.addEventListener('input', function () {
      const searchTerm = searchInput.value;

      tableRows.forEach(function (row) {
        // Email is the 4th column in the table, and we will search on that.
        const nameCell = row.querySelector('td:nth-child(4)');
        const originalText = nameCell.getAttribute('data-original-text');
        const name = originalText.toLowerCase();

        if (name.includes(searchTerm.toLowerCase())) {
          // Highlight matching text
          const highlightedText = originalText.replace(
            new RegExp(searchTerm, 'gi'),
            match => `<span style="background-color: yellow;">${match}</span>`
          );
          nameCell.innerHTML = highlightedText;

          row.style.display = '';
        } else {
          // Reset the content and hide the row if not matching
          nameCell.innerHTML = originalText;
          row.style.display = 'none';
        }
      });
    });

    // Store the original text in a data attribute
    tableRows.forEach(function (row) {
      const nameCell = row.querySelector('td:nth-child(4)');
      nameCell.setAttribute('data-original-text', nameCell.textContent);
    });
  });