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

interface Monedero {
  id: number;
  saldo: number;
  fecha_creacion: string;
  dni_cliente: string;
}

interface MonederoTableProps {
  monedero: Monedero[];
}

export const MonederoTable = ({ monedero }: MonederoTableProps) => (
  <TableContainer component={Paper} sx={{ mt: 3 }}>
    <Typography variant="h6" sx={{ p: 2, fontWeight: 600 }}>
      Saldo de Monedero ({monedero.length})
    </Typography>
    <Table>
      <TableHead sx={{ backgroundColor: '#f5f5f5' }}>
        <TableRow>
          <TableCell sx={{ fontWeight: 600 }}>ID</TableCell>
          <TableCell sx={{ fontWeight: 600 }}>DNI Cliente</TableCell>
          <TableCell sx={{ fontWeight: 600 }}>Saldo</TableCell>
          <TableCell sx={{ fontWeight: 600 }}>Fecha Creación</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {monedero.map((item) => (
          <TableRow key={item.id} hover>
            <TableCell>{item.id}</TableCell>
            <TableCell>{item.dni_cliente}</TableCell>
            <TableCell>
              <Chip
                label={`S/ ${parseFloat(item.saldo.toString()).toFixed(2)}`}
                color={parseFloat(item.saldo.toString()) > 0 ? 'success' : 'error'}
                variant="outlined"
              />
            </TableCell>
            <TableCell>{item.fecha_creacion}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  </TableContainer>
);
