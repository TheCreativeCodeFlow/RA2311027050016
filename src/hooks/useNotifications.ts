import { useState, useEffect, useCallback } from 'react';
import { getNotifications, Notification } from '../services/api';

interface UseNotificationsParams {
  page: number;
  limit: number;
  notificationType?: string;
}

interface UseNotificationsReturn {
  notifications: Notification[];
  total: number;
  loading: boolean;
  error: string | null;
  refetch: () => void;
}

export const useNotifications = ({
  page,
  limit,
  notificationType,
}: UseNotificationsParams): UseNotificationsReturn => {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchNotifications = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await getNotifications({
        page,
        limit,
        notification_type: notificationType,
      });
      setNotifications(response.notifications);
      setTotal(response.total);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch notifications');
      setNotifications([]);
      setTotal(0);
    } finally {
      setLoading(false);
    }
  }, [page, limit, notificationType]);

  useEffect(() => {
    fetchNotifications();
  }, [fetchNotifications]);

  return {
    notifications,
    total,
    loading,
    error,
    refetch: fetchNotifications,
  };
};

export const usePriorityNotifications = (topN: number = 10): UseNotificationsReturn => {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchPriority = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await getNotifications({
        page: 1,
        limit: 100,
        notification_type: undefined,
      });
      
      const typeWeights: Record<string, number> = {
        placement: 3,
        result: 2,
        event: 1,
      };

      const scored = response.notifications.map((n) => {
        const ts = typeof n.timestamp === 'string' 
          ? new Date(n.timestamp).getTime() 
          : Number(n.timestamp);
        const maxTs = Math.max(...response.notifications.map(x => 
          typeof x.timestamp === 'string' 
            ? new Date(x.timestamp).getTime() 
            : Number(x.timestamp)
        ));
        const recency = maxTs > 0 ? ts / maxTs : 0;
        const typeWeight = typeWeights[n.type] || 0;
        return { ...n, _priority: typeWeight + recency };
      });

      scored.sort((a, b) => b._priority - a._priority);
      const top = scored.slice(0, topN).map(({ _priority, ...n }) => n);

      setNotifications(top);
      setTotal(top.length);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch priority notifications');
      setNotifications([]);
      setTotal(0);
    } finally {
      setLoading(false);
    }
  }, [topN]);

  useEffect(() => {
    fetchPriority();
  }, [fetchPriority]);

  return {
    notifications,
    total,
    loading,
    error,
    refetch: fetchPriority,
  };
};

export type { Notification };