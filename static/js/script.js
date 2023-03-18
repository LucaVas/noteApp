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




