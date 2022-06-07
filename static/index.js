// try {
//   document.getElementById("Search").onclick = function () {
//     console.log([
//         document.getElementById("movie1").value,
//         document.getElementById("movie2").value,
//         document.getElementById("movie3").value,
//     ])
//   };
// } catch (e) {

// }

// try {
//   document.getElementById("Search").onclick = function () {
//     console.log([
//         document.getElementById("actor1").value,
//         document.getElementById("actor2").value,
//         document.getElementById("actor3").value,
//     ])
//   };
// } catch (e) {

// }

// try {
//   document.getElementById("Search").onclick = function () {
//     console.log(
//         [document.getElementById("movie1").value,document.getElementById("movie2")?.value,document.getElementById("movie3")?.value]
//     )
//   };
// } catch (e) {

// }


function GoMovies() {
  window.location.href = 'moviesearch';
}

function GoActors() {
  window.location.href = 'ActorSearch.html';
}

function GoCustomSearch() {
  window.location.href = 'GoCustomSearch.html';

}

function GetMovie(div) {
  console.log(div.childNodes[3].innerHTML);
}

function Git() {
  open('https://github.com/tameemalaa/towatch-recommender')
}

function Doc() {
  open('/docs');
}

var Data = {movies: []};


function handleChange(input) {
  var suggest_list=input.parentElement.getElementsByClassName("suggest-list")[0]
  if (Data.movies.includes(input.value)) {
    document.getElementById("Search").disabled=false
  } else{
    document.getElementById("Search").disabled=true
  }

  fetch('/movieupdate?input=' + input.value, {method: "POST", })
  .then(response => response.json())
  .then(data=>{
    Data = data;
    suggest_list.innerHTML=data.movies.map(m=>`<li class="dropdown-item" onclick="handleClick(this)">${m}</li>`).join('')
  })
}

function handleChangeActor(input) {
  var suggest_list=input.parentElement.getElementsByClassName("suggest-list")[0]
  if (Data.movies.includes(input.value)) {
    document.getElementById("Search").disabled=false
  } else{
    document.getElementById("Search").disabled=true
  }

  fetch('/movieupdate?input=' + input.value, {method: "POST", })
  .then(response => response.json())
  .then(data=>{
    Data = data;
    suggest_list.innerHTML=data.movies.map(m=>`<li class="dropdown-item" onclick="handleClick(this)">${m}</li>`).join('')
  })
}

function handleClick(li) {
  var ul=li.parentElement
  var input=ul.parentElement.parentElement.getElementsByTagName("input")[0]
  ul.style.display="none"
  input.value=li.innerHTML

  if (Data.movies.includes(input.value)) {
    document.getElementById("Search").disabled=false
  }
  // console.log(input)
}



function handleFocus(input,isfocused){
  var suggest_list=input.parentElement.getElementsByClassName("suggest-list")[0]
  if(isfocused){
    suggest_list.style.display="block"
  }else{
    setTimeout(function(){
      suggest_list.style.display="none"
    },150)
  }
}

function SingleSearch() {
  open('/recommend?input=' + document.getElementById("movie1").value, "_self")
  
}

function TripleSearch() {
  open(`/recommends?movie=${document.getElementById('movie1').value},${document.getElementById('movie2').value},${document.getElementById('movie3').value}`, "_self")
}