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
} from '@mui/material';

interface Cliente {
  id: number;
  direccion: string;
  dni: string;
  nombre: string;
  apellido: string;
  telefono?: string;
  email?: string;
}

interface ClientesTableProps {
  clientes: Cliente[];
}

export const ClientesTable = ({ clientes }: ClientesTableProps) => (
  <TableContainer component={Paper} sx={{ mt: 3 }}>
    <Typography variant="h6" sx={{ p: 2, fontWeight: 600 }}>
      Lista de Clientes ({clientes.length})
    </Typography>
    <Table>
      <TableHead sx={{ backgroundColor: '#f5f5f5' }}>
        <TableRow>
          <TableCell sx={{ fontWeight: 600 }}>ID</TableCell>
          <TableCell sx={{ fontWeight: 600 }}>DNI</TableCell>
          <TableCell sx={{ fontWeight: 600 }}>Nombre</TableCell>
          <TableCell sx={{ fontWeight: 600 }}>Apellido</TableCell>
          <TableCell sx={{ fontWeight: 600 }}>Dirección</TableCell>
          <TableCell sx={{ fontWeight: 600 }}>Email</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {clientes.map((cliente) => (
          <TableRow key={cliente.id} hover>
            <TableCell>{cliente.id}</TableCell>
            <TableCell>{cliente.dni}</TableCell>
            <TableCell>{cliente.nombre}</TableCell>
            <TableCell>{cliente.apellido}</TableCell>
            <TableCell>{cliente.direccion}</TableCell>
            <TableCell>{cliente.email || '-'}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  </TableContainer>
);