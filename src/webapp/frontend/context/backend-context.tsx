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

const joinUrl = (base: string, endpoint: string): string => {
  if (!base) {
    return endpoint;
  }

  const normalizedBase = base.endsWith('/') ? base.slice(0, -1) : base;
  const normalizedEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;

  return `${normalizedBase}${normalizedEndpoint}`;
};

const computeCandidateUrls = (): string[] => {
  const candidates = new Set<string>();

  if (BACKEND_URL_ENV && BACKEND_URL_ENV.trim().length > 0) {
    candidates.add(BACKEND_URL_ENV.trim());
  }

  if (typeof window !== 'undefined') {
    const current = new URL(window.location.href);
    const hostname = current.hostname.toLowerCase();
    const isGitHubHost =
      hostname.endsWith('.github.io') ||
      hostname.endsWith('.githubusercontent.com') ||
      hostname === 'localhost.github.io';

    if (!isGitHubHost) {
      candidates.add('/api');

      const isLoopback =
        hostname === 'localhost' || hostname === '127.0.0.1' || hostname === '::1';
      const isCustomLocal = hostname.endsWith('.local');
      const port = current.port?.trim();
      const hasNonDefaultPort = port && port !== '80' && port !== '443';

      if (isLoopback || isCustomLocal || hasNonDefaultPort) {
        const protocol = current.protocol === 'https:' ? 'https:' : 'http:';
        candidates.add(`${protocol}//${hostname}:4000`);
      }
    }
  }

  return Array.from(candidates);
};

const pingBackend = async (baseUrl: string) => {
  try {
    const response = await fetch(joinUrl(baseUrl, HEALTH_ENDPOINT), {
      method: 'GET',
      cache: 'no-store',
    });
    return response.ok;
  } catch (error) {
    console.warn('[BackendProvider] Backend check failed for', baseUrl, error);
    return false;
  }
};

export const BackendProvider = ({ children }: { children: React.ReactNode }) => {
  const [reachable, setReachable] = useState<boolean>(false);
  const [backendUrl, setBackendUrl] = useState<string | undefined>(undefined);

  useEffect(() => {
    const candidateUrls = computeCandidateUrls();
    if (candidateUrls.length === 0) {
      setReachable(false);
      setBackendUrl(undefined);
      return;
    }

    let active = true;
    let timeout: NodeJS.Timeout | undefined;

    const schedule = (fn: () => void) => {
      if (timeout) {
        clearTimeout(timeout);
      }
      timeout = setTimeout(fn, POLL_INTERVAL_MS);
    };

    const monitor = async (currentBase: string) => {
      if (!active) return;
      const ok = await pingBackend(currentBase);
      if (!active) return;

      if (ok) {
        setReachable(true);
        setBackendUrl(currentBase);
        schedule(() => monitor(currentBase));
      } else {
        setReachable(false);
        setBackendUrl(undefined);
        schedule(() => findReachable());
      }
    };

    const findReachable = async () => {
      for (const candidate of candidateUrls) {
        if (!active) return;
        const ok = await pingBackend(candidate);
        if (!active) return;

        if (ok) {
          setReachable(true);
          setBackendUrl(candidate);
          schedule(() => monitor(candidate));
          return;
        }
      }

      if (active) {
        setReachable(false);
        setBackendUrl(undefined);
        schedule(() => findReachable());
      }
    };

    findReachable();

    return () => {
      active = false;
      if (timeout) {
        clearTimeout(timeout);
      }
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
