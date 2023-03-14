const notes = {
    //frequency in hz for each note in hz
    C4: 261.63,
    D4: 293.66,
    E4: 329.63,
    F4: 349.23,
    G4: 392.00,
    A4: 440.00,
    B4: 493.88,
    C5: 523.25,
    D5: 587.33,
    E5: 622.25,
    F5: 698.46,
    G5: 783.99
};

const notesSequence = []; //array to store the sequence of notes

const buttonsDiv = document.getElementById("buttons");
for (const note in notes) {
    const button = document.createElement("button");//for each note, make a button
    button.innerText = note; //make the text inside the button text
    buttonsDiv.appendChild(button);//append this to the button div
    button.addEventListener("click", () => {//upon pressing play, play the note
        playSound(notes[note]);
        notesSequence.push(note); // add the note to the sequence so it can be played later
    });
}

const playButton = document.createElement("button");//for playing the sounds altogether
playButton.innerText = "Play";
playButton.addEventListener("click", () => {
    playNotesSequence(notesSequence);//play the sequence of notes if this button is pressed
});
buttonsDiv.appendChild(playButton);

function playSound(frequency) {
    //creates a new AudioContext object, checks if the window object has an AudioContext property and 
    //if its not windows we can fall back on webkit
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    //generate a waveform at a frequency to play
    const oscillator = audioCtx.createOscillator();
    //used to control volume of an audio signal. multiplies input signal by a factor provided
    const gainNode = audioCtx.createGain();
    //volume of audio signal/gain value output goes in here
    oscillator.connect(gainNode);
    //in order to listen you give it a destination to listen through your headphones
    gainNode.connect(audioCtx.destination);
    //a triangle wave with a linear increase and decrease in amplitude
    oscillator.type = "triangle";
    //use the frequency we provide it
    oscillator.frequency.value = frequency;
    //set inital gain value to 1 (anything more makes it suuuuper pitchy)
    gainNode.gain.setValueAtTime(1, audioCtx.currentTime);
    //start the oscillating
    oscillator.start();
    //goes down to a very low volume (0.001) and only lasts 0.7s
    //make it zero and it lasts freakin forever
    gainNode.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 0.7);
    //when should the oscillator actually stop running? in 0.7s seconds
    oscillator.stop(audioCtx.currentTime + 0.7);
}

function playNotesSequence(notesSequence) {
    let currentTime = 0;
    notesSequence.forEach(note => {
        setTimeout(() => {
            playSound(notes[note]);//play each note every
        }, currentTime * 700);//each note plays 0.7seconds
        currentTime += 0.5;//play next note with a delay of a half a second
    });
    notesSequence.length = 0 //reset sequence to nothing so dude can put new notes in
}
