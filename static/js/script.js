// script that filters notes based on the tag clicked

const tags = document.querySelectorAll(".nav-tag-item");
const notes = document.querySelectorAll('.notes');

// function which filters notes by tag selected
function filterNotesByTag(e) {

    eventTarget = e.target;

    if (e.target.className == "navbar-tag") {
        eventTarget = e.target.parentElement;
    }


    // remove background from any parent element
    for (let i = 0; i < tags.length; i++) {
        tags[i].style.backgroundColor = "";
    }

    // make all notes visible
    for (let i = 0; i < notes.length; i++) {
        if (notes[i].firstElementChild.childNodes[5].value == "active") {
            notes[i].style.display = "flex";
        }
    }

    eventTarget.style.backgroundColor = "white";

    if (eventTarget.innerText == "Show All") {
        console.log(eventTarget.innerText);
    } 
    else {
        for (let i = 0; i < notes.length; i++) {

            if (notes[i].firstElementChild.childNodes[3].value != eventTarget.children[0].innerText) {
                notes[i].style.display = "none";
            }
        }
    }

    eventTarget.children[0].style.backgroundColor = "";



}

function filterByInput(e) {
    filter = e.target.value.toLowerCase();

    // make all notes visible
    for (z = 0; z < notes.length; z++) {
        notes[z].style.display = "flex";
    }

    // loop through each note
    for (i = 0; i < notes.length; i++) {

        noteStatus = notes[i].querySelector(".scroll-bar-note-header").children[2].value;
        title = notes[i].querySelector(".scroll-bar-note-title").innerHTML.toLowerCase();
        description = notes[i].querySelector(".scroll-bar-note-description").innerHTML.toLowerCase();

        // check if input value is included in title or description
        if (title.includes(filter) || description.includes(filter)) {
            // do nothing
        } else {
            // hide note
            notes[i].style.display = "none";
        }
    }
}

document.addEventListener("DOMContentLoaded", function() {
    // apply event listener to all tags
    for (let i = 0; i < tags.length; i++) {
        tags[i].addEventListener("click", filterNotesByTag);
    }


    // change color of note if archived or deleted
    for (i = 0; i < notes.length; i++) {
        if (notes[i].firstElementChild.childNodes[5].value == "deleted") {
            notes[i].style.backgroundColor = "rgba(255, 0, 0, 0.308)";
        }
        else if (notes[i].firstElementChild.childNodes[5].value == "archived") {
            notes[i].style.backgroundColor = "rgba(232, 197, 71, 0.286)";
        }
    }

    // remove delete button
    for (i = 0; i < notes.length; i++) {
        if (notes[i].firstElementChild.childNodes[5].value == "deleted") {
            document.querySelector(".delete-note-btn").style.display = "none";
            document.querySelector("#scroll-bar-note-edit-icon").style.display = "none";
        }
    }

    // filter notes by input
    document.querySelector("#input-search").onkeyup = filterByInput;
    }
);