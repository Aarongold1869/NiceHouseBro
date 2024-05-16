import htmx from 'htmx.org';

// declare global {
//     var activeIndex: number;
//     var cards: HTMLCollectionOf<HTMLElement>;
// }
(window as any).activeIndex = 69;
(window as any).cards = document.getElementsByClassName("property-card") as HTMLCollectionOf<HTMLElement>;

console.log((window as any).activeIndex)

function setImageAtIndex(index: number) {
    if (index === 0) {
        return
    }
    const cardAtIndex: HTMLElement | null = document.querySelector(`[data-index="${index}"]`);
    if (!cardAtIndex) {
        console.log('no card at index', index)
        return
    }
    if (cardAtIndex.dataset.imgdidset === "true") {
        return
    }
    const addressEl: HTMLElement | null = document.getElementById(`property-address-${cardAtIndex.id}`)
    if (addressEl) { 
        const address = addressEl.innerText.replace('/','|');
        htmx.ajax('GET', `/explore/get-card-image/`, { target:`#property-card-image-${ cardAtIndex.id }`, swap:'outerHTML', values: { address: address, property_id: cardAtIndex.id } })
        cardAtIndex.dataset.imgdidset = "true";
    }
}

function updateMapMarkers(currentMarkerId: string, nextMarkerId: string) {
    const currentMapMarker: HTMLElement | null = document.getElementById(`marker-div-${currentMarkerId}`)
    if (currentMapMarker) {
        currentMapMarker.dataset.focused = "false";
    }
    const nextMapMarker: HTMLElement | null = document.getElementById(`marker-div-${nextMarkerId}`)
    if (nextMapMarker) {
        nextMapMarker.dataset.focused = "true";
    }
}

function setPreciseCardIndex(index: number) {
    let activeIndex = (window as any).activeIndex;

    const currentCard: HTMLElement | null = document.querySelector(`[data-index="${activeIndex}"]`);
    let nextIndex = index;
    const nextCard: HTMLElement | null = document.querySelector(`[data-index="${nextIndex}"]`);
    if (!currentCard || !nextCard) {
        return
    }
    currentCard.dataset.status = "left";
    nextCard.dataset.status = "becoming-active-from-right";
    setImageAtIndex(nextIndex);
    setTimeout(() => {
        nextCard.dataset.status = "active";
        activeIndex = nextIndex;
    }, 100);  

    updateMapMarkers(currentCard.id, nextCard.id);
    const mapContainer: HTMLElement = document.getElementById("map-container")!;
    setTimeout(() => {
        mapContainer.dataset.visible = "false" ;
    }, 800);
    
    setImageAtIndex(nextIndex + 1);
    setImageAtIndex(nextIndex - 1);
}

function handleNextCard() {
    let activeIndex = (window as any).activeIndex;
    let cards = document.getElementsByClassName("property-card") as HTMLCollectionOf<HTMLElement>;

    const currentCard: HTMLElement | null = document.querySelector(`[data-index="${activeIndex}"]`);
    let nextIndex = activeIndex + 1 <= cards.length - 1 ? activeIndex + 1 : 0;
    const nextCard: HTMLElement | null = document.querySelector(`[data-index="${nextIndex}"]`);
    if (!currentCard || !nextCard) {
        return
    }
    currentCard.dataset.status = "left";
    nextCard.dataset.status = "becoming-active-from-right";
    setTimeout(() => {
        nextCard.dataset.status = "active";
        activeIndex = nextIndex;
    }, 100);  
    updateMapMarkers(currentCard.id, nextCard.id);

    setImageAtIndex(nextIndex + 1);
}

