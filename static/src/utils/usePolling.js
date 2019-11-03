import React, { useState, useEffect, useRef } from "react";

// Sourced and Repurposed from https://github.com/vivek12345/react-polling-hook
// Since it isn't released on npm
const usePolling = config => {
  let {
    urls,
    interval = 3000,
    onSuccess,
    onFailure = () => {},
    ...api
  } = config;

  const [isPolling, togglePolling] = useState(false);

  const persistedIsPolling = useRef();
  const isMounted = useRef();
  const poll = useRef();
  const urlsToPoll = useRef();
  urlsToPoll.current = urls;

  persistedIsPolling.current = isPolling;

  useEffect(() => {
    isMounted.current = true;
    startPolling();
    return () => {
      isMounted.current = false;
      stopPolling();
    };
  }, []);

  const shouldRetry = false;

  const stopPolling = () => {
    if (isMounted.current) {
      if (poll.current) {
        clearTimeout(poll.current);
        poll.current = null;
      }
      togglePolling(false);
    }
  };

  const startPolling = () => {
    // why this does not update state?
    togglePolling(true);
    // call runPolling, which will start timer and call our api
    runPolling();
  };

  const runPolling = () => {
    // console.log(urlsToPoll.current);
    const timeoutId = setTimeout(() => {
      /* onSuccess would be handled by the user of service which would either return true or false
       * true - This means we need to continue polling
       * false - This means we need to stop polling
       */
      // console.log(urlsToPoll.current);
      // console.log(urls);
      for (const url of urls) {
        if (!urlsToPoll.current.includes(url)) {
          continue;
        }
        console.log("Polling " + url.split("/").pop());
        fetch(url, api)
          .then(resp => {
            return resp.json().then(data => {
              if (resp.ok) {
                return resp;
              } else {
                return Promise.reject({ status: resp.status, data });
              }
            });
          })
          .then(onSuccess)
          .then(continuePolling => {
            // console.log("Continue Polling: " + continuePolling);
            urlsToPoll.current = urlsToPoll.current.filter(u => u !== url);
            if (
              persistedIsPolling.current &&
              continuePolling &&
              !!urlsToPoll.current.length
            ) {
              runPolling();
            } else {
              stopPolling();
            }
          })
          .catch(error => {
            onFailure(error);
          });
      }
    }, interval);
    poll.current = timeoutId;
  };

  return [isPolling, startPolling, stopPolling];
};

export default usePolling;
