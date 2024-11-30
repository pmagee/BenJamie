document.addEventListener("DOMContentLoaded", function() {
    console.log("test.js loaded and running");

    // Get the buttons and product display div
    const listViewBtn = document.getElementById("listViewBtn");
    const gridViewBtn = document.getElementById("gridViewBtn");
    const productDisplayDiv = document.getElementById("product_display_div");

    // Check if the elements exist
    if (listViewBtn && gridViewBtn && productDisplayDiv) {
        console.log("Buttons and product display div found");

        // List View Button Click
        listViewBtn.addEventListener("click", function() {
            console.log("List view clicked");

            // Remove grid-view class, add list-view class
            productDisplayDiv.classList.remove("grid-view");
            productDisplayDiv.classList.add("list-view");

            // Mark the button as active
            listViewBtn.classList.add("active");
            gridViewBtn.classList.remove("active");
        });

        // Grid View Button Click
        gridViewBtn.addEventListener("click", function() {
            console.log("Grid view clicked");

            // Remove list-view class, add grid-view class
            productDisplayDiv.classList.remove("list-view");
            productDisplayDiv.classList.add("grid-view");

            // Mark the button as active
            gridViewBtn.classList.add("active");
            listViewBtn.classList.remove("active");
        });
    }
});









