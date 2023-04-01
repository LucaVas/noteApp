// function which filters notes by tag selected
function filterNotesByTag(e) {

    const tags = document.querySelectorAll(".nav-tag-item");
    const notes = document.querySelectorAll('.notes');

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
        //
    } 
    else {
        for (let i = 0; i < notes.length; i++) {

            if (notes[i].firstElementChild.childNodes[3].value != eventTarget.children[0].innerText) {
                notes[i].style.display = "none";
            }
        }
    }

    eventTarget.children[0].style.backgroundColor = "";



};

function filterByInput(e) {
    
    const notes = document.querySelectorAll('.notes');
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
};

function disableButtons() {

    if (!document.querySelector("#current-note-id").value) {

        // disable save and delete buttons when note is not yet saved (first note)
        footerButtons = document.querySelectorAll(".note-section-footer-btn");
        footerButtons.forEach(element => {
            element.disabled = true;
            element.style.backgroundColor = "grey";
        });
    }


}

function enableButtons(e) {

    disableButtons();

    // loop through elements of the form
    titleLength = document.querySelector("#note-title").value.length;
    tagLength = document.querySelector("#note-tag").value.length;
    textLength = document.querySelector(".note-text_bottom").innerHTML.length;
    
    if (titleLength < 1 || tagLength < 1 || textLength < 1) {
        // do nothing
    } else {
        footerButtons.forEach(element => {
            element.disabled = false;
            element.style.backgroundColor = "rgb(232, 197, 71)";
        });
    }
};

function removeButtonsFromDeletedNotes() {
    const notes = document.querySelectorAll('.notes');
    
    // remove delete button
    for (i = 0; i < notes.length; i++) {
        if (notes[i].firstElementChild.childNodes[5].value === "deleted") {
            notes[i].querySelector(".delete-note-btn").style.display = "none";
            notes[i].querySelector("#scroll-bar-note-edit-icon").style.display = "none";
            notes[i].querySelector("#mobile-scroll-bar-note-edit-icon").style.display = "none";
        }
    }
}

function makeBold(e) {
    const strongElement = document.createElement("strong");
    const userSelection = window.getSelection();
    const selectedTextRange = userSelection.getRangeAt(0);
    console.log(selectedTextRange)
    selectedTextRange.surroundContents(strongElement);

    e.preventDefault();
}

function makeItalic(e) {
    const strongElement = document.createElement("em");
    const userSelection = window.getSelection();
    const selectedTextRange = userSelection.getRangeAt(0);
    selectedTextRange.surroundContents(strongElement);

    e.preventDefault();
}

function makeStrikedthrough(e) {
    const strongElement = document.createElement("s");
    const userSelection = window.getSelection();
    const selectedTextRange = userSelection.getRangeAt(0);
    selectedTextRange.surroundContents(strongElement);

    e.preventDefault();
}

function makeUnderlined(e) {
    const strongElement = document.createElement("u");
    const userSelection = window.getSelection();
    const selectedTextRange = userSelection.getRangeAt(0);
    selectedTextRange.surroundContents(strongElement);

    e.preventDefault();
}

function openNote() {

    const textArea = document.querySelector(".note-text")


    if (!textArea.style.display || textArea.style.display == 'none') {
        document.querySelector(".note-text").style.display = 'block'
    } else{
        document.querySelector(".note-text").style.display = 'none'
    } 
}

function editNote(e) {
    const note = e.target.parentElement.parentElement;
    const scrollId = note.querySelector("#scroll-bar-note-id").value
    const scrollTitle = note.querySelector(".scroll-bar-note-title").innerHTML
    const scrollText = note.querySelector(".scroll-bar-note-description").innerHTML
    const scrollTag = note.querySelector(".scroll-bar-note-tag").innerHTML
    
    eraseNote()
        
    const id = document.querySelector("#current-note-id")
    const title = document.querySelector("#note-title")
    const tag = document.querySelector("#note-tag")
    const textValue = document.querySelector("#note-text-bottom-hidden")
    const textContent = document.querySelector(".note-text_bottom")

    id.setAttribute("value", scrollId)
    title.setAttribute("placeholder", scrollTitle)
    tag.setAttribute("placeholder", scrollTag)
    textValue.setAttribute("value", scrollText)
    
    textContent.innerHTML = scrollText

    footerButtons = document.querySelectorAll(".note-section-footer-btn");
    footerButtons.forEach(element => {
        element.disabled = false;
        element.style.backgroundColor = "rgb(232, 197, 71)";
    });

    openNote()

}

