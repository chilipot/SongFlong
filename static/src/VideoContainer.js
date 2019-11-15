import React, { useEffect, useState } from 'react';
import { BASE_URL } from './utils/API';
import Request from 'axios-request-handler';
import VideoPlayer from './VideoPlayer';

const MetaContainer = ({ video, index, major = false }) => (
    <div className={'title column'}>
        <img
            id={`art${index}`}
            src={
                video.art ||
                'https://s3.amazonaws.com/assets.jog.fm/images/missing-600x600.png'
            }
            alt="Album art"
            height="240px"
            width="240px"
        />
        <h3>{video.title}</h3>
        <p>{video.artist}</p>
    </div>
);

const PlaybackContainer = ({ video, index, major = false }) => (
    <div className={'video column'}>
        <VideoPlayer filepath={video.filepath} />
    </div>
);

const VideoContainer = ({ id, index }) => {
    const [video, setVideo] = useState(null);
    useEffect(() => {
        const url = `${BASE_URL}/results/${id}`;
        const jobResult = new Request(url);
        jobResult.poll(1000).get(res => {
            if (res.status === 400) {
                throw 'Unable To Retrieve Video Src';
            } else if (res.status === 200) {
                setVideo(res.data);
                return false;
            }
            return true;
        });
    }, [id]);
    if (!video) {
        return null;
    }
    const major = index % 2 === 0;
    let components = [
        <PlaybackContainer video={video} index={index} />,
        <MetaContainer video={video} index={index} />
    ];
    return (
        <div className="row">
            {(major ? components : components.reverse()).map(
                Component => Component
            )}
        </div>
    );
};

export default VideoContainer;
