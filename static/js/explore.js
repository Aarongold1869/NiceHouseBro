"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var htmx_org_1 = require("htmx.org");
// declare global {
//     var activeIndex: number;
//     var cards: HTMLCollectionOf<HTMLElement>;
// }
window.activeIndex = 69;
window.cards = document.getElementsByClassName("property-card");
console.log(window.activeIndex);
function setImageAtIndex(index) {
    if (index === 0) {
        return;
    }
    var cardAtIndex = document.querySelector("[data-index=\"".concat(index, "\"]"));
    if (!cardAtIndex) {
        console.log('no card at index', index);
        return;
    }
    if (cardAtIndex.dataset.imgdidset === "true") {
        return;
    }
    var addressEl = document.getElementById("property-address-".concat(cardAtIndex.id));
    if (addressEl) {
        var address = addressEl.innerText.replace('/', '|');
        htmx_org_1.default.ajax('GET', "/explore/get-card-image/", { target: "#property-card-image-".concat(cardAtIndex.id), swap: 'outerHTML', values: { address: address, property_id: cardAtIndex.id } });
        cardAtIndex.dataset.imgdidset = "true";
    }
}
function updateMapMarkers(currentMarkerId, nextMarkerId) {
    var currentMapMarker = document.getElementById("marker-div-".concat(currentMarkerId));
    if (currentMapMarker) {
        currentMapMarker.dataset.focused = "false";
    }
    var nextMapMarker = document.getElementById("marker-div-".concat(nextMarkerId));
    if (nextMapMarker) {
        nextMapMarker.dataset.focused = "true";
    }
}
function setPreciseCardIndex(index) {
    var activeIndex = window.activeIndex;
    var currentCard = document.querySelector("[data-index=\"".concat(activeIndex, "\"]"));
    var nextIndex = index;
    var nextCard = document.querySelector("[data-index=\"".concat(nextIndex, "\"]"));
    if (!currentCard || !nextCard) {
        return;
    }
    currentCard.dataset.status = "left";
    nextCard.dataset.status = "becoming-active-from-right";
    setImageAtIndex(nextIndex);
    setTimeout(function () {
        nextCard.dataset.status = "active";
        activeIndex = nextIndex;
    }, 100);
    updateMapMarkers(currentCard.id, nextCard.id);
    var mapContainer = document.getElementById("map-container");
    setTimeout(function () {
        mapContainer.dataset.visible = "false";
    }, 800);
    setImageAtIndex(nextIndex + 1);
    setImageAtIndex(nextIndex - 1);
}
function handleNextCard() {
    var activeIndex = window.activeIndex;
    var cards = document.getElementsByClassName("property-card");
    var currentCard = document.querySelector("[data-index=\"".concat(activeIndex, "\"]"));
    var nextIndex = activeIndex + 1 <= cards.length - 1 ? activeIndex + 1 : 0;
    var nextCard = document.querySelector("[data-index=\"".concat(nextIndex, "\"]"));
    if (!currentCard || !nextCard) {
        return;
    }
    currentCard.dataset.status = "left";
    nextCard.dataset.status = "becoming-active-from-right";
    setTimeout(function () {
        nextCard.dataset.status = "active";
        activeIndex = nextIndex;
    }, 100);
    updateMapMarkers(currentCard.id, nextCard.id);
    setImageAtIndex(nextIndex + 1);
}
function handlePrevCard() {
    var activeIndex = window.activeIndex;
    var cards = document.getElementsByClassName("property-card");
    var currentCard = document.querySelector("[data-index=\"".concat(activeIndex, "\"]"));
    var nextIndex = activeIndex - 1 >= 0 ? activeIndex - 1 : cards.length - 1;
    var nextCard = document.querySelector("[data-index=\"".concat(nextIndex, "\"]"));
    if (!currentCard || !nextCard) {
        return;
    }
    currentCard.dataset.status = "right";
    nextCard.dataset.status = "becoming-active-from-left";
    setTimeout(function () {
        nextCard.dataset.status = "active";
        activeIndex = nextIndex;
    }, 100);
    updateMapMarkers(currentCard.id, nextCard.id);
    setImageAtIndex(nextIndex - 1);
}
function handleSaveCard() {
    var activeIndex = window.activeIndex;
    var currentCard = document.querySelector("[data-index=\"".concat(activeIndex, "\"]"));
    if (!currentCard) {
        return;
    }
    currentCard.classList.toggle("saved");
    currentCard.classList.toggle("bounce2");
    var imgElement = document.getElementById("property-card-image-".concat(currentCard.id));
    var imageStr = imgElement.src;
    var addressStr = document.getElementById("property-address-".concat(currentCard.id)).innerText;
    htmx_org_1.default.ajax('POST', "/explore/explore-toggle-saved/".concat(currentCard.id, "/"), { target: "#save-button-".concat(currentCard.id), swap: 'outerHTML', values: { address: addressStr, image: imageStr } });
}
function handleHideCard() {
    var activeIndex = window.activeIndex;
    var cards = document.getElementsByClassName("property-card");
    // get current card
    var currentCard = document.querySelector("[data-index=\"".concat(activeIndex, "\"]"));
    if (!currentCard) {
        return;
    }
    // set status to hidden -> hidden css transition
    currentCard.dataset.status = "hidden";
    // remove card from DOM following transition
    setTimeout(function () {
        currentCard.remove();
    }, 300);
    // update index of remaining cards
    for (var i = 0; i < cards.length; i++) {
        cards[i].dataset.index = i.toString();
    }
    // if no cards left, retrieve new cards
    if (cards.length === 0) {
        console.log('retrieve new cards');
        // htmx.ajax('GET', `/property/get-explore-controls/${nextCard.id}/`, {target:'#explore-controls', swap:'outerHTML'})
        return;
    }
    // increment index
    var nextIndex = activeIndex <= cards.length - 1 ? activeIndex : 0;
    // get and display next card
    var nextCard = document.querySelector("[data-index=\"".concat(nextIndex, "\"]"));
    if (!nextCard) {
        return;
    }
    nextCard.dataset.status = "becoming-active-from-right";
    setTimeout(function () {
        nextCard.dataset.status = "active";
        activeIndex = nextIndex;
    }, 100);
    var currentMapMarker = document.getElementById("marker-div-".concat(currentCard.id));
    if (currentMapMarker) {
        currentMapMarker.remove();
    }
    var nextMapMarker = document.getElementById("marker-div-".concat(nextCard.id));
    if (nextMapMarker) {
        nextMapMarker.dataset.focused = "true";
    }
    setImageAtIndex(nextIndex + 1);
}
function toggleMapView() {
    var mapContainer = document.getElementById("map-container");
    // const swipingComponent = document.getElementById("swiping-component");
    mapContainer.dataset.visible = mapContainer.dataset.visible === "false" ? "true" : "false";
    // swipingComponent.style.display = swipingComponent.style.display === "none" ? "block" : "none";
}
function submitSearch(event) {
    event.preventDefault();
    var searchInput = document.getElementById('location-search');
    var searchStr = searchInput.value;
    if (searchStr === '') {
        return;
    }
    window.location.replace("/explore/search=".concat(searchStr));
}
var searchButton = document.getElementById('search-button');
searchButton.addEventListener("click", submitSearch, false);
function initialize() {
    new google.maps.places.Autocomplete(searchInput);
}
var searchInput = document.getElementById('location-search');
searchInput.addEventListener('keypress', initialize);
