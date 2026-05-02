import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Chip,
  Box,
} from '@mui/material';
import { Notification } from '../services/api';

interface NotificationCardProps {
  notification: Notification;
  viewed: boolean;
  onClick: () => void;
}

const typeColors: Record<string, 'primary' | 'secondary' | 'success' | 'error' | 'warning' | 'info' | 'default'> = {
  placement: 'primary',
  result: 'success',
  event: 'warning',
};

const formatTimestamp = (ts: number | string): string => {
  const timestamp = typeof ts === 'string' ? new Date(ts).getTime() : Number(ts);
  if (isNaN(timestamp)) return 'Invalid date';
  
  const date = new Date(timestamp);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

  if (diffDays === 0) {
    return date.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' });
  } else if (diffDays === 1) {
    return 'Yesterday';
  } else if (diffDays < 7) {
    return date.toLocaleDateString('en-IN', { weekday: 'short' });
  } else {
    return date.toLocaleDateString('en-IN', { day: 'numeric', month: 'short' });
  }
};

export const NotificationCard: React.FC<NotificationCardProps> = ({
  notification,
  viewed,
  onClick,
}) => {
  const typeColor = typeColors[notification.type] || 'default';

  return (
    <Card
      onClick={onClick}
      sx={{
        cursor: 'pointer',
        transition: 'all 0.2s ease',
        borderLeft: '4px solid',
        borderLeftColor: viewed ? 'grey.300' : typeColor === 'primary' ? 'primary.main' : typeColor === 'success' ? 'success.main' : 'warning.main',
        backgroundColor: viewed ? 'grey.50' : 'background.paper',
        '&:hover': {
          transform: 'translateY(-2px)',
          boxShadow: 3,
        },
      }}
    >
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="flex-start" gap={1}>
          <Box flex={1}>
            <Typography
              variant="subtitle1"
              component="div"
              fontWeight={viewed ? 400 : 700}
              color={viewed ? 'text.secondary' : 'text.primary'}
            >
              {notification.title || `Notification ${notification.id}`}
            </Typography>
            {notification.message && (
              <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
                {notification.message}
              </Typography>
            )}
            <Typography variant="caption" color="text.disabled" sx={{ mt: 1, display: 'block' }}>
              {formatTimestamp(notification.timestamp)}
            </Typography>
          </Box>
          <Chip
            label={notification.type}
            size="small"
            color={typeColor}
            variant="outlined"
            sx={{ textTransform: 'capitalize' }}
          />
        </Box>
      </CardContent>
    </Card>
  );
};

export default NotificationCard;