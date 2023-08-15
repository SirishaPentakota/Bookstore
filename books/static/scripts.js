


function buyBook(bookId) {
    // Perform the logic for the 'Buy' button here.
    // For example, you could make an AJAX request to handle the purchase process.
    // In this example, we'll simply log the book ID to the console.
    console.log('Buy book:', bookId);
}


document.addEventListener('DOMContentLoaded', function() {
    const buyButtons = document.querySelectorAll('.buy-button');
    buyButtons.forEach(button => {
      button.addEventListener('click', function(event) {
        event.preventDefault();
        const bookId = this.getAttribute('data-book-id');
        const form = document.createElement('form');
        form.method = 'post';
        form.action = this.href;
        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'book_id';
        input.value = bookId;
        form.appendChild(input);
        const csrfInput = document.createElement('input');
        csrfInput.type = 'hidden';
        csrfInput.name = 'csrfmiddlewaretoken';
        csrfInput.value = csrfToken;
        form.appendChild(csrfInput);
        document.body.appendChild(form);
        form.submit();
      });
    });
  });


  function toggleDropdown() {
    var dropdownContent = document.getElementById("dropdown-content");
    if (dropdownContent.style.display === "block") {
        dropdownContent.style.display = "none";
    } else {
        dropdownContent.style.display = "block";
    }
}
  
  
