import React, { useState } from 'react';
import {
  Container,
  Typography,
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material';
import { usePriorityNotifications } from '../hooks/useNotifications';
import { useViewedStore } from '../state/viewedStore';
import NotificationList from '../components/NotificationList';

const PriorityInbox: React.FC = () => {
  const [topN, setTopN] = useState(10);
  const { markAsViewed, isViewed } = useViewedStore();

  const { notifications, total, loading, error } = usePriorityNotifications(topN);

  const handleTopNChange = (event: any) => {
    setTopN(event.target.value);
  };

  const handleNotificationClick = (id: string) => {
    markAsViewed(id);
  };

  return (
    <Container maxWidth="md" sx={{ py: 3 }}>
      <Typography variant="h4" component="h1" gutterBottom fontWeight={600}>
        Priority Inbox
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Showing top notifications ranked by type priority and recency
      </Typography>

      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3} flexWrap="wrap" gap={2}>
        <FormControl size="small" sx={{ minWidth: 150 }}>
          <InputLabel id="topN-label">Show Top</InputLabel>
          <Select
            labelId="topN-label"
            value={topN}
            label="Show Top"
            onChange={handleTopNChange}
          >
            <MenuItem value={10}>10</MenuItem>
            <MenuItem value={15}>15</MenuItem>
            <MenuItem value={20}>20</MenuItem>
          </Select>
        </FormControl>

        <Typography variant="body2" color="text.secondary">
          {total} priority notification{total !== 1 ? 's' : ''}
        </Typography>
      </Box>

      <NotificationList
        notifications={notifications}
        loading={loading}
        error={error}
        isViewed={isViewed}
        onNotificationClick={handleNotificationClick}
      />
    </Container>
  );
};

export default PriorityInbox;