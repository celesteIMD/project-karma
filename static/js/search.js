const searchBar = document.getElementById("searchBar");
const searchCardTemplate = document.querySelector("[search-card-template]");
const dropdown = document.getElementById("searchDropdown");

let searchCards = [];
searchBar.addEventListener('focus', (e) =>{
    dropdown.style.display = "block";
})
document.addEventListener('click', (e)=>{
    if(!searchBar.contains(e.target) && !dropdown.contains(e.target)){
        dropdown.style.display = "none";
    }
})
searchBar.addEventListener('input', (e) => {
    const currentSearch = e.target.value.toLowerCase()
    searchCards.forEach(card => {
        const isVisible = card.title.toLowerCase().includes(currentSearch)
        card.element.classList.toggle("hide", !isVisible)
    })
})
let url = `/api/searchData`
fetch(url, {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
})
.then(response => {
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
})
.then(data => {
    const roomCards = data.Rooms.map(room => {
        const card = searchCardTemplate.content.cloneNode(true)
        const outerCard = card.querySelector("[search-card]")
        const title = card.querySelector("[search-title]")
        outerCard.href = `/room/${room.id}`
        title.textContent = `${room.title}`
        dropdown.append(card)
        return { title: room.title, element : outerCard }
    });

    const buildingCards = data.Buildings.map(building =>{
        const card = searchCardTemplate.content.cloneNode(true)
        const outerCard = card.querySelector("[search-card]")
        const title = card.querySelector("[search-title]")
        outerCard.href = `/building/${building.id}`
        dropdown.append(card)
        title.textContent = `${building.title}`
        return { title: building.title, element : outerCard }
    });
    searchCards = [...roomCards, ...buildingCards];
})
.catch(error => {
    console.error('There was a problem with the fetch operation:', error);
});
