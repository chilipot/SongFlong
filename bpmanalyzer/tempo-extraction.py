#convert mp3 to wav

from pydub import AudioSegment
sound = AudioSegment.from_mp3("\Users\Skyler\Sound-Repo-Thingfile\Avicii.mp3")
sound.export("/Users/Skyler/Sound-Repo-Thingfile/file.wav", format="wav")

#Step 1

/*
This may take several seconds to load depending on bandwidth. 
Once completed it will provide two global arrays: originalBuffer and lowPassBuffer.
*/

function createBuffers(url) {

    // Fetch Audio Track via AJAX with URL
    request = new XMLHttpRequest();
   
    request.open('GET', url, true);
    request.responseType = 'arraybuffer';


    request.onload = function(ajaxResponseBuffer) {

        // Create and Save Original Buffer Audio Context in 'originalBuffer'
        var audioCtx = new AudioContext();
        var songLength = ajaxResponseBuffer.total;

        // Arguments: Channels, Length, Sample Rate
        var offlineCtx = new OfflineAudioContext(1, songLength, 44100);
        source = offlineCtx.createBufferSource();
        var audioData = request.response;
        audioCtx.decodeAudioData(audioData, function(buffer) {

                window.originalBuffer = buffer.getChannelData(0);
                var source = offlineCtx.createBufferSource();
                source.buffer = buffer;

                // Create a Low Pass Filter to Isolate Low End Beat
                var filter = offlineCtx.createBiquadFilter();
                filter.type = "lowpass";
                filter.frequency.value = 140;
                source.connect(filter);
                filter.connect(offlineCtx.destination);
                
                // Schedule start at time 0
                source.start(0);

                // Render this low pass filter data to new Audio Context and Save in 'lowPassBuffer'
                offlineCtx.startRendering().then(function(lowPassAudioBuffer){

                    var audioCtx = new(window.AudioContext || window.webkitAudioContext)(); 
                    var song = audioCtx.createBufferSource(); 
                    song.buffer = lowPassAudioBuffer;
                    song.connect(audioCtx.destination);
                    
                    // Save lowPassBuffer in Global Array
                    window.lowPassBuffer = song.buffer.getChannelData(0);

                    play.onclick = function() {
                        song.start();
                    }

                    console.log("Low Pass Buffer Rendered!");
                });

            },
            function(e) {});
    }
    request.send();
}


createBuffers('https://askmacgyver.com/test/Maroon5-Moves-Like-Jagger-128bpm.mp3');

#step 3


function getClip(length, startTime, data) {

    var clip_length = length * 44100;
    var section = startTime * 44100;
    var newArr = [];

    for (var i = 0; i < clip_length; i++) {
        newArr.push(data[section + i]);
    }

    return newArr;
}

// Overwrite our array buffer to a 10 second clip starting from 00:10 seconds into the song.

window.lowPassFilter = getClip(10, 10, lowPassFilter);

#step 4



function getSampleClip(data, samples) {

    var newArray = [];
    var modulus_coefficient = Math.round(data.length / samples);

    for (var i = 0; i < data.length; i++) {
        if (i % modulus_coefficient == 0) {
            newArray.push(data[i]);
        }
    }
    return newArray;
}

// Overwrite our array to down-sampled array.

lowPassBuffer = getSampleClip(lowPassFilter, 300);

#step 5




function normalizeArray(data) {

    var newArray = [];

    for (var i = 0; i < data.length; i++) {
        newArray.push(Math.abs(Math.round((data[i + 1] - data[i]) * 1000)));
    }

    return newArray;
}

// Overwrite our array to the normalized array
lowPassBuffer = normalizeArray(lowPassBuffer);

#step 6


function countFlatLineGroupings(data) {

    var groupings = 0;
    var newArray = normalizeArray(data);

    function getMax(a) {
        var m = -Infinity,
            i = 0,
            n = a.length;

        for (; i != n; ++i) {
            if (a[i] > m) {
                m = a[i];
            }
        }
        return m;
    }

    function getMin(a) {
        var m = Infinity,
            i = 0,
            n = a.length;

        for (; i != n; ++i) {
            if (a[i] < m) {
                m = a[i];
            }
        }
        return m;
    }

    var max = getMax(newArray);
    var min = getMin(newArray);
    var count = 0;
    var threshold = Math.round((max - min) * 0.2);

    for (var i = 0; i < newArray.length; i++) {

       if (newArray[i] > threshold && newArray[i + 1] < threshold && newArray[i + 2] < threshold && newArray[i + 3] < threshold && newArray[i + 6] < threshold) {
            count++;
        }
    }

    return count;
}

#step 6



var final_tempo = countFlatLineGroupings(lowPassBuffer);

// final_tempo will be 21

final_tempo = final_tempo * 6;

console.log("Tempo: " + final_tempo);

// final_tempo will be 126
