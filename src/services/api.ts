const PROXY_URL = process.env.REACT_APP_PROXY_URL || 'http://localhost:5001';

interface Notification {
  id: string;
  type: string;
  timestamp: number | string;
  title?: string;
  message?: string;
}

interface GetNotificationsParams {
  page: number;
  limit: number;
  notification_type?: string;
}

interface ApiResponse {
  notifications: Notification[];
  total: number;
  page: number;
  limit: number;
}

export const getNotifications = async ({
  page = 1,
  limit = 10,
  notification_type,
}: GetNotificationsParams): Promise<ApiResponse> => {
  const params = new URLSearchParams({
    page: page.toString(),
    limit: limit.toString(),
  });

  if (notification_type && notification_type !== 'all') {
    params.append('notification_type', notification_type);
  }

  const response = await fetch(`${PROXY_URL}/api/notifications?${params.toString()}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.status} ${response.statusText}`);
  }

  const data = await response.json();
  return {
    notifications: data.notifications || data || [],
    total: data.total || 0,
    page: data.page || page,
    limit: data.limit || limit,
  };
};

export const getPriorityNotifications = async (
  topN: number = 10
): Promise<Notification[]> => {
  const params = new URLSearchParams({
    page: '1',
    limit: '100',
  });

  const response = await fetch(`${PROXY_URL}/api/notifications?${params.toString()}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.status} ${response.statusText}`);
  }

  const data = await response.json();
  const notifications: Notification[] = data.notifications || data || [];
  return notifications.slice(0, topN);
};

export type { Notification, GetNotificationsParams, ApiResponse };