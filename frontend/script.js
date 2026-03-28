function searchPlayer() {
    const name = document.getElementById("playerSearch").value;
    document.getElementById("results").innerHTML = "Searching for: " + name;
}