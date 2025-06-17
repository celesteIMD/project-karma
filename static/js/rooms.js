const pathSegments = window.location.pathname.split("/");
const roomId = pathSegments[pathSegments.length - 1];
const url = `/api/rooms/${roomId}/reviews`
const reviewCardTemplate = document.querySelector("[review-card-template]");
const reviewsContainer = document.querySelector('.reviews-body')
let reviewCards = []
let selectedTags = []
let currentSort;
const photo = document.querySelector(".review-photos");
console.log(photo);
let mappedReviews
let chartData = [0,0,0,0,0]
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
    console.log('Reviews:', data)
    mappedReviews = data.map((review) => review.rating)
    for(let i = 0; i < mappedReviews.length; i++){
        chartData[mappedReviews[i] - 1]++;
    }
    buildChart()
    reviewCards = data.map(review => {
        const card = reviewCardTemplate.content.cloneNode(true)
        const outerCard = card.querySelector("[review-card]")


        const reviewTitle = outerCard.querySelector(".review-title")
        reviewTitle.textContent = review.title;

        const reviewRating = outerCard.querySelector(".review-rating")
        reviewRating.textContent = `${review.rating}/5`

        const reviewContent = outerCard.querySelector(".review-content")
        reviewContent.textContent = review.userReview

        const reviewAuthor = outerCard.querySelector(".review-author")
        reviewAuthor.textContent = review.user

        const datePosted = outerCard.querySelector(".date-posted")
        datePosted.textContent = new Date(review.date).toLocaleDateString()

        const tagsContainer = outerCard.querySelector(".review-tags")
        const reviewTags = [];

        const photoCopy = photo.cloneNode(true)
        reviewContent.appendChild(photoCopy)

        review.tags.forEach(tag => {
            const tagComp = document.createElement("div")
            tagComp.classList.add("tag")
            tagComp.textContent = tag.name
            tagsContainer.appendChild(tagComp)
            reviewTags.push(tag.name.toLowerCase());
        })

        if(review.photos){
            review.photos.forEach(photo =>{
                const img = document.createElement("img");
                img.src = photo.image
                img.classList.add("review-photo")
                photoCopy.appendChild(img)
            })
        }
        reviewsContainer.append(outerCard)
        return {
            title: review.title,
            element: outerCard,
            tags: reviewTags,
            date: review.date,
            rating: review.rating
        }
    })

})
.catch(error => {
    console.error('There was a problem with the fetch operation:', error)
});

const ctx = document.getElementById('myChart');
function buildChart(){
    new Chart(ctx, {
        type: 'bar',
        data: {
          labels: ['1★', '2★', '3★', '4★', '5★'],
          datasets: [{
            label: '# of Votes',
            data: chartData,
            borderWidth: 1
          }]
        },
        options: {
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
    });
}
function sortReviews(){

    let filteredReviews = reviewCards.filter(review => {
        return selectedTags.every(tag => review.tags.includes(tag.toLowerCase()));
    });
    if(currentSort == "most-recent"){
        filteredReviews.sort((a,b) => new Date(b.date) - new Date(a.date))
    }
    else if(currentSort == "oldest"){
        filteredReviews.sort((a,b) => new Date(a.date) - new Date(b.date))
    }
    else if (currentSort === "highest-rating") {
        filteredReviews.sort((a, b) => b.rating - a.rating);
    }
    else if (currentSort === "lowest-rating") {
        filteredReviews.sort((a, b) => a.rating - b.rating);
    }
    reviewsContainer.innerHTML = "";
    filteredReviews.forEach(card => reviewsContainer.appendChild(card.element));
}
const filterOptions = document.querySelector(".filter-options")
filterOptions.addEventListener("change", (e) =>{
    currentSort = e.target.value
    sortReviews()
})
new MultiSelect(document.getElementById('example-multi-select'), {
    placeholder: 'Select options',
    max: 5,  // Maximum number of items that can be selected
    search: true,  // Enable the search box
    selectAll: true,  // Add a select all option
    // onChange: function(value, text, element) {
    //     console.log('Change:', value, text, element);
    // },
    onSelect: function(value, text, element) {
        selectedTags.push(value)
        sortReviews()
    },
    onUnselect: function(value, text, element) {
        selectedTags = selectedTags.filter(tag => tag !== value);
        sortReviews();
    }
});