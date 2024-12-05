document.addEventListener("DOMContentLoaded", function () {
  // get search params from URL
  const urlParams = new URLSearchParams(window.location.search);

  // get the first_name from the URL
  const first_name = urlParams.get("first_name");

  // set the first_name to the span with class name
  document.querySelector("span.name").textContent = first_name;

  // gotosuccess function
  document.provider_listing.addEventListener("submit", (e) => {
    e.preventDefault();

    // redirect to success.html
    window.location.href = `success.html?first_name=${first_name}`;
  });
});
