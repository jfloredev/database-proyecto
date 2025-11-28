import React from 'react';
import { AppBar, Toolbar, Box, Typography } from '@mui/material';
import { MedicalInformation } from '@mui/icons-material';

export const Header = () => {
  return (
    <AppBar position="static" sx={{ bgcolor: '#1976d2' }}>
      <Toolbar>
        <MedicalInformation sx={{ mr: 2, fontSize: 28 }} />
        <Box sx={{ flexGrow: 1 }}>
          <Typography variant="h6" component="div" sx={{ fontWeight: 700 }}>
            MiFarma
          </Typography>
          <Typography variant="caption" sx={{ opacity: 0.8 }}>
            Sistema de Gestión de Farmacia
          </Typography>
        </Box>
      </Toolbar>
    </AppBar>
  );
};