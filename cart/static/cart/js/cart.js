function updateCart() {
    fetch('/cart/', {
        headers: {
            "x-requested-with": "XMLHttpRequest",
        }
    })
    .then(response => {
        if (!response.ok) throw new Error('Network response was not ok!');
        return response.json();
    })
    .then(result => {
        if (result.status === "success") {
            let productCartContainer = document.getElementById('cart-container');
            document.getElementById('cart-navbar-counter').textContent = result.total_cart_quantity;

            // if there are no products in cart (session)
            if (!result.products || result.products.length === 0) {
                productCartContainer.innerHTML = `
        <div class="d-flex flex-column justify-content-center mx-auto" style="margin-top: 100px; width: 1000px; box-shadow: 1px 1px 18px 12px rgb(165, 164, 164); border-radius: 15px; padding: 20px;">
            <h2>MyStore Cart</h2>
            <hr>
                <div id="empty-cart" class="card mb-3" style="width: 100%; height: 250px;">
                    <div class="row g-0">
                        <div class="col-md-4" style="width: 250px; height: 250px;">
                            <img src="/static/images/products/empty_cart.png" class="img-fluid rounded-start" style="width: 100%; height: 100%; object-fit: cover;" alt="product image">
                        </div>
                        <div class="col-md-8">
                        <div class="card-body">
                            <h5 class="card-title">MyStore's cart is empty!</h5>
                            <p class="card-text">
                                Go to the products section and add the products you want from <a href="/products/all/">here</a> to buy them immediately or later.
                            </p>
                        </div>
                        </div>
                    </div>
                </div>
        </div>
        <hr>
                `;
                return;
            }
            


            // if there are products in cart (session)
            let htmlContent = `
            <div class="d-flex flex-column justify-content-center mx-auto" style="margin-top: 100px; width: 1000px; box-shadow: 1px 1px 18px 12px rgb(165, 164, 164); border-radius: 15px; padding: 20px;">
                <h2>MyStore Cart</h2>
                <hr>
            `;


            // Get The CSRF Token
            const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
            const csrfTokenCookie = csrfInput ? csrfInput.value : "";
            
            
            // 2. adding cards data in variables
            result.products.forEach(element => {
                const prodId = element.id;
                const title = element.title;
                const description = element.description || "";
                const img = element.img;
                const price = element.price;
                const totalProductPrice = element.total;
                const productQuantity = element.qty;
                
                // price logic (Discount)
                let priceElement = (element.discount) 
                    ? `<p class="card-text"><b>price: </b><del>${price}</del>$ -- ${element.price}$</p>` 
                    : `<p class="card-text"><b>price: </b>${price}$</p>`;

                // control buttons logic
                let isQtyGreatThanOne = parseInt(productQuantity) > 1;
                let controlCartButtons = `
                    <i class="fa-solid fa-minus cart-minus ${isQtyGreatThanOne ? '' : 'd-none'}" data-place="in_cart" onclick="manageCart(this, 'minus')"></i> 
                    <i class="fa-regular fa-trash-can cart-trash ${isQtyGreatThanOne ? 'd-none' : ''}" data-place="in_cart" onclick="manageCart(this, 'delete')"></i> 
                    <span class="cart-items-number">${productQuantity}</span> 
                    <i class="fa-solid fa-plus cart-plus" data-place="in_cart" onclick="manageCart(this, 'plus')"></i> 
                `;

                htmlContent += `
                <div class="card mb-3" style="width: 100%; height: 250px;" data-product-id="${prodId}">
                    <div class="row g-0 h-100">
                        <div class="col-md-4" style="width: 250px; height: 250px;">
                            <img src="${img}" class="img-fluid rounded-start" style="width: 100%; height: 100%; object-fit: cover;" alt="product image">
                        </div>
                        <div class="col-md-8">
                            <div class="card-body">
                                <h5 class="card-title">${title}</h5>
                                <p class="card-text">${description}</p>
                                ${priceElement}
                                <p id="total-product-price" class="card-text"><b>total price: </b>${totalProductPrice}$</p>
                                <div class="d-flex justify-content-between align-items-end">
                                    <div class="btn btn-info d-flex justify-content-between align-items-center cart-adding-controls" 
                                         style="width: 20%; background-color: transparent; border: 1px solid blue; border-radius: 20px;">
                                        ${controlCartButtons}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <hr>
                `;
            });

            // 3. close the outer structure and add the total price
            htmlContent += `
                <h4 id="total_cart_price"><b>Total price</b>: ${result.total_cart_price}$</h4>
                <form id="checkout-form" method="POST" class="d-flex justify-content-center">
                    <input type="hidden" name="csrfmiddlewaretoken" value="${csrfTokenCookie}">
                    <button type="submit" class="btn btn-info w-50">Checkout</button>
                </form>
            </div>
            <hr>
            `;

            // 4. put all the contents in the container at once
            productCartContainer.innerHTML = htmlContent;
        }
    });
}



