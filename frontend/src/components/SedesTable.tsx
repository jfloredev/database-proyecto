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

interface Sede {
  direccion: string;
  nombre: string;
  cantidad_empleados: number;
}

interface SedesTableProps {
  sedes: Sede[];
}

export const SedesTable = ({ sedes }: SedesTableProps) => (
  <TableContainer component={Paper} sx={{ mt: 3 }}>
    <Typography variant="h6" sx={{ p: 2, fontWeight: 600 }}>
      Lista de Sedes ({sedes.length})
    </Typography>
    <Table>
      <TableHead sx={{ backgroundColor: '#f5f5f5' }}>
        <TableRow>
          <TableCell sx={{ fontWeight: 600 }}>Nombre</TableCell>
          <TableCell sx={{ fontWeight: 600 }}>Dirección</TableCell>
          <TableCell sx={{ fontWeight: 600 }}>Empleados</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {sedes.map((sede) => (
          <TableRow key={sede.direccion} hover>
            <TableCell sx={{ fontWeight: 500 }}>{sede.nombre}</TableCell>
            <TableCell>{sede.direccion}</TableCell>
            <TableCell>
              <Chip
                label={sede.cantidad_empleados}
                color="primary"
                variant="outlined"
              />
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  </TableContainer>
);