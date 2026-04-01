    function changeImage(element) {
    // 1. Get the (src) of the image that was clicked
    let newSrc = element.src;
    
    // 2. Finding the big Image and change its src (path)
    document.querySelector('.ecommerce-gallery-main-img').src = newSrc;
    
    // 3. make it active
    let thumbs = document.querySelectorAll('.thumb-img');
    thumbs.forEach(img => img.classList.remove('active'));
    element.classList.add('active');

}