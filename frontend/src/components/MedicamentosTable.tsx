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

interface Medicamento {
  id: number;
  nombre: string;
  marca?: string;
  precio: number;
  necesita_receta: boolean;
  descripcion?: string;
}

interface MedicamentosTableProps {
  medicamentos: Medicamento[];
}

export const MedicamentosTable = ({ medicamentos }: MedicamentosTableProps) => (
  <TableContainer component={Paper} sx={{ mt: 3 }}>
    <Typography variant="h6" sx={{ p: 2, fontWeight: 600 }}>
      Lista de Medicamentos ({medicamentos.length})
    </Typography>
    <Table>
      <TableHead sx={{ backgroundColor: '#f5f5f5' }}>
        <TableRow>
          <TableCell sx={{ fontWeight: 600 }}>ID</TableCell>
          <TableCell sx={{ fontWeight: 600 }}>Nombre</TableCell>
          <TableCell sx={{ fontWeight: 600 }}>Marca</TableCell>
          <TableCell sx={{ fontWeight: 600 }}>Precio</TableCell>
          <TableCell sx={{ fontWeight: 600 }}>Receta</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {medicamentos.map((med) => (
          <TableRow key={med.id} hover>
            <TableCell>{med.id}</TableCell>
            <TableCell>{med.nombre}</TableCell>
            <TableCell>{med.marca || '-'}</TableCell>
            <TableCell>S/ {med.precio}</TableCell>
            <TableCell>
              <Chip
                label={med.necesita_receta ? 'Sí' : 'No'}
                color={med.necesita_receta ? 'error' : 'success'}
                variant="outlined"
                size="small"
              />
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  </TableContainer>
);