import React from 'react';
import { FormControl, InputLabel, Select, MenuItem, SelectChangeEvent } from '@mui/material';

interface FilterBarProps {
  notificationType: string;
  onTypeChange: (type: string) => void;
}

export const FilterBar: React.FC<FilterBarProps> = ({
  notificationType,
  onTypeChange,
}) => {
  const handleChange = (event: SelectChangeEvent) => {
    onTypeChange(event.target.value);
  };

  return (
    <FormControl size="small" sx={{ minWidth: 150 }}>
      <InputLabel id="filter-type-label">Notification Type</InputLabel>
      <Select
        labelId="filter-type-label"
        value={notificationType}
        label="Notification Type"
        onChange={handleChange}
      >
        <MenuItem value="all">All Types</MenuItem>
        <MenuItem value="placement">Placement</MenuItem>
        <MenuItem value="result">Result</MenuItem>
        <MenuItem value="event">Event</MenuItem>
      </Select>
    </FormControl>
  );
};

export default FilterBar;