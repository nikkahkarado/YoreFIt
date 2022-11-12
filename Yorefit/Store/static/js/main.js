// let products = document.querySelectorAll('.product');
let windowWidth = window.innerWidth;
let sectionTwo = document.querySelector('.sec-2').children;
let categories = sectionTwo.length;


if (localStorage.getItem('cart') == null) {
    var cart = {};
} else {
    cart = JSON.parse(localStorage.getItem('cart'));
    updateCart(cart);
}

$('.add-to-cart').on('click', '.btn-add-to-cart', function () {
    var idStr = this.id.toString();
    if (cart[idStr] == undefined) {
        let name = document.getElementById('name-' + idStr.slice(4,)).innerHTML;
        let price = document.getElementById('price-' + idStr.slice(4,)).innerHTML;
        let img = document.getElementById('img-' + idStr.slice(4,)).src;
        let qty = 1;
        cart[idStr] = [qty, name, img, parseInt(price)];
    }
    updateCart(cart);
});

function updateCart(cart) {
    var noOfItems = 0;
    for (var item in cart) {
        if (cart[item][0] > 0) {
            noOfItems += cart[item][0];
            document.getElementById('div-' + item).innerHTML = "<button id='minus-" + item +
                "' class='btn-add-to-cart-minus'> - </button> <p class='val' id='val-" + item + "''>" +
                cart[item][0] + "</p> <button id='plus-" + item +
                "' class='btn-add-to-cart-plus'> + </button>";
        } else {
            document.getElementById('div-' + item).innerHTML = "<button id='" + item + "' class='btn-add-to-cart'> Add To Cart </button>";
            delete cart[item];
        }
    }
    document.getElementById('cart-badge').innerHTML = noOfItems;
    localStorage.setItem('cart', JSON.stringify(cart));
}

function clearCart() {
    cart = JSON.parse(localStorage.getItem('cart'));
    for (var item in cart) {
        document.getElementById('div-' + item).innerHTML = "<button id='" + item + "' class='btn-add-to-cart'> Add To Cart </button>";
    }
    localStorage.clear();
    cart = {}
    updateCart(cart);
}

$('.add-to-cart').on('click', '.btn-add-to-cart-minus', function () {
    var id = this.id.slice(6,);
    cart[id][0] = Math.max(0, cart[id][0] - 1);
    document.getElementById('val-' + id).innerHTML = cart[id][0];
    updateCart(cart);
});

$('.add-to-cart').on('click', '.btn-add-to-cart-plus', function () {
    var id = this.id.slice(5,);
    cart[id][0]++;
    document.getElementById('val-' + id).innerHTML = cart[id][0];
    updateCart(cart);
});

// Carousel


function slideRight(id) {
    let ind = id.split("-")[1];
    let productDiv = document.querySelector(".products-" + ind);
    let productDivWidth = productDiv.getBoundingClientRect().width;
    let products = productDiv.children;
    let productWidth = products[0].getBoundingClientRect().width;
    let noOfProds = products.length;
    let oneSlide = parseInt(((productDivWidth / productWidth).toString()).split('.')[0]);
    let gridGap = parseInt(window.getComputedStyle(productDiv).gap);

    let maxSlides = noOfProds - oneSlide;
    let currentElement = productDiv.querySelector('.current-slide');
    let currentElementIndex = getIndex(products, currentElement);

    if (currentElementIndex < maxSlides) {
        for (let i = 0; i < noOfProds; i++) {
            products[i].style.transform = "translateX(-" + (productWidth + gridGap) * (currentElementIndex + 1) + "px)";
        }
        currentElement.nextElementSibling.classList.add('current-slide');
        currentElement.classList.remove('current-slide');
    }

}


function slideLeft(id) {
    let ind = id.split("-")[1];
    let productDiv = document.querySelector(".products-" + ind);
    let productDivWidth = productDiv.getBoundingClientRect().width;
    let products = productDiv.children;
    let productWidth = products[0].getBoundingClientRect().width;
    let noOfProds = products.length;
    let oneSlide = parseInt(((productDivWidth / productWidth).toString()).split('.')[0]);
    let gridGap = parseInt(window.getComputedStyle(productDiv).gap);

    let maxSlides = noOfProds - oneSlide;
    let currentElement = productDiv.querySelector('.current-slide');
    let currentElementIndex = getIndex(products, currentElement);

    if (currentElementIndex > 0) {
        for (let i = 0; i < noOfProds; i++) {
            products[i].style.transform = "translateX(-" + (((productWidth + gridGap) * (currentElementIndex)) - (productWidth + gridGap)) + "px)";
        }
        currentElement.previousElementSibling.classList.add('current-slide');
        currentElement.classList.remove('current-slide');
    }

}


/*
let slide = {
    slides: 0,
    currentRight: 1,
    currentLeft: 1,
    rightSlides: 0,
    leftSlides: 0,
    availableRightSlides: 0,
    availableLeftSlides: 0,

};

function slideRight(id) {
    let ind = id.split("-")[1];
    let productDiv = document.querySelector(".products-" + ind);
    let products = productDiv.children;
    let productWidth = products[0].getBoundingClientRect().width;
    let noOfProds = products.length;
    slide.slides = noOfProds;
    slide.currentLeft = slide.slides - 4;
    slide.availableRightSlides = (slide.slides - 5) - slide.rightSlides;
    slide.rightSlides = slide.slides - slide.availableRightSlides - 5;
    slide.leftSlides = slide.availableRightSlides;
    slide.availableLeftSlides = slide.rightSlides;


    if (slide.availableRightSlides > 0) {
        
        slide.currentRight++;
        slide.currentLeft--;
        slide.rightSlides++;
        slide.availableLeftSlides++;
        slide.leftSlides--;
        slide.availableRightSlides--;
        for (let i = 0; i < noOfProds; i++) {
            products[i].style.transform = "translateX(-" + (productWidth + 24) * slide.currentRight + "px)";
        }
    }
} 

function slideLeft(id) {
    let ind = id.split("-")[1];
    let productDiv = document.querySelector(".products-" + ind);
    let products = productDiv.children;
    let productWidth = products[0].getBoundingClientRect().width;
    let noOfProds = products.length;
    slide.slides = noOfProds;
    // slide.currentLeft = slide.slides - 4;
    slide.availableRightSlides = (slide.slides - 5) - slide.rightSlides;
    slide.rightSlides = slide.slides - slide.availableRightSlides - 5;
    slide.leftSlides = slide.availableRightSlides;
    slide.availableLeftSlides = slide.rightSlides;

    if (slide.availableLeftSlides > 0) {
        
        for (let i = 0; i < noOfProds; i++) {
            products[i].style.transform = "translateX(-" + (((productWidth + 24) * slide.currentRight) - ((productWidth + 24) * slide.currentLeft)) + "px)";
        }
        slide.currentRight--;
        slide.currentLeft++;
        slide.rightSlides--;
        slide.availableLeftSlides--;
        slide.leftSlides++;
        slide.availableRightSlides++;
    }
} */


// Extra Usage Functions

function getIndex(array, elem) {
    for (let i = 0; i < array.length; i++) {
        if (array[i] == elem) {
            return i;
        }
    }
}

let nextBtns = document.querySelectorAll('.category_arrows-next');
let prevBtns = document.querySelectorAll('.category_arrows-prev');

