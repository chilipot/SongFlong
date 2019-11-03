import React, { useState, useEffect } from "react";
import VideoContainer from "./VideoContainer";

const VideosContainer = ({ jobs }) => {
  const [videos, setVideos] = useState([]);
  const pollJobs = () => {
    // Poll stuff
  };
  useEffect(() => {
    // Do rest of stuff
  }, [jobs]);
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
