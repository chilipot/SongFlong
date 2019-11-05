import React, { useState } from 'react';
import { Player } from 'video-react';


const VideoPlayer = props => {
    const [video, setVideo] = useState("")
    var endTime = Number(new Date()) + 10000;
    function fn() {
        const url = `http://localhost:5000/results/${props.id}`
        fetch(url).then((res) => res.json()).then((json) => {
            if (json.status == "Job has not finished!") {
                return false
            }
            if (json.status == "Job has failed!") {
                throw json.status
            }

            // Really bad assumption but it we make it here, assume success
            setVideo(`http://localhost:5000/video/${json.filepath}`)
            return true
        })
        .catch((err) => console.log(err))
    }

    (function p() {
            // If the condition is met, we're done! 
            if(fn()) {
                console.log("Hello")
            }
            // If the condition isn't met but the timeout hasn't elapsed, go again
            else if (Number(new Date()) < endTime) {
                setTimeout(p, 1000);
            }
            // Didn't match and too much time, reject!
            else {
                console.log("request timed out");
            }
    })();
    return (
        <Player
            playsInline
            src={video}
        />
    )
}

export default VideoPlayer