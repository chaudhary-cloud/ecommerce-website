// ================================
// PRODUCTS
// ================================

const products = [

    {
        id: 1,
        name: "Wireless Headphones",
        description: "Comfortable wireless headphones with clear sound.",
        price: 1499,
        image: "🎧"
    },

    {
        id: 2,
        name: "Smart Watch",
        description: "Stylish smartwatch for your everyday lifestyle.",
        price: 2499,
        image: "⌚"
    },

    {
        id: 3,
        name: "Running Shoes",
        description: "Lightweight and comfortable running shoes.",
        price: 1999,
        image: "👟"
    },

    {
        id: 4,
        name: "Backpack",
        description: "Spacious backpack for college and travel.",
        price: 999,
        image: "🎒"
    },

    {
        id: 5,
        name: "Sunglasses",
        description: "Modern sunglasses with a stylish design.",
        price: 799,
        image: "🕶️"
    },

    {
        id: 6,
        name: "Coffee Mug",
        description: "Simple and elegant coffee mug for your desk.",
        price: 399,
        image: "☕"
    }

];


// ================================
// DOM ELEMENTS
// ================================

const productContainer =
    document.querySelector("#productContainer");

const cartContainer =
    document.querySelector("#cartContainer");

const cartCount =
    document.querySelector("#cartCount");

const cartTotal =
    document.querySelector("#cartTotal");

const clearCartBtn =
    document.querySelector("#clearCartBtn");

const searchInput =
    document.querySelector("#searchInput");

const shopNowBtn =
    document.querySelector("#shopNowBtn");


// ================================
// GET CART FROM LOCAL STORAGE
// ================================

let cart = JSON.parse(
    localStorage.getItem("cart")
) || [];


// ================================
// DISPLAY PRODUCTS
// ================================

function displayProducts(productList) {

    productContainer.innerHTML = "";


    if (productList.length === 0) {

        productContainer.innerHTML = `
            <p>
                No products found.
            </p>
        `;

        return;
    }


    productList.forEach(function(product) {

        const card =
            document.createElement("div");

        card.classList.add("product-card");


        card.innerHTML = `

            <div class="product-image">
                ${product.image}
            </div>

            <div class="product-info">

                <h3>
                    ${product.name}
                </h3>

                <p>
                    ${product.description}
                </p>

                <div class="product-bottom">

                    <span class="product-price">
                        ₹${product.price}
                    </span>

                    <button
                        class="add-btn"
                        onclick="addToCart(${product.id})"
                    >
                        Add to Cart
                    </button>

                </div>

            </div>
        `;


        productContainer.appendChild(card);

    });

}


// ================================
// ADD TO CART
// ================================

function addToCart(productId) {

    const product =
        products.find(function(item) {

            return item.id === productId;

        });


    const existingProduct =
        cart.find(function(item) {

            return item.id === productId;

        });


    if (existingProduct) {

        existingProduct.quantity++;

    } else {

        cart.push({

            ...product,

            quantity: 1

        });

    }


    saveCart();

    displayCart();

}


// ================================
// DISPLAY CART
// ================================

function displayCart() {

    cartContainer.innerHTML = "";


    if (cart.length === 0) {

        cartContainer.innerHTML = `
            <p class="empty-cart">
                Your cart is empty.
            </p>
        `;

        cartCount.textContent = "0";

        cartTotal.textContent = "0";

        return;
    }


    let total = 0;

    let totalItems = 0;


    cart.forEach(function(item) {

        total +=
            item.price * item.quantity;

        totalItems += item.quantity;


        const cartItem =
            document.createElement("div");

        cartItem.classList.add("cart-item");


        cartItem.innerHTML = `

            <div>

                <h3>
                    ${item.name}
                </h3>

                <p>
                    ₹${item.price}
                </p>

            </div>


            <div class="cart-actions">

                <button
                    class="quantity-btn"
                    onclick="decreaseQuantity(${item.id})"
                >
                    -
                </button>

                <span class="quantity">
                    ${item.quantity}
                </span>

                <button
                    class="quantity-btn"
                    onclick="increaseQuantity(${item.id})"
                >
                    +
                </button>

                <button
                    class="remove-btn"
                    onclick="removeFromCart(${item.id})"
                >
                    Remove
                </button>

            </div>
        `;


        cartContainer.appendChild(cartItem);

    });


    cartCount.textContent = totalItems;

    cartTotal.textContent = total;

}


// ================================
// INCREASE QUANTITY
// ================================

function increaseQuantity(productId) {

    const product =
        cart.find(function(item) {

            return item.id === productId;

        });


    if (product) {

        product.quantity++;

    }


    saveCart();

    displayCart();

}


// ================================
// DECREASE QUANTITY
// ================================

function decreaseQuantity(productId) {

    const product =
        cart.find(function(item) {

            return item.id === productId;

        });


    if (!product) {
        return;
    }


    product.quantity--;


    if (product.quantity <= 0) {

        cart =
            cart.filter(function(item) {

                return item.id !== productId;

            });

    }


    saveCart();

    displayCart();

}


// ================================
// REMOVE FROM CART
// ================================

function removeFromCart(productId) {

    cart =
        cart.filter(function(item) {

            return item.id !== productId;

        });


    saveCart();

    displayCart();

}


// ================================
// CLEAR CART
// ================================

clearCartBtn.addEventListener(
    "click",
    function() {

        cart = [];

        saveCart();

        displayCart();

    }
);


// ================================
// SEARCH PRODUCTS
// ================================

searchInput.addEventListener(
    "input",
    function() {

        const searchText =
            searchInput.value
                .toLowerCase()
                .trim();


        const filteredProducts =
            products.filter(function(product) {

                return product.name
                    .toLowerCase()
                    .includes(searchText);

            });


        displayProducts(filteredProducts);

    }
);


// ================================
// SHOP NOW BUTTON
// ================================

shopNowBtn.addEventListener(
    "click",
    function() {

        document
            .querySelector("#products")
            .scrollIntoView({
                behavior: "smooth"
            });

    }
);


// ================================
// SAVE CART
// ================================

function saveCart() {

    localStorage.setItem(
        "cart",
        JSON.stringify(cart)
    );

}


// ================================
// INITIAL DISPLAY
// ================================

displayProducts(products);

displayCart();