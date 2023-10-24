/**
* Likes or unlikes a post. This is called by ajax to update the likes count and button
* 
* parameter postId - The id of the post
*/
function like(postId) {
    const likeCount = document.getElementById(`likes-count-${postId}`);
    const likeButton = document.getElementById(`like-button-${postId}`);
  
    fetch(`/like-post/${postId}`, { method: "POST" })
      .then((res) => res.json())
      .then((data) => {
        likeCount.innerHTML = data["likes"];
        // If liked is true then the button is shown as a button.
        if (data["liked"] === true) {
          likeButton.className = "fas fa-thumbs-up";
        } else {
          likeButton.className = "far fa-thumbs-up";
        }
      })
      .catch((e) => alert("Could not like post."));
  }

new SimpleLightbox({
  elements: '#portfolio a.portfolio-box'
});