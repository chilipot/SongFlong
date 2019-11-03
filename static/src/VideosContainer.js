import React, { useState, useEffect } from "react";
import VideoContainer from "./VideoContainer";
import usePolling from "./utils/usePolling";
import { BASE_URL } from "./utils/API";

const VideosContainer = ({ jobs }) => {
  const [videos, setVideos] = useState([]);

  const urlsToPoll = jobs.map(job => `${BASE_URL}/results/${job}`);

  const pollingProps = {
    urls: urlsToPoll,
    interval: 2000, // in milliseconds(ms)
    onSuccess: resp => {
      if (resp.status === 200) {
        console.log(resp);
        return true;
      } else {
        return false;
      }
    },
    onFailure: err => console.log(err),
    method: "GET"
  };
  usePolling(pollingProps);

  return (
    <div className="content" style={{ clear: "both" }}>
      <div className="videos container">
        {videos.map((video, index) => (
          <VideoContainer
            key={`video-container-${index}`}
            index={index}
            {...video}
          />
        ))}
      </div>
    </div>
  );
};

export default VideosContainer;
