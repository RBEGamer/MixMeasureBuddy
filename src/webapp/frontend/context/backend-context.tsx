'use client';

import React, { useContext, useEffect, useState } from 'react';

const BackendContext = React.createContext<boolean>(false);

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL;
const HEALTH_ENDPOINT = '/recipes/available';

export const BackendProvider = ({ children }: { children: React.ReactNode }) => {
  const [reachable, setReachable] = useState<boolean>(false);

  useEffect(() => {
    if (!BACKEND_URL) {
      setReachable(false);
      return;
    }

    let active = true;

    const checkBackend = async () => {
      try {
        const response = await fetch(`${BACKEND_URL}${HEALTH_ENDPOINT}`, {
          method: 'HEAD',
        });
        if (active) {
          setReachable(response.ok);
        }
      } catch (error) {
        if (active) {
          setReachable(false);
        }
      }
    };

    checkBackend();

    return () => {
      active = false;
    };
  }, []);

  return (
    <BackendContext.Provider value={reachable}>{children}</BackendContext.Provider>
  );
};

export const useBackendReachable = () => useContext(BackendContext);
