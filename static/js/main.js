
feather.replace()

/* Set the width of the sidebar to 250px (show it) */
function openNav() {
  document.getElementById("mySidepanel").style.width = "250px";
}

/* Set the width of the sidebar to 0 (hide it) */
function closeNav() {
  document.getElementById("mySidepanel").style.width = "0";
} 


function toggleFilter() {

  let filterBox = document.getElementById("search-filter");
  if (filterBox.style.display === "none" || filterBox.style.display === "") {
    filterBox.style.display = "block";
  } else {
    filterBox.style.display = "none";
  }
} 


function toggleSearch() {

  let searchForm = document.getElementById("mobileSearchForm");
  if (searchForm.style.display === "none" || searchForm.style.display === "") {
    searchForm.style.display = "block";
  } else {
    searchForm.style.display = "none";
  }
} 


