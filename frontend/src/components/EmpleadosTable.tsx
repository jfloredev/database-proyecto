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

interface Empleado {
  id: number;
  dni: string;
  nombre: string;
  apellido: string;
  sueldo: number;
  turno: string;
  estado: string;
  sede_nombre: string;
}

interface EmpleadosTableProps {
  empleados: Empleado[];
}

export const EmpleadosTable = ({ empleados }: EmpleadosTableProps) => (
  <TableContainer component={Paper} sx={{ mt: 3 }}>
    <Typography variant="h6" sx={{ p: 2, fontWeight: 600 }}>
      Lista de Empleados ({empleados.length})
    </Typography>
    <Table>
      <TableHead sx={{ backgroundColor: '#f5f5f5' }}>
        <TableRow>
          <TableCell sx={{ fontWeight: 600 }}>ID</TableCell>
          <TableCell sx={{ fontWeight: 600 }}>Nombre</TableCell>
          <TableCell sx={{ fontWeight: 600 }}>Sueldo</TableCell>
          <TableCell sx={{ fontWeight: 600 }}>Turno</TableCell>
          <TableCell sx={{ fontWeight: 600 }}>Estado</TableCell>
          <TableCell sx={{ fontWeight: 600 }}>Sede</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {empleados.map((emp) => (
          <TableRow key={emp.id} hover>
            <TableCell>{emp.id}</TableCell>
            <TableCell>{emp.nombre} {emp.apellido}</TableCell>
            <TableCell>S/ {emp.sueldo}</TableCell>
            <TableCell>
              <Chip label={emp.turno} variant="outlined" size="small" />
            </TableCell>
            <TableCell>
              <Chip
                label={emp.estado}
                color={emp.estado === 'Activo' ? 'success' : 'default'}
                variant={emp.estado === 'Activo' ? 'filled' : 'outlined'}
                size="small"
              />
            </TableCell>
            <TableCell>{emp.sede_nombre}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  </TableContainer>
);