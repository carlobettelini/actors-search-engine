<template>
    <body>
        <div id="header">
            <img alt="Vue logo" src="../assets/art-computer-magnifying-glass-anime.png">
            <div id="lateral">
                <h2>Information Retrieval Project</h2>
                <h1>Course Project N.05: A Hollywood Actors Search Engine</h1>
                <h3>Carlo Bettelini</h3>
            </div>
        </div>
        <br>
        <br>
        <div class="searchBar">
            <p>Search for an actor using their name, their movies, their birthplace, anything really...</p>
            <br>
            <div id="searchContainer">
            <form v-on:submit.prevent="onSubmit">
                <input type="text" placeholder="Search..." name="search">
                <button type="submit">Submit</button>
            </form>
            </div>
        </div>
        <div id="results"></div>
    </body>
</template>

<script>
export default {
    name: 'HelloWorld',

    props: {
        msg: String
    },

    methods: {

        async onSubmit(evt) {
            var myHeaders = new Headers();
            myHeaders.append("Accept", "application/json");
            myHeaders.append("Content-Type", "application/x-www-form-urlencoded");
            var requestOptions = {
                method: 'GET',
                headers: myHeaders,
                redirect: 'follow'
            };

            var searchValue = evt.target.elements.search.value;
            // how many words are being searched
            var nmb = searchValue.split(" ").length;
            // If we have a multiple word query, we bake in the %20 symbol as separator
            var query = nmb < 2 ? `http://localhost:8983/solr/actors/query?q=${searchValue}` : `http://localhost:8983/solr/actors/query?q=${searchValue.replace(/\s/g, "%20")}`;
        
            var datas;

            // Fetch datas using the query
            await fetch(query, requestOptions)
                .then(response => response.json())
                .then(result => {
                    console.log(result);
                    datas = result.response.docs;
                })
                .catch(error => console.log('error', error));

            // datas is array of results
            var div = document.querySelector('#results');

            // Snippet is gonna contain the results in a google style way.
            var snippet = '<ul>';

            var that = searchValue.split(" "); // searched value

            var names = []; // to not repeat names, we store them here

            // Iterating through results that are not already been posted
            for (let element in datas) {
                if (names.includes(datas[element].name)) continue;
                // Each result is an object with different fields like 
                // name, biography, birhtdate, birthplace,...
                for (const item in datas[element]) 
                {
                    // Skip these fields
                    if (item == "link" || item == "_text_" || item == "id" || item == "_root_" || item == "_version_") continue;

                    // if acting, writing, or directing
                    // iterate through corresponding array
                    if (item.includes("acting")||item.includes("writing")||item.includes("directing"))
                    {
                        var movies = datas[element][item];
                        for (let i=0; i<movies.length; i++)
                        {
                            // console.log("this could be the error: ", movies[i]);
                            var arr = String(movies[i]).split(" "); // current movie being checked
                        
                            arr.forEach(function (value, index, array) {
                                for (var i = 0; i < this.length; i++) {
                                    // This checks if the searched words appear
                                    // in the current field
                                    // It is necessary to make everything lowercase for a correct match
                                    if (value.toLowerCase().indexOf(this[i].toLowerCase()) != -1) {
                                        // if we already found the searched word in a field we skip
                                        if (names.includes(datas[element].name)) continue;
                                        names.push(datas[element].name); // insert this element into array
                                        // Prints words before and after matched results
                                        // If there are no words before, starts from matched result
                                        var crtIndex = index-4 >= 0 ? index-4 : index;
                                        var relevantWords = "";
                                        // There are not enough words, so we print the field instead
                                        if (arr.length < 4) {
                                            let field = item.split(".")[0];
                                            // Capitalize first letter of field
                                            const capField = field.charAt(0).toUpperCase() + field.slice(1);
                                            relevantWords += `${capField}: `;
                                            for (let g=0;g<array.length;g++) {
                                                // Matching word, we make it bold
                                                if (crtIndex == index) relevantWords += `<b>${array[crtIndex++]}</b> `;
                                                else if (array[crtIndex]) relevantWords += `${array[crtIndex++]} `;
                                            }
                                        }
                                        else 
                                        {
                                            for (let g=0;g<8;g++) {
                                                // Matching word, we make it bold
                                                if (crtIndex == index) relevantWords += `<b>${array[crtIndex++]}</b> `;
                                                // We check if there's a word
                                                else if (array[crtIndex]) relevantWords += `${array[crtIndex++]} `;
                                            }
                                        }
                                        // Add words to the snippet
                                        snippet += `<li><p><i>${datas[element].link}</i></p><br>
                                                    <a href=${datas[element].link} target="_blank"><h5><p>${datas[element].name}</p></h5></a><br> 
                                                    <p>${relevantWords}</p></li>`;
                                    }
                                }
                            }, that);
                        }
                        continue;   // skip to the next since we already know it s either
                                    // acting, directing or writing
                    }

                    arr = datas[element][item].split(" ");
                    
                    // otherwise, scan the corresponding string
                    arr.forEach(function (value, index, array) {
                        for (var i = 0; i < this.length; i++) {
                            // This checks if the searched words appear
                            // in the current field
                            // It is necessary to make everything lowercase for comparison
                            if (value.toLowerCase().indexOf(this[i].toLowerCase()) != -1) {
                                // if we already found the searched word in a field we skip
                                if (names.includes(datas[element].name)) continue;
                                names.push(datas[element].name); // insert this element into array
                                // Prints words before and after matched results
                                // If there are no words before, starts from matched result
                                var crtIndex = index-4 >= 0 ? index-4 : index;
                                var relevantWords = "";
                                // There are not enough words, so we print the field instead
                                if (arr.length < 4) {
                                    let field = item.split(".")[0];
                                    // Capitalize first letter of field
                                    const capField = field.charAt(0).toUpperCase() + field.slice(1);
                                    relevantWords += `${capField}: `;
                                    for (let g=0;g<array.length;g++) {
                                        if (crtIndex == index) relevantWords += `<b>${array[crtIndex++]}</b> `;
                                        else if (array[crtIndex]) relevantWords += `${array[crtIndex++]} `;
                                    }
                                } else {
                                    for (let g=0;g<8;g++) {
                                        if (crtIndex == index) relevantWords += `<b>${array[crtIndex++]}</b> `;
                                        else if (array[crtIndex]) relevantWords += `${array[crtIndex++]} `;
                                    }
                                }
                                 // Add words to the snippet
                                snippet += `<li><p><i>${datas[element].link}</i></p><br>
                                            <a href=${datas[element].link} target="_blank"><h5><p>${datas[element].name}</p></h5></a><br> 
                                            <p>${relevantWords}</p></li>`;
                            }
                        }
                    }, that);
                }
            }

            snippet += "</ul>";

            // We didn t find any result
            if (names.length == 0) {
                snippet = "<br><br><br><p>No results were found</p>";
            }

            div.innerHTML = snippet.trim();
        }
    }
    }
    </script>

    <!-- Add "scoped" attribute to limit CSS to this component only -->
    <style scoped>
    </style>