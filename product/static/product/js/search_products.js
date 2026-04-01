{
    const productsContainer = document.getElementById('products');
    const paginationElement = document.getElementById('pagination');
    const moreProductsElement = document.querySelector('#more-products');
    const searchProductsButton = document.getElementById('search-products');

    // A function for creating cards
    function createCardHTML(element) {
        let prod_id = element.id;
        let img_url = element.img;
        let title = element.title;
        let description = element.description.split(' ').slice(0, 4).join(' ') + '...';
        let discount = element.discount;
        let price = element.price;
        let final_price = element.final_price;
        let slug = element.slug;
        let product_url = `/product/${slug}/`;

        let price_element = (discount > 0) 
            ? `<p class="card-text"><b>price: </b><del>${price}</del>$ -- ${final_price}$</p>` 
            : `<p class="card-text"><b>price: </b>${final_price}$</p>`;

        return `
        <div class="card mt-5" style="width: 19rem; box-shadow: 1px 0px 20px 4px grey;" data-product-id="${prod_id}">
            <div class="img-container" style="width: 100%; height: 300px; background-size: auto;">
                <img src=${img_url} width="100%" height="100%" class="card-img-top" alt="product image">
            </div>
            <div class="card-body d-flex flex-column">
                <h5 class="card-title">${title}</h5>
                <p class="card-text" style="font-size: 14px;">${description}</p>
                ${price_element}
                <div class="d-flex justify-content-between align-items-end mt-auto">
                    <a href="${product_url}" class="btn btn-primary" style="width: 49%;">Open product</a>
                    <a class="btn btn-info cart ms-auto" style="width: 49%;" onclick="manageCart(this, 'add')">Add to cart</a>
                    <div class="btn btn-info d-flex justify-content-between align-items-center d-none cart-adding-controls ms-auto" 
                        style="width: 49%; background-color: transparent; border: 1px solid blue; border-radius: 20px;">
                        <i class="fa-solid fa-minus d-none cart-minus" onclick="manageCart(this, 'minus')"></i> 
                        <i class="fa-regular fa-trash-can cart-trash" onclick="manageCart(this, 'delete')"></i> 
                        <span class="cart-items-number"></span> 
                        <i class="fa-solid fa-plus cart-plus" onclick="manageCart(this, 'plus')"></i> 
                    </div>
                </div>
            </div>
        </div>`;
    }

    // Searching logic
    searchProductsButton.addEventListener('input', function(e) {
        sessionStorage.setItem('last_count_products', 12);
        let title = e.target.value.trim();

        if (paginationElement) paginationElement.classList.add('d-none');
        if (moreProductsElement) moreProductsElement.classList.add('d-none');

        fetch(`/products/search/?title=${encodeURIComponent(title)}`)
        .then(response => response.json())
        .then(result => {
            productsContainer.innerHTML = ''; // reset the counter when searching ...
            if (result.status == "success"){
                result.data.forEach(element => {
                    productsContainer.innerHTML += createCardHTML(element);
                });
                
                // Update the counter based on what has actually been displayed.
                sessionStorage.setItem("last_count_products", result.data.length);
            }

            if(result.exists && result.is_there_more) {
                moreProductsElement.classList.remove('d-none');
            }
        });
    });

    // Load More logic
    if (moreProductsElement) {
        moreProductsElement.addEventListener("click", function(e) {
            e.preventDefault();
            // get the exact current number of items on the page.
            let currentDisplayedCount = productsContainer.querySelectorAll('.card').length;
            let title = searchProductsButton.value.trim();

            fetch(`/products/load-more-products/?title=${encodeURIComponent(title)}&more=${currentDisplayedCount}`)
            .then(response => response.json())
            .then(result => {
                if (result.status == "success"){
                    result.data.forEach(element => {
                        // Do not add the item if it already exists with the ID.
                        if (!document.querySelector(`[data-product-id="${element.id}"]`)) {
                            productsContainer.innerHTML += createCardHTML(element);
                        }
                    });
                    
                    if (!result.is_there_more) {
                        moreProductsElement.classList.add("d-none");
                    }
                }
            });
        });
    }
}