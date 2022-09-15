async function sendLike(event) {
    event.preventDefault();
    let target = event.target;
    let url = target.href;
    let response = await fetch(url);
    let response_json = await response.json()
    let count = response_json.count
    console.log(count)

    if (target.innerText === "Dislike") {
        target.innerText = "Like";
    } else {
        target.innerText = "Dislike";
    }
}


function onLoadFunc(){
    let likes = document.getElementsByClassName("likes");

    for (let i=0;i<likes.length;i++) {
        likes[i].addEventListener("click", sendLike)
    }
}

window.addEventListener("load", onLoadFunc);
