document
  .getElementById("messageForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    const message = document.getElementById("message").value;

    fetch("/message", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: message }),
    })
      .then((response) => response.blob())
      .then((data) => {
        const audioPlayer = document.getElementById("audioPlayer");
        audioPlayer.src = URL.createObjectURL(data);
        audioPlayer.play();
      });
  });
