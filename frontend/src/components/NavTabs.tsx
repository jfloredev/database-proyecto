import React from 'react';
import {
  Tabs,
  Tab,
} from '@mui/material';
import {
  ShoppingCart,
  MedicalInformation,
  Business,
  Store,
  AccountBalance,
} from '@mui/icons-material';

interface NavTabsProps {
  activeTab: number;
  onTabChange: (event: React.SyntheticEvent, newValue: number) => void;
}

export const NavTabs = ({ activeTab, onTabChange }: NavTabsProps) => {
  return (
    <Tabs 
      value={activeTab} 
      onChange={onTabChange}
      indicatorColor="primary"
      textColor="primary"
      variant="fullWidth"
      sx={{ borderBottom: '1px solid #e0e0e0' }}
    >
      <Tab label="Clientes" icon={<ShoppingCart />} iconPosition="start" />
      <Tab label="Medicamentos" icon={<MedicalInformation />} iconPosition="start" />
      <Tab label="Monedero" icon={<AccountBalance />} iconPosition="start" />
      <Tab label="Empleados" icon={<Business />} iconPosition="start" />
      <Tab label="Sedes" icon={<Store />} iconPosition="start" />
    </Tabs>
  );
};