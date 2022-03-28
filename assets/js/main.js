init();
async function init() {
  document.querySelector("#tweets").innerHTML = "";
  const tweets = await getTweets();
  tweets.forEach((tweet) => {
    displayTweet(tweet, false);
  });
}

async function getTweets() {
  const conn = await fetch("/tweets", {
    method: "GET",
  });
  if (!conn.ok) {
    const error = await conn.json();
    console.log(conn);
    console.log(error);
    return;
  }

  const tweets = await conn.json();
  return tweets;
}

//
//
// DISPLAY TWEET
function displayTweet(tweet, appendToTop) {
  // Clone tweet template
  const temp = document.querySelector("#tweet_temp");
  const clone = temp.content.cloneNode(true);

  // Insert values
  clone.querySelector("form").dataset.tweet_id = tweet.tweet_id;
  clone.querySelector("[name='tweet_id']").value = tweet.tweet_id;
  clone.querySelector("[name='tweet_user_id']").value = tweet.tweet_user_id;
  clone.querySelector(".user_icon").textContent = tweet.user_tag[0];
  clone.querySelector(".user_name").textContent = `${tweet.user_first_name} ${tweet.user_last_name}`;
  clone.querySelector(".user_tag").textContent = `@${tweet.user_tag}`;
  clone.querySelector(".created_ago").textContent = epochToTime(tweet.tweet_created_at);
  clone.querySelector(".tweet_text").textContent = tweet.tweet_text;

  // If have image
  if (tweet.tweet_image) {
    const tweet_image = document.createElement("img");
    tweet_image.src = `images/${tweet.tweet_image}`;
    clone.querySelector(".tweet_text").after(tweet_image);
  }

  // Session specific functionality
  const session_user_id = document.querySelector("#session_user_id").value;
  console.log(session_user_id);
  console.log(tweet.tweet_user_id);
  console.log(tweet);

  if (!session_user_id) clone.querySelector(".action_bar").hidden = true;

  if (session_user_id == tweet.tweet_user_id) {
    clone.querySelector(".delete_btn").hidden = false;
    clone.querySelector(".edit_btn").hidden = false;
  }

  // Append to container
  const container = document.querySelector("#tweets");
  if (container.querySelector("*") == null || !appendToTop) container.appendChild(clone);
  else container.firstElementChild.before(clone);
}

function epochToTime(tweet_epoch) {
  const current_epoch = (new Date().getTime() / 1000).toFixed();
  const epoch_ago = current_epoch - tweet_epoch;

  // Seconds
  if (epoch_ago < 60) {
    return epoch_ago + "s";
  }
  // Minutes
  if (epoch_ago < 3600) {
    return (epoch_ago / 60).toFixed() + "m";
  }
  // Hours
  if (epoch_ago < 86400) {
    return (epoch_ago / 3600).toFixed() + "h";
  }
  // Days
  if (epoch_ago < 31536000) {
    return (epoch_ago / 86400).toFixed() + "d";
  }
  // Years
  return (epoch_ago / 86400).toFixed() + "y";
}

//
//
// CREATE TWEET
async function postTweet(event) {
  const form = event.target.form;

  const conn = await fetch("/tweets", {
    method: "POST",
    body: new FormData(form),
  });

  if (!conn.ok) {
    const error = await conn.json();
    console.log(conn);
    console.log(error);
    return;
  }
  const tweet = await conn.json();
  console.log(tweet);

  displayTweet(tweet, "top");
}

//
//
// LIKE TWEET
async function likeTweet() {
  alert("This feature is under development :D");
}

//
//
// DELETE TWEET
async function deleteTweet(event) {
  const form = event.target.form;
  const tweetId = form.tweet_id.value;

  const conn = await fetch(`/tweets/${tweetId}`, {
    method: "DELETE",
  });

  if (!conn.ok) {
    console.log(conn);
    alert("Could not delete tweet");
    return;
  }
  const response = await conn.json();
  console.log(response);
  form.remove();
}

//
//
// UPDATE TWEET
function showUpdateTweet(event) {
  // Get tweet id from tweet and pass it to modal
  const form = event.target.form;
  const tweetId = form.tweet_id.value;
  const tweetText = form.querySelector(".tweet_text").textContent;
  document.querySelector("#update_tweet input[name='tweet_id']").value = tweetId;
  // Show modal
  document.querySelector("#update_tweet textarea").value = tweetText;
  document.querySelector("#update_tweet").classList.remove("hide");
}

function hideUpdateTweet() {
  document.querySelector("#update_tweet").classList.add("hide");
  document.querySelector("#update_tweet form").reset();
}

async function updateTweet(event) {
  const form = event.target.form;
  const tweetId = form.tweet_id.value;

  const conn = await fetch(`/tweets/${tweetId}`, {
    method: "PUT",
    body: new FormData(form),
  });

  if (!conn.ok) {
    console.log(conn);
    alert("Could not udpate tweet");
    return;
  }

  const data = await conn.json();

  const tweet = document.querySelector(`[data-tweet_id="${tweetId}"]`);
  tweet.querySelector(".tweet_text").textContent = data.tweet_text;
  const tweetImage = tweet.querySelector("img");

  // Img logic
  if (tweetImage && tweetImage.getAttribute("src") == data.tweet_image) {
    return;
  } else if (data.tweet_image) {
    const newTweetImage = document.createElement("img");
    newTweetImage.src = `/images/${data.tweet_image}`;
    tweet.querySelector(".tweet_text").after(newTweetImage);
  } else if (tweetImage) {
    tweetImage.remove();
  }

  hideUpdateTweet();
}

async function getTweetsByUserId(event) {
  console.log("hej");
  const form = event.target.form;
  const tweet_user_id = form.tweet_user_id.value;

  const conn = await fetch(`/tweets/by-user/${tweet_user_id}`, {
    method: "GET",
  });

  if (!conn.ok) {
    const error = await conn.text();
    console.log(conn);
    console.log(error);
  }

  const tweets = await conn.json();
  document.querySelector("#tweets").innerHTML = "";
  tweets.forEach((tweet) => {
    displayTweet(tweet);
  });
}

// AUTO-RESIZR textareas
function autoResize(event) {
  const elm = event.target;
  elm.style.height = "auto";
  elm.style.height = elm.scrollHeight + 1 + "px";
}
