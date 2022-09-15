async function sendLike(event){
    event.preventDefault();
    let target = event.target;
    let url = target.href;
    let response = await fetch(url);
    let response_json = await response.json();
    let data = target.innerText
    console.log(target.dataset)

    if (target.dataset.articleId) {
        let count = response_json.count;
        console.log(count);
        let articleId = target.dataset.articleId;
        let span = document.getElementById(articleId);
        span.innerText = `${count} Likes`;
        target.innerText = likeDislike(data);
    }

    else if (target.dataset.commentId) {
        let count = response_json.count;
        console.log(count);
        let commentId = target.dataset.commentId;
        let span1 = document.getElementById(commentId);
        span1.innerText = `${count} Likes`;
        target.innerText = likeDislike(data);
    }

    /*if (target.innerText === "Dislike"){
        target.innerText = "Like";
    } else{
        target.innerText = "Dislike";
    }*/
}

function likeDislike(data) {
    if (data === "Dislike") {
        data = "Like";
    } else {
        data = "Dislike";
    }
    return data;
}



function onLoadFunc(){
    let likes = document.getElementsByClassName("likes");
    for (let i=0;i<likes.length;i++) {
        likes[i].addEventListener("click", sendLike)
    }

    let comLikes = document.getElementsByClassName("com_likes");
    for (let i=0;i<comLikes.length;i++) {
        comLikes[i].addEventListener("click", sendLike)
    }
}

window.addEventListener("load", onLoadFunc);