async function addCart(id) {
    return fetch(`/cart/add/${id}/`)
    .then(response => {
        if (!response.ok) throw new Error('Network response was not ok!');
        return response.json()
    })

    .then(result => {
        if (result.status === "success") {
            return result
        }
    });
}



async function minusCart(id) {
    return fetch(`/cart/minus/${id}/`)
    .then(response => response.json())
    .then(result => {
        if (result.status === "success") return result;
    });
}


async function removeCart(id) {
    return fetch(`/cart/delete/${id}/`)
    .then(response => response.json())
    .then(result => {
        if (result.status === "success") return result;
    });
}

async function manageCart(element, action) {
    // 1. Identifying the basic elements based on the element that was clicked
    const parent = element.closest('.card');
    const addBtn = parent.querySelector('.cart');
    const controls = parent.querySelector('.cart-adding-controls');
    const counter = parent.querySelector('.cart-items-number');
    const minusBtn = parent.querySelector('.cart-minus');
    const trashBtn = parent.querySelector('.cart-trash');
    const navCounter = document.querySelector('#cart-navbar-counter');
    const productId = parent.dataset.productId;

    // Retrieve the current value of the counter (inside the card) and the navbar.


    if (action === 'add' || action === 'plus') {
        const result = await addCart(productId); // wait the result (add to cart by the server)
        
        if (result && result.status === "success") {
            // Update numbers based on actual server response
            if (element.dataset.place === "in_cart") {
                const totalProductPrice = parent.querySelector('#total-product-price');
                const totalCartPrice = document.getElementById('total_cart_price');
            if (totalProductPrice) {
                totalProductPrice.innerHTML = `<p id="total-product-price" class="card-text"><b>total price: </b>${result.total_product_price}$</p>`;
            }
            if (totalCartPrice) {
                totalCartPrice.innerHTML = `<h4 id="total_cart_price"><b>Total price</b>: ${result.total_cart_price}$</h4>`;
            }
            }
            counter.textContent = result.item_quantity;
            if (navCounter) navCounter.textContent = result.total_cart_quantity;
            

            if (action === 'add') {
                addBtn.classList.add('d-none');
                controls.classList.remove('d-none');
            }
            
            // Update the appearance of the minus and delete buttons
            if (result.item_quantity > 1) {
                minusBtn.classList.remove('d-none');
                trashBtn.classList.add('d-none');
            } else {
                minusBtn.classList.add('d-none');
                trashBtn.classList.remove('d-none');
            }
        }
    }


    
    else if (action === 'minus') {
    const result = await minusCart(productId); // wait result (Reducing the number of products in the cart by the server)
    if (result && result.status === "success") {
        if (element.dataset.place === "in_cart") {
            const totalProductPrice = parent.querySelector('#total-product-price');
            const totalCartPrice = document.getElementById('total_cart_price');
            if (totalProductPrice) {
                totalProductPrice.innerHTML = `<p id="total-product-price" class="card-text"><b>total price: </b>${result.total_product_price}$</p>`;
            }
            if (totalCartPrice) {
                totalCartPrice.innerHTML = `<h4 id="total_cart_price"><b>Total price</b>: ${result.total_cart_price}$</h4>`;
            }
            
            
            
        }
        counter.textContent = result.item_quantity;
        if (navCounter) navCounter.textContent = result.total_cart_quantity;

        // If the quantity returns 0 or 1, control the appearance of the delete button
        if (result.item_quantity <= 1) {
            minusBtn.classList.add('d-none');
            trashBtn.classList.remove('d-none');
        }
        
        // If the product is deleted in bulk (reaches 0)
        if (result.item_quantity === 0) {
            addBtn.classList.remove('d-none');
            controls.classList.add('d-none');
        }
    }
    } 
    
    else if (action === 'delete') {
        const result = await removeCart(productId);// wait result (delete from the server)
        if (element.dataset.place === "in_cart") {
            if (result && result.status === "success") {
                updateCart();

            }
        }
        else if (result && result.status === "success") {
            // update the interface after server confirmation.
            addBtn.classList.remove('d-none');
            controls.classList.add('d-none');
            counter.textContent = ""; // Reset the counter
            if (navCounter) navCounter.textContent = result.total_cart_quantity;
        }


    }

}




