'use client';

import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react';

type ScaleContextValue = {
  scaleId: string;
  setScaleId: (value: string) => void;
  clearScaleId: () => void;
  declinedPrompts: boolean;
  markDeclined: () => void;
  resetDecline: () => void;
  promptOpen: boolean;
  openPrompt: (initialValue?: string) => void;
  closePrompt: () => void;
  declinePrompt: () => void;
  pendingScaleId: string;
  setPendingScaleId: (value: string) => void;
  confirmPendingScaleId: (value?: string) => string | null;
};

const STORAGE_KEY_SYSTEM_ID = 'mixmeasurebuddy:scale-id';
const STORAGE_KEY_DECLINED = 'mixmeasurebuddy:scale-declined';

const ScaleContext = createContext<ScaleContextValue | undefined>(undefined);

export const ScaleProvider = ({ children }: { children: React.ReactNode }) => {
  const [scaleId, setScaleIdState] = useState<string>('');
  const [declinedPrompts, setDeclinedPrompts] = useState<boolean>(false);
  const [promptOpen, setPromptOpen] = useState<boolean>(false);
  const [pendingScaleId, setPendingScaleIdState] = useState<string>('');

  useEffect(() => {
    if (typeof window === 'undefined') {
      return;
    }
    const savedId = window.localStorage.getItem(STORAGE_KEY_SYSTEM_ID) ?? '';
    const declined = window.localStorage.getItem(STORAGE_KEY_DECLINED) === 'true';
    setScaleIdState(savedId);
    setDeclinedPrompts(declined);
  }, []);

  const setScaleId = useCallback((value: string) => {
    const trimmed = value.trim();
    setScaleIdState(trimmed);
    if (typeof window !== 'undefined') {
      if (trimmed) {
        window.localStorage.setItem(STORAGE_KEY_SYSTEM_ID, trimmed);
        window.localStorage.removeItem(STORAGE_KEY_DECLINED);
      } else {
        window.localStorage.removeItem(STORAGE_KEY_SYSTEM_ID);
      }
    }
    setDeclinedPrompts(false);
    setPendingScaleIdState(trimmed);
  }, []);

  const clearScaleId = useCallback(() => {
    setScaleIdState('');
    if (typeof window !== 'undefined') {
      window.localStorage.removeItem(STORAGE_KEY_SYSTEM_ID);
    }
    setPendingScaleIdState('');
  }, []);

  const markDeclined = useCallback(() => {
    setDeclinedPrompts(true);
    if (typeof window !== 'undefined') {
      window.localStorage.setItem(STORAGE_KEY_DECLINED, 'true');
    }
  }, []);

  const resetDecline = useCallback(() => {
    setDeclinedPrompts(false);
    if (typeof window !== 'undefined') {
      window.localStorage.removeItem(STORAGE_KEY_DECLINED);
    }
  }, []);

  const openPrompt = useCallback(
    (initialValue?: string) => {
      const initial = (initialValue ?? scaleId).trim();
      setPendingScaleIdState(initial);
      setPromptOpen(true);
      setDeclinedPrompts(false);
    },
    [scaleId],
  );

  const closePrompt = useCallback(() => {
    setPromptOpen(false);
  }, []);

  const declinePrompt = useCallback(() => {
    setPromptOpen(false);
    if (!scaleId) {
      markDeclined();
    }
  }, [markDeclined, scaleId]);

  const setPendingScaleId = useCallback((value: string) => {
    setPendingScaleIdState(value);
  }, []);

  const confirmPendingScaleId = useCallback(
    (value?: string) => {
      const next = (value ?? pendingScaleId).trim();
      if (!next) {
        return null;
      }
      setScaleId(next);
      setPendingScaleIdState(next);
      setPromptOpen(false);
      return next;
    },
    [pendingScaleId, setScaleId],
  );

  const value = useMemo(
    () => ({
      scaleId,
      setScaleId,
      clearScaleId,
      declinedPrompts,
      markDeclined,
      resetDecline,
      promptOpen,
      openPrompt,
      closePrompt,
      declinePrompt,
      pendingScaleId,
      setPendingScaleId,
      confirmPendingScaleId,
    }),
    [
      scaleId,
      setScaleId,
      clearScaleId,
      declinedPrompts,
      markDeclined,
      resetDecline,
      promptOpen,
      openPrompt,
      closePrompt,
      declinePrompt,
      pendingScaleId,
      setPendingScaleId,
      confirmPendingScaleId,
    ],
  );

  return <ScaleContext.Provider value={value}>{children}</ScaleContext.Provider>;
};

export const useScaleContext = () => {
  const context = useContext(ScaleContext);
  if (!context) {
    throw new Error('useScaleContext must be used within a ScaleProvider');
  }
  return context;
};

export const SCALE_STORAGE_KEYS = {
  id: STORAGE_KEY_SYSTEM_ID,
  declined: STORAGE_KEY_DECLINED,
};
