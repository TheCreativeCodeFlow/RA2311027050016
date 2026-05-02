import React from 'react';
import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { Box, AppBar, Toolbar, Typography, Container } from '@mui/material';
import { theme } from './theme';
import AllNotifications from './pages/AllNotifications';
import PriorityInbox from './pages/PriorityInbox';
import './styles/global.css';

const navLinkBase: React.CSSProperties = {
  textDecoration: 'none',
  color: 'white',
  padding: '6px 12px',
  borderRadius: '4px',
  fontWeight: 400,
  transition: 'all 0.2s',
};

const App: React.FC = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <BrowserRouter>
        <Box sx={{ flexGrow: 1 }}>
          <AppBar position="static" elevation={1}>
            <Container maxWidth="md">
              <Toolbar disableGutters>
                <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 600 }}>
                  Campus Notifications
                </Typography>
                <Box display="flex" gap={2}>
                  <NavLink
                    to="/"
                    style={({ isActive }) => ({
                      ...navLinkBase,
                      fontWeight: isActive ? 700 : 400,
                      borderBottom: isActive ? '2px solid white' : 'none',
                    })}
                  >
                    All Notifications
                  </NavLink>
                  <NavLink
                    to="/priority"
                    style={({ isActive }) => ({
                      ...navLinkBase,
                      fontWeight: isActive ? 700 : 400,
                      borderBottom: isActive ? '2px solid white' : 'none',
                    })}
                  >
                    Priority Inbox
                  </NavLink>
                </Box>
              </Toolbar>
            </Container>
          </AppBar>
        </Box>

        <Container maxWidth="md" sx={{ backgroundColor: 'background.default', minHeight: '100vh' }}>
          <Routes>
            <Route path="/" element={<AllNotifications />} />
            <Route path="/priority" element={<PriorityInbox />} />
          </Routes>
        </Container>
      </BrowserRouter>
    </ThemeProvider>
  );
};

export default App;