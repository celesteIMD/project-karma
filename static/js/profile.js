let userUrl = `/api/userReviews`
const reviewCardTemplate = document.querySelector("[review-card-template]");
const reviewsContainer = document.querySelector(".reviews-container")
let reviewCards = []
const reviewSearchBar = document.querySelector(".review-search-bar")
reviewSearchBar.addEventListener('input', (e) =>{
    const currentReviewSearch = e.target.value.toLowerCase()
    reviewCards.forEach(card =>{
        const isVisible = card.title.toLowerCase().includes(currentReviewSearch)
        card.element.classList.toggle("hide", !isVisible)
    })
})
const filterOptions = document.querySelector(".filter-options")
filterOptions.addEventListener("change", (e) =>{
    sortReviews(e.target.value)
})
fetch(userUrl, {
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
    console.log(data)
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

        review.tags.forEach(tag => {
            const tagComp = document.createElement("div")
            tagComp.classList.add("tag")
            tagComp.textContent = tag.name
            tagsContainer.appendChild(tagComp)
            reviewTags.push(tag.name.toLowerCase());
        })
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
    console.error('There was a problem with the fetch operation:', error);
});

function sortReviews(option){
    if(option == "most-recent"){
        reviewCards.sort((a,b) => new Date(b.date) - new Date(a.date))
    }
    else if(option == "oldest"){
        reviewCards.sort((a,b) => new Date(a.date) - new Date(b.date))
    }
    else if (option === "highest-rating") {
        reviewCards.sort((a, b) => b.rating - a.rating);
    }
    else if (option === "lowest-rating") {
        reviewCards.sort((a, b) => a.rating - b.rating);
    }
    reviewsContainer.innerHTML = "";
    reviewCards.forEach(card => reviewsContainer.appendChild(card.element));
}