function closeNote() {
    document.querySelector(".note-text").style.display = 'none'
}

function eraseNote() {
    const id = document.querySelector("#current-note-id")
    const title = document.querySelector("#note-title")
    const tag = document.querySelector("#note-tag")
    const textValue = document.querySelector("#note-text-bottom-hidden")
    const textContent = document.querySelector(".note-text_bottom")

    id.setAttribute("value", "")
    title.setAttribute("placeholder", "")
    tag.setAttribute("placeholder", "")
    textValue.setAttribute("value", "")
    if (textContent.firstElementChild) {
        textContent.removeChild(textContent.firstElementChild);
    } 
    textContent.innerHTML = ""
    
}

function createNewNote() {

    eraseNote()
    const textArea = document.querySelector(".note-text")

    if (!textArea.style.display || textArea.style.display == 'none') {
        document.querySelector(".note-text").style.display = 'block'
    } else{
        document.querySelector(".note-text").style.display = 'none'
    } 

}

function removeFlash(flash) {
    flash.parentElement.remove()
}


document.addEventListener("DOMContentLoaded", function() {
    const notes = document.querySelectorAll('.notes');
    const tags = document.querySelectorAll(".nav-tag-item");
    
    // apply event listener to all tags
    for (let i = 0; i < tags.length; i++) {
        tags[i].addEventListener("click", filterNotesByTag);
    }

    removeButtonsFromDeletedNotes();

    document.querySelector("#scroll-bar-note-delete-icon").onclick = removeButtonsFromDeletedNotes;
    document.querySelector(".delete-note-btn").onclick = removeButtonsFromDeletedNotes;


    // change color of note if archived or deleted
    for (i = 0; i < notes.length; i++) {
        if (notes[i].firstElementChild.childNodes[5].value == "deleted") {
            notes[i].style.backgroundColor = "rgba(255, 0, 0, 0.308)";
        }
        else if (notes[i].firstElementChild.childNodes[5].value == "archived") {
            notes[i].style.backgroundColor = "rgba(232, 197, 71, 0.286)";
        }
    }

    // add to textarea an even listener which adds the content to the hidden input
    document.addEventListener("mousemove", () => {
        let text = document.querySelector(".note-text_bottom").innerHTML;
        document.querySelector("#note-text-bottom-hidden").value = text;
    });

    // filter notes by input
    document.querySelector("#input-search").onkeyup = filterByInput;

    
    // disable/enable save and delete buttons when note is not yet saved (first note)
    disableButtons();
    document.querySelector("#note-text-form").onkeyup = enableButtons;

    

    document.querySelector("#bold-icon").onclick = makeBold;
    document.querySelector("#italic-icon").onclick = makeItalic;
    document.querySelector("#strikethrough-icon").onclick = makeStrikedthrough;
    document.querySelector("#underline-icon").onclick = makeUnderlined;

    const burgerMenu = document.querySelector('.burger-menu');
    burgerMenu.addEventListener('click', () => {
        const isOpened = burgerMenu.getAttribute('aria-expanded');

        if (isOpened == 'false') {
            burgerMenu.setAttribute('aria-expanded', 'true')
            document.querySelector('#primary-navigation').style.display = 'flex';
            document.querySelector(".scroll_bar").style.opacity = 0.5;
        } else {
            burgerMenu.setAttribute('aria-expanded', 'false')
            document.querySelector('#primary-navigation').style.display = 'none';
            document.querySelector(".scroll_bar").style.opacity = 1;
        }
    });
    
    
    const mobileEditNoteBtns = document.querySelectorAll("#mobile-scroll-bar-note-edit-icon")
    mobileEditNoteBtns.forEach(element => {
        element.addEventListener("click", editNote);
    });
     

    // button which opens a new note (mobile & tablet)
    const navNewNote = document.querySelector(".nav-new-note");
    const tabletNewNote = document.querySelector(".tablet-nav-new-note")
    navNewNote.addEventListener("click", createNewNote);  
    tabletNewNote.addEventListener("click", createNewNote);  

    
    // button which closes the new note (mobile & table)
    const closeNoteBtn = document.querySelector("#close-note");
    closeNoteBtn.addEventListener("click", closeNote);

});