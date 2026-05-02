import React from 'react';
import { Box, Typography,CircularProgress, Alert } from '@mui/material';
import { Notification } from '../services/api';
import NotificationCard from './NotificationCard';

interface NotificationListProps {
  notifications: Notification[];
  loading: boolean;
  error: string | null;
  isViewed: (id: string) => boolean;
  onNotificationClick: (id: string) => void;
}

export const NotificationList: React.FC<NotificationListProps> = ({
  notifications,
  loading,
  error,
  isViewed,
  onNotificationClick,
}) => {
  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" py={8}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ m: 2 }}>
        {error}
      </Alert>
    );
  }

  if (notifications.length === 0) {
    return (
      <Box textAlign="center" py={8}>
        <Typography variant="h6" color="text.secondary">
          No notifications found
        </Typography>
        <Typography variant="body2" color="text.disabled">
          There are no notifications to display at the moment.
        </Typography>
      </Box>
    );
  }

  return (
    <Box display="flex" flexDirection="column" gap={2}>
      {notifications.map((notification) => (
        <NotificationCard
          key={notification.id}
          notification={notification}
          viewed={isViewed(notification.id)}
          onClick={() => onNotificationClick(notification.id)}
        />
      ))}
    </Box>
  );
};

export default NotificationList;