import React from 'react';
import { Box, Typography, Button } from '@mui/material';

interface SplashScreenProps {
  onStart: () => void;
}

export const SplashScreen = ({ onStart }: SplashScreenProps) => {
  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        background: '#f8f9fa',
        padding: '20px',
      }}
    >
      {/* Logo UTEC centrado */}
      <Box
        sx={{
          mb: 2,
          textAlign: 'center',
        }}
      >
        <Box
          component="img"
          src="https://upload.wikimedia.org/wikipedia/commons/7/7a/UTEC.jpg"
          alt="UTEC Logo"
          sx={{
            width: '200px',
            height: 'auto',
            mb: 2,
            objectFit: 'contain',
          }}
        />
      </Box>

      {/* Facultad */}
      <Typography
        sx={{
          fontSize: '16px',
          fontWeight: 600,
          color: '#333',
          mb: 0.5,
          letterSpacing: '0.5px',
        }}
      >
        FACULTAD DE COMPUTACIÓN
      </Typography>

      {/* Curso */}
      <Typography
        sx={{
          fontSize: '14px',
          color: '#666',
          mb: 2,
          letterSpacing: '0.3px',
        }}
      >
        BASE DE DATOS
      </Typography>

      {/* Línea separadora */}
      <Box
        sx={{
          width: '60px',
          height: '2px',
          backgroundColor: '#333',
          mb: 2.5,
        }}
      />

      {/* MiFarma */}
      <Typography
        sx={{
          fontSize: '28px',
          fontWeight: 700,
          color: '#333',
          mb: 0.5,
        }}
      >
        MiFarma
      </Typography>

      <Typography
        sx={{
          fontSize: '13px',
          color: '#888',
          mb: 3,
          letterSpacing: '0.5px',
        }}
      >
        Sistema de Gestión
      </Typography>

      {/* Nombres de integrantes */}
      <Box sx={{ textAlign: 'center', mb: 3 }}>
        <Typography sx={{ fontSize: '12px', color: '#555', lineHeight: 1.6 }}>
          André Alejandro Contreras<br />
          Andrés Martín Benjamín<br />
          Saul Sebastián Morales<br />
          Juan Renato Flores<br />
          <br />
          <span style={{ fontWeight: 600, color: '#333', fontSize: '12px' }}>Docente: Ing. Nina Wilder</span>
        </Typography>
      </Box>

      {/* Botón simple */}
      <Button
        onClick={onStart}
        sx={{
          backgroundColor: '#333',
          color: '#fff',
          padding: '10px 40px',
          fontSize: '14px',
          fontWeight: 600,
          border: 'none',
          cursor: 'pointer',
          letterSpacing: '0.5px',
          '&:hover': {
            backgroundColor: '#555',
          },
          textTransform: 'uppercase',
        }}
      >
        Continuar
      </Button>
    </Box>
  );
};