const categoryDropdown = document.getElementById('categoryDropdown');
const clothingGrid = document.getElementById('clothingGrid');
const outfitMakerBtn = document.getElementById('outfitMakerBtn');
const outfitImageContainer = document.getElementById('outfitImageContainer');

// Data for each category
const items = {
    tops: [
        { src: 'images/top1.png', name: 'Top 1', heart: 'images/unfillheart.svg' },
        { src: 'images/top2.png', name: 'Top 2', heart: 'images/fillheart.svg' },
        { src: 'images/top3.png', name: 'Top 3', heart: 'images/unfillheart.svg' }
    ],
    bottoms: [
        { src: 'images/bottom1.png', name: 'Bottom 1', heart: 'images/fillheart.svg' },
        { src: 'images/bottom2.png', name: 'Bottom 2', heart: 'images/unfillheart.svg' },
        { src: 'images/bottom3.png', name: 'Bottom 3', heart: 'images/fillheart.svg' }
    ],
    dresses: [
        { src: 'images/dress1.png', name: 'Dress 1', heart: 'images/fillheart.svg' },
        { src: 'images/dress2.png', name: 'Dress 2', heart: 'images/unfillheart.svg' },
        { src: 'images/dress3.png', name: 'Dress 3', heart: 'images/fillheart.svg' }
    ],
    outfits: [
        { src: 'images/outfit1.png', name: 'Outfit 1', heart: 'images/fillheart.svg' }
    ]
};

// Function to display items
function displayItems(category = null) {
    clothingGrid.innerHTML = ''; // Clear the grid

    const savedItems = JSON.parse(localStorage.getItem('closetItems')) || {};
    const allItems = category
        ? [...(items[category] || []), ...(savedItems[category] || [])]
        : [
              ...items.tops,
              ...items.bottoms,
              ...items.dresses,
              ...items.outfits,
              ...(savedItems.tops || []),
              ...(savedItems.bottoms || []),
              ...(savedItems.dresses || []),
              ...(savedItems.outfits || []),
          ];

    allItems.forEach((item, index) => {
        const clothingItem = document.createElement('div');
        clothingItem.classList.add('clothing-item');

        clothingItem.innerHTML = `
            <img src="${item.src}" alt="${item.name}" class="item-image" data-category="${category}" data-index="${index}">
            <p>${item.name}</p>
            <div class="item-actions">
                <img src="${item.heart}" alt="Heart Icon" class="heart-icon">
            </div>
        `;

        clothingGrid.appendChild(clothingItem);

        // Add click event to redirect to item.html
        clothingItem.querySelector('.item-image').addEventListener('click', () => {
            const queryParams = new URLSearchParams({
                src: item.src,
                name: item.name,
                category: category || 'all',
                index: index,
            });
            window.location.href = `item.html?${queryParams.toString()}`;
        });
    });
}

// Event listener for category selection
categoryDropdown.addEventListener('change', () => {
    const selectedCategory = categoryDropdown.value;
    displayItems(selectedCategory);
});

// Function to request the generated outfit image from the backend
async function fetchOutfitImage() {
    try {
        const response = await fetch('http://127.0.0.1:8000/generate-outfit'); // API endpoint
        if (response.ok) {
            const imageUrl = await response.text(); // The backend will return the URL of the image
            displayOutfitImage(imageUrl);
        } else {
            console.error('Failed to fetch outfit image');
        }
    } catch (error) {
        console.error('Error fetching outfit image:', error);
    }
}

// Function to display the fetched outfit image
function displayOutfitImage(imageUrl) {
    outfitImageContainer.innerHTML = `<img src="${imageUrl}" alt="Generated Outfit">`;
}

// Event listener for the Outfit Maker button
outfitMakerBtn.addEventListener('click', fetchOutfitImage);

// Display all items by default
displayItems();
