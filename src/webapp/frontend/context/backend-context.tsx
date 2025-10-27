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

const BACKEND_URL_ENV = process.env.NEXT_PUBLIC_BACKEND_URL;
const HEALTH_ENDPOINT = '/recipes/available';
const POLL_INTERVAL_MS = 30000;

export const BackendProvider = ({ children }: { children: React.ReactNode }) => {
  const [reachable, setReachable] = useState<boolean>(false);
  const [backendUrl, setBackendUrl] = useState<string | undefined>(undefined);

  useEffect(() => {
    let resolvedUrl = BACKEND_URL_ENV;
    if (!resolvedUrl && typeof window !== 'undefined') {
      const current = new URL(window.location.href);
      resolvedUrl = `${current.protocol}//${current.hostname}:4000`;
    }

    setBackendUrl(resolvedUrl);

    if (!resolvedUrl) {
      setReachable(false);
      return;
    }

    let active = true;
    let timeout: NodeJS.Timeout | undefined;

    const checkBackend = async () => {
      console.info('[BackendProvider] Checking backend reachability', resolvedUrl);
      try {
        const response = await fetch(`${resolvedUrl}${HEALTH_ENDPOINT}`, {
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
        if (active && resolvedUrl) {
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
    <BackendContext.Provider value={{ reachable, backendUrl }}>
      {children}
    </BackendContext.Provider>
  );
};

export const useBackendReachable = () => {
  const ctx = useContext(BackendContext);
  return ctx.reachable;
};

export const useBackendInfo = () => useContext(BackendContext);
