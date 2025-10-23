import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { Auth0Provider } from '@auth0/auth0-react';

createRoot(document.getElementById('root')!).render(
  // <StrictMode>
  <Auth0Provider
    domain="dev-hm5czhc562zt2xae.us.auth0.com"
    clientId="PLG7EcvnQ7PLZ0QtSN7PoRlquXR4qKhz"
    authorizationParams={{
      redirect_uri: `${window.location.origin}/callback`,   // http://localhost:5173
    }}
  >
    <App />
  </Auth0Provider>
  // </StrictMode>,
)
