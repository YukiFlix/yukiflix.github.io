const defaultMovies = Array.from(document.querySelectorAll('#animes-grid-films .movie-card'));
const defaultSeries = Array.from(document.querySelectorAll('#animes-grid-series .movie-card'));

function resetMoviesAndSeries(category) {
    const moviesGrid = document.getElementById(`animes-grid-${category}`);
    const movies = Array.from(moviesGrid.getElementsByClassName('movie-card'));
    const sortedMovies = Array.from(moviesGrid.getElementsByClassName('sorted'));
    sortedMovies.forEach((movie) => moviesGrid.removeChild(movie));
    movies.forEach((movie) => moviesGrid.appendChild(movie));
}

function sortMoviesAndSeries(category, option, sortFunction) {
    const moviesGrid = document.getElementById(`animes-grid-${category}`);
    const movies = Array.from(moviesGrid.getElementsByClassName('movie-card'));
    if (option === 'default') {
        resetMoviesAndSeries(category);
        if (category === 'films') defaultMovies.forEach((movie) => moviesGrid.appendChild(movie));
        else if (category === 'series') defaultSeries.forEach((serie) => moviesGrid.appendChild(serie));
    } else {
        movies.sort(sortFunction);
        resetMoviesAndSeries(category);
        movies.forEach((movie) => {
            movie.classList.add('sorted');
            moviesGrid.appendChild(movie);
        });
    }
}

function sortByRating(a, b) {
    const ratingA = parseFloat(a.querySelector('.rating').dataset.star);
    const ratingB = parseFloat(b.querySelector('.rating').dataset.star);
    return ratingB - ratingA;
}

function sortByTitle(a, b) {
    const titleA = a.querySelector('.card-title').textContent.toLowerCase();
    const titleB = b.querySelector('.card-title').textContent.toLowerCase();
    return titleA.localeCompare(titleB);
}

function setupFilter(category) {
    document.querySelectorAll(`#${category} .filter-options input`).forEach((input) => {
        input.addEventListener('change', function () {
            const option = this.value;
            if (option === 'rating') sortMoviesAndSeries(category, option, sortByRating);
            else if (option === 'alphabetical') sortMoviesAndSeries(category, option, sortByTitle);
            else sortMoviesAndSeries(category, option);
        });
    });
}

// Initialiser les filtres pour les Films et les Séries
setupFilter('films');
setupFilter('series');
