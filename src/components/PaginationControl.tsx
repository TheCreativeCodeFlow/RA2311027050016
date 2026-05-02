import React from 'react';
import { Pagination as MuiPagination } from '@mui/material';

interface PaginationControlProps {
  page: number;
  total: number;
  limit: number;
  onPageChange: (page: number) => void;
}

export const PaginationControl: React.FC<PaginationControlProps> = ({
  page,
  total,
  limit,
  onPageChange,
}) => {
  const totalPages = Math.ceil(total / limit);

  if (totalPages <= 1) {
    return null;
  }

  const handleChange = (_: React.ChangeEvent<unknown>, value: number) => {
    onPageChange(value);
  };

  return (
    <MuiPagination
      count={totalPages}
      page={page}
      onChange={handleChange}
      color="primary"
      showFirstButton
      showLastButton
      sx={{ display: 'flex', justifyContent: 'center', mt: 3 }}
    />
  );
};

export default PaginationControl;