import React from 'react';
import { Box, Typography } from '@mui/material';

export const Footer = () => {
  return (
    <Box
      component="footer"
      sx={{
        bgcolor: '#f5f5f5',
        py: 2,
        textAlign: 'center',
        borderTop: '1px solid #e0e0e0',
        mt: 4,
      }}
    >
      <Typography variant="caption" color="textSecondary">
        Backend API: localhost:8080
      </Typography>
    </Box>
  );
};