const products = [
    {
        id: 1,
        name: "Paracetamol Tablets IP 500 mg",
        category: "painkillers",
        price: 12.0,
        image: "static/images/Picture4.png",
        pack: "Pack of 15 Tablets",
    },
    {
        id: 2,
        name: "Ibuprofen Tablets 400 mg",
        category: "painkillers",
        price: 15.0,
        image: "static/images/Picture4.png",
        pack: "Pack of 10 Tablets",
    },
    {
        id: 3,
        name: "Amoxicillin Capsules 500 mg",
        category: "antibiotics",
        price: 45.0,
        image: "static/images/Picture4.png",
        pack: "Pack of 6 Capsules",
    },
    {
        id: 4,
        name: "Azithromycin Tablets 250 mg",
        category: "antibiotics",
        price: 60.0,
        image: "static/images/Picture4.png",
        pack: "Pack of 5 Tablets",
    },
    {
        id: 5,
        name: "Aspirin Tablets 75 mg",
        category: "painkillers",
        price: 8.0,
        image: "static/images/Picture4.png",
        pack: "Pack of 14 Tablets",
    },
    {
        id: 6,
        name: "Ciprofloxacin Tablets 500 mg",
        category: "antibiotics",
        price: 65.0,
        image: "static/images/Picture4.png",
        pack: "Pack of 10 Tablets",
    },
    {
        id: 7,
        name: "Digital Thermometer",
        category: "equipment",
        price: 250.0,
        image: "static/images/Picture4.png",
        pack: "1 Unit",
    },
    {
        id: 8,
        name: "Blood Pressure Monitor",
        category: "equipment",
        price: 1200.0,
        image: "static/images/Picture4.png",
        pack: "1 Unit",
    },
];

const cart = [];

// Function to display products
function displayProducts(filteredProducts) {
    const grid = document.getElementById("product-grid");
    grid.innerHTML = "";

    filteredProducts.forEach((product) => {
        const productDiv = document.createElement("div");
        productDiv.classList.add("product");
        productDiv.innerHTML = `
            <img src="${product.image}" alt="${product.name}">
            <h4>${product.name}</h4>
            <div class="product-container">
                <div class="product-info">
                    <div class="pack-info">
                        <p>${product.pack}</p>
                    </div>
                    <div class="price">₹${product.price.toFixed(2)}</div>
                </div>
                <button class="add-to-cart" onclick="addToCart(${product.id})">
                    <img src="static/images/add-to-cart.png" alt="Add to Cart">
                </button>
            </div>
        `;
        grid.appendChild(productDiv);
    });
}

function searchProducts() {
    const searchTerm = document.getElementById("search-input").value.toLowerCase();
    const activeCategoryBtn = document.querySelector(".category-btn.active");
    const activeCategory = activeCategoryBtn.getAttribute("data-category");

    let filtered = products;

    // First filter by category if not "all"
    if (activeCategory !== "all") {
        filtered = products.filter((product) => product.category === activeCategory);
    }

    // Then filter by search term
    if (searchTerm) {
        filtered = filtered.filter(
            (product) =>
                product.name.toLowerCase().includes(searchTerm) ||
                product.category.toLowerCase().includes(searchTerm),
        );
    }

    displayProducts(filtered);
}

// Function to filter by category
function filterCategory(category) {
    // Update active button
    document.querySelectorAll(".category-btn").forEach((btn) => {
        btn.classList.remove("active");
    });
    document.querySelector(`.category-btn[data-category="${category}"]`).classList.add("active");

    // Filter products
    const filtered =
        category === "all" ? products : products.filter((product) => product.category === category);

    displayProducts(filtered);
}

// Function to add item to cart
function addToCart(productId) {
    const product = products.find((p) => p.id === productId);
    if (product) {
        cart.push(product);
        showCartNotification();
    }
}

// Function to show cart notification
function showCartNotification() {
    const notification = document.getElementById("cart-notification");
    notification.style.display = "block";
    setTimeout(() => {
        notification.style.display = "none";
    }, 2000);
}

// Event listeners
document.addEventListener("DOMContentLoaded", function () {
    // Initial display of all products
    displayProducts(products);

    // Search input event listener
    document.getElementById("search-input").addEventListener("input", searchProducts);

    // Category filter buttons event listeners
    document.querySelectorAll(".category-btn").forEach((button) => {
        button.addEventListener("click", function () {
            const category = this.getAttribute("data-category");
            filterCategory(category);
        });
    });
});
