import React from 'react';
import {
  TableContainer,
  Table,
  TableHead,
  TableBody,
  TableRow,
  TableCell,
  Paper,
  Typography,
  Chip,
} from '@mui/material';

interface Usuario {
  dni: string;
  nombre: string;
  apellido: string;
  telefono?: string;
  email?: string;
  fecha_registro: string;
}

interface UsuariosTableProps {
  usuarios: Usuario[];
}

export const UsuariosTable = ({ usuarios }: UsuariosTableProps) => (
  <TableContainer component={Paper} sx={{ mt: 3 }}>
    <Typography variant="h6" sx={{ p: 2, fontWeight: 600 }}>
      Lista de Usuarios ({usuarios.length})
    </Typography>
    <Table>
      <TableHead sx={{ backgroundColor: '#f5f5f5' }}>
        <TableRow>
          <TableCell sx={{ fontWeight: 600 }}>DNI</TableCell>
          <TableCell sx={{ fontWeight: 600 }}>Nombre</TableCell>
          <TableCell sx={{ fontWeight: 600 }}>Apellido</TableCell>
          <TableCell sx={{ fontWeight: 600 }}>Teléfono</TableCell>
          <TableCell sx={{ fontWeight: 600 }}>Email</TableCell>
          <TableCell sx={{ fontWeight: 600 }}>Fecha Registro</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {usuarios.map((usuario) => (
          <TableRow key={usuario.dni} hover>
            <TableCell>{usuario.dni}</TableCell>
            <TableCell>{usuario.nombre}</TableCell>
            <TableCell>{usuario.apellido}</TableCell>
            <TableCell>{usuario.telefono || '-'}</TableCell>
            <TableCell>{usuario.email || '-'}</TableCell>
            <TableCell>{usuario.fecha_registro}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  </TableContainer>
);