function handlePrevCard() {
    let activeIndex = (window as any).activeIndex;
    let cards = document.getElementsByClassName("property-card") as HTMLCollectionOf<HTMLElement>;

    const currentCard: HTMLElement | null = document.querySelector(`[data-index="${activeIndex}"]`);
    let nextIndex = activeIndex - 1 >= 0 ? activeIndex - 1 : cards.length - 1;
    const nextCard: HTMLElement | null = document.querySelector(`[data-index="${nextIndex}"]`);
    if (!currentCard || !nextCard) {
        return
    }
    currentCard.dataset.status = "right";
    nextCard.dataset.status = "becoming-active-from-left";
    setTimeout(() => {
        nextCard.dataset.status = "active";
        activeIndex = nextIndex;
    }, 100);  
    updateMapMarkers(currentCard.id, nextCard.id);

    setImageAtIndex(nextIndex - 1);
}

function handleSaveCard() {
    let activeIndex = (window as any).activeIndex;

    const currentCard: HTMLElement | null = document.querySelector(`[data-index="${activeIndex}"]`);
    if (!currentCard) {
        return
    }
    currentCard.classList.toggle("saved")
    currentCard.classList.toggle("bounce2")
    const imgElement: HTMLImageElement = document.getElementById(`property-card-image-${currentCard.id}`)! as HTMLImageElement;
    let imageStr: string = imgElement.src;
    let addressStr: string = document.getElementById(`property-address-${currentCard.id}`)!.innerText;
    htmx.ajax('POST', `/explore/explore-toggle-saved/${currentCard.id}/`, {target:`#save-button-${currentCard.id}`, swap:'outerHTML', values: { address: addressStr, image: imageStr } })
}

function handleHideCard() {
    let activeIndex = (window as any).activeIndex;
    let cards = document.getElementsByClassName("property-card") as HTMLCollectionOf<HTMLElement>;

    // get current card
    const currentCard: HTMLElement | null = document.querySelector(`[data-index="${activeIndex}"]`);
    if (!currentCard) {
        return
    }
    // set status to hidden -> hidden css transition
    currentCard.dataset.status = "hidden";
    // remove card from DOM following transition
    setTimeout(() => {
        currentCard.remove();
    },300);
    // update index of remaining cards
    for (let i = 0; i < cards.length; i++) {
        cards[i].dataset.index = i.toString();
    } 
    // if no cards left, retrieve new cards
    if (cards.length === 0) {
        console.log('retrieve new cards')
        // htmx.ajax('GET', `/property/get-explore-controls/${nextCard.id}/`, {target:'#explore-controls', swap:'outerHTML'})
        return
    }
    // increment index
    let nextIndex = activeIndex <= cards.length - 1 ? activeIndex : 0;
    // get and display next card
    const nextCard: HTMLElement | null  = document.querySelector(`[data-index="${nextIndex}"]`);
    if (!nextCard) {
        return
    }
    nextCard.dataset.status = "becoming-active-from-right";
    setTimeout(() => {
        nextCard.dataset.status = "active";
        activeIndex = nextIndex;
    }, 100);   
    
    const currentMapMarker: HTMLElement | null = document.getElementById(`marker-div-${currentCard.id}`)
    if (currentMapMarker) {
        currentMapMarker.remove();
    }
    const nextMapMarker: HTMLElement | null = document.getElementById(`marker-div-${nextCard.id}`)
    if (nextMapMarker) {
        nextMapMarker.dataset.focused = "true";
    }

    setImageAtIndex(nextIndex + 1);
}

function toggleMapView() {
    const mapContainer: HTMLElement = document.getElementById("map-container")!;
    // const swipingComponent = document.getElementById("swiping-component");
    mapContainer.dataset.visible = mapContainer.dataset.visible === "false" ? "true" : "false";
    // swipingComponent.style.display = swipingComponent.style.display === "none" ? "block" : "none";
}

function submitSearch(event) {
    event.preventDefault();
    const searchInput = document.getElementById('location-search')! as HTMLInputElement;
    const searchStr: string = searchInput.value;
    if (searchStr === '') {
        return;
    }
    window.location.replace(`/explore/search=${searchStr}`)
}

const searchButton = document.getElementById('search-button')!;
searchButton.addEventListener("click", submitSearch, false);

function initialize() {
    new google.maps.places.Autocomplete(searchInput);
}
const searchInput = document.getElementById('location-search')! as HTMLInputElement;
searchInput.addEventListener('keypress', initialize);