document.addEventListener("DOMContentLoaded", function () {
  // activate Bootstrap5 tooltips
  let tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  let tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  /**
     * getCookie takes 1 argument and is from the Django docs to deal with CSRF token.
     * https://docs.djangoproject.com/en/4.0/ref/csrf/
     */
  const getCookie = name => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        //  Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  };

  // Define Global Variables
  let csrftoken = getCookie("csrftoken");
  let togglers = document.getElementsByClassName("caret");
  let volume = document.querySelector("#volume");
  let credits = document.querySelector("#credits-left");
  let allInTitle = document.querySelector("#all-in-title");
  let goldenRatio = document.querySelector("#golden-ratio");

  for (let i = 0; i < togglers.length; i++) {
    togglers[i].addEventListener("click", function () {
      this.parentElement.querySelector(".nested").classList.toggle("active");
      this.classList.toggle("caret-down");
    });
  }

  // Listen for kw competition search
  if (document.querySelector("#kw-comp-search")) {
    document.querySelector("#kw-comp-search").addEventListener("submit", event => searchKeywordComp(event));
  }

  /**
     * searchKeywordComp passes a keyword to the check_keyword view which then
     * queries the Keywords Everywhere API. It takes the return response and
     * populates the goldenRatio div area underneath the search bar on the
     * cat-details.html page.
     */
  const searchKeywordComp = event => {
    // Prevent form submission
    event.preventDefault();

    // Get information from the form
    const keyword = document.querySelector("#kw-comp-input").value;

    // Convert submission via API and send to database
    fetch("/check-keyword", {
      method: "POST",
      headers: {
        "X-CSRFToken": csrftoken
      },
      mode: "same-origin", // Do not send CSRF token to another domain.
      body: JSON.stringify({keyword: keyword})
    }).then(response => {
      // check response and handle errors
      if (response.ok) {
        return response.json();
      }
      return Promise.reject(response);
    }).then(result => {
      // fill in the result divs
      credits.innerHTML = `Credits Remaining: ${result.credits_left}`;
      allInTitle.innerHTML = `All In Title Vol: ${result.all_in_title}`;

      if (result.zero_volume > 0) {
        volume.classList.add("text-danger");
        // I couldn't figure out how to add the tooltip to the innerHTML a
        // different way. I don't like this either.
        volume.innerHTML = `Volume: ${result.zero_volume} <i id="volume-explainer" 
          class="ms-1 .fs-6 fa-solid fa-circle-question" 
          data-bs-toggle="tooltip text-danger" data-bs-placement="right" 
          title="Volume for this search returned 0. 
          Since you can't divide by 0, the equation substitutes allintitle 
          results * 3 for volume. This is a niche worth looking at with more
          research."></i>`;
      } else {
        if (volume.classList.contains("text-danger")) {
          volume.classList.remove("text-danger");
        }
        volume.innerHTML = `Volume: ${result.true_volume}`;
      }

      // style the golden ratio so it's easy to know if this is a good kw or not
      if (goldenRatio.classList.contains("text-danger")) {
        goldenRatio.classList.remove("text-danger");
      }
      if (goldenRatio.classList.contains("text-warning")) {
        goldenRatio.classList.remove("text-warning");
      }
      if (result.golden_ratio > 1) {
        goldenRatio.classList.add("text-danger");
      } else if (result.golden_ratio >= 0.25) {
        goldenRatio.classList.add("text-warning");
      } else if (result.golden_ratio < 0.25) {
        goldenRatio.classList.add("text-success");
      }

      // If your Keywords Everywhere Credit Balance is below 100, change color
      if (result.credits_left < 100) {
        credits.classList.add("text-danger");
      }

      // return the properly styled golden ratio result
      goldenRatio.innerHTML = `Golden Ratio: ${result.golden_ratio}`;
    }).catch(response => {
      console.log(response.status, response.statusText);
      // 3. get error messages, if any
      response.json().then(res => {
        console.log(res);
        kwErr = document.querySelector("#kw-error");
        kwErr.innerHTML = '<div class="alert alert-danger alert-dismissible fade show " id="kw-error" role="alert"><li class="error-msg">Invalid Search Query</li><button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>';
        volume.innerHTML = "";
        allInTitle.innerHTML = "";
        goldenRatio.innerHTML = "";
        credits.innerHTML = "";
      });
    });

    return false;
  };
});
