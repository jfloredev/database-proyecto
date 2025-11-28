import React, { useState, useEffect } from 'react';
import { Box, CircularProgress, Container } from '@mui/material';
import {
  Header,
  Footer,
  NavTabs,
  ClientesTable,
  MedicamentosTable,
  EmpleadosTable,
  MonederoTable,
  SedesTable,
  SplashScreen,
} from './components';

// Interfaces para tipado

interface Cliente {
  id: number;
  direccion: string;
  dni: string;
  nombre: string;
  apellido: string;
  telefono?: string;
  email?: string;
}

interface Medicamento {
  id: number;
  nombre: string;
  marca?: string;
  precio: number;
  necesita_receta: boolean;
  descripcion?: string;
}

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

interface Monedero {
  id: number;
  saldo: number;
  fecha_creacion: string;
  dni_cliente: string;
}

interface Sede {
  direccion: string;
  nombre: string;
  cantidad_empleados: number;
}

// API Base URL
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8080';

function App() {
  const [showSplash, setShowSplash] = useState<boolean>(true);
  const [activeTab, setActiveTab] = useState<number>(0);
  const [loading, setLoading] = useState<boolean>(false);
  
  // Estados para los datos
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [medicamentos, setMedicamentos] = useState<Medicamento[]>([]);
  const [empleados, setEmpleados] = useState<Empleado[]>([]);
  const [monedero, setMonedero] = useState<Monedero[]>([]);
  const [sedes, setSedes] = useState<Sede[]>([]);

  // Función genérica para fetch
  const fetchData = async (endpoint: string, setter: (data: any) => void) => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`);
      const data = await response.json();
      
      // Extraer el array correcto según el endpoint
      if (data.clientes) setter(data.clientes);
      else if (data.medicamentos) setter(data.medicamentos);
      else if (data.empleados) setter(data.empleados);
      else if (data.monedero) setter(data.monedero);
      else if (data.sedes) setter(data.sedes);
      
    } catch (error) {
      console.error('Error fetching data:', error);
      alert('Error conectando con la API. ¿Está el backend ejecutándose en el puerto 8080?');
    } finally {
      setLoading(false);
    }
  };

  // Cargar datos cuando cambia la tab
  useEffect(() => {
    const endpoints = [
      { tab: 0, endpoint: '/clientes', setter: setClientes },
      { tab: 1, endpoint: '/medicamentos', setter: setMedicamentos },
      { tab: 2, endpoint: '/monedero', setter: setMonedero },
      { tab: 3, endpoint: '/empleados', setter: setEmpleados },
      { tab: 4, endpoint: '/sedes', setter: setSedes },
    ];

    const current = endpoints.find(e => e.tab === activeTab);
    if (current) {
      fetchData(current.endpoint, current.setter);
    }
  }, [activeTab]);

  // Renderizar contenido según tab activa
  const renderContent = () => {
    if (loading) {
      return (
        <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
          <CircularProgress />
        </Box>
      );
    }

    switch (activeTab) {
      case 0:
        return <ClientesTable clientes={clientes} />;
      case 1:
        return <MedicamentosTable medicamentos={medicamentos} />;
      case 2:
        return <MonederoTable monedero={monedero} />;
      case 3:
        return <EmpleadosTable empleados={empleados} />;
      case 4:
        return <SedesTable sedes={sedes} />;
      default:
        return null;
    }
  };

  // Mostrar splash screen inicialmente
  if (showSplash) {
    return <SplashScreen onStart={() => setShowSplash(false)} />;
  }

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh', bgcolor: '#fafafa' }}>
      <Header />
      <NavTabs activeTab={activeTab} onTabChange={(_, value: number) => setActiveTab(value)} />
      <Container maxWidth="lg" sx={{ py: 3, flexGrow: 1 }}>
        {renderContent()}
      </Container>
      <Footer />
    </Box>
  );
}

export default App;
