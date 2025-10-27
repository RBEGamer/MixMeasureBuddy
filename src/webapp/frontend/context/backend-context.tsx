'use client';

import React, { useContext, useEffect, useState } from 'react';

type BackendContextValue = {
  reachable: boolean;
  backendUrl?: string;
};

const BackendContext = React.createContext<BackendContextValue>({
  reachable: false,
  backendUrl: undefined,
});

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL;
const HEALTH_ENDPOINT = '/recipes/available';
const POLL_INTERVAL_MS = 30000;

export const BackendProvider = ({ children }: { children: React.ReactNode }) => {
  const [reachable, setReachable] = useState<boolean>(false);

  useEffect(() => {
    if (!BACKEND_URL) {
      setReachable(false);
      return;
    }

    let active = true;
    let timeout: NodeJS.Timeout | undefined;

    const checkBackend = async () => {
      console.info('[BackendProvider] Checking backend reachability', BACKEND_URL);
      try {
        const response = await fetch(`${BACKEND_URL}${HEALTH_ENDPOINT}`, {
          method: 'GET',
          cache: 'no-store',
        });
        if (active) {
          console.info('[BackendProvider] Backend response status', response.status);
          setReachable(response.ok);
        }
      } catch {
        if (active) {
          console.warn('[BackendProvider] Backend unreachable');
          setReachable(false);
        }
      } finally {
        if (active && BACKEND_URL) {
          timeout = setTimeout(checkBackend, POLL_INTERVAL_MS);
        }
      }
    };

    checkBackend();

    return () => {
      active = false;
      if (timeout) clearTimeout(timeout);
    };
  }, []);

  return (
    <BackendContext.Provider value={{ reachable, backendUrl: BACKEND_URL }}>
      {children}
    </BackendContext.Provider>
  );
};

export const useBackendReachable = () => {
  const ctx = useContext(BackendContext);
  return ctx.reachable;
};

export const useBackendInfo = () => useContext(BackendContext);
