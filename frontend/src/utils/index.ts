export * from './settings';

// Auth0 user data utilities
export const getUserData = () => {
  return {
    userId: localStorage.getItem('userId'),
    userEmail: localStorage.getItem('userEmail'),
    userName: localStorage.getItem('userName')
  };
};

export const clearUserData = () => {
  localStorage.removeItem('userId');
  localStorage.removeItem('userEmail');
  localStorage.removeItem('userName');
  localStorage.removeItem('hasCompletedWelcome');
}; 