import React from "react";

const MetaContainer = ({ title, artist, art, index, major = false }) => (
  <div
    className={`title ${major ? "two" : "one"}-third${(major && "s") ||
      ""} column`}
  >
    <img
      id={`art${index}`}
      src={
        art ||
        "https://s3.amazonaws.com/assets.jog.fm/images/missing-600x600.png"
      }
      alt="Album art"
      height="240px"
      width="240px"
    />
    <h3>{title}</h3>
    <p>{artist}</p>
  </div>
);

const PlaybackContainer = ({ filepath, index, major = false }) => (
  <div className="video two-thirds column">
    <video id={`video${index}`} controls>
      <source src={filepath} type="video/mp4" />
    </video>
  </div>
);

const VideoContainer = ({ title, artist, filepath, art, index }) => {
  const major = index % 2 === 0;
  let components = [
    <PlaybackContainer filepath={filepath} index={index} major={major} />,
    <MetaContainer
      title={title}
      artist={artist}
      art={art}
      index={index}
      major={major}
    />
  ];
  return (
    <div className="row">
      {(major ? components : components.reverse()).map(Component => Component)}
    </div>
  );
};

export default VideoContainer;
