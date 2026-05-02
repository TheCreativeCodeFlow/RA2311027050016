import React, { useState } from 'react';
import {
  Container,
  Typography,
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  SelectChangeEvent,
} from '@mui/material';
import { useNotifications } from '../hooks/useNotifications';
import { useViewedStore } from '../state/viewedStore';
import NotificationList from '../components/NotificationList';
import PaginationControl from '../components/PaginationControl';

const AllNotifications: React.FC = () => {
  const [page, setPage] = useState(1);
  const [limit] = useState(10);
  const [notificationType, setNotificationType] = useState('all');
  const { markAsViewed, isViewed } = useViewedStore();

  const { notifications, total, loading, error } = useNotifications({
    page,
    limit,
    notificationType: notificationType === 'all' ? undefined : notificationType,
  });

  const handleTypeChange = (event: SelectChangeEvent) => {
    setNotificationType(event.target.value);
    setPage(1);
  };

  const handlePageChange = (newPage: number) => {
    setPage(newPage);
  };

  const handleNotificationClick = (id: string) => {
    markAsViewed(id);
  };

  return (
    <Container maxWidth="md" sx={{ py: 3 }}>
      <Typography variant="h4" component="h1" gutterBottom fontWeight={600}>
        All Notifications
      </Typography>

      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3} flexWrap="wrap" gap={2}>
        <FormControl size="small" sx={{ minWidth: 150 }}>
          <InputLabel id="filter-type-label">Filter by Type</InputLabel>
          <Select
            labelId="filter-type-label"
            value={notificationType}
            label="Filter by Type"
            onChange={handleTypeChange}
          >
            <MenuItem value="all">All Types</MenuItem>
            <MenuItem value="placement">Placement</MenuItem>
            <MenuItem value="result">Result</MenuItem>
            <MenuItem value="event">Event</MenuItem>
          </Select>
        </FormControl>

        <Typography variant="body2" color="text.secondary">
          {total} notification{total !== 1 ? 's' : ''} total
        </Typography>
      </Box>

      <NotificationList
        notifications={notifications}
        loading={loading}
        error={error}
        isViewed={isViewed}
        onNotificationClick={handleNotificationClick}
      />

      <PaginationControl
        page={page}
        total={total}
        limit={limit}
        onPageChange={handlePageChange}
      />
    </Container>
  );
};

export default AllNotifications;