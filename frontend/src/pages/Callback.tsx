import { useEffect } from 'react';
import { useAuth0 } from '@auth0/auth0-react';

function Callback() {
  const { handleRedirectCallback } = useAuth0();

  useEffect(() => {
    handleRedirectCallback();
  }, [handleRedirectCallback]);

  return <div>Loading...</div>;
}

export default Callback;
