// Example: Button click to open alert or redirect
document.addEventListener("DOMContentLoaded", function () {
    const speechBtn = document.querySelector("#speech-btn");
    const marsBtn = document.querySelector("#mars-btn");
    const playgroundBtn = document.querySelector("#playground-btn");
  
    speechBtn.addEventListener("click", function () {
      alert("Redirecting to Image-Based Speech App...");
      // window.location.href = "https://demospeechapp.com";
    });
  
    marsBtn.addEventListener("click", function () {
      alert("Redirecting to MARS Dashboard...");
      // window.location.href = "https://demomarsdash.com";
    });
  
    playgroundBtn.addEventListener("click", function () {
      alert("Opening Coding Playground...");
      // window.location.href = "https://demoplayground.com";
    });
  });
  