// Parse query parameters
const params = new URLSearchParams(window.location.search);
const itemSrc = params.get('src');
const itemName = params.get('name');
const itemCategory = params.get('category');
const itemIndex = params.get('index');

// Populate item details
const savedItems = JSON.parse(localStorage.getItem('closetItems')) || {};
const currentItem = savedItems[itemCategory]?.[itemIndex];

if (currentItem) {
    document.getElementById('itemImage').src = currentItem.src;
    document.getElementById('itemDescription').textContent = currentItem.name;
    document.getElementById('categorySelect').value = itemCategory;
    document.getElementById('itemBrand').value = currentItem.brand || '';
    document.getElementById('itemSize').value = currentItem.size || '';
    document.getElementById('itemDate').value = currentItem.date || '';
}

// Save changes functionality
document.getElementById('saveChanges').addEventListener('click', () => {
    const newCategory = document.getElementById('categorySelect').value;
    const newDescription = document.getElementById('itemDescription').textContent;
    const newBrand = document.getElementById('itemBrand').value;
    const newSize = document.getElementById('itemSize').value;
    const newDate = document.getElementById('itemDate').value;

    // Remove the item from the old category
    if (savedItems[itemCategory]) {
        savedItems[itemCategory].splice(itemIndex, 1);
    }

    // Add the updated item to the new category
    if (!savedItems[newCategory]) {
        savedItems[newCategory] = [];
    }
    savedItems[newCategory].push({
        src: itemSrc,
        name: newDescription,
        heart: 'images/unfillheart.svg',
        brand: newBrand,
        size: newSize,
        date: newDate,
    });

    // Save changes to localStorage
    localStorage.setItem('closetItems', JSON.stringify(savedItems));

    alert('Changes saved successfully!');
    window.location.href = 'mycloset.html'; // Redirect back to the closet page
});

// Delete item functionality
document.getElementById('deleteItem').addEventListener('click', () => {
    if (savedItems[itemCategory]) {
        savedItems[itemCategory].splice(itemIndex, 1); // Remove the item
        localStorage.setItem('closetItems', JSON.stringify(savedItems)); // Update localStorage
        alert('Item deleted successfully!');
        window.location.href = 'mycloset.html'; // Redirect back to the closet page
    }
});