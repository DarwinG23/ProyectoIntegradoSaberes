function getCharacters(done) {
    fetch("https://rickandmortyapi.com/api/character")
        .then(response => response.json())
        .then(data => {
            done(data);
        })
        .catch(error => {
            console.error("Error fetching data:", error);
        });
}
getCharacters(data => {
    data.results.forEach(personaje => {
        const article = document.createRange().createContextualFragment(/*html*/`
        <article>
        <div class="image-container">
            <img src="${personaje.image}"alt="Personaje">
        </div>
        <h2>${personaje.name}</h2>
        <span>${personaje.status}</span>
    </article>
    `);
   const main = document.querySelector("main");
   main.append(article);
    });
});