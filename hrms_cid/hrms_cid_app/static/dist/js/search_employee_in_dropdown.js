// JS Code for searching employees in dropdown menu - for Login Accounts

document.addEventListener('DOMContentLoaded', function () {
    const employeeSearchInput = document.getElementById('employeeSearchInput');
    const dropdownMenu = document.querySelector('.dropdown-menu');
    const emailInput = document.getElementById('email');
    const originalDropdownItems = Array.from(dropdownMenu.children);

    // Function to update the email field based on the selected employee
    function updateEmail(selectedEmployee) {
        if (selectedEmployee) {
            emailInput.value = selectedEmployee.dataset.email;
        } else {
            emailInput.value = '';
        }
    }

    // Function to reset the dropdown to its original state
    function resetDropdown() {
        dropdownMenu.innerHTML = '';
        originalDropdownItems.forEach(function (item) {
            dropdownMenu.appendChild(item.cloneNode(true));
        });
    }

    // Function to highlight the matching text in yellow
    function highlightText(cell, searchTerm) {
        const cellText = cell.textContent;
        const highlightedText = cellText.replace(
            new RegExp(searchTerm, 'gi'),
            match => `<span style="background-color: yellow;">${match}</span>`
        );
        cell.innerHTML = highlightedText;
    }

    // Event listener for input in the search bar
    employeeSearchInput.addEventListener('input', function () {
        const searchTerm = employeeSearchInput.value.toLowerCase();

        if (searchTerm === '') {
            // If search term is empty, reset the dropdown and exit
            resetDropdown();
            return;
        }

        // Filter dropdown items based on the search term
        originalDropdownItems.forEach(function (employeeOption) {
            const employeeText = employeeOption.textContent.toLowerCase();
            const isVisible = employeeText.includes(searchTerm);
            employeeOption.style.display = isVisible ? 'block' : 'none';

            // Highlight matching text directly
            if (isVisible) {
                highlightText(employeeOption, searchTerm);
            }
        });

        // Show "No results found" if no matching items
        const noResultsFound = originalDropdownItems.every(function (employeeOption) {
            return employeeOption.style.display === 'none';
        });

        if (noResultsFound) {
            showNoResultsMessage();
        } else {
            resetDropdown();
        }
    });

    // Event listener for clicking on an employee option
    dropdownMenu.addEventListener('click', function (event) {
        if (event.target.tagName === 'A') {
            // Set the selected employee value
            employeeSearchInput.value = event.target.textContent;

            // Extract employee data from the selected option
            const empId = event.target.dataset.value;
            const email = event.target.dataset.email;

            // Update the readonly field with the selected employee's email
            document.getElementById('email').value = email;

            // Append a hidden input field to submit the selected employee data with the form
            const hiddenInput = document.createElement('input');
            hiddenInput.type = 'hidden';
            hiddenInput.name = 'employee'; // This should match the name attribute in the form
            hiddenInput.value = empId;

            // Check if the hidden input already exists and replace it if needed
            const existingHiddenInput = document.querySelector('input[name="employee"]');
            if (existingHiddenInput) {
                existingHiddenInput.replaceWith(hiddenInput);
            } else {
                document.querySelector('form').appendChild(hiddenInput);
            }
        }
    });

    // Event listener for closing the dropdown
    document.addEventListener('click', function (event) {
        if (!event.target.matches('.dropdown-toggle') && !event.target.matches('#employeeSearchInput')) {
            // Hide the dropdown menu when clicking outside
            dropdownMenu.style.display = 'none';
        }
    });

    // Event listener for focusing on the search input
    employeeSearchInput.addEventListener('focus', function () {
        // Show the dropdown menu when focusing on the search input
        dropdownMenu.style.display = 'block';
    });

    // Event listener for clicking on the search input
    employeeSearchInput.addEventListener('click', function () {
        // Show the dropdown menu when clicking on the search input
        dropdownMenu.style.display = 'block';
    });

    // Function to show "No results found" message
    function showNoResultsMessage() {
        dropdownMenu.innerHTML = '<div class="dropdown-item">No results found</div>';
    }
});

document.addEventListener('DOMContentLoaded', function () {
    // Add event listener to the clear button to the search and select button.
    const clearSearchButton = document.getElementById('clearSearchButton');
    if (clearSearchButton) {
        clearSearchButton.addEventListener('click', function () {
            const employeeSearchInput = document.getElementById('employeeSearchInput');
            if (employeeSearchInput) {
                employeeSearchInput.value = '';
            }
        });
    }
});
