import { useState, useEffect, useCallback } from 'react';

const STORAGE_KEY = 'campus_notifications_viewed';

const getStoredViewedIds = (): Set<string> => {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      return new Set(JSON.parse(stored));
    }
  } catch {
    console.warn('Failed to parse viewed notifications from localStorage');
  }
  return new Set();
};

const saveViewedIds = (ids: Set<string>): void => {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(Array.from(ids)));
  } catch {
    console.warn('Failed to save viewed notifications to localStorage');
  }
};

export const useViewedStore = () => {
  const [viewedIds, setViewedIds] = useState<Set<string>>(() => getStoredViewedIds());

  useEffect(() => {
    saveViewedIds(viewedIds);
  }, [viewedIds]);

  const markAsViewed = useCallback((id: string) => {
    setViewedIds((prev) => {
      if (prev.has(id)) return prev;
      const newSet = new Set(prev);
      newSet.add(id);
      return newSet;
    });
  }, []);

  const isViewed = useCallback((id: string): boolean => {
    return viewedIds.has(id);
  }, [viewedIds]);

  const clearViewed = useCallback(() => {
    setViewedIds(new Set());
  }, []);

  return {
    viewedIds,
    markAsViewed,
    isViewed,
    clearViewed,
  };
};

export type